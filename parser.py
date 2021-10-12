import re

expr = input("enter ur expression bitch or q to exit: ")
# flag  = 0

NUM = re.compile(r"(?P<NUM>\d+)")


def generate(expr):
    if isinstance(expr, int):
        print(f".load {expr}")
        return

    elif isinstance(expr, str):
        print(".mult" if expr == "*" else ".add")
        return

    left, middle, right = expr

    generate(left)
    generate(right)
    generate(middle)


def parser():
    global expr

    while expr != "q":
        expr = expr.replace(" ", "")
        # flag = 0
        try:
            ex = e()
            print("valid" if not expr else f"invalid, {expr=}")
            print(ex)
            generate(ex)
        except (IndexError, ValueError):
            print("invalid")

        expr = input("enter ur expression bitch or q to exit: ")


# def check_stop():
#     if flag:
#         raise ValueError


def advance(offset=1):
    global expr
    expr = expr[offset:]


def e():
    # check_stop()

    prod = p()

    if expr and expr[0] == "+":
        match("+")
        ex = e()
        return (prod, "+", ex)

    return prod


def p():
    # check_stop()

    term = t()

    if expr and expr[0] == "*":
        match("*")
        prod = p()
        return (term, "*", prod)

    return term


def t():
    # check_stop()

    if expr[0] == "(":
        match("(")
        ex = e()
        match(")")
        return ex

    return read_number()


def match(symbol):
    # check_stop()

    # global flag

    next = expr[0]
    advance()

    if next != symbol:
        # flag = 1
        raise ValueError


def read_number():
    global expr

    if not expr:
        return

    # if check_stop():
    #     return

    match = NUM.match(expr)

    if not match:
        raise ValueError

    number = match.group("NUM")

    advance(len(number))

    return int(number)


if __name__ == "__main__":
    parser()
