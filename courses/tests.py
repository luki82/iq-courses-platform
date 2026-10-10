from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from courses.lesson_format import parse_lesson
from courses.models import Course, Enrollment, Lesson

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

    def test_unstructured_text_still_displays(self):
        blocks = parse_lesson("Just some notes.\nAnother line.")
        self.assertEqual(blocks, [{"type": "para", "items": ["Just some notes.", "Another line."]}])

    def test_every_seeded_english_lesson_parses(self):
        for command in ("seed_english_esl", "seed_workplace_english", "seed_school_english"):
            call_command(command, stdout=open("/dev/null", "w"))
        exercises = 0
        for lesson in Lesson.objects.all():
            blocks = parse_lesson(lesson.content, seed=lesson.slug)
            self.assertTrue(blocks, lesson.slug)
            exercises += types(blocks).count("exercise")
        self.assertGreaterEqual(exercises, 6)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class LessonPageTests(TestCase):
    def test_lesson_page_has_voice_bar_and_exercise(self):
        call_command("seed_english_esl", stdout=open("/dev/null", "w"))
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
