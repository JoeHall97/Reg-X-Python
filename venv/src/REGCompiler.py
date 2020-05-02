"""
Takes in a regular expression and checks if it is valid.
Valid Expressions will be output as a FSM, while invalid expressions will print an error and terminate.
The expressions that are accepted can be found in GRAMMER.md.
"""
import sys


regx = ""
states = []
current_char = 0
state = 0
operators = ['!', '[', ']', '(', ')', '*', '|', '?', '+', '\\']


class FSMState:
    def __init__(self, state_num, chars, connection1, connection2):
        self.state_number = state_num
        self.chars = chars
        self.connection1 = connection1
        self.connection2 = connection2

    def printState(self):
        print(str(self.state_number) + " " + self.chars + " " + str(self.connection1) + " " + str(self.connection2))


def parse():
    global state, states, current_char
    # set initial state
    setState(state, " ", state+1, state+1)
    state += 1
    # parse expression
    initial_state = expression()
    states[0].connection1 = initial_state
    states[0].connection2 = initial_state
    # if the expression was invalid, error out
    if current_char < len(regx):
        error()
    # set final state
    setState(state, " ", 0, 0)


def expression():
    global states, state, current_char
    prev_state = state-1
    curr_state = term1 = term()
    if current_char < len(regx) and regx[current_char] == '|':
        if states[prev_state].connection1 == states[prev_state].connection2:
            states[prev_state].connection1 = state
        states[prev_state].connection2 = state
        current_char += 1
        prev_state = state-1
        curr_state = state
        # create a branch state
        setState(state, " ", term1, term1-1)
        state += 1
        term2 = expression()
        states[curr_state].connection2 = term2
        if states[prev_state].connection1 == states[prev_state].connection2:
            states[prev_state].connection1 = state
        states[prev_state].connection2 = state
        setState(state, " ", state+1, state+1)
        state += 1
    return curr_state


def term():
    global state, current_char
    prev_state = state-1
    curr_factor = factor()
    if current_char < len(regx):
        if regx[current_char] == '*':
            if states[prev_state].connection1 == states[prev_state].connection2:
                states[prev_state].connection1 = state
            states[prev_state].connection2 = state
            # create a branch state
            setState(state, " ", curr_factor, state+1)
            current_char += 1
            curr_factor = state
            state += 1
        elif regx[current_char] == '+':
            setState(state, " ", curr_factor, state+1)
            state += 1
            current_char += 1
        elif regx[current_char] == '?':
            if states[prev_state].connection1 == states[prev_state].connection2:
                states[prev_state].connection1 = state
            states[prev_state].connection2 = state
            if states[state-1].connection1 == states[state-1].connection2:
                states[state-1].connection1 = state+1
            states[state-1].connection2 = state+1
            # create a branch state
            setState(state, " ", curr_factor, state+1)
            curr_factor = state
            state += 1
            current_char += 1
            # create a blank state
            setState(state, " ", state+1, state+1)
            state += 1
        if current_char < len(regx):
            if regx[current_char] != ')' and regx[current_char] != '|' and regx[current_char] != '|':
                term()
    return curr_factor


def factor():
    global current_char, regx, state
    factor_pos = 0
    if current_char < len(regx):
        # if it's a literal
        if regx[current_char] not in operators:
            setState(state, regx[current_char], state+1, state+1)
            factor_pos = state
            current_char += 1
            state += 1
        # if it's escape character
        elif regx[current_char] == '\\':
            setState(state, '('+regx[current_char+1]+')', state+1, state+1)
            factor_pos = state
            state += 1
            current_char += 2
        # if it's an open bracket
        elif regx[current_char] == '(':
            current_char += 1
            # if there's a following character
            if current_char < len(regx):
                # insert a dummy state
                setState(state, " ", state+1, state+1)
                factor_pos = state
                state += 1
                expression()
                # if it's a closing bracket
                if regx[current_char] == ')':
                    current_char += 1
                # if the character isn't a closing bracket, error out
                else:
                    error()
        elif regx[current_char] == '[':
            current_char += 1
            if current_char < len(regx):
                setState(state, " ", state+1, state+1)
                factor_pos = state
                state += 1
                temp_char = current_char
                if regx[temp_char] == ']':
                    temp_char += 1
                else:
                    while 1 < 2:
                        if temp_char > len(regx):
                            error()
                        if regx[temp_char] == ']':
                            break
                        temp_char += 1
                setState(state, '('+regx[current_char:temp_char]+')', state+1, state+1)
                state += 1
                current_char = temp_char+1
            else:
                error()
        elif regx[current_char] == '!' and current_char+1 < len(regx) and regx[current_char+1] == '[':
            current_char += 2
            if current_char < len(regx):
                setState(state, " ", state+1, state+1)
                factor_pos = state
                state += 1
                temp_char = current_char
                if regx[temp_char] == ']':
                    temp_char += 1
                else:
                    while 1 < 2:
                        if temp_char > len(regx):
                            error()
                        if regx[temp_char] == ']':
                            break
                        temp_char += 1
                setState(state, ')' + regx[current_char:temp_char] + '(', state + 1, state + 1)
                state += 1
                current_char = temp_char + 1
        else:
            error()
    return factor_pos


def error():
    print("Expression is not valid.")
    states = []
    sys.exit(1)


def setState(num, chars, connection1, connection2):
    global states
    states.append(FSMState(num, chars, connection1, connection2))


def main():
    global states, regx
    if len(sys.argv) != 2:
        print('Usage: python3 REGCompiler.py <regular_expression>')
    regx = sys.argv[1]
    print(regx)
    parse()
    if states:
        for s in states:
            s.printState()
    else:
        error()

main()

