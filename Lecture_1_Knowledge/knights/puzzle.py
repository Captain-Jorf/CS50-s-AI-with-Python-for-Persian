from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


def rules(*chars):
    facts = []
    for c in chars:
        k, n = c
        facts.append(Or(k, n))
        facts.append(Not(And(k, n)))
    return And(*facts)


# Puzzle 0
# A says "I am both a knight and a knave."
sA0 = And(AKnight, AKnave)
knowledge0 = And(
    rules((AKnight, AKnave)),
    Biconditional(AKnight, sA0)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sA1 = And(AKnave, BKnave)
knowledge1 = And(
    rules((AKnight, AKnave), (BKnight, BKnave)),
    Biconditional(AKnight, sA1)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sA2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sB2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    rules((AKnight, AKnave), (BKnight, BKnave)),
    Biconditional(AKnight, sA2),
    Biconditional(BKnight, sB2)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave.'"
# B then says "C is a knave."
# C says "A is a knight."
sA3 = Or(AKnight, AKnave)
sB3a = Biconditional(AKnight, AKnave)
sB3b = CKnave
sC3 = AKnight
knowledge3 = And(
    rules((AKnight, AKnave), (BKnight, BKnave), (CKnight, CKnave)),
    Biconditional(AKnight, sA3),
    Biconditional(BKnight, sB3a),
    Biconditional(BKnight, sB3b),
    Biconditional(CKnight, sC3)
)


def main():
    symbols = [
        AKnight, AKnave, BKnight, BKnave, CKnight, CKnave
    ]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()