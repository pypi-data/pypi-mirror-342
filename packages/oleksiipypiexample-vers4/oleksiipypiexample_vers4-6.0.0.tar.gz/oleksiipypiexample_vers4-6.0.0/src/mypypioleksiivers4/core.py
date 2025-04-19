# src/mypypioleksiivers4/core.py

import os

def read_file() -> str:
    data_path = os.path.join(os.path.dirname(__file__), "data", "1.txt")
    try:
        with open(data_path, "r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        return "[data file missing]"

def greet(name: str) -> str:
    file_line = read_file()
    return f"{file_line} — Hello, {name}!"

# Testing
if __name__ == "__main__":
    print(greet("HI: "))
