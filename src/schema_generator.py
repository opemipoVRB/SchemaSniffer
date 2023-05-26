import json


class JSONSchemaGenerator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.schema = {}

    def analyze_schema(self, data):
        schema = {}
        for key, value in data.items():
            if isinstance(value, dict):
                # Handle nested objects
                schema[key] = {
                    "type": "object",
                    "properties": self.analyze_schema(value),
                    "tag": "",
                    "description": "",
                    "required": False
                }
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    # Handle arrays of objects
                    schema[key] = {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": self.analyze_schema(value[0]),
                            "tag": "",
                            "description": "",
                            "required": False
                        },
                        "tag": "",
                        "description": "",
                        "required": False
                    }
                elif value and all(isinstance(item, str) for item in value):
                    # Handle arrays of strings (enums)
                    schema[key] = {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "tag": "",
                            "description": "",
                            "enum": list(set(value)),
                            "required": False
                        },
                        "tag": "",
                        "description": "",
                        "required": False
                    }
                else:
                    # Handle arrays of other types
                    schema[key] = {
                        "type": "array",
                        "items": {},
                        "tag": "",
                        "description": "",
                        "required": False
                    }
            elif value is None:
                # Handle null values
                schema[key] = {
                    "type": "null",
                    "tag": "",
                    "description": "",
                    "required": False
                }
            elif isinstance(value, bool):
                # Handle boolean values before integer as it is a subclass of integer
                schema[key] = {
                    "type": "boolean",
                    "tag": "",
                    "description": "",
                    "required": False
                }
            elif isinstance(value, int):
                # Handle integer values
                schema[key] = {
                    "type": "integer",
                    "tag": "",
                    "description": "",
                    "required": False
                }
            elif isinstance(value, str):
                # Handle string values
                schema[key] = {
                    "type": "string",
                    "tag": "",
                    "description": "",
                    "required": False
                }

        return schema

    def generate_schema_file(self):
        with open(self.input_file, 'r') as file:
            json_data = json.load(file)

        # Analyze the schema of the "message" key in the JSON data
        self.schema = {
            "message": {
                "type": "object",
                "properties": self.analyze_schema(json_data["message"]),
                "tag": "",
                "description": "",
                "required": False
            }
        }

        with open(self.output_file, 'w') as file:
            # Write the schema to the output file
            json.dump(self.schema, file, indent=2)

