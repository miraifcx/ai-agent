import os, sys
sys.path.append("../")

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file at a specified path relative to the working directory, with a set limit of 10,000 characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file, relative to the working directory",
                },
            },
        },
        "required": ["file_path"],
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, file_path))
        common_path = os.path.commonpath([absolute_path, target_directory]) == absolute_path

        if not common_path:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(target_directory, "r") as file:
            read_content = file.read(MAX_CHARS)

            if file.read(1):
                read_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return read_content

    except Exception as e:
        return f"Error: {e}"