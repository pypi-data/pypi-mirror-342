import json
import logging
from datetime import datetime
from decimal import Decimal
import sys
from time import sleep
from typing import Type, Dict, List, Any, Tuple

import boto3
from boto3.dynamodb.conditions import (
    Key,
    And,
    Or,
    Equals,
    NotEquals,
    GreaterThanEquals,
    LessThanEquals,
    GreaterThan,
    LessThan,
)
import boto3.exceptions
import botocore
from botocore.client import BaseClient
import botocore.exceptions
from hmd_meta_types import Noun, Relationship, Entity

from hmd_schema_loader import DefaultLoader
from .base_engine import BaseEngine, gen_new_key

CURRENT_VERSION = "v0"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def decimal_decoder(obj: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in obj.items():
        if isinstance(value, Decimal):
            if "." in str(value):
                obj[key] = float(value)
            else:
                obj[key] = int(value)
    return obj


def _build_filter_expression(condition_: Dict[str, Any]):
    operator_map = {
        ">=": GreaterThanEquals,
        ">": GreaterThan,
        "<=": LessThanEquals,
        "<": LessThan,
        "=": Equals,
        "!=": NotEquals,
    }
    value = condition_.get("value", None)

    if isinstance(value, float):
        value = Decimal(value)

    if value is None and "attribute_target" in condition_:
        value = Key(condition_["attribute_target"])

    if condition_["operator"] not in operator_map:
        raise ValueError(f"Operator, {condition_['operator']}, is not supported.")

    return operator_map[condition_["operator"]](Key(condition_["attribute"]), value)


def _build_search_expression(filter_: Dict[str, Any]):
    if len(filter_) == 0:
        return None

    if "and" in filter_:
        return And(
            *[
                _build_search_expression(sub_condition)
                for sub_condition in filter_["and"]
            ]
        )
    elif "or" in filter_:
        return Or(
            *[
                _build_search_expression(sub_condition)
                for sub_condition in filter_["or"]
            ]
        )
    else:
        return _build_filter_expression(filter_)


def _build_key_expression(filter_: Dict[str, Any], version_begins_with: bool = True):
    assert len(filter_) > 0, "len(search_filter) must be > 0"

    condition = None

    for field, value in filter_.items():
        if field == "version" and version_begins_with:
            condition = (
                condition & Key(field).begins_with(value)
                if condition
                else Key(field).begins_with(value)
            )
        else:
            condition = (
                condition & Key(field).eq(value) if condition else Key(field).eq(value)
            )
    return condition


class DynamoDbEngine(BaseEngine):
    def __init__(
        self, table_name: str, dynamo_url: str, pitr: str = None, session=boto3
    ):
        dynamo_resource = session.resource("dynamodb", endpoint_url=dynamo_url)
        dynamo_client = session.client("dynamodb", endpoint_url=dynamo_url)
        existing_tables = [t.table_name for t in dynamo_resource.tables.all()]
        if table_name not in existing_tables:
            dynamo_resource.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {"AttributeName": "identifier", "AttributeType": "S"},
                    {"AttributeName": "version", "AttributeType": "S"},
                    {"AttributeName": "ref_from", "AttributeType": "S"},
                    {"AttributeName": "ref_to", "AttributeType": "S"},
                    {"AttributeName": "entity_name", "AttributeType": "S"},
                ],
                KeySchema=[
                    {"AttributeName": "identifier", "KeyType": "HASH"},
                    {"AttributeName": "version", "KeyType": "RANGE"},
                ],
                BillingMode="PAY_PER_REQUEST",
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "FromIndex",
                        "Projection": {"ProjectionType": "ALL"},
                        "KeySchema": [
                            {"KeyType": "HASH", "AttributeName": "ref_from"},
                            {"KeyType": "RANGE", "AttributeName": "entity_name"},
                        ],
                    },
                    {
                        "IndexName": "ToIndex",
                        "Projection": {"ProjectionType": "ALL"},
                        "KeySchema": [
                            {"KeyType": "HASH", "AttributeName": "ref_to"},
                            {"KeyType": "RANGE", "AttributeName": "entity_name"},
                        ],
                    },
                    {
                        "IndexName": "EntityNameIndex",
                        "Projection": {"ProjectionType": "ALL"},
                        "KeySchema": [
                            {"KeyType": "HASH", "AttributeName": "entity_name"},
                            {"KeyType": "RANGE", "AttributeName": "version"},
                        ],
                    },
                ],
            )
            sleep(10)
            while True:
                try:
                    result = dynamo_client.describe_table(TableName=table_name)
                    if result["Table"]["TableStatus"] == "ACTIVE":
                        break
                except dynamo_client.exceptions.ResourceNotFoundException:
                    pass

        if pitr:
            self._toggle_dynamodb_pitr(table_name, dynamo_client, pitr)

        self.table = dynamo_resource.Table(table_name)

    def _toggle_dynamodb_pitr(self, table_name: str, client: BaseClient, pitr: str):
        while True:
            try:
                backup_result = client.describe_continuous_backups(
                    TableName=table_name
                )["ContinuousBackupsDescription"]
                # NOTE: Continuous backups are enabled on table creation by default
                # As of now, there appears to be no way to Disable continuous backups
                # This code may need to be refactor once disabling ability is introduced
                if backup_result["ContinuousBackupsStatus"] == "ENABLED":
                    break
                else:
                    sleep(5)
            except client.exceptions.ResourceNotFoundException:
                pass

        pitr_status = backup_result["PointInTimeRecoveryDescription"][
            "PointInTimeRecoveryStatus"
        ]
        pitr_enabled = None

        if pitr_status == "DISABLED" and pitr.lower() == "enabled":
            pitr_enabled = True
        elif pitr_status == "ENABLED" and pitr.lower() == "disabled":
            pitr_enabled = False

        if pitr_enabled is not None:
            client.update_continuous_backups(
                TableName=table_name,
                PointInTimeRecoverySpecification={
                    "PointInTimeRecoveryEnabled": pitr_enabled
                },
            )

    def _get_current_entity(self, id_: str):
        response = self.table.get_item(
            Key={"identifier": id_, "version": CURRENT_VERSION}
        )
        return response["Item"] if "Item" in response else None

    def get_entity(self, entity_def: Type[Entity], id_: str) -> Entity:
        result = self._get_current_entity(id_)
        return self._result_to_entity(entity_def, result) if result else None

    def get_entities(self, entity_def: Type[Entity], ids_: List[str]) -> List[Entity]:
        # todo: attempt to query multiple entities at the same time
        results = []
        for id_ in ids_:
            result = self._get_current_entity(id_)
            if not result:
                raise Exception(
                    f"Entity of type {entity_def.get_namespace_name()} with id {id_} not found."
                )
            results.append(self._result_to_entity(entity_def, result))
        return results

    def search_entities(
        self, entity_def: Type[Entity], search_filter: Dict[str, Any] = dict()
    ) -> List[Entity]:
        self._validate_search_criteria(entity_def.entity_definition(), search_filter)
        key_filter = {
            "entity_name": entity_def.get_namespace_name(),
            "version": CURRENT_VERSION,
        }
        return [
            self._result_to_entity(entity_def, data)
            for data in self._do_search_entities(
                keys=key_filter,
                filter_expression=_build_search_expression(search_filter),
                index="EntityNameIndex",
            )
        ]

    def _do_search_entities(
        self, keys: Dict[str, Any], filter_expression=None, index: str = None
    ) -> List[Dict]:
        """Search and filter items.

        Retrieves values from the primary index or a specified secondary index. Items
        are retrieved based on both keys and attribute filters.

        :param keys: A Dict of key name/value pairs to restrict the search.
        :param search_filter: A Dict of field name/value pairs to restrict the search.
        :param index: The name of the index to search. Defaults to the primary index.
        :return: List of the raw search results.
        """
        result = []
        done = False
        start_key = None
        scan_kwargs = {
            "KeyConditionExpression": _build_key_expression(
                keys, filter_expression is not None
            )
        }
        if index:
            scan_kwargs["IndexName"] = index

        if filter_expression:
            scan_kwargs["FilterExpression"] = filter_expression

        while not done:
            if start_key:
                scan_kwargs["ExclusiveStartKey"] = start_key
            response = self.table.query(**scan_kwargs)
            result += response["Items"]

            start_key = response.get("LastEvaluatedKey", None)
            done = start_key is None

        return result

    def list_entities(self, loader: DefaultLoader, id: str = None) -> List[Noun]:
        raise NotImplementedError()

    def _get_next_version(self, id_: int):
        existing = self._do_search_entities({"identifier": id_})
        max_version = CURRENT_VERSION
        if existing:
            max_version = max(ent["version"].split('#')[0] for ent in existing)
        return "v" + str(int(max_version[1:]) + 1)

    def put_entity(self, entity: Entity):
        utcnow = datetime.utcnow()
        if not hasattr(entity, "identifier") or entity.identifier is None:
            entity.identifier = gen_new_key()
            entity._created = utcnow
        entity._updated = utcnow
        # when we put an entity, we need to put it as "v0" (current)
        # as well as the actual version that it represents, e.g. "v5"
        data = entity.serialize()
        for attr, val in data.items():
            if isinstance(val, float):
                data[attr] = Decimal(val)

        data["entity_name"] = entity.get_namespace_name()
        data["version"] = CURRENT_VERSION
        new_version = self._get_next_version(entity.identifier)
        data["current_version"] = new_version

        if isinstance(entity, Relationship):
            relationship = entity  # type: Relationship
            self._do_freeze_current_rel_nouns(relationship.identifier)

            # we need to reference the actual version number, not "v0"
            if isinstance(relationship.ref_to, relationship.ref_to_type()):
                data["ref_to"] = relationship.ref_to.identifier
            else:
                data["ref_to"] = relationship.ref_to
            data["ref_to_type"] = relationship.ref_to_type().get_namespace_name()

            # we need to reference the actual version number, not "v0"
            if isinstance(relationship.ref_from, relationship.ref_from_type()):
                data["ref_from"] = relationship.ref_from.identifier
            else:
                data["ref_from"] = relationship.ref_from
            data["ref_from_type"] = relationship.ref_from_type().get_namespace_name()
        try:
            self.table.put_item(Item=data)
        except botocore.exceptions.ClientError as e:
            logger.error(f"Exception: {e.response['Error']['Message']}")
            self._put_large_entity(entity, data)
        # now put it as the actual version...
        del data["current_version"]
        data["version"] = new_version
        try:
            self.table.put_item(Item=data)
        except botocore.exceptions.ClientError as e:
            self._put_large_entity(entity, data)
        return entity

    def _put_large_entity(self, entity: Entity, data: dict):
        for k, attr in entity.entity_definition()["attributes"].items():
            item = {
                "identifier": entity.identifier,
                "version": f"{data['version']}#{k}",
                "entity_name": data["entity_name"],
                "_extended": True,
                k: data.get(k),
            }
            if "current_version" in data:
                item["current_version"] = f"{data['current_version']}#{k}"

            item_size = sys.getsizeof(json.dumps(item))
            if attr["type"] in ["mapping", "collection", "blob"] and item_size > 400000:
                blob_size = sys.getsizeof(data.get(k))
                meta_size = item_size - blob_size
                x = 400000 - meta_size
                chunk = 0
                blob = data.get(k).encode("utf-8")
                for i in range(0, len(blob), x):
                    blob_chunk = blob[i : i + x].decode("utf-8")
                    item = {
                        "identifier": entity.identifier,
                        "version": f"{data['version']}#{k}#{chunk}",
                        "entity_name": data["entity_name"],
                        "_extended": True,
                        k: blob_chunk,
                    }
                    if "current_version" in data:
                        item["current_version"] = (
                            f"{data['current_version']}#{k}#{chunk}"
                        )
                    self.table.put_item(Item=item)
                    chunk += 1
            else:
                self.table.put_item(Item=item)
        item = {
            "identifier": entity.identifier,
            "version": data["version"],
            "entity_name": data["entity_name"],
            "_created": data["_created"],
            "_updated": data["_updated"],
            "_extended": True,
        }
        if "current_version" in data:
            item["current_version"] = data["current_version"]
        self.table.put_item(Item=item)

    def _do_freeze_current_rel_nouns(self, id_: int):
        """
        Freeze the current version of the from and to nouns of the relationship.

        :param id_: The relationship id.
        :return:
        """
        raw_rels = self._do_search_entities(keys={"identifier": id_})
        v0_version = list(
            filter(lambda rel: rel["version"] == CURRENT_VERSION, raw_rels)
        )
        if v0_version:
            v0_version = v0_version[0]
            current_version = list(
                filter(
                    lambda rel: rel["version"] == v0_version["current_version"],
                    raw_rels,
                )
            )
            assert (
                len(current_version) == 1
            ), f"The version marked as current does not exist for entity: {id_}"
            current_version = current_version[0]

            raw_from = self._get_current_entity(current_version["ref_from"])
            if raw_from:
                current_version["ref_from_version"] = raw_from["current_version"]

            raw_to = self._get_current_entity(current_version["ref_to"])
            if raw_to:
                current_version["ref_to_version"] = raw_to["current_version"]

            self.table.put_item(Item=current_version)

    def delete_entity(self, entity_def: Type[Entity], id_: int) -> None:
        if issubclass(entity_def, Noun):
            # if it's a noun, then delete all relationships...
            results = self._do_search_entities(
                keys={"ref_from": id_},
                filter_expression=_build_key_expression({"version": CURRENT_VERSION}),
                index="FromIndex",
            )
            for data in results:
                self._do_freeze_current_rel_nouns(data["identifier"])
                self.table.delete_item(
                    Key={"identifier": data["identifier"], "version": CURRENT_VERSION}
                )

            results = self._do_search_entities(
                keys={"ref_to": id_},
                filter_expression=_build_key_expression({"version": CURRENT_VERSION}),
                index="ToIndex",
            )
            for data in results:
                self._do_freeze_current_rel_nouns(data["identifier"])
                self.table.delete_item(
                    Key={"identifier": data["identifier"], "version": CURRENT_VERSION}
                )
        else:
            self._do_freeze_current_rel_nouns(id_)

        self.table.delete_item(Key={"identifier": id_, "version": CURRENT_VERSION})

    def _remove_fields(self, adict: Dict, field_names: List[str]):
        for fn in field_names:
            if fn in adict:
                del adict[fn]

    def _result_to_entity(self, entity_def: Type[Entity], data: Dict):
        if "_extended" in data:
            items = self.table.query(
                KeyConditionExpression=And(
                    Key("identifier").eq(data["identifier"]),
                    Key("version").begins_with(CURRENT_VERSION),
                )
            )
            if "Items" in items:
                items = sorted(items["Items"], key=lambda i: i["version"])
                for item in items:
                    if len(item["version"].split("#")) >= 3:
                        key = item["version"].split("#")[1]
                        data = {**data, key: data.get(key, "") + item[key]}
                    else:
                        data = {**data, **item}

        self._remove_fields(
            data,
            [
                "entity_name",
                "version",
                "current_version",
                "ref_from_version",
                "ref_to_version",
                "_extended",
            ],
        )
        if issubclass(entity_def, Relationship):
            del data["ref_from_type"]
            del data["ref_to_type"]

        data = decimal_decoder(data)
        return Entity.deserialize(entity_def, data)

    def get_relationships_from(
        self, relationship_def: Type[Relationship], id_: int
    ) -> List[Relationship]:
        results = self._do_search_entities(
            keys={
                "ref_from": id_,
                "entity_name": relationship_def.get_namespace_name(),
            },
            filter_expression=_build_key_expression({"version": CURRENT_VERSION}),
            index="FromIndex",
        )
        return [self._result_to_entity(relationship_def, data) for data in results]

    def get_relationships_to(
        self, relationship_def: Type[Relationship], id_: int
    ) -> List[Relationship]:
        results = self._do_search_entities(
            keys={"ref_to": id_, "entity_name": relationship_def.get_namespace_name()},
            filter_expression=_build_key_expression({"version": CURRENT_VERSION}),
            index="ToIndex",
        )

        return [self._result_to_entity(relationship_def, data) for data in results]

    def native_query_nouns(
        self, query: Any, data: Dict[str, Any]
    ) -> List[Tuple[str, Dict]]:
        raise NotImplementedError()

    def native_query_relationships(
        self, query: Any, data: Dict[str, Any]
    ) -> List[Tuple[str, Dict]]:
        raise NotImplementedError()

    def begin_transaction(self) -> None:
        pass

    def commit_transaction(self) -> None:
        pass

    def rollback_transaction(self) -> None:
        pass
