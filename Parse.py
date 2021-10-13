import re

# match numbers
NUM = re.compile(r"(?P<NUM>\d+)")


class Parse:
    def __init__(self, expr):
        self.expr = expr

    def generate(self, expr):
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
        self.generate(left)
        self.generate(right)
        self.generate(middle)

    def parser(self):
        """
        the actual parsing function,
        processes the expression and handles getting the next expression
        """
        while self.expr != "q":
            print(f"expression: {self.expr}")
            self.expr = self.expr.replace(" ", "")  # strip whitespace

            try:
                ex = self.e()  # call e since it's the first production rule

                # valid iff no error and all of expression consumed
                print("valid" if not self.expr else f"invalid, {self.expr=}")
                print(f"parse tree: {ex}")  # the generated tree
                print()

                self.generate(ex)

            except (IndexError, ValueError):
                # handle invalid expressions
                print("invalid")

            print()
            self.expr = input("enter your expression or q to exit: ")
            print()

    def advance(self, offset=1):
        """
        consumes string based on the rule applied
        """
        self.expr = self.expr[offset:]

    def e(self):
        """
        E → P + E | P
        """
        prod = self.p()

        # need to check to verify if it is P + E
        if self.expr and self.expr[0] == "+":
            self.match("+")
            ex = self.e()
            # we return tuples to represent a node and its left and right nodes
            # since then we can apply tuple unpacking to neatly process the tree
            return (prod, "+", ex)

        return prod

    def p(self):
        """
        P → T * P | T
        """
        term = self.t()

        if self.expr and self.expr[0] == "*":
            self.match("*")
            prod = self.p()
            return (term, "*", prod)

        return term

    def t(self):
        """
        T → Num | (E)
        """
        if self.expr[0] == "(":
            self.match("(")
            ex = self.e()
            self.match(")")

            return ex

        # numbers are the leafs of our tree
        # so we just keep them as ints and not tuples
        return self.read_number()

    def match(self, symbol):
        """
        match provided symbol to the next element in expression
        """
        next = self.expr[0]
        self.advance()

        if next != symbol:
            raise ValueError

    def read_number(self):
        """
        read a number from the expression
        """
        if not self.expr:
            return

        match = NUM.match(self.expr)

        if not match:
            raise ValueError

        # get the actual number from the match object
        number = match.group("NUM")

        self.advance(len(number))

        return int(number)


if __name__ == "__main__":
    Parse(input("enter your expression or q to exit: ")).parser()
