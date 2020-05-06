"""
Takes in a regular expression and checks if it is valid.
Valid Expressions will be output as a FSM, while invalid expressions will print an error and terminate.
The expressions that are accepted can be found in GRAMMER.md.
"""
import sys


_regx = ""
_states = []
_current_char = 0
_state = 0
_operators = ['!', '[', ']', '(', ')', '*', '|', '?', '+', '\\']


class FSMState:
    def __init__(self, state_num, chars, connection1, connection2):
        self.state_number = state_num
        self.chars = chars
        self.connection1 = connection1
        self.connection2 = connection2

    def printState(self):
        print(str(self.state_number) + " " + self.chars + " " + str(self.connection1) + " " + str(self.connection2))


def parse():
    global _state, _states, _current_char
    # set initial state
    setState(_state, " ", _state+1, _state+1)
    _state += 1
    # parse expression
    initial_state = expression()
    _states[0].connection1 = initial_state
    _states[0].connection2 = initial_state
    # if the expression was invalid, error out
    if _current_char < len(_regx):
        error()
    # set final state
    setState(_state, " ", 0, 0)


def expression():
    global _states, _state, _current_char
    prev_state = _state-1
    curr_state = term1 = term()
    if _current_char < len(_regx) and _regx[_current_char] == '|':
        if _states[prev_state].connection1 == _states[prev_state].connection2:
            _states[prev_state].connection1 = _state
        _states[prev_state].connection2 = _state
        _current_char += 1
        prev_state = _state-1
        curr_state = _state
        # create a branch state
        setState(_state, " ", term1, term1-1)
        _state += 1
        term2 = expression()
        _states[curr_state].connection2 = term2
        if _states[prev_state].connection1 == _states[prev_state].connection2:
            _states[prev_state].connection1 = _state
        _states[prev_state].connection2 = _state
        setState(_state, " ", _state+1, _state+1)
        _state += 1
    return curr_state


def term():
    global _state, _current_char
    prev_state = _state-1
    curr_factor = factor()
    if _current_char < len(_regx):
        if _regx[_current_char] == '*':
            if _states[prev_state].connection1 == _states[prev_state].connection2:
                _states[prev_state].connection1 = _state
            _states[prev_state].connection2 = _state
            # create a branch state
            setState(_state, " ", curr_factor, _state+1)
            _current_char += 1
            curr_factor = _state
            _state += 1
        elif _regx[_current_char] == '+':
            setState(_state, " ", curr_factor, _state+1)
            _state += 1
            _current_char += 1
        elif _regx[_current_char] == '?':
            if _states[prev_state].connection1 == _states[prev_state].connection2:
                _states[prev_state].connection1 = _state
            _states[prev_state].connection2 = _state
            if _states[_state-1].connection1 == _states[_state-1].connection2:
                _states[_state-1].connection1 = _state+1
            _states[_state-1].connection2 = _state+1
            # create a branch state
            setState(_state, " ", curr_factor, _state+1)
            curr_factor = _state
            _state += 1
            _current_char += 1
            # create a blank state
            setState(_state, " ", _state+1, _state+1)
            _state += 1
        if _current_char < len(_regx):
            if _regx[_current_char] != ')' and _regx[_current_char] != '|' and _regx[_current_char] != '|':
                term()
    return curr_factor


def factor():
    global _current_char, _regx, _state
    factor_pos = 0
    if _current_char < len(_regx):
        # if it's a literal
        if _regx[_current_char] not in _operators:
            setState(_state, _regx[_current_char], _state+1, _state+1)
            factor_pos = _state
            _current_char += 1
            _state += 1
        # if it's escape character
        elif _regx[_current_char] == '\\':
            setState(_state, '('+_regx[_current_char+1]+')', _state+1, _state+1)
            factor_pos = _state
            _state += 1
            _current_char += 2
        # if it's an open bracket
        elif _regx[_current_char] == '(':
            _current_char += 1
            # if there's a following character
            if _current_char < len(_regx):
                # insert a dummy state
                setState(_state, " ", _state+1, _state+1)
                factor_pos = _state
                _state += 1
                expression()
                # if it's a closing bracket
                if _regx[_current_char] == ')':
                    _current_char += 1
                # if the character isn't a closing bracket, error out
                else:
                    error()
        elif _regx[_current_char] == '[':
            _current_char += 1
            if _current_char < len(_regx):
                setState(_state, " ", _state+1, _state+1)
                factor_pos = _state
                _state += 1
                temp_char = _current_char
                if _regx[temp_char] == ']':
                    temp_char += 1
                else:
                    while 1 < 2:
                        if temp_char > len(_regx):
                            error()
                        if _regx[temp_char] == ']':
                            break
                        temp_char += 1
                setState(_state, '('+_regx[_current_char:temp_char]+')', _state+1, _state+1)
                _state += 1
                _current_char = temp_char+1
            else:
                error()
        elif _regx[_current_char] == '!' and _current_char+1 < len(_regx) and _regx[_current_char+1] == '[':
            _current_char += 2
            if _current_char < len(_regx):
                setState(_state, " ", _state+1, _state+1)
                factor_pos = _state
                _state += 1
                temp_char = _current_char
                if temp_char+1 >= len(_regx):
                    error()
                elif _regx[temp_char] == ']' and _regx[temp_char+1] == '!':
                    temp_char += 1
                else:
                    while 1 < 2:
                        if temp_char >= len(_regx) or temp_char+1 >= len(_regx):
                            error()
                        if _regx[temp_char] == ']' and _regx[temp_char+1] == '!':
                            break
                        temp_char += 1
                setState(_state, ')' + _regx[_current_char:temp_char] + '(', _state + 1, _state + 1)
                _state += 1
                _current_char = temp_char + 2
        else:
            error()
    return factor_pos


def error():
    print("Expression is not valid.")
    sys.exit(1)


def setState(num, chars, connection1, connection2):
    global _states
    _states.append(FSMState(num, chars, connection1, connection2))


def main():
    global _states, _regx
    if len(sys.argv) != 2:
        print('Usage: python3 REGCompiler.py <regular_expression>')
        sys.exit(1)
    _regx = sys.argv[1]
    print(_regx)
    parse()
    if _states:
        for s in _states:
            s.printState()
    else:
        error()

main()

