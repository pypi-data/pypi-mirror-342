from pathlib import Path
import jsonref

current_path = Path(__file__).parent.resolve()
schema_path = Path("{}/schemas/bdp.schema.json".format(current_path)).absolute()
with open(schema_path, "r") as file:
    schema = jsonref.load(file, base_uri=schema_path.as_uri())
