import pytest

from Parse import Parse

# the expression and the expected tree for it
# easier to test than valid assembly that depends on this anyway
expr_trees = [
    ("12", 12),
    ("(12)", 12),
    ("3 + 4 * 2", (3, "+", (4, "*", 2))),
    ("3 * 4 + 2", ((3, "*", 4), "+", 2)),
    ("(3 + 4) * 2", ((3, "+", 4), "*", 2)),
    ("(((3 + 4) * 2 + 4))", (((3, "+", 4), "*", 2), "+", 4)),
    ("(12 * 2) + ((2 + 4) * 3)) * (((3 * 2) + 4))", None),
    ("2 + ((3 (((5 + 7) * 2)) + 17 * 3) + 1) * 3", None),
    ("(((((2 * 3) + 1) )))", ((2, "*", 3), "+", 1)),
    (
        "(( 3 * 32) + 1) * ((2 + 7 * 2) + ((4 * 3)))",
        (((3, "*", 32), "+", 1), "*", ((2, "+", (7, "*", 2)), "+", (4, "*", 3))),
    ),
    ("(12 * (2 + 4) * 3)", (12, "*", ((2, "+", 4), "*", 3))),
]


@pytest.mark.parametrize("input, expected", expr_trees)
def test_asm(input, expected):
    assert Parse(input).parser() == expected
