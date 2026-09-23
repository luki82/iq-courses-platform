from django.core.management.base import BaseCommand
from django.db.models import Max

from iqtest.models import Category, Choice, Question


class Command(BaseCommand):
    help = (
        "Seeds a real, general-purpose IQ test question bank: Verbal Reasoning, "
        "Numerical Reasoning, Logical Reasoning (adds to the existing category "
        "from seed_iqtest if present) and Spatial/Pattern Recognition -- roughly "
        "10 questions each, all free access. Safe to re-run; it will not create "
        "duplicate questions."
    )

    def handle(self, *args, **options):
        verbal, _ = Category.objects.get_or_create(
            slug="verbal-reasoning",
            defaults={
                "name": "Verbal Reasoning",
                "description": "Vocabulary, analogies, and sentence logic.",
                "is_premium": False,
            },
        )
        numerical, _ = Category.objects.get_or_create(
            slug="numerical-reasoning",
            defaults={
                "name": "Numerical Reasoning",
                "description": "Arithmetic, ratios, percentages, and number sequences.",
                "is_premium": False,
            },
        )
        logical, _ = Category.objects.get_or_create(
            slug="logical-reasoning",
            defaults={
                "name": "Logical Reasoning",
                "description": "Number and letter sequences, pattern spotting.",
                "is_premium": False,
            },
        )
        spatial, _ = Category.objects.get_or_create(
            slug="spatial-pattern-recognition",
            defaults={
                "name": "Spatial & Pattern Recognition",
                "description": "Grids, sequences, and visual-style patterns described in text.",
                "is_premium": False,
            },
        )

        self._seed_questions(verbal, VERBAL_QUESTIONS)
        self._seed_questions(numerical, NUMERICAL_QUESTIONS)
        self._seed_questions(logical, LOGICAL_QUESTIONS)
        self._seed_questions(spatial, SPATIAL_QUESTIONS)

        self.stdout.write(self.style.SUCCESS(
            "IQ question bank seeded: Verbal Reasoning (%d), Numerical Reasoning (%d), "
            "Logical Reasoning (%d total), Spatial & Pattern Recognition (%d)." % (
                verbal.questions.count(),
                numerical.questions.count(),
                logical.questions.count(),
                spatial.questions.count(),
            )
        ))

    def _seed_questions(self, category, question_list):
        """Idempotent: only creates a question if one with the same text doesn't
        already exist in this category, so re-running the command is safe and
        won't disturb any questions already seeded (e.g. by seed_iqtest)."""
        next_order = (
            Question.objects.filter(category=category).aggregate(Max("order"))["order__max"] or 0
        ) + 1

        for q in question_list:
            if Question.objects.filter(category=category, text=q["text"]).exists():
                continue
            question = Question.objects.create(
                category=category,
                text=q["text"],
                explanation=q["explanation"],
                order=next_order,
            )
            next_order += 1
            for choice_text, is_correct in q["choices"]:
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)


VERBAL_QUESTIONS = [
    {
        "text": "Choose the word closest in meaning to 'abundant'.",
        "explanation": "Abundant means existing in large quantities; plentiful is the closest match.",
        "choices": [("Scarce", False), ("Plentiful", True), ("Hidden", False), ("Fragile", False)],
    },
    {
        "text": "Choose the word opposite in meaning to 'reluctant'.",
        "explanation": "Reluctant means unwilling to do something; willing is its opposite.",
        "choices": [("Willing", True), ("Hesitant", False), ("Unsure", False), ("Afraid", False)],
    },
    {
        "text": "Complete the analogy: Doctor is to Hospital as Teacher is to ___.",
        "explanation": "A doctor's typical workplace is a hospital; a teacher's typical workplace is a school.",
        "choices": [("Student", False), ("School", True), ("Book", False), ("Lesson", False)],
    },
    {
        "text": "Which word does not belong with the others: Whisper, Shout, Mumble, Chair?",
        "explanation": "Whisper, shout and mumble are all ways of speaking; a chair is an object, not a way of speaking.",
        "choices": [("Whisper", False), ("Shout", False), ("Mumble", False), ("Chair", True)],
    },
    {
        "text": (
            "Choose the best word to complete the sentence: 'The manager decided to proceed "
            "with the plan, ___ the objections raised by her team.'"
        ),
        "explanation": "'Notwithstanding' means 'in spite of', which matches proceeding despite objections.",
        "choices": [("Because of", False), ("Notwithstanding", True), ("Due to", False), ("In favor of", False)],
    },
    {
        "text": "Choose the word closest in meaning to 'meticulous'.",
        "explanation": "Meticulous means showing great attention to detail; 'thorough' is the closest match.",
        "choices": [("Careless", False), ("Thorough", True), ("Hasty", False), ("Uncertain", False)],
    },
    {
        "text": "Which word does not belong: Optimistic, Hopeful, Cheerful, Pessimistic?",
        "explanation": "Pessimistic means expecting the worst -- the opposite of the other three positive words.",
        "choices": [("Optimistic", False), ("Hopeful", False), ("Cheerful", False), ("Pessimistic", True)],
    },
    {
        "text": "Complete the analogy: Author is to Book as Composer is to ___.",
        "explanation": "An author creates a book; a composer creates a symphony (a piece of music).",
        "choices": [("Piano", False), ("Symphony", True), ("Orchestra", False), ("Concert", False)],
    },
    {
        "text": "Choose the meaning closest to 'ambiguous'.",
        "explanation": "Ambiguous means open to more than one interpretation.",
        "choices": [
            ("Clearly stated", False),
            ("Open to more than one interpretation", True),
            ("Completely false", False),
            ("Very detailed", False),
        ],
    },
    {
        "text": "Choose the correct word: 'The new policy will ___ everyone in the department.'",
        "explanation": "'Affect' is a verb meaning to influence something; 'effect' is usually a noun meaning a result.",
        "choices": [("Effect", False), ("Affect", True), ("Effecting", False), ("Affective", False)],
    },
]

NUMERICAL_QUESTIONS = [
    {
        "text": "What is 15% of 240?",
        "explanation": "15% of 240 = 0.15 x 240 = 36.",
        "choices": [("24", False), ("36", True), ("42", False), ("48", False)],
    },
    {
        "text": "A shirt originally priced at $80 is discounted by 25%. What is the sale price?",
        "explanation": "25% of 80 = 20; 80 - 20 = 60.",
        "choices": [("$55", False), ("$60", True), ("$65", False), ("$70", False)],
    },
    {
        "text": (
            "If 3 workers can build a wall in 12 days, how many days would it take 6 "
            "workers working at the same rate?"
        ),
        "explanation": "Doubling the number of workers halves the time needed: 12 / 2 = 6 days.",
        "choices": [("3", False), ("6", True), ("9", False), ("12", False)],
    },
    {
        "text": "What is the next number in the sequence: 3, 6, 12, 24, ___?",
        "explanation": "Each number doubles the previous one: 24 x 2 = 48.",
        "choices": [("30", False), ("36", False), ("48", True), ("60", False)],
    },
    {
        "text": "A train travels 240 km in 3 hours. At the same speed, how far will it travel in 5 hours?",
        "explanation": "Speed = 240 / 3 = 80 km/h; 80 x 5 = 400 km.",
        "choices": [("350 km", False), ("380 km", False), ("400 km", True), ("420 km", False)],
    },
    {
        "text": "What is the ratio of 15 to 45, in simplest form?",
        "explanation": "15:45 simplifies by dividing both sides by 15, giving 1:3.",
        "choices": [("1:2", False), ("1:3", True), ("1:4", False), ("3:1", False)],
    },
    {
        "text": "If x + 7 = 15, what is the value of 2x?",
        "explanation": "x = 15 - 7 = 8, so 2x = 16.",
        "choices": [("8", False), ("14", False), ("16", True), ("22", False)],
    },
    {
        "text": "A recipe needs 2 cups of flour for 12 cookies. How many cups are needed for 30 cookies?",
        "explanation": "2 cups / 12 cookies = 1/6 cup per cookie; 1/6 x 30 = 5 cups.",
        "choices": [("4", False), ("5", True), ("6", False), ("7", False)],
    },
    {
        "text": "What is the next number in the sequence: 2, 5, 11, 23, ___?",
        "explanation": "Each number is roughly doubled and then one is added: 23 x 2 + 1 = 47.",
        "choices": [("35", False), ("41", False), ("47", True), ("53", False)],
    },
    {
        "text": (
            "A car depreciates in value by 10% each year. If it is worth $20,000 now, "
            "approximately what will it be worth after 2 years?"
        ),
        "explanation": "Year 1: 20,000 x 0.9 = 18,000. Year 2: 18,000 x 0.9 = 16,200.",
        "choices": [("$16,000", False), ("$16,200", True), ("$18,000", False), ("$19,800", False)],
    },
]

LOGICAL_QUESTIONS = [
    {
        "text": (
            "All roses are flowers. Some flowers fade quickly. What can we conclude about "
            "roses?"
        ),
        "explanation": (
            "The premises don't specify whether roses are among the flowers that fade "
            "quickly, so it cannot be determined from this information alone."
        ),
        "choices": [
            ("All roses fade quickly", False),
            ("Some roses fade quickly", False),
            ("It cannot be determined whether any roses fade quickly", True),
            ("No roses fade quickly", False),
        ],
    },
    {
        "text": "If today is Wednesday, what day of the week will it be in 100 days?",
        "explanation": "100 divided by 7 leaves a remainder of 2; two days after Wednesday is Friday.",
        "choices": [("Thursday", False), ("Friday", True), ("Saturday", False), ("Sunday", False)],
    },
    {
        "text": (
            "No cats are dogs. All dogs are mammals. Which conclusion correctly follows "
            "from these two statements alone?"
        ),
        "explanation": (
            "The statements link cats to dogs, and dogs to mammals, but say nothing "
            "directly connecting cats to mammals, so it cannot be determined."
        ),
        "choices": [
            ("No cats are mammals", False),
            ("All mammals are dogs", False),
            ("Some cats are mammals", False),
            ("It cannot be determined whether cats are mammals from these statements alone", True),
        ],
    },
    {
        "text": "Complete the sequence: A, D, G, J, ___?",
        "explanation": "Each letter skips two letters, moving 3 positions forward: A(+3)D(+3)G(+3)J(+3)M.",
        "choices": [("K", False), ("L", False), ("M", True), ("N", False)],
    },
    {
        "text": (
            "In a race, Amy finished before Ben. Ben finished before Cleo. Cleo finished "
            "before Dan. Who finished last?"
        ),
        "explanation": "The finishing order is Amy, Ben, Cleo, Dan -- so Dan finished last.",
        "choices": [("Amy", False), ("Ben", False), ("Cleo", False), ("Dan", True)],
    },
    {
        "text": "If some Xs are Ys, and all Ys are Zs, which statement must be true?",
        "explanation": (
            "Since some Xs are Ys, and every Y is also a Z, those particular Xs must also "
            "be Zs -- so at minimum, some Xs are Zs."
        ),
        "choices": [
            ("All Xs are Zs", False),
            ("Some Xs are Zs", True),
            ("No Xs are Zs", False),
            ("All Zs are Xs", False),
        ],
    },
    {
        "text": "Which number is the odd one out: 2, 3, 5, 9, 11, 13?",
        "explanation": "All the others are prime numbers; 9 = 3 x 3 is not prime.",
        "choices": [("2", False), ("9", True), ("11", False), ("13", False)],
    },
    {
        "text": (
            "A box contains only red and blue balls. It is false that 'all the balls are "
            "red.' Which statement must be true?"
        ),
        "explanation": (
            "The negation of 'all are red' means at least one ball is not red -- i.e., at "
            "least one is blue."
        ),
        "choices": [
            ("All the balls are blue", False),
            ("At least one ball is blue", True),
            ("No balls are red", False),
            ("There are no balls in the box", False),
        ],
    },
    {
        "text": "Complete the pattern: 1, 1, 2, 3, 5, 8, ___?",
        "explanation": "This is the Fibonacci sequence -- each number is the sum of the two before it: 5 + 8 = 13.",
        "choices": [("11", False), ("12", False), ("13", True), ("14", False)],
    },
    {
        "text": (
            "It is true that 'some engineers are pilots' and 'some pilots are teachers.' "
            "Can we conclude that 'some engineers are teachers'?"
        ),
        "explanation": (
            "The overlap between engineers and pilots, and the overlap between pilots and "
            "teachers, don't have to involve the same pilots -- so the conclusion doesn't "
            "necessarily follow. This is a classic logical trap."
        ),
        "choices": [
            ("Yes, always", False),
            ("No, not necessarily", True),
            ("Only if all engineers are pilots", False),
            ("Only on weekdays", False),
        ],
    },
]

SPATIAL_QUESTIONS = [
    {
        "text": (
            "A 3x3 grid contains these numbers, reading left to right, top to bottom:\n"
            "2   4   6\n8   10  12\n14  16  ?\n"
            "Each row increases by 2 from left to right. What number completes the grid?"
        ),
        "explanation": "Following the pattern of the third row (14, 16, ...), the next number is 18.",
        "choices": [("17", False), ("18", True), ("19", False), ("20", False)],
    },
    {
        "text": "Complete the sequence: Circle, Square, Triangle, Circle, Square, Triangle, Circle, ___?",
        "explanation": (
            "The three shapes repeat in a fixed cycle of Circle, Square, Triangle. After "
            "the 7th item (Circle), the next one is Square."
        ),
        "choices": [("Circle", False), ("Square", True), ("Triangle", False), ("Pentagon", False)],
    },
    {
        "text": "If A=1, B=2, C=3, and so on through the alphabet, which letter corresponds to the number 20?",
        "explanation": "Counting through the alphabet, the 20th letter is T.",
        "choices": [("S", False), ("T", True), ("U", False), ("V", False)],
    },
    {
        "text": (
            "A 3x3 grid contains these numbers:\n"
            "1    2    4\n8    16   32\n64   128  ?\n"
            "Each number doubles the one before it, reading left to right, top to bottom. "
            "What number completes the grid?"
        ),
        "explanation": "Following the doubling pattern, 128 x 2 = 256.",
        "choices": [("192", False), ("224", False), ("256", True), ("288", False)],
    },
    {
        "text": (
            "A clock's hour hand points to 12. It rotates 90 degrees clockwise, then "
            "another 90 degrees clockwise. Where does it now point?"
        ),
        "explanation": (
            "Each 90-degree clockwise turn moves the hand a quarter of the way around the "
            "clock face; two turns (180 degrees total) moves it from 12 to 6."
        ),
        "choices": [("3", False), ("6", True), ("9", False), ("12", False)],
    },
    {
        "text": "Which of these words reads the same forwards and backwards (a palindrome)?",
        "explanation": "LEVEL reads the same forwards and backwards.",
        "choices": [("LEVEL", True), ("HOUSE", False), ("WATER", False), ("LIGHT", False)],
    },
    {
        "text": (
            "A grid follows a checkerboard pattern:\n"
            "Row 1: X  O  X\nRow 2: O  X  O\nRow 3: X  O  ?\n"
            "What completes Row 3?"
        ),
        "explanation": "The pattern alternates like a checkerboard, so Row 3 continues X, O, X.",
        "choices": [("X", True), ("O", False), ("Both", False), ("Neither", False)],
    },
    {
        "text": (
            "A 2x2 grid is numbered clockwise starting from the top-left: 1 (top-left), "
            "2 (top-right), 3 (bottom-right), 4 (bottom-left). If the whole grid is rotated "
            "90 degrees clockwise, which number is now in the top-left position?"
        ),
        "explanation": (
            "Rotating the grid 90 degrees clockwise moves the bottom-left number (4) into "
            "the top-left position."
        ),
        "choices": [("1", False), ("2", False), ("3", False), ("4", True)],
    },
    {
        "text": (
            "Facing North, you turn 90 degrees clockwise, then another 90 degrees "
            "clockwise, then 90 degrees counter-clockwise. Which direction do you now face?"
        ),
        "explanation": (
            "North -> 90 CW -> East -> 90 CW -> South -> 90 CCW -> East. You end up facing "
            "East."
        ),
        "choices": [("North", False), ("South", False), ("East", True), ("West", False)],
    },
    {
        "text": "Complete the sequence: Triangle (3 sides), Square (4 sides), Pentagon (5 sides), Hexagon (6 sides), ___?",
        "explanation": "Each shape has one more side than the last; a hexagon (6 sides) is followed by a heptagon (7 sides).",
        "choices": [("Circle", False), ("Heptagon", True), ("Octagon", False), ("Nonagon", False)],
    },
]
