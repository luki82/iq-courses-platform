from django.core.management.base import BaseCommand
from django.db import transaction

from iqtest.models import Category, Choice, Question

CATEGORY_SLUG = "full-iq-assessment"
TIME_LIMIT_MINUTES = 30
PRICE_CENTS = 1000  # $10 one-off, per attempt
CURRENCY = "aud"

# 30 items, ordered from easiest to hardest (as in Raven's and the Wechsler
# scales, where difficulty rises through the test). Each item has exactly four
# options so the chance of guessing correctly is the same (25%) everywhere.
#
# Domains are modelled loosely on the CHC factors that WAIS-IV and SB5 measure:
#   Gf  fluid reasoning (figural matrices, series, deduction)
#   Gc  verbal comprehension (similarities, vocabulary, analogies)
#   Gq  quantitative reasoning
#   Gv  visual-spatial processing
#   Gwm working memory (mental re-ordering and multi-step arithmetic)
#
# All items are original. None is copied from a published test.
QUESTIONS = [
    # 1 -- Gf, letter series (easy)
    {
        "text": "What letter comes next in the sequence?\n\nC, F, I, L, O, ?",
        "explanation": "Each letter moves 3 places forward in the alphabet: C, F, I, L, O, R.",
        "choices": [("P", False), ("Q", False), ("R", True), ("S", False)],
    },
    # 2 -- Gq, rate (easy)
    {
        "text": "A vehicle travels at a constant 60 km/h for 45 minutes. How far does it go?",
        "explanation": "60 km/h is 1 km per minute, so 45 minutes covers 45 km.",
        "choices": [("40 km", False), ("45 km", True), ("50 km", False), ("55 km", False)],
    },
    # 3 -- Gf, figural matrix (easy)
    {
        "text": (
            "Which symbol completes the grid?\n\n"
            "●   ▲   ■\n"
            "▲   ■   ●\n"
            "■   ●   ?"
        ),
        "explanation": (
            "Every row and every column contains each of ●, ▲ and ■ exactly once. "
            "The bottom row already has ■ and ●, so the missing symbol is ▲."
        ),
        "choices": [("●", False), ("▲", True), ("■", False), ("◆", False)],
    },
    # 4 -- Gc, similarities (easy)
    {
        "text": "In what way are a THERMOMETER and a RULER most alike?",
        "explanation": (
            "Both are instruments for measuring. The other options describe surface "
            "features some examples share, not what the two things fundamentally are."
        ),
        "choices": [
            ("Both are usually made of glass", False),
            ("Both are measuring instruments", True),
            ("Both have numbers printed on them", False),
            ("Both are used in science classrooms", False),
        ],
    },
    # 5 -- Gv, mental rotation (easy)
    {
        "text": "Which capital letter looks exactly the same after being turned upside down (rotated 180 degrees)?",
        "explanation": (
            "Rotating N by 180 degrees gives N again. R, F and G all look different "
            "when turned upside down."
        ),
        "choices": [("R", False), ("N", True), ("F", False), ("G", False)],
    },
    # 6 -- Gf, alternating series (easy)
    {
        "text": "What pair of letters comes next?\n\nA, Z, B, Y, C, X, ?",
        "explanation": (
            "The letters alternate between counting forward from A (A, B, C, D) and "
            "backward from Z (Z, Y, X, W). The next pair is D, W."
        ),
        "choices": [("D, W", True), ("E, V", False), ("D, V", False), ("E, W", False)],
    },
    # 7 -- Gf/Gq, number matrix (easy)
    {
        "text": (
            "Which number completes the grid?\n\n"
            "3    5    8\n"
            "4    6    10\n"
            "5    7    ?"
        ),
        "explanation": "In each row the first two numbers add up to the third: 5 + 7 = 12.",
        "choices": [("11", False), ("12", True), ("13", False), ("14", False)],
    },
    # 8 -- Gv, paper folding (easy-medium)
    {
        "text": (
            "A square sheet of paper is folded in half from left to right, then in half "
            "again from top to bottom. One hole is punched through all the layers, away "
            "from the folds. How many holes are there when the paper is unfolded?"
        ),
        "explanation": (
            "Two folds stack the paper into 4 layers. One punch goes through all 4, "
            "so unfolding shows 4 holes."
        ),
        "choices": [("1", False), ("2", False), ("4", True), ("8", False)],
    },
    # 9 -- Gc, odd one out (easy-medium)
    {
        "text": "Which word does NOT belong with the others?",
        "explanation": (
            "Elated, jubilant and euphoric all describe intense happiness. "
            "Placid means calm and untroubled, which is a different state."
        ),
        "choices": [("Elated", False), ("Jubilant", False), ("Euphoric", False), ("Placid", True)],
    },
    # 10 -- Gf, number series (medium)
    {
        "text": "What number comes next in the sequence?\n\n3, 5, 9, 17, 33, ?",
        "explanation": "Each term is doubled and then 1 is subtracted: 33 x 2 - 1 = 65.",
        "choices": [("49", False), ("55", False), ("65", True), ("67", False)],
    },
    # 11 -- Gf, alternating operations (medium)
    {
        "text": "Which number completes the pattern?\n\n84, 42, 44, 22, 24, 12, ?",
        "explanation": (
            "The pattern alternates between halving and adding 2: "
            "84 / 2 = 42, + 2 = 44, / 2 = 22, + 2 = 24, / 2 = 12, + 2 = 14."
        ),
        "choices": [("6", False), ("10", False), ("14", True), ("16", False)],
    },
    # 12 -- Gc, analogy (medium)
    {
        "text": "CARTOGRAPHER is to MAP as LEXICOGRAPHER is to:",
        "explanation": "A cartographer compiles maps; a lexicographer compiles dictionaries.",
        "choices": [("Atlas", False), ("Dictionary", True), ("Language", False), ("Library", False)],
    },
    # 13 -- Gf, figural matrix with two rules (medium)
    {
        "text": (
            "Which cell completes the grid?\n\n"
            "●      ▲▲      ■■■\n"
            "▲      ■■      ●●●\n"
            "■      ●●      ?"
        ),
        "explanation": (
            "Two rules apply at once. The number of symbols equals the column number "
            "(1, 2, 3), and each row uses each shape once. The bottom row already has "
            "■ and ●, so the missing cell is three triangles: ▲▲▲."
        ),
        "choices": [("■■■", False), ("▲▲▲", True), ("●●●", False), ("▲▲", False)],
    },
    # 14 -- Gwm, letter-number sequencing (medium)
    {
        "text": (
            "Read the list once, then re-order it in your head: numbers first from "
            "smallest to largest, then letters in alphabetical order.\n\n"
            "7, K, 2, B, 9, F"
        ),
        "explanation": "Numbers in order are 2, 7, 9. Letters in order are B, F, K. Together: 2 7 9 B F K.",
        "choices": [
            ("2 7 9 B F K", True),
            ("B F K 2 7 9", False),
            ("2 7 9 K F B", False),
            ("2 9 7 B F K", False),
        ],
    },
    # 15 -- Gf, categorical syllogism (medium)
    {
        "text": (
            "All architects are designers. No designers are careless.\n\n"
            "Which conclusion must be true?"
        ),
        "explanation": (
            "Every architect is inside the group of designers, and no designer is "
            "careless, so no architect can be careless. 'Some designers are not "
            "architects' may be true in real life, but it does not follow from the "
            "two statements."
        ),
        "choices": [
            ("Some architects are careless", False),
            ("No architects are careless", True),
            ("All designers are architects", False),
            ("Some designers are not architects", False),
        ],
    },
    # 16 -- Gv, cube net (medium)
    {
        "text": (
            "A cube net is laid out as a cross. A vertical strip of four squares is "
            "labelled 2, 1, 3, 6 from top to bottom. Square 4 is attached to the left "
            "of square 1, and square 5 to the right of square 1.\n\n"
            "When the net is folded into a cube, which face is opposite face 1?"
        ),
        "explanation": (
            "In a straight strip of four squares, faces two apart end up opposite each "
            "other: 2 is opposite 3, and 1 is opposite 6. The side flaps 4 and 5 are "
            "opposite each other."
        ),
        "choices": [("2", False), ("3", False), ("5", False), ("6", True)],
    },
    # 17 -- Gf, second-order series (medium)
    {
        "text": "What number comes next in the sequence?\n\n2, 6, 12, 20, 30, 42, ?",
        "explanation": (
            "The gaps are 4, 6, 8, 10, 12, growing by 2 each time. The next gap is 14, "
            "so 42 + 14 = 56."
        ),
        "choices": [("52", False), ("54", False), ("56", True), ("58", False)],
    },
    # 18 -- Gf, ordering constraints (medium)
    {
        "text": (
            "Five people (A, B, C, D, E) sit in a row of five seats. C is in the middle "
            "seat. D sits immediately to the right of C. A does not sit next to C.\n\n"
            "Where must A sit?"
        ),
        "explanation": (
            "Number the seats 1 to 5. C is in seat 3 and D in seat 4. A cannot be in "
            "seat 2 or 4, which are next to C, so A must be in seat 1 or seat 5, at one "
            "of the ends."
        ),
        "choices": [
            ("Immediately left of C", False),
            ("At one of the two ends", True),
            ("Next to D", False),
            ("There is no valid seat", False),
        ],
    },
    # 19 -- Gc, vocabulary (medium)
    {
        "text": "Which word is closest in meaning to EPHEMERAL?",
        "explanation": "Ephemeral means lasting for a very short time.",
        "choices": [("Short-lived", True), ("Ethereal", False), ("Essential", False), ("Recurring", False)],
    },
    # 20 -- Gwm/Gq, multi-step mental arithmetic (medium)
    {
        "text": (
            "A bus leaves the depot with 24 passengers. At the first stop, a quarter of "
            "them get off and 6 new passengers get on. At the second stop, a third of "
            "the people on board get off.\n\n"
            "How many passengers are left on the bus?"
        ),
        "explanation": (
            "A quarter of 24 is 6, so 18 remain; 6 get on, making 24. A third of 24 is "
            "8, so 24 - 8 = 16 remain."
        ),
        "choices": [("14", False), ("16", True), ("18", False), ("20", False)],
    },
    # 21 -- Gf, conditional reasoning / modus tollens (medium-hard)
    {
        "text": (
            "If it rains, the match is cancelled. The match was not cancelled.\n\n"
            "What can you conclude?"
        ),
        "explanation": (
            "If rain always leads to cancellation, and there was no cancellation, then "
            "it cannot have rained. This form of reasoning is called modus tollens."
        ),
        "choices": [
            ("It rained", False),
            ("It did not rain", True),
            ("The match was moved indoors", False),
            ("Nothing can be concluded", False),
        ],
    },
    # 22 -- Gq, rate problem (medium-hard)
    {
        "text": (
            "If 3 cats catch 3 mice in 3 minutes, how many cats are needed to catch "
            "100 mice in 100 minutes?"
        ),
        "explanation": (
            "Together the 3 cats catch 1 mouse per minute. Over 100 minutes the same "
            "3 cats catch 100 mice."
        ),
        "choices": [("3", True), ("33", False), ("100", False), ("300", False)],
    },
    # 23 -- Gf, geometric series (medium-hard)
    {
        "text": "What number comes next in the sequence?\n\n100, 96, 88, 72, 40, ?",
        "explanation": (
            "The amount subtracted doubles each step: 4, 8, 16, 32, then 64. "
            "40 - 64 = -24."
        ),
        "choices": [("0", False), ("-8", False), ("-24", True), ("-32", False)],
    },
    # 24 -- Gc, abstract analogy (medium-hard)
    {
        "text": "EPIPHANY is to REALISATION as PARADOX is to:",
        "explanation": (
            "An epiphany is a sudden realisation. In the same way, a paradox is a "
            "statement that contains an apparent contradiction."
        ),
        "choices": [("Contradiction", True), ("Solution", False), ("Confusion", False), ("Argument", False)],
    },
    # 25 -- Gf, figural matrix with rotation (hard)
    {
        "text": (
            "Which arrow completes the grid?\n\n"
            "↑    →    ↓\n"
            "↗    ↘    ↙\n"
            "→    ↓    ?"
        ),
        "explanation": (
            "Moving one cell to the right turns the arrow 90 degrees clockwise. "
            "In the bottom row, → turns to ↓, and ↓ turns to ←."
        ),
        "choices": [("←", True), ("↑", False), ("↙", False), ("↖", False)],
    },
    # 26 -- Gv, 3D visualisation (hard)
    {
        "text": (
            "A 3 x 3 x 3 cube is painted on all its outside faces, then cut into 27 "
            "equal small cubes. How many of the small cubes have paint on exactly "
            "two faces?"
        ),
        "explanation": (
            "Corner cubes have 3 painted faces (8 of them). Each of the 12 edges has "
            "one middle cube with 2 painted faces, giving 12. Face centres have 1 "
            "painted face (6), and the single core cube has none. Check: "
            "8 + 12 + 6 + 1 = 27."
        ),
        "choices": [("6", False), ("8", False), ("12", True), ("24", False)],
    },
    # 27 -- Gq, percentage reasoning (hard)
    {
        "text": (
            "A shop raises the price of an item by 20%, then later reduces the new "
            "price by 20%. Compared with the original price, the final price is:"
        ),
        "explanation": (
            "Take an original price of $100. Up 20% gives $120. Down 20% of $120 is "
            "$24, giving $96, which is 4% lower than the original."
        ),
        "choices": [
            ("The same", False),
            ("2% lower", False),
            ("4% lower", True),
            ("4% higher", False),
        ],
    },
    # 28 -- Gv, mirror image (hard)
    {
        "text": (
            "An analogue clock (one with hands and no numbers) is seen in a mirror. "
            "In the mirror it appears to show 3:40. What is the real time?"
        ),
        "explanation": (
            "A mirror flips the clock left to right, so the real time and the mirrored "
            "time always add up to 12:00. 12:00 - 3:40 = 8:20."
        ),
        "choices": [("8:20", True), ("9:20", False), ("8:40", False), ("3:20", False)],
    },
    # 29 -- Gq, algebraic word problem (hard)
    {
        "text": (
            "A father is 4 times as old as his son. In 20 years he will be twice as "
            "old as his son. How old is the son now?"
        ),
        "explanation": (
            "Let the son be S, so the father is 4S. In 20 years: 4S + 20 = 2(S + 20), "
            "so 4S + 20 = 2S + 40, giving 2S = 20 and S = 10."
        ),
        "choices": [("5", False), ("10", True), ("12", False), ("15", False)],
    },
    # 30 -- Gf, figural matrix, exclusive-or rule (hardest)
    {
        "text": (
            "Each cell contains a set of letters. Which set completes the grid?\n\n"
            "A B      B C      A C\n"
            "D E      E F      D F\n"
            "G H      H K      ?"
        ),
        "explanation": (
            "In each row, the third cell keeps only the letters that appear in exactly "
            "one of the first two cells; a letter shared by both cancels out. "
            "G H and H K share H, so the answer is G K."
        ),
        "choices": [("G K", True), ("G H K", False), ("H", False), ("G H", False)],
    },
]


class Command(BaseCommand):
    help = (
        "Seeds the 30-question Full IQ Assessment (timed). Does nothing if the "
        "category already has questions, unless --reset is given."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help=(
                "Delete and recreate this category's questions. Warning: this also "
                "deletes users' saved answers to those questions."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        category, created = Category.objects.get_or_create(
            slug=CATEGORY_SLUG,
            defaults={
                "name": "Full IQ Assessment",
                "description": (
                    "30 questions on patterns and matrices, numbers, word meaning, "
                    "spatial thinking and working memory, getting harder as you go."
                ),
                "is_premium": False,
                "time_limit_minutes": TIME_LIMIT_MINUTES,
                "price_cents": PRICE_CENTS,
                "currency": CURRENCY,
            },
        )

        if category.questions.exists():
            if not options["reset"]:
                self.stdout.write(
                    "Full IQ Assessment already has questions; skipping (use --reset to replace them)."
                )
                return
            category.questions.all().delete()

        for order, item in enumerate(QUESTIONS, start=1):
            correct = [text for text, is_correct in item["choices"] if is_correct]
            if len(correct) != 1:
                raise ValueError(f"Question {order} must have exactly one correct choice.")
            question = Question.objects.create(
                category=category,
                text=item["text"],
                explanation=item["explanation"],
                order=order,
            )
            Choice.objects.bulk_create(
                Choice(question=question, text=text, is_correct=is_correct)
                for text, is_correct in item["choices"]
            )

        self.stdout.write(self.style.SUCCESS(
            f"Full IQ Assessment seeded with {len(QUESTIONS)} questions "
            f"({category.time_limit_minutes or 'no'} minute time limit)."
        ))
