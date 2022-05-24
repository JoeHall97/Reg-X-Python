"""
Takes in a FSM and a string, then checks if the string is accepted by the FSM.
"""
import sys


class FSMState:
    def __init__(self, state_num, chars, connection1, connection2):
        self.state_number = state_num
        self.chars = chars
        self.connection1 = connection1
        self.connection2 = connection2

    def print_state(self):
        print(str(self.state_number) + " " + self.chars + " " + str(self.connection1) + " " + str(self.connection2))


def parse_states(s):
    states = s.split('\n')
    for x in range(len(states)):
        # if the state isn't blank, parse and add it to the list
        if states[x]:
            state = states[x]
            state_split = state.split(' ')
            state_num = int(state_split[0])
            state_con_1 = int(state_split[len(state_split)-2])
            state_con_2 = int(state_split[len(state_split)-1])
            if len(state_split) == 4:
                state_char = state_split[1]
            elif len(state_split) == 5:
                state_char = state_split[1]
            # ! need to implement check if char has a space in it !
            states[x] = FSMState(state_num, state_char, state_con_1, state_con_2)
        # if the state is blank, remove it
        else:
            states.pop(x)
    return states


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python3 REGCompile.py <regular_expression> | python3 REGCheck.py <string>")
        print("OR")
        print("Usage: python3 REGCheck.py <FSM> <string>")
        sys.exit(1)
    # fsm = string = ""
    if len(sys.argv) == 2:
        fsm = parse_states(sys.stdin.read())
        string = sys.argv[1]
    else:
        file = sys.argv[1]
        f = open(file, 'r')
        fsm = parse_states(f.read())
        string = sys.argv[2]
    final_state = len(fsm)-1
    for state in fsm:
        state.print_state()
    deque = []
    chars = list(string)
    curr_char = 0
    deque.append(fsm[0])
    while True:
        if deque[0].chars == '':
            # check that the whole string has been parsed too.
            if deque[0].state_number == final_state:
                print("String is accepted by the REG-X")
                break
            if deque[0].connection1 == deque[0].connection2:
                deque.append(fsm[deque[0].connection1])
            else:
                deque.append(fsm[deque[0].connection1])
                deque.append(fsm[deque[0].connection2])
            deque.pop(0)
        else:
            if curr_char < len(chars) and deque[0].chars == chars[curr_char]:
                if deque[0].connection1 == deque[0].connection2:
                    deque.append(fsm[deque[0].connection1])
                else:
                    deque.append(fsm[deque[0].connection1])
                    deque.append(fsm[deque[0].connection2])
                curr_char += 1
            deque.pop(0)
        if not deque:
            print("String not accepted by the REG-X")
            break
    print("Finished")


main()