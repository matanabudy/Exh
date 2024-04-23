from exh import *

universe = Universe(fs = [a, b])
# Test AND
and_sentence = a & b
evaluated = universe.evaluate(and_sentence)

assert np.equal(evaluated, [[False], [False], [False], [True]]).all(), f"And failed: {evaluated}"

# Test OR
or_sentence = a | b
evaluated = universe.evaluate(or_sentence)

assert np.equal(evaluated, [[False], [True], [True], [True]]).all(), f"Or failed: {evaluated}"

# Test NOT
not_sentence = ~a
evaluated = universe.evaluate(not_sentence)

assert np.equal(evaluated, [[True], [False], [True], [False]]).all(), f"Not failed: {evaluated}"

# Test Nand
nand_sentence = Nand(a, b)
evaluated = universe.evaluate(nand_sentence)

assert np.equal(evaluated, [[True], [True], [True], [False]]).all(), f"Nand failed: {evaluated}"

# Test Nor
nor_sentence = Nor(a, b)
evaluated = universe.evaluate(nor_sentence)

assert np.equal(evaluated, [[True], [False], [False], [False]]).all(), f"Nor failed: {evaluated}"

# Test Xor
xor_sentence = Xor(a, b)
evaluated = universe.evaluate(xor_sentence)

assert np.equal(evaluated, [[False], [True], [True], [False]]).all(), f"Xor failed: {evaluated}"

# Test Iff
iff_sentence = Iff(a, b)
evaluated = universe.evaluate(iff_sentence)

assert np.equal(evaluated, [[True], [False], [False], [True]]).all(), f"Iff failed: {evaluated}"