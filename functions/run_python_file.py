import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    inside = os.path.commonpath([abs_working, abs_path]) == abs_working
    exist = os.path.exists(abs_path)
    
    if not inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not exist:
        return f'Error: File "{file_path}" not found.'
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run([sys.executable, abs_path, *args], capture_output=True, text=True, timeout=30, cwd=abs_working)

        stdout = result.stdout or ""
        stderr = result.stderr or ""


        if not stdout and not stderr:
            return "No output produced."

        parts = []
        parts.append(f"STDOUT: {stdout}")
        parts.append(f"STDERR: {stderr}")
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")

        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute.",
            )
        }
    )
)
