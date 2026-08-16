import os, subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python script at the specified relative file path, optionally with command-line arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The Python file path relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Optional list of arguments to pass to the Python file",
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, file_path))
        common_path = os.path.commonpath([absolute_path, target_directory]) == absolute_path
    
        if not common_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_directory):    
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_directory.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_directory]

        if args:
            command.extend(args)

        result = subprocess.run(
            command, 
            cwd=absolute_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        retcode = result.returncode

        if retcode != 0:
            print(f'Process exited with code {result.returncode}')

        output_summary = (
            f'STDOUT: {result.stdout if result.stdout else f"No output produced"}\n'
            f'"result": {retcode}\n'
            f'STDERR: {result.stderr if result.stderr else f"No output produced"}'
        ) 
        return output_summary

    except Exception as e:
        return f"Error: {e}"