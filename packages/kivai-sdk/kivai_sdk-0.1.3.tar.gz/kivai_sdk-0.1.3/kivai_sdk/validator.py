import json
import pkg_resources
from jsonschema import validate, ValidationError

# Load schema from package resources
schema_path = pkg_resources.resource_filename(
    __name__, "schema/kivai-command.schema.json"
)
with open(schema_path, "r") as file:
    kivai_schema = json.load(file)

def validate_command(command: dict) -> tuple[bool, str]:
    try:
        validate(instance=command, schema=kivai_schema)
        return True, "✅ Command is valid!"
    except ValidationError as e:
        return False, f"❌ Validation failed: {e.message}"
