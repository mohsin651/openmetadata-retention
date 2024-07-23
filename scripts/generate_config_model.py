import json
import sys
import tempfile
import os
from datamodel_code_generator.__main__ import main

APP_NAME = sys.argv[1]
SCHEMA_JSON_FILE = APP_NAME[0].lower() + APP_NAME[1:] + ".json"
GENERATED_PYTHON_APP_PATH = "src/metadata/community/applications/" + APP_NAME + "/generated"
os.makedirs(GENERATED_PYTHON_APP_PATH, exist_ok=True)

market_place_definition_file = (
    os.path.dirname(__file__)
    + "/../src/json/data/appMarketPlaceDefinition/"
    + SCHEMA_JSON_FILE
)

with (
    open(market_place_definition_file, "r") as fp,
    tempfile.NamedTemporaryFile(mode="w+") as temp_fp,
):
    market_place_definition = json.load(fp)
    config_schema = market_place_definition["configSchema"]
    temp_fp.write(json.dumps(config_schema, indent=2))
    temp_fp.flush()
    main(
        [
            "--input-file-type",
            "jsonschema",
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--input",
            temp_fp.name,
            "--output",
            GENERATED_PYTHON_APP_PATH + "/config.py",
            "--class-name",
            APP_NAME + "Config",
        ]
    )
