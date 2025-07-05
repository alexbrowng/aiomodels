from openai.types.shared_params.response_format_json_schema import JSONSchema, ResponseFormatJSONSchema
from openai.types.shared_params.response_format_text import ResponseFormatText

from aiomodels.response_formats.json_schema_response_format import JsonSchemaResponseFormat
from aiomodels.response_formats.response_format import ResponseFormat
from aiomodels.response_formats.text_response_format import TextResponseFormat


class FromResponseFormat:
    @staticmethod
    def from_json_schema_response(response_format: JsonSchemaResponseFormat) -> ResponseFormatJSONSchema:
        return ResponseFormatJSONSchema(
            type="json_schema",
            json_schema=JSONSchema(
                name=response_format.json_schema.name,
                description=response_format.json_schema.description,
                schema=response_format.json_schema.schema.to_primitives(),
                strict=response_format.json_schema.strict,
            ),
        )

    @staticmethod
    def from_text_response(_response_format: TextResponseFormat) -> ResponseFormatText:
        return ResponseFormatText(type="text")

    @staticmethod
    def from_response_format(response_format: ResponseFormat) -> ResponseFormatText | ResponseFormatJSONSchema:
        match response_format:
            case JsonSchemaResponseFormat():
                return FromResponseFormat.from_json_schema_response(response_format)
            case TextResponseFormat():
                return FromResponseFormat.from_text_response(response_format)
