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

def main():
    init()  # Initialize colorama

    parser = argparse.ArgumentParser(description="Vibepy: talking to and running codes from open-ai")
    parser.add_argument("-r", "--run", action="store_true", help="Run mode (execute code from responses)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    args = parser.parse_args()

    print(Fore.GREEN + "Welcome to Vibepy!")
    print(Fore.YELLOW + "Press 'q' to exit")

    while True:
        user_input = input(Fore.CYAN + "Say something: ")

        try:
            # Get OpenAI's response
            response = client.chat.completions.create(model=args.model,
            messages=[
                {"role": "system", "content": "You are a helpful Python coding assistant."},
                {"role": "user", "content": user_input}
            ])
            reply = response.choices[0].message.content
            print(Fore.RED + "\nVibepy: " + reply + "\n")
            
            if args.run:
                # Create code blocks from the reply
                code_blocks = codeblock.create_code_block(reply)
                try:
                    # Try running the code blocks in order
                    run.run_code_ordered(code_blocks)
                except Exception as e:
                    print(Fore.YELLOW + f"Trying alternative execution order due to: {str(e)}")
                    # If that fails, try all permutations
                    run.run_code_permutations(code_blocks)
        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")

        if user_input == 'q':
            print(Fore.RED + "\nExiting vibepy...")
            break

        print(Fore.YELLOW + "Press 'q' to exit")

if __name__ == "__main__":
    main()
