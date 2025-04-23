import json

def parse_dict(data):
    schema = {}

    for key, value in data.items():
        if isinstance(value, dict):
            schema[key] = parse_dict(value)

        elif isinstance(value, list):
            schema[key] = parse_list(value)

        else:
            schema[key] = value.__class__.__name__
    return schema
        
def parse_list(data):

    if len(data) == 0:
        return 'list' 

    if isinstance(data[0], dict):
        list_length = len(data)
        parsed_schema = parse_dict(data[0])
        return parsed_schema, {"_length": list_length}
    
    return 'list'

def initialise_schema(data):
    if isinstance(data, dict):
        schema = parse_dict(data)
    elif isinstance(data, list):
        schema = parse_list(data)
    else:
        schema = "Not valid JSON"
    return schema


def schema(data):
     return json.dumps(initialise_schema(data), indent=3)

