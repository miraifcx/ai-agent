import os, argparse, json, sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

from config import MAXITER

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("No API keys were loaded. Please update your .env file.")

def main():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]

    for _ in range(MAXITER):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=messages,
            temperature=0,
            tools=available_functions
        )

        if response.usage is None:
            raise RuntimeError("API response did not include usage metadata")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=True)
                messages.append(result_message)
        else:
            print(f"-> {message.content}")
            break

    else:
        print(f"Error: Model failed to provide a final response within {MAXITER} iterations.")
        sys.exit(1)

if __name__ == "__main__":
    main()  
