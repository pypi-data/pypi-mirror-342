"""
Vibepy CLI interface
"""

import argparse
from .main import main as vibepy_main

def parse_args():
    parser = argparse.ArgumentParser(description="Vibepy: A Python REPL with hotkey functionality")
    parser.add_argument("-r", "--run", action="store_true", help="Run mode (execute code from responses)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    return parser.parse_args()

def run_vibepy(run: bool = False, model: str = "gpt-4o-mini"):
    """Run vibepy.py with the specified run parameter."""
    vibepy_main(run=run, model=model)

def main():
    args = parse_args()
    run_vibepy(run=args.run, model=args.model)

if __name__ == "__main__":
    main() 