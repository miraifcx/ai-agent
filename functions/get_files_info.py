import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "List the files and directories in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The relative path of the directory to list",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, directory))
        common_path = os.path.commonpath([absolute_path, target_directory]) == absolute_path

        if not common_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        print(f'Success: "{directory}" is within the working directory')

        outputs = []

        list_dir = os.listdir(target_directory)
        for d in list_dir:
            full_path = os.path.join(target_directory, d)

            is_directory = os.path.isdir(full_path)
            byte_size = os.path.getsize(full_path) if not is_directory else 0
            
            outputs.append(f" - {d}: file_size={byte_size}, is_dir={is_directory}")

        return "\n".join(outputs)

    except Exception as e:  
        return f"Error: {e}"

# print(get_files_info("calculator", "."))