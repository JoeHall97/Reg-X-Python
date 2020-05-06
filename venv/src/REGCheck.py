import sys


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python3 REGCompile.py <regular_expression> | python3 REGCheck.py <string>")
        print("OR")
        print("Usage: python3 REGCheck.py <FSM> <string>")
        sys.exit(1)
    fsm = string = ""
    if len(sys.argv) == 2:
        fsm = sys.stdin.read()
        string = sys.argv[1]
    else:
        fsm = sys.argv[1]
        string = sys.argv[2]
    print(fsm)
    print(string)


main()