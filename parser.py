import re

# use a global variable which isn't ideal
# but I wanted to avoid all the boilerplate that comes with a class
# since we primarily care about the logic
expr = input("enter the expression or q to exit: ")

# match numbers
NUM = re.compile(r"(?P<NUM>\d+)")


def generate(expr):
    """
    generate assembly code for an expression
    traverses the parse "tree" recursively
    e.g. for (12 * (2 + 4) * 3), the tree looks like
    (12, '*', ((2, '+', 4), '*', 3))
    """
    # check for int and string since python doesn't have pattern matching
    if isinstance(expr, int):
        print(f".load {expr}")
        return

    elif isinstance(expr, str):
        print(".mult" if expr == "*" else ".add")
        return

    # if we're here then we have a triplet
    left, middle, right = expr

    # post order traversal
    generate(left)
    generate(right)
    generate(middle)


def parser():
    """
    the actual parsing function,
    processes the expression and handles getting the next expression
    """
    global expr

    while expr != "q":
        expr = expr.replace(" ", "")  # strip whitespace

        try:
            ex = e()  # call e since it's the first production rule

            # valid iff no error and all of expression consumed
            print("valid" if not expr else f"invalid, {expr=}")
            print()
            print(f"parse tree: {ex}")  # the generated tree
            print()

            generate(ex)
            print()

        except (IndexError, ValueError):
            # handle invalid expressions
            print("invalid")

        expr = input("enter your expression or q to exit: ")


def advance(offset=1):
    """
    consumes string based on the rule applied
    """
    global expr
    expr = expr[offset:]


def e():
    """
    E → P + E | P
    """
    prod = p()

    # need to check to very if it is P + E
    if expr and expr[0] == "+":
        match("+")
        ex = e()
        # we return tuples to represent a node and its left and right nodes
        # since then we can apply tuple unpacking to neatly process the tree
        return (prod, "+", ex)

    return prod


def p():
    """
    P → T * P | T
    """
    term = t()

    if expr and expr[0] == "*":
        match("*")
        prod = p()
        return (term, "*", prod)

    return term


def t():
    """
    T → Num | (E)
    """
    if expr[0] == "(":
        match("(")
        ex = e()
        match(")")

        return ex

    # numbers are the leafs of our tree
    # so we just keep them as ints and not tuples
    return read_number()


def match(symbol):
    """
    match provided symbol to the next element in expression
    """
    next = expr[0]
    advance()

    if next != symbol:
        raise ValueError


def read_number():
    """
    read a number from the expression
    """
    if not expr:
        return

    match = NUM.match(expr)

    if not match:
        raise ValueError

    # get the actual number from the match object
    number = match.group("NUM")

    advance(len(number))

    return int(number)


if __name__ == "__main__":
    parser()
