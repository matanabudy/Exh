from exh import *

universe = Universe(fs=[a, b])
# Test AND
and_sentence = a & b
evaluated = universe.evaluate(and_sentence)

assert np.equal(evaluated, [[False], [False], [False], [True]]).all(), f"And failed: {evaluated}"
assert a & b == b & a, f"And failed: {a & b} != {b & a}"

# Test OR
or_sentence = a | b
evaluated = universe.evaluate(or_sentence)

assert np.equal(evaluated, [[False], [True], [True], [True]]).all(), f"Or failed: {evaluated}"
assert a | b == b | a, f"Or failed: {a | b} != {b | a}"

# Test NOT
not_sentence = ~a
evaluated = universe.evaluate(not_sentence)

assert np.equal(evaluated, [[True], [False], [True], [False]]).all(), f"Not failed: {evaluated}"

# Test Nand
nand_sentence = Nand(a, b)
evaluated = universe.evaluate(nand_sentence)

assert np.equal(evaluated, [[True], [True], [True], [False]]).all(), f"Nand failed: {evaluated}"
assert Nand(a, b) == Nand(b, a), f"Nand failed: {Nand(a, b)} != {Nand(b, a)}"

# Test Nor
nor_sentence = Nor(a, b)
evaluated = universe.evaluate(nor_sentence)

assert np.equal(evaluated, [[True], [False], [False], [False]]).all(), f"Nor failed: {evaluated}"
assert Nor(a, b) == Nor(b, a), f"Nor failed: {Nor(a, b)} != {Nor(b, a)}"

# Test Xor
xor_sentence = Xor(a, b)
evaluated = universe.evaluate(xor_sentence)

assert np.equal(evaluated, [[False], [True], [True], [False]]).all(), f"Xor failed: {evaluated}"
assert Xor(a, b) == Xor(b, a), f"Xor failed: {Xor(a, b)} != {Xor(b, a)}"

# Test Iff
iff_sentence = Iff(a, b)
evaluated = universe.evaluate(iff_sentence)

assert np.equal(evaluated, [[True], [False], [False], [True]]).all(), f"Iff failed: {evaluated}"
assert Iff(a, b) == Iff(b, a), f"Iff failed: {Iff(a, b)} != {Iff(b, a)}"

# Test OnlyL
onlyl_sentence = OnlyL(a, b)
evaluated = universe.evaluate(onlyl_sentence)

assert np.equal(evaluated, [[False], [True], [False], [False]]).all(), f"OnlyL failed: {evaluated}"
assert OnlyL(a, b) != OnlyL(b, a), f"OnlyL failed: {OnlyL(a, b)} == {OnlyL(b, a)}"

# Test OnlyR
onlyr_sentence = OnlyR(a, b)
evaluated = universe.evaluate(onlyr_sentence)

assert np.equal(evaluated, [[False], [False], [True], [False]]).all(), f"OnlyR failed: {evaluated}"
assert OnlyR(a, b) != OnlyR(b, a), f"OnlyR failed: {OnlyR(a, b)} == {OnlyR(b, a)}"
