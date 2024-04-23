import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from exh import *


def test_operator(operator, preds, is_commutative, expected_evaluation):
    if operator == Not:
        sentence = operator(preds[0])
        reversed_sentence = sentence
    else:
        sentence = operator(*preds)
        reversed_sentence = operator(*reversed(preds))
    universe = Universe(fs=preds)
    evaluated = universe.evaluate(sentence)

    assert np.equal(evaluated, expected_evaluation).all(), f"{sentence} failed: {evaluated}"

    if is_commutative:
        assert sentence == reversed_sentence, f"{sentence} failed commutativity test"
    else:
        assert sentence != reversed_sentence, f"{sentence} failed commutativity test"


# Tests config
operators_tests = {
    And:
        {
            "preds": [a, b],
            "is_commutative": True,
            "expected_evaluation": [[False], [False], [False], [True]]
        },
    Or:
        {
            "preds": [a, b],
            "is_commutative": True,
            "expected_evaluation": [[False], [True], [True], [True]]
        },
    Not:
        {
            "preds": [a, b],
            "is_commutative": True,  # Vacuously true
            "expected_evaluation": [[True], [False], [True], [False]]
        },
    Nand:
        {
            "preds": [a, b],
            "is_commutative": True,
            "expected_evaluation": [[True], [True], [True], [False]]
        },
    Nor:
        {
            "preds": [a, b],
            "is_commutative": True,
            "expected_evaluation": [[True], [False], [False], [False]]
        },
    Xor:
        {
            "preds": [a, b],
            "is_commutative": True,
            "expected_evaluation": [[False], [True], [True], [False]]
        },
    Iff:
        {
            "preds": [a, b],
            "is_commutative": True,
            "expected_evaluation": [[True], [False], [False], [True]]
        },
    OnlyL:
        {
            "preds": [a, b],
            "is_commutative": False,
            "expected_evaluation": [[False], [True], [False], [False]]
        },
    OnlyR:
        {
            "preds": [a, b],
            "is_commutative": False,
            "expected_evaluation": [[False], [False], [True], [False]]
        }
}

for operator, test in operators_tests.items():
    test_operator(operator, test["preds"], test["is_commutative"], test["expected_evaluation"])