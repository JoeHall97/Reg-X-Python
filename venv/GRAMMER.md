# RegX-Grammer

The grammer that this compiler accepts is:

E -> T

E -> T|E

T -> F

T -> F*

T -> F+

T -> F?	

T -> FT

F -> .	

F -> v

F -> \F	

F -> (E)

F -> [E]

F -> ![E]!

Where: E = expression, T = terminal, * = any number of, | = either or, + = one or more, ? = one or none, . = any literal, \T = turns T into a literal, [] = matches any contained literal, ![]! = matches none of the contained literals

Note:
This grammer assumes the things like:

a**

b++

c??

are not valid, and so it rejects them.
