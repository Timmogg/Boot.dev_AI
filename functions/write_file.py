import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    inside = os.path.commonpath([abs_working, abs_path]) == abs_working
    dirs = os.path.dirname(abs_path)
    if not inside:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(dirs, exist_ok=True)
        with open(abs_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content for writing or overwriting in the file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write or overwrite.",
            )
        }
    )
)
