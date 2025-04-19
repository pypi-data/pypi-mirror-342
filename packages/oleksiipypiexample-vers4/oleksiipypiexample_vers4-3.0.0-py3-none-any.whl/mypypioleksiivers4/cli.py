from simple_greeter.core import greeting
import sys
def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(greeting(name))

if __name__ == "__main__":
    main()
