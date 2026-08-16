import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file at a specified path relative to the working directory. Creates parent directories if they don't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path relative to the working directory to write to",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        join_path = os.path.normpath(os.path.join(abs_path, file_path))
        common_paths = os.path.commonpath([abs_path, join_path]) == abs_path

        if not common_paths:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(join_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        complete_dir = os.path.dirname(join_path)
        os.makedirs(complete_dir, exist_ok=True)

        with open(join_path, "w") as file:
            overwrite_file = file.write(content)

            if overwrite_file:
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"