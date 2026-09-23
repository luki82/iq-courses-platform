from django.core.management.base import BaseCommand

from iqtest.models import Category, Choice, Question


class Command(BaseCommand):
    help = "Creates a couple of sample IQ test categories with demo questions."

    def handle(self, *args, **options):
        logical, _ = Category.objects.get_or_create(
            slug="logical-reasoning",
            defaults={
                "name": "Logical Reasoning",
                "description": "Number and letter sequences, pattern spotting.",
                "is_premium": False,
            },
        )
        numerical, _ = Category.objects.get_or_create(
            slug="numerical-advanced",
            defaults={
                "name": "Advanced Numerical",
                "description": "Harder numerical reasoning -- Premium category.",
                "is_premium": True,
            },
        )

        if not logical.questions.exists():
            demo_questions = [
                {
                    "text": "What comes next in the sequence? 2, 4, 8, 16, ...",
                    "explanation": "Each number doubles the previous one, so 16 x 2 = 32.",
                    "choices": [("24", False), ("30", False), ("32", True), ("36", False)],
                },
                {
                    "text": "Which word does not belong: Apple, Banana, Carrot, Mango?",
                    "explanation": "Apple, Banana and Mango are fruits; Carrot is a vegetable.",
                    "choices": [("Apple", False), ("Banana", False), ("Carrot", True), ("Mango", False)],
                },
                {
                    "text": "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?",
                    "explanation": "This is a valid syllogism, so yes -- all Bloops are Lazzies.",
                    "choices": [("Yes", True), ("No", False), ("Cannot be determined", False)],
                },
                {
                    "text": "Complete the pattern: A, C, E, G, ...",
                    "explanation": "The pattern skips one letter each time: A(+2)C(+2)E(+2)G(+2)I.",
                    "choices": [("H", False), ("I", True), ("J", False), ("K", False)],
                },
                {
                    "text": "5 machines take 5 minutes to make 5 widgets. How long would 100 machines take to make 100 widgets?",
                    "explanation": "Each machine makes 1 widget in 5 minutes, regardless of how many machines run in parallel.",
                    "choices": [("5 minutes", True), ("20 minutes", False), ("100 minutes", False), ("500 minutes", False)],
                },
            ]
            for i, q in enumerate(demo_questions):
                question = Question.objects.create(
                    category=logical, text=q["text"], explanation=q["explanation"], order=i
                )
                for choice_text, is_correct in q["choices"]:
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

        if not numerical.questions.exists():
            question = Question.objects.create(
                category=numerical,
                text="A train travels 60 miles in 45 minutes. What is its speed in mph?",
                explanation="60 miles / 0.75 hours = 80 mph.",
                order=0,
            )
            for choice_text, is_correct in [("60 mph", False), ("75 mph", False), ("80 mph", True), ("90 mph", False)]:
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS("IQ test sample data seeded."))
