import typing

from aiomodels.json_schema.array import Array
from aiomodels.json_schema.boolean import Boolean
from aiomodels.json_schema.enum import Enum
from aiomodels.json_schema.integer import Integer
from aiomodels.json_schema.json_schema import JsonSchema
from aiomodels.json_schema.number import Number
from aiomodels.json_schema.object import Object
from aiomodels.json_schema.property import Property
from aiomodels.json_schema.string import String
from aiomodels.json_schema.type import JsonSchemaType


class JsonSchemaBuilder:
    @staticmethod
    def build_json_schema(data: dict) -> JsonSchema:
        schema_dict: dict = data.get("schema", {})
        schema_object = JsonSchemaBuilder.build_object(schema_dict)
        return JsonSchema(
            name=data.get("name") or "",
            description=data.get("description") or "",
            strict=data.get("strict", False),
            schema=schema_object,
        )

    @staticmethod
    def build_type(schema: dict) -> JsonSchemaType:
        if not isinstance(schema, dict):
            raise ValueError("schema must be a dict")

        type_value = schema.get("type")

        base_type: str | None
        if isinstance(type_value, list):
            base_type = next((t for t in type_value if t != "null"), None)
        else:
            base_type = typing.cast(str | None, type_value)

        if base_type == "object":
            return JsonSchemaBuilder.build_object(schema)
        if base_type == "array":
            return JsonSchemaBuilder.build_array(schema)
        if base_type == "string":
            if "enum" in schema:
                return JsonSchemaBuilder.build_enum(schema)
            return JsonSchemaBuilder.build_string(schema)
        if base_type == "integer":
            return JsonSchemaBuilder.build_integer(schema)
        if base_type == "number":
            return JsonSchemaBuilder.build_number(schema)
        if base_type == "boolean":
            return JsonSchemaBuilder.build_boolean(schema)

        raise ValueError(f"Unsupported or missing type in schema: {type_value}")

    @staticmethod
    def _is_nullable(schema: dict) -> bool:
        type_value = schema.get("type")
        return isinstance(type_value, list) and "null" in type_value

    @staticmethod
    def build_object(schema: dict) -> Object:
        properties_dict: dict = schema.get("properties", {})
        required_list: list[str] = schema.get("required", [])

        properties: list[Property] = []
        for property_name, property_schema in properties_dict.items():
            parameter = JsonSchemaBuilder.build_type(property_schema)
            properties.append(
                Property(name=property_name, parameter=parameter, required=property_name in required_list)
            )

        return Object(*properties, description=schema.get("description"))

    @staticmethod
    def build_array(schema: dict) -> Array:
        items_schema = schema.get("items", {})
        items_type = JsonSchemaBuilder.build_type(items_schema)
        return Array(
            items=items_type,
            description=schema.get("description"),
            nullable=JsonSchemaBuilder._is_nullable(schema),
        )

    @staticmethod
    def build_string(schema: dict) -> String:
        return String(
            description=schema.get("description"),
            default=schema.get("default"),
            nullable=JsonSchemaBuilder._is_nullable(schema),
        )

    @staticmethod
    def build_integer(schema: dict) -> Integer:
        return Integer(
            description=schema.get("description"),
            default=schema.get("default"),
            nullable=JsonSchemaBuilder._is_nullable(schema),
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
        )

    @staticmethod
    def build_number(schema: dict) -> Number:
        return Number(
            description=schema.get("description"),
            default=schema.get("default"),
            nullable=JsonSchemaBuilder._is_nullable(schema),
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
        )

    @staticmethod
    def build_boolean(schema: dict) -> Boolean:
        return Boolean(
            description=schema.get("description"),
            default=schema.get("default"),
            nullable=JsonSchemaBuilder._is_nullable(schema),
        )

    @staticmethod
    def build_enum(schema: dict) -> Enum:
        return Enum(
            choices=schema.get("enum", []),
            description=schema.get("description"),
            default=schema.get("default"),
            nullable=JsonSchemaBuilder._is_nullable(schema),
        )
