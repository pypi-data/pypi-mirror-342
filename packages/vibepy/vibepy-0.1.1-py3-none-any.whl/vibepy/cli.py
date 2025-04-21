"""
Vibepy CLI interface
"""

import argparse
import sys
from .main import main as vibepy_main

def parse_args():
    parser = argparse.ArgumentParser(description="Vibepy: A Python REPL with hotkey functionality")
    parser.add_argument("--run", type=str, default="False", help="Run mode (True/False)")
    return parser.parse_args()

def run_vibepy(run: bool = False):
    """Run vibepy.py with the specified run parameter."""
    sys.argv = ["vibepy", "--run", str(run)]
    vibepy_main()

def main():
    args = parse_args()
    run_vibepy(run=args.run.lower() == "true")

if __name__ == "__main__":
    main() 