import json
from os.path import join, dirname
from jsonschema import validate


def assert_valid_schema(data, schema_file):
    """ Comprueba si unos datos determinados se corresponden con el esquema """

    schema = _load_json_schema(schema_file)
    return validate(data, schema)


def _load_json_schema(filename):
    """ Carga el esquema """

    relative_path = join('schemas', filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())
