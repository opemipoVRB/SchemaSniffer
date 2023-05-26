# Usage example
from src.schema_generator import JSONSchemaGenerator


def main():
    input_files = ['../data/data_1.json', '../data/data_2.json']
    output_files = ['../schema/schema_1.json', '../schema/schema_2.json']

    for index, input_file in enumerate(input_files):
        schema_generator = JSONSchemaGenerator(input_file, output_files[index])
        schema_generator.generate_schema_file()


if __name__ == "__main__":
    main()
