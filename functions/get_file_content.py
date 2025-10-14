import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    inside = os.path.commonpath([abs_working, abs_path]) == abs_working
    if not inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            next_char = f.read(1)
            if next_char:
                return file_content_string + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]' 
            return file_content_string 
    except Exception as e:
        return f"Error: {e}" 

            

