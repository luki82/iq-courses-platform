from io import StringIO
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from courses.lesson_format import parse_lesson
from courses.models import Course, Enrollment, Lesson
from ielts.models import IELTSLesson

GREETINGS = """
GOAL: Say hello, give your name and ask someone's name.

KEY WORDS
- Hello / Hi
- Nice to meet you.

DIALOGUE
Anna: Hi! My name is Anna. What's your name?
Omar: Hello, Anna. My name is Omar.

GRAMMAR TIP: the verb "to be"
- I am (I'm) Omar.

PRACTICE
Complete the sentences.
1. Hello, my name ___ Lina.
2. ___ to meet you.
3. I ___ from Vietnam.

ANSWERS: 1. is  2. Nice  3. am
"""


def types(blocks):
    return [b["type"] for b in blocks]


class ParseLessonTests(TestCase):
    def test_greetings_lesson(self):
        blocks = parse_lesson(GREETINGS, seed="greetings")
        self.assertEqual(
            types(blocks),
            ["goal", "heading", "list", "heading", "dialogue", "heading", "list", "heading", "exercise"],
        )
        self.assertEqual(blocks[0]["text"], "Say hello, give your name and ask someone's name.")
        self.assertEqual(blocks[4]["items"][1], {"speaker": "Omar", "text": "Hello, Anna. My name is Omar."})
        self.assertEqual(blocks[5], {"type": "heading", "title": "GRAMMAR TIP", "subtitle": 'the verb "to be"'})

        exercise = blocks[-1]
        self.assertEqual(exercise["instruction"], "Complete the sentences.")
        self.assertEqual(
            [(i["before"], i["answer"], i["after"]) for i in exercise["items"]],
            [("Hello, my name", "is", "Lina."), ("", "Nice", "to meet you."), ("I", "am", "from Vietnam.")],
        )
        self.assertEqual(sorted(exercise["bank"]), ["Nice", "am", "is"])
        self.assertNotEqual(exercise["bank"], ["is", "Nice", "am"])  # not in answer order

    def test_bank_order_is_stable_per_lesson(self):
        self.assertEqual(
            parse_lesson(GREETINGS, seed="a")[-1]["bank"], parse_lesson(GREETINGS, seed="a")[-1]["bank"]
        )

    def test_items_on_one_line_and_notes_in_answers(self):
        text = "PRACTICE\nComplete: 1. I have a sore ___.  2. My leg ___.\nANSWERS: 1. throat (or back, etc.)  2. hurts"
        exercise = parse_lesson(text)[-1]
        self.assertEqual(exercise["type"], "exercise")
        self.assertEqual([i["answer"] for i in exercise["items"]], ["throat", "hurts"])

    def test_non_gap_practice_hides_answers_behind_a_button(self):
        text = "PRACTICE\nMatch: 1. opposite  2. next to\na) beside  b) on the other side\nANSWERS: 1-b  2-a"
        blocks = parse_lesson(text)
        self.assertNotIn("exercise", types(blocks))
        self.assertEqual(blocks[-1]["type"], "answers")

    def test_answers_heading_outside_practice_is_shown(self):
        text = "QUESTIONS\n- What do you do?\n\nANSWERS\n- I'm a driver.\n\nA / AN\na driver, an engineer"
        blocks = parse_lesson(text)
        self.assertEqual(
            [b.get("title") for b in blocks if b["type"] == "heading"], ["QUESTIONS", "ANSWERS", "A / AN"]
        )
        self.assertNotIn("answers", types(blocks))

    def test_alphabet_line_is_not_a_heading(self):
        blocks = parse_lesson("THE ALPHABET\nA B C D E F G")
        self.assertEqual(types(blocks), ["heading", "para"])

    def test_wrapped_dialogue_line_joins_previous_turn(self):
        blocks = parse_lesson("DIALOGUE\nMan: Turn left at the lights.\nIt's opposite the shop.")
        self.assertEqual(blocks[-1]["items"][0]["text"], "Turn left at the lights. It's opposite the shop.")

    def test_quiz_section(self):
        text = (
            "QUIZ: Check Your Understanding\n"
            "Q: What is 10% of $50?\n- $10\n* $5\n- $0.50\n"
            "Explanation: Move the decimal point one place left.\n"
            "Q: Is 25% off the same as paying 75%?\n* Yes\n- No\n"
        )
        quiz = parse_lesson(text)[-1]
        self.assertEqual(quiz["type"], "quiz")
        self.assertEqual(quiz["title"], "Check Your Understanding")
        self.assertEqual(quiz["answers_json"], "[1, 0]")
        self.assertEqual(quiz["questions"][0]["options"], ["$10", "$5", "$0.50"])
        self.assertEqual(quiz["questions"][0]["explanation"], "Move the decimal point one place left.")
        self.assertEqual(quiz["questions"][1]["explanation"], "")

    def test_quiz_with_two_correct_answers_falls_back_to_text(self):
        text = "QUIZ\nQ: Pick one\n* A\n* B\n"
        self.assertNotIn("quiz", types(parse_lesson(text)))

    def test_diagram_section(self):
        text = "DIAGRAM: mosquito-life-cycle\nEggs, larva, pupa, adult.\n\nKEY WORDS\n- Larva"
        blocks = parse_lesson(text)
        self.assertEqual(blocks[0], {
            "type": "diagram",
            "name": "mosquito-life-cycle",
            "src": "img/lessons/mosquito-life-cycle.svg",
            "caption": "Eggs, larva, pupa, adult.",
        })
        self.assertEqual(blocks[1]["title"], "KEY WORDS")

    def test_diagram_with_bad_name_is_not_an_image(self):
        self.assertNotIn("diagram", types(parse_lesson("DIAGRAM: ../../secret\nhello")))

    def test_every_lesson_diagram_file_exists(self):
        from pathlib import Path
        from django.conf import settings
        for command in ("seed_english_esl", "seed_workplace_english", "seed_school_english",
                        "seed_practical_maths", "seed_science_health", "seed_economics", "seed_religion_culture"):
            call_command(command, stdout=StringIO())
        found = 0
        for lesson in Lesson.objects.all():
            for block in parse_lesson(lesson.content, seed=lesson.slug):
                if block["type"] == "diagram":
                    found += 1
                    self.assertTrue((Path(settings.BASE_DIR) / "static" / block["src"]).exists(), block["src"])
                    self.assertTrue(block["caption"], lesson.slug)
        self.assertGreaterEqual(found, 28)

    def test_unstructured_text_still_displays(self):
        blocks = parse_lesson("Just some notes.\nAnother line.")
        self.assertEqual(blocks, [{"type": "para", "items": ["Just some notes.", "Another line."]}])

    def test_every_seeded_english_lesson_parses(self):
        for command in ("seed_english_esl", "seed_workplace_english", "seed_school_english", "seed_practical_maths", "seed_science_health", "seed_economics", "seed_religion_culture"):
            call_command(command, stdout=StringIO())
        exercises = 0
        for lesson in Lesson.objects.all():
            blocks = parse_lesson(lesson.content, seed=lesson.slug)
            self.assertTrue(blocks, lesson.slug)
            exercises += types(blocks).count("exercise")
        self.assertGreaterEqual(exercises, 6)

    def test_every_practical_maths_lesson_has_practice_and_quiz(self):
        call_command("seed_practical_maths", stdout=StringIO())
        lessons = Lesson.objects.filter(module__course__slug="practical-maths")
        self.assertGreaterEqual(lessons.count(), 5)
        for lesson in lessons:
            blocks = parse_lesson(lesson.content, seed=lesson.slug)
            self.assertIn("exercise", types(blocks), lesson.slug)
            quiz = next(b for b in blocks if b["type"] == "quiz")
            self.assertGreaterEqual(quiz["total"], 3, lesson.slug)
            self.assertTrue(all(q["explanation"] for q in quiz["questions"]), lesson.slug)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class LessonPageTests(TestCase):
    def test_lesson_page_has_voice_bar_and_exercise(self):
        call_command("seed_english_esl", stdout=StringIO())
        user = get_user_model().objects.create_user("learner", "l@example.com", "pw-12345-x")
        course = Course.objects.get(slug="english-for-beginners")
        Enrollment.objects.create(user=user, course=course)
        lesson = Lesson.objects.get(slug="greetings-and-introductions")
        self.client.force_login(user)
        response = self.client.get(reverse("courses:lesson_detail", args=[course.slug, lesson.id]))
        self.assertContains(response, "data-voice-bar")
        self.assertContains(response, 'data-answer="is"')
        self.assertContains(response, 'class="word-chip" data-word="Nice"')
        self.assertContains(response, "js/lesson.js")
        self.assertNotContains(response, "ANSWERS: 1. is")

    def test_lessons_in_former_premium_modules_open_for_free(self):
        call_command("seed_workplace_english", stdout=StringIO())
        user = get_user_model().objects.create_user("worker", "w@example.com", "pw-12345-x")
        lesson = Lesson.objects.filter(module__is_free_preview=False).select_related("module__course").first()
        self.assertIsNotNone(lesson)
        course = lesson.module.course
        Enrollment.objects.create(user=user, course=course)
        self.client.force_login(user)

        detail = self.client.get(reverse("courses:course_detail", args=[course.slug]))
        self.assertNotContains(detail, "Premium")
        self.assertContains(detail, reverse("courses:lesson_detail", args=[course.slug, lesson.id]))

        page = self.client.get(reverse("courses:lesson_detail", args=[course.slug, lesson.id]))
        self.assertEqual(page.status_code, 200)

    def test_ielts_tier_3_lesson_is_free(self):
        lesson = IELTSLesson.objects.create(
            module_title="Advanced", tier="TIER_3", skill="WRITING_T2", title="Problem and solution essays",
            passage_or_prompt="Write about traffic.",
        )
        user = get_user_model().objects.create_user("ielts", "i@example.com", "pw-12345-x")
        self.client.force_login(user)
        self.assertNotContains(self.client.get(reverse("ielts:lesson_list")), "Premium")
        self.assertEqual(self.client.get(reverse("ielts:lesson_detail", args=[lesson.slug])).status_code, 200)

    def test_quiz_renders_on_lesson_page(self):
        call_command("seed_practical_maths", stdout=StringIO())
        lesson = Lesson.objects.get(slug="how-to-calculate-discounts")
        response = self.client.get(reverse("courses:lesson_detail", args=["practical-maths", lesson.id]))
        self.assertContains(response, "Check Your Understanding")
        self.assertContains(response, 'class="quiz-option"', count=18)
        self.assertContains(response, "answers: [2, 0, 1, 2, 0]")

    def test_conversion_lessons_render_with_quiz(self):
        call_command("seed_practical_maths", stdout=StringIO())
        for slug in ("cooking-measurement-conversions", "metric-imperial-conversions", "temperature-and-time-conversions"):
            lesson = Lesson.objects.get(slug=slug)
            response = self.client.get(reverse("courses:lesson_detail", args=["practical-maths", lesson.id]))
            self.assertContains(response, "Check Your Understanding")
            self.assertContains(response, 'data-exercise')

    def test_science_health_lessons_have_practice_and_quiz(self):
        call_command("seed_science_health", stdout=StringIO())
        lessons = Lesson.objects.filter(module__course__slug="science-and-health")
        self.assertGreaterEqual(lessons.count(), 4)
        for lesson in lessons:
            blocks = parse_lesson(lesson.content, seed=lesson.slug)
            self.assertIn("exercise", types(blocks), lesson.slug)
            quiz = next(b for b in blocks if b["type"] == "quiz")
            self.assertGreaterEqual(quiz["total"], 3, lesson.slug)
            self.assertTrue(all(q["explanation"] for q in quiz["questions"]), lesson.slug)
        lesson = lessons.get(slug="typhoid-prevention-safe-water-and-food")
        response = self.client.get(reverse("courses:lesson_detail", args=["science-and-health", lesson.id]))
        self.assertContains(response, "Check Your Understanding")

    def test_diagram_renders_with_read_aloud_caption(self):
        call_command("seed_science_health", stdout=StringIO())
        lesson = Lesson.objects.get(slug="mosquito-life-cycle")
        response = self.client.get(reverse("courses:lesson_detail", args=["science-and-health", lesson.id]))
        self.assertContains(response, "img/lessons/mosquito-life-cycle.svg")
        self.assertContains(response, '<figcaption class="say-row">')

    def test_economics_lessons_have_diagram_practice_and_quiz(self):
        call_command("seed_economics", stdout=StringIO())
        lessons = Lesson.objects.filter(module__course__slug="economics-and-money")
        self.assertEqual(lessons.count(), 5)
        for lesson in lessons:
            blocks = parse_lesson(lesson.content, seed=lesson.slug)
            kinds = types(blocks)
            self.assertIn("diagram", kinds, lesson.slug)
            self.assertIn("exercise", kinds, lesson.slug)
            quiz = next(b for b in blocks if b["type"] == "quiz")
            self.assertEqual(quiz["total"], 5, lesson.slug)
        lesson = lessons.get(slug="what-is-inflation")
        response = self.client.get(reverse("courses:lesson_detail", args=["economics-and-money", lesson.id]))
        self.assertContains(response, "img/lessons/inflation-basket.svg")
        self.assertContains(response, "Check Your Understanding")

    def test_religion_lessons_have_diagram_practice_and_quiz(self):
        call_command("seed_religion_culture", stdout=StringIO())
        lessons = Lesson.objects.filter(module__course__slug="religion-and-culture-in-africa")
        self.assertEqual(lessons.count(), 4)
        for lesson in lessons:
            blocks = parse_lesson(lesson.content, seed=lesson.slug)
            kinds = types(blocks)
            self.assertIn("diagram", kinds, lesson.slug)
            self.assertIn("exercise", kinds, lesson.slug)
            quiz = next(b for b in blocks if b["type"] == "quiz")
            self.assertEqual(quiz["total"], 5, lesson.slug)
        lesson = lessons.get(slug="were-christianity-and-islam-imposed-on-africa")
        response = self.client.get(reverse("courses:lesson_detail", args=["religion-and-culture-in-africa", lesson.id]))
        self.assertContains(response, "img/lessons/imposed-debate.svg")
        self.assertContains(response, "PART 1")
