from jsonschema_explorer import print_schema
import json

def test_flat_json():
    data = {"name": "Alice", "age": 30}
    result = print_schema(data)
    expected = json.dumps({"name": "str", "age": "int"}, indent=3)
    assert result == expected
    