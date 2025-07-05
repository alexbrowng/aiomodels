from aiomodels.response_formats.json_schema_response_format import JsonSchema, JsonSchemaResponseFormat
from aiomodels.response_formats.text_response_format import TextResponseFormat


def test_text_response_format():
    fmt = TextResponseFormat()
    assert fmt.type == "text"


def test_json_schema_response_format():
    schema_dict = {"type": "object", "properties": {"foo": {"type": "string"}}}
    json_schema = JsonSchema(
        name="TestSchema",
        description="A test schema",
        strict=True,
        schema=schema_dict,
    )
    fmt = JsonSchemaResponseFormat(json_schema=json_schema)
    assert fmt.type == "json_schema"
    assert fmt.json_schema == json_schema
    assert fmt.json_schema.schema == schema_dict
