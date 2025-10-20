import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file content
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    verbose = "--verbose" in sys.argv
    user_prompt = next((arg for arg in sys.argv[1:] if not arg.startswith('--')), None)
    if user_prompt == None:
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    try:
        for i in range(20):
            response = client.models.generate_content(
                model = "gemini-2.0-flash-001",
                contents = messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
            if response.text:
                print(response.text)
                break
    except Exception as e:
        return f"Error: {e}"
    for candidate in response.candidates:
        messages.append(candidate.content)
        if hasattr(candidate.content, 'function_call'):
            function_call_object = candidate.content.function_call
            function_responses = call_function(function_call_object)
            messages.append(types.Content(role="user", parts=[types.Part.from_function_response(function_responses)]))

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose)

            if not hasattr(function_call_result, 'parts'):
                raise Exception("function_call_result is missing 'parts'")

            if not function_call_result.parts or len(function_call_result.parts) == 0:
                raise Exception("function_call_result.parts is empty")

            first_part = function_call_result.parts[0]
            if not hasattr(first_part, 'function_response'):
                raise Exception("first_part is missing 'function_response'")

            function_response_obj = first_part.function_response
            if not hasattr(function_response_obj, 'response'):
                raise Exception("function_response_obj is missing 'response'")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(response.text) 
if __name__ == "__main__":
    main()
