from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ValidationError


schema = {
    "type": "array",
    "items": {
        type: "object",
    },
}


def validate(pipeline_descriptor: dict):
    jsonschema_validate(instance=pipeline_descriptor, schema=schema)
