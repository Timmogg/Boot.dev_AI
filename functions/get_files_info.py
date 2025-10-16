import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    path_to_dir = os.path.abspath(os.path.join(working_directory, directory))
    inside = os.path.commonpath([abs_working, path_to_dir]) == abs_working
    if not inside:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(path_to_dir) is False:
        return f'Error: "{directory}" is not a directory'
    try:
        lines = []
        for name in os.listdir(path_to_dir):
            full = os.path.join(path_to_dir, name)
            is_dir = os.path.isdir(full)
            file_size = os.path.getsize(full) if not is_dir else 0
            lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(lines)
    except OSError as e:
        return f"Error: {e}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
