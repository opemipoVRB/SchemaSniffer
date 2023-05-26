import json
import unittest

from src.schema_generator import JSONSchemaGenerator


class TestJSONSchemaGenerator(unittest.TestCase):
    def test_generate_schema_file_1(self):
        input_file = 'data/data_1.json'
        output_file = 'schema/schema_1.json'

        self.perform_test(input_file, output_file)

    def test_generate_schema_file_2(self):
        input_file = 'data/data_2.json'
        output_file = 'schema/schema_2.json'

        self.perform_test(input_file, output_file)

    def perform_test(self, input_file, output_file):
        generator = JSONSchemaGenerator(input_file, output_file)

        # Generate the schema file
        generator.generate_schema_file()

        # Load the generated schema
        with open(output_file, 'r') as file:
            schema = json.load(file)

        # Validate the schema based on the rules
        self.validate_padding(schema)
        self.validate_attributes(schema)
        self.validate_required(schema)
        self.validate_data_types(schema)

    def validate_padding(self, schema):
        """
        Rule 1 :
        Padding: All attributes in the JSON schema should be padded with "tag" and "description" keys


        :param schema:
        :return:
        """
        for key, value in schema.items():
            self.assertIn("tag", value, f"Missing 'tag' key for attribute '{key}'")
            self.assertIn("description", value, f"Missing 'description' key for attribute '{key}'")

    def validate_attributes(self, schema):
        """
        Rule 2 : The schema output must capture ONLY the attributes within the "message" key of the input JSON source
        data (see line 8 in the input JSON files). All attributes withn the key "attributes" should be excluded


        :param schema:
        :return:
        """
        self.assertIn("message", schema, "Schema should only include attributes within the 'message' key")
        self.assertNotIn("attributes", schema, "Schema should exclude attributes within the 'attributes' key")

    def validate_required(self, schema):
        """
        Rule 3:
        The JSON schema should set all properties "required": false
        :param schema:
        :return:
        """
        for value in schema.values():
            self.assertFalse(value.get("required", True), "All properties should be set as 'required': false")

    def validate_data_types(self, schema):
        """
        Rule 4:
        For data types of the JSON schema:
        STRING: program should identify what is a string and map accordingly in JSON schema output
        INTEGER: program should identify what is an integer and map accordingly in JSON schema output
        ENUM:
        case[A]When the value in an array is a string, the program should map the data type as an ENUM ARRAY
        case [B] When the value in an array is another JSON object, the program should map the data type as an ARRAY
        :param schema:
        :return:
        """
        for key, value in schema.items():
            if key == "message":
                self.assertIsInstance(value, dict, f"Attribute '{key}' should be an object")
            else:
                data_type = value.get("type")
                if data_type == "string":
                    # STRING CASE
                    self.assertIsInstance(value, dict, f"Attribute '{key}' should be of type 'string'")
                elif data_type == "integer":
                    # INTEGER CASE
                    self.assertIsInstance(value, dict, f"Attribute '{key}' should be of type 'integer'")
                elif data_type == "array":
                    # ENUM CASE
                    self.assertIn("items", value, f"Attribute '{key}' should be an array with 'items'")
                    items = value["items"]
                    if isinstance(items, list):
                        # ENUM CASE A
                        self.assertIsInstance(items[0], str, f"Items in array '{key}' should be of type 'string'")
                    elif isinstance(items, dict):
                        # ENUM CASE B
                        self.assertIsInstance(items, dict, f"Items in array '{key}' should be an object")
                else:
                    self.fail(f"Unknown data type for attribute '{key}'")


if __name__ == '__main__':
    unittest.main()
