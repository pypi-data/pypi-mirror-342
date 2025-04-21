"""
Vibepy: A Python REPL talking to and running codes from open-ai
"""

import argparse
import sys
from colorama import init, Fore
from openai import OpenAI
import requests
from vibepy import codeblock, run

client = OpenAI()

def main(execute: bool = False, model: str = "gpt-4o-mini"):
    init()  # Initialize colorama

    print(Fore.GREEN + "Welcome to Vibepy!")
    print(Fore.YELLOW + "Press 'q' to exit")

    while True:
        user_input = input(Fore.CYAN + "Say something: ")

        try:
            # Get OpenAI's response
            response = client.chat.completions.create(model=model,
            messages=[
                {"role": "system", "content": "You are a helpful Python coding assistant. Please first use uv to manage the environment: source .venv/bin/activate, then using uv add or uv pip install, then generate the code to be executed. Please keep the code blocks as few as possible and in order of being executed."},
                {"role": "user", "content": user_input}
            ])
            reply = response.choices[0].message.content
            print(Fore.RED + "\nVibepy: " + reply + "\n")
            
            if execute:
                # Create code blocks from the reply
                code_blocks = codeblock.create_code_block(reply)
                max_retries = 5
                retry_count = 0
                last_error = None
                
                while retry_count < max_retries:
                    try:
                        # Try running the code blocks in order
                        run.run_code_ordered(code_blocks)
                        break  # Success, exit retry loop
                    except Exception as e:
                        last_error = str(e)
                        retry_count += 1
                        if retry_count < max_retries:
                            print(Fore.YELLOW + f"Attempt {retry_count}/{max_retries} failed: {last_error}")
                            print(Fore.YELLOW + "Retrying with error feedback...")
                            
                            # Get new response with error feedback
                            error_response = client.chat.completions.create(
                                model=model,
                                messages=[
                                    {"role": "system", "content": "You are a helpful Python coding assistant. Please first use uv to manage the environment: source .venv/bin/activate, then using uv add or uv pip install, then generate the code to be executed. Please keep the code blocks as few as possible and in order of being executed."},
                                    {"role": "user", "content": user_input},
                                    {"role": "assistant", "content": reply},
                                    {"role": "user", "content": f"The code failed with error: {last_error}. Please fix the code and try again."}
                                ]
                            )
                            reply = error_response.choices[0].message.content
                            print(Fore.RED + "\nVibepy: " + reply + "\n")
                            code_blocks = codeblock.create_code_block(reply)
                        else:
                            print(Fore.RED + f"Failed after {max_retries} attempts. Last error: {last_error}")
                            # If all retries fail, try all permutations as last resort
                            try:
                                run.run_code_permutations(code_blocks)
                            except Exception as e:
                                print(Fore.RED + f"All execution attempts failed: {str(e)}")
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")

        if user_input == 'q':
            print(Fore.RED + "\nExiting vibepy...")
            break

        print(Fore.YELLOW + "Press 'q' to exit")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vibepy: talking to and running codes from open-ai")
    parser.add_argument("-e", "--execute", action="store_true", help="Execute code from responses")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    args = parser.parse_args()
    main(execute=args.execute, model=args.model)
