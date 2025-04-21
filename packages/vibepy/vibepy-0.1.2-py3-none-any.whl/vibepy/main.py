"""
Vibepy: A Python REPL with hotkey functionality
"""

import argparse
import sys
from colorama import init, Fore
from readchar import readkey, key
from openai import OpenAI

client = OpenAI()
import requests
import pyperclip

def main():
    init()  # Initialize colorama

    parser = argparse.ArgumentParser(description="Vibepy: A Python REPL with hotkey functionality")
    parser.add_argument("--run", type=str, default="False", help="Run mode (True/False)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    args = parser.parse_args()

    run_mode = args.run.lower() == "true"

    print(Fore.GREEN + "Welcome to Vibepy!")
    print(Fore.YELLOW + "Press ↑ to initiate vibepy")
    print(Fore.YELLOW + "Press ↓ to copy last output to clipboard")
    print(Fore.YELLOW + "Press ESC or 'q' to exit")

    last_output = ""

    while True:
        k = readkey()
        if k == key.UP:
            print(Fore.GREEN + "\nVibepy initiated!")
            user_input = input(Fore.CYAN + "Enter your Python code: ")

            try:
                if run_mode:
                    # Execute the code
                    exec(user_input)
                else:
                    # Get OpenAI's response
                    response = client.chat.completions.create(model=args.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful Python coding assistant."},
                        {"role": "user", "content": user_input}
                    ])
                    reply = response.choices[0].message.content
                    last_output = reply
                    print(Fore.RED + "\nVibepy: " + reply + "\n")
            except Exception as e:
                print(Fore.RED + f"Error: {str(e)}")

        elif k == key.DOWN:
            if last_output:
                pyperclip.copy(last_output)
                print(Fore.GREEN + "\nLast output copied to clipboard!")
            else:
                print(Fore.YELLOW + "\nNo output to copy yet.")

        elif k == key.ESC or k == 'q':
            print(Fore.RED + "\nExiting vibepy...")
            break

        print(Fore.YELLOW + "\nPress ↑ to initiate vibepy")
        print(Fore.YELLOW + "Press ↓ to copy last output to clipboard")
        print(Fore.YELLOW + "Press ESC or 'q' to exit")

if __name__ == "__main__":
    main()
