"""
Seed the "English for Beginners (ESL Adults)" course.

Place this file at:  courses/management/commands/seed_english_esl.py
Run it with:         python manage.py seed_english_esl

Safe to run more than once: it updates existing rows instead of duplicating them.
The whole course is free (every module is a free preview).
"""
from textwrap import dedent

from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Course, Lesson, Module

COURSE = {
    "slug": "english-for-beginners",
    "title": "English for Beginners (ESL Adults)",
    "description": (
        "A free, friendly English course for adults starting from the basics. "
        "Learn to introduce yourself, handle everyday situations, get around town "
        "and talk about work. Short lessons, real-life dialogues and practice "
        "with answers."
    ),
}

# Each module: (title, [lessons]); each lesson: (slug, title, content)
MODULES = [
    (
        "Module 1: Hello! First Words",
        [
            (
                "greetings-and-introductions",
                "Greetings and Introductions",
                """
                GOAL: Say hello, give your name and ask someone's name.

                KEY WORDS
                - Hello / Hi
                - Good morning / Good afternoon / Good evening
                - My name is ...
                - Nice to meet you.
                - Goodbye / Bye / See you later.

                DIALOGUE
                Anna: Hi! My name is Anna. What's your name?
                Omar: Hello, Anna. My name is Omar.
                Anna: Nice to meet you, Omar.
                Omar: Nice to meet you too.

                GRAMMAR TIP: the verb "to be"
                - I am (I'm) Omar.
                - You are (You're) Anna.
                - He is (He's) / She is (She's) my friend.

                PRACTICE
                Complete the sentences.
                1. Hello, my name ___ Lina.
                2. ___ to meet you.
                3. I ___ from Vietnam.

                ANSWERS: 1. is  2. Nice  3. am
                """,
            ),
            (
                "the-alphabet-and-spelling",
                "The Alphabet and Spelling Your Name",
                """
                GOAL: Say the alphabet and spell your name clearly.

                THE ALPHABET
                A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

                Letters people often mix up:
                - A (ay) and E (ee) and I (eye)
                - G (jee) and J (jay)
                - B and V, P and B
                - W is "double-you"
                - Z is "zed" in Australia

                DIALOGUE
                Receptionist: What's your family name, please?
                Mei: Chen.
                Receptionist: How do you spell that?
                Mei: C - H - E - N.
                Receptionist: Thank you.

                USEFUL PHRASES
                - How do you spell that?
                - Can you repeat that, please?
                - Is that "B" for "Bob"?

                PRACTICE
                Spell these words out loud: CAT, JOB, VISA, ZERO.
                Now spell your first name and family name three times.
                """,
            ),
            (
                "numbers-and-phone-numbers",
                "Numbers and Phone Numbers",
                """
                GOAL: Count to 100 and say phone numbers.

                NUMBERS
                1 one, 2 two, 3 three, 4 four, 5 five, 6 six, 7 seven, 8 eight,
                9 nine, 10 ten, 11 eleven, 12 twelve, 13 thirteen, 20 twenty,
                30 thirty, 40 forty, 50 fifty, 100 one hundred.

                Be careful:
                - 13 (thir-TEEN) and 30 (THIR-ty)
                - 14 (four-TEEN) and 40 (FOR-ty)

                PHONE NUMBERS
                We say each number one by one. "0" is "oh" or "zero".
                0412 345 678 = "oh-four-one-two, three-four-five, six-seven-eight"
                "Double" = the same number twice: 55 = "double five".

                DIALOGUE
                Tom: What's your phone number?
                Priya: It's 0433 219 870.
                Tom: Sorry, can you say that again, slowly?

                PRACTICE
                Write these in words: 15, 50, 72, 99.
                ANSWERS: fifteen, fifty, seventy-two, ninety-nine
                """,
            ),
            (
                "survival-phrases",
                "Survival Phrases",
                """
                GOAL: Ask for help when you don't understand.

                KEY PHRASES
                - Sorry, I don't understand.
                - Can you speak more slowly, please?
                - What does "___" mean?
                - How do you say "___" in English?
                - Can you write it down, please?
                - Excuse me, where is the toilet?

                POLITE WORDS
                - Please, Thank you / Thanks, You're welcome
                - Excuse me (to get attention)
                - Sorry (when you make a mistake or didn't hear)

                DIALOGUE
                Worker: You need to fill in form B12.
                Sara: Sorry, can you speak more slowly, please?
                Worker: Of course. Form ... B ... 12.
                Sara: Can you write it down, please?
                Worker: Sure, here you go.
                Sara: Thank you!

                PRACTICE
                What do you say?
                1. You don't hear someone.  2. Someone gives you something.
                3. You want to know a word's meaning.
                ANSWERS: 1. Sorry? / Can you repeat that?  2. Thank you.
                3. What does "___" mean?
                """,
            ),
        ],
    ),
    (
        "Module 2: Everyday Life",
        [
            (
                "daily-routine",
                "My Daily Routine (Present Simple)",
                """
                GOAL: Talk about things you do every day.

                KEY VERBS
                wake up, get up, have breakfast, go to work, start work,
                finish work, cook dinner, watch TV, go to bed

                GRAMMAR: present simple
                - I / You / We / They work.
                - He / She / It works.  (add -s)
                - Negative: I don't work. She doesn't work.
                - Question: Do you work? Does he work?

                EXAMPLE
                "I wake up at 6 o'clock. I have breakfast and I go to work by bus.
                I finish work at 4. In the evening I cook dinner and I go to bed at 10."

                PRACTICE
                Correct the mistakes.
                1. She work in a shop.
                2. He don't like coffee.
                3. Do she drive?
                ANSWERS: 1. works  2. doesn't  3. Does she drive?

                YOUR TURN: Write 5 sentences about your day.
                """,
            ),
            (
                "time-days-and-dates",
                "Time, Days and Dates",
                """
                GOAL: Tell the time and talk about days and dates.

                TIME
                - 7:00 = seven o'clock
                - 7:15 = quarter past seven / seven fifteen
                - 7:30 = half past seven / seven thirty
                - 7:45 = quarter to eight / seven forty-five
                - am = morning, pm = afternoon/evening

                DAYS: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
                MONTHS: January ... December

                DATES
                In Australia we write day / month / year: 25/09/2026.
                We say: "the twenty-fifth of September".
                1st first, 2nd second, 3rd third, 4th fourth, 21st twenty-first.

                PREPOSITIONS
                - at 3 o'clock
                - on Monday, on 5 May
                - in May, in 2026, in the morning

                PRACTICE
                Fill in at / on / in:
                1. ___ Friday  2. ___ 9:30  3. ___ July  4. ___ the evening
                ANSWERS: 1. on  2. at  3. in  4. in
                """,
            ),
            (
                "family-and-people",
                "Family and People",
                """
                GOAL: Talk about your family and describe people.

                FAMILY WORDS
                mother (mum), father (dad), parents, brother, sister, son, daughter,
                husband, wife, partner, grandmother, grandfather, aunt, uncle, cousin

                HAVE GOT / HAVE
                - I have two brothers.  (or: I've got two brothers.)
                - She has a daughter.  (or: She's got a daughter.)

                DESCRIBING PEOPLE
                - He is tall / short.
                - She has long hair / short hair / brown eyes.
                - My dad is kind and funny.

                POSSESSIVES
                my, your, his, her, our, their
                "This is my sister. Her name is Hana."

                DIALOGUE
                Ali: Do you have any children?
                Rosa: Yes, I have a son. His name is Leo. He's eight.
                Ali: That's lovely.

                PRACTICE
                Complete: 1. This is ___ (he) wife.  2. They love ___ (they) dog.
                ANSWERS: 1. his  2. their
                """,
            ),
            (
                "food-and-shopping",
                "Food and Shopping",
                """
                GOAL: Buy things, ask prices and understand money.

                MONEY
                $1 = one dollar, 50c = fifty cents, $4.50 = four dollars fifty

                SHOPPING PHRASES
                - How much is this? / How much are these?
                - Can I have ..., please?
                - Do you have ...?
                - I'd like a kilo of apples, please.
                - Can I pay by card?

                COUNTABLE / UNCOUNTABLE
                - Countable: an apple, two apples -> How many?
                - Uncountable: rice, milk, bread -> How much?
                - some (positive), any (questions and negatives)

                DIALOGUE
                Shop assistant: Hi, can I help you?
                Khan: Yes, how much are the bananas?
                Shop assistant: They're $3.90 a kilo.
                Khan: I'd like one kilo, please. Can I pay by card?
                Shop assistant: Sure. Tap here.

                PRACTICE
                How much or How many?
                1. ___ eggs?  2. ___ milk?  3. ___ bottles?
                ANSWERS: 1. How many  2. How much  3. How many
                """,
            ),
        ],
    ),
    (
        "Module 3: Getting Around",
        [
            (
                "asking-for-directions",
                "Asking for and Giving Directions",
                """
                GOAL: Ask how to get somewhere and understand the answer.

                ASKING
                - Excuse me, where is the post office?
                - How do I get to the train station?
                - Is there a chemist near here?

                GIVING DIRECTIONS
                - Go straight ahead.
                - Turn left / Turn right.
                - It's on the corner.
                - It's next to / opposite / between the bank and the cafe.
                - It's about five minutes' walk.

                DIALOGUE
                Nadia: Excuse me, is there a chemist near here?
                Man: Yes. Go straight ahead, then turn left at the traffic lights.
                     It's opposite the supermarket.
                Nadia: Thank you so much!

                PRACTICE
                Match: 1. opposite  2. next to  3. between
                a) beside   b) in the middle of two things   c) on the other side
                ANSWERS: 1-c  2-a  3-b
                """,
            ),
            (
                "transport-and-tickets",
                "Transport and Tickets",
                """
                GOAL: Use buses, trains and taxis.

                KEY WORDS
                bus stop, train station, platform, timetable, ticket, fare,
                return / one-way, next stop, get on, get off

                USEFUL QUESTIONS
                - Does this bus go to the city?
                - What time is the next train to ...?
                - Which platform is it?
                - How much is the fare?
                - Can you tell me when to get off?

                DIALOGUE (on the bus)
                Leo: Hi, does this bus go to the hospital?
                Driver: Yes, it does. About 15 minutes.
                Leo: Great. Can you tell me when to get off?
                Driver: No worries, I'll let you know.

                NOTE: "No worries" is common Australian English. It means
                "That's OK" or "You're welcome".

                PRACTICE
                Put the words in order:
                1. next / What / is / the / time / bus / ?
                ANSWER: What time is the next bus?
                """,
            ),
            (
                "appointments-and-health",
                "Making Appointments at the Doctor",
                """
                GOAL: Book an appointment and explain a simple problem.

                BOOKING
                - I'd like to make an appointment, please.
                - Is there anything available today / tomorrow?
                - Can I see a doctor this afternoon?

                THE BODY
                head, eye, ear, throat, back, arm, hand, leg, foot, stomach

                SAYING WHAT'S WRONG
                - I have a headache / a sore throat / a cough / a fever.
                - My back hurts.
                - I feel sick.

                DIALOGUE
                Receptionist: Good morning, City Medical Centre.
                Amir: Hi, I'd like to make an appointment, please.
                Receptionist: What's the problem?
                Amir: I have a bad cough and a sore throat.
                Receptionist: We have 2:30 this afternoon. Is that OK?
                Amir: Yes, perfect. Thank you.

                IMPORTANT: In an emergency in Australia, call 000 (triple zero).

                PRACTICE
                Complete: 1. I have a sore ___.  2. My leg ___.
                ANSWERS: 1. throat (or back, etc.)  2. hurts
                """,
            ),
            (
                "last-weekend-past-simple",
                "Last Weekend (Past Simple)",
                """
                GOAL: Talk about what you did in the past.

                REGULAR VERBS: add -ed
                work -> worked, watch -> watched, visit -> visited, play -> played

                IRREGULAR VERBS (learn these!)
                go -> went, have -> had, see -> saw, eat -> ate, buy -> bought,
                make -> made, get -> got, do -> did

                NEGATIVES AND QUESTIONS use "did"
                - I didn't go out.  (NOT: I didn't went)
                - Did you have a good weekend?
                - What did you do?

                DIALOGUE
                Jin: Did you have a good weekend?
                Maria: Yes! I visited my cousin and we went to the beach.
                Jin: Nice. What did you do after that?
                Maria: We had fish and chips. What about you?
                Jin: I stayed home and watched a movie.

                PRACTICE
                Write the past form: 1. go  2. buy  3. watch  4. eat
                ANSWERS: 1. went  2. bought  3. watched  4. ate
                """,
            ),
        ],
    ),
    (
        "Module 4: Work and Community",
        [
            (
                "talking-about-jobs",
                "Talking About Jobs",
                """
                GOAL: Say what you do and ask about other people's jobs.

                JOBS
                driver, cleaner, cook, nurse, teacher, builder, mechanic,
                shop assistant, farmer, office worker, electrician

                QUESTIONS
                - What do you do?  (= What is your job?)
                - Where do you work?
                - Do you like your job?
                - How long have you worked there?

                ANSWERS
                - I'm a driver. I work for a bus company.
                - I work at a hospital.
                - I'm looking for work at the moment.

                A / AN
                a driver, a nurse -> "a" before a consonant sound
                an electrician, an engineer -> "an" before a vowel sound

                PRACTICE
                a or an? 1. ___ cook  2. ___ office worker  3. ___ mechanic
                ANSWERS: 1. a  2. an  3. a
                """,
            ),
            (
                "filling-in-forms",
                "Filling In Forms",
                """
                GOAL: Understand common words on forms.

                COMMON FORM WORDS
                - First name / Given name: your personal name
                - Family name / Surname / Last name
                - Date of birth (DOB): DD/MM/YYYY
                - Address, Suburb, State, Postcode
                - Mobile / Phone
                - Email
                - Occupation: your job
                - Signature: sign your name
                - Tick the box / Circle one / Please print (use CAPITAL letters)

                EXAMPLE
                First name: MARIA
                Family name: LOPEZ
                Date of birth: 14/03/1990
                Suburb: KALGOORLIE   State: WA   Postcode: 6430

                TIPS
                - Use a black or blue pen.
                - If a question is not for you, write N/A (not applicable).
                - Ask: "What does this part mean?" if you are not sure.

                PRACTICE
                What goes in each box? 1. Surname  2. Occupation  3. DOB
                ANSWERS: 1. family name  2. your job  3. your date of birth
                """,
            ),
            (
                "phone-calls",
                "Making Phone Calls",
                """
                GOAL: Start, manage and finish a simple phone call.

                STARTING
                - Hello, this is ___ speaking.
                - Hi, can I speak to ___, please?
                - I'm calling about ...

                IF YOU DON'T UNDERSTAND
                - Sorry, the line is bad. Can you repeat that?
                - Could you spell that, please?

                LEAVING A MESSAGE
                "Hi, this is Sam Nguyen. I'm calling about the job advertisement.
                My number is 0412 555 019. Please call me back. Thanks, bye."

                FINISHING
                - Thanks for your help.
                - Have a good day. Bye.

                DIALOGUE
                Office: Good morning, Green Cleaning.
                Sam: Hi, this is Sam. I'm calling about the cleaner job.
                Office: Great. Can I have your phone number?
                Sam: Sure, it's 0412 555 019.
                Office: Thanks, Sam. We'll call you tomorrow.

                PRACTICE: Write a message you could leave for a dentist to change
                your appointment.
                """,
            ),
            (
                "writing-short-messages",
                "Writing Short Emails and Messages",
                """
                GOAL: Write a short, polite email or text message.

                EMAIL STRUCTURE
                1. Greeting: Hi Sarah, / Dear Mr Brown,
                2. Reason: I'm writing to ...
                3. Details: short and clear
                4. Closing: Thank you. / Kind regards,
                5. Your name

                EXAMPLE EMAIL
                Hi Sarah,

                I'm writing to tell you that I am sick today and I can't come to work.
                I will see a doctor this morning. I hope to be back tomorrow.

                Kind regards,
                Omar

                TEXT MESSAGE EXAMPLE
                "Hi John, sorry I'm running 10 minutes late. See you soon. Omar"

                USEFUL PHRASES
                - I'm writing to ask about ...
                - Could you please ...?
                - Please let me know.
                - Thanks for your help.

                PRACTICE
                Write an email to your teacher. Say you can't come to class on
                Monday and ask for the homework.

                Congratulations! You have finished English for Beginners.
                """,
            ),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the free 'English for Beginners (ESL Adults)' course."

    @transaction.atomic
    def handle(self, *args, **options):
        course, created = Course.objects.update_or_create(
            slug=COURSE["slug"],
            defaults={
                "title": COURSE["title"],
                "description": COURSE["description"],
                "is_published": True,
            },
        )

        lesson_total = 0
        for m_order, (module_title, lessons) in enumerate(MODULES, start=1):
            module, _ = Module.objects.update_or_create(
                course=course,
                order=m_order,
                defaults={"title": module_title, "is_free_preview": True},
            )
            for l_order, (slug, title, content) in enumerate(lessons, start=1):
                Lesson.objects.update_or_create(
                    module=module,
                    slug=slug,
                    defaults={
                        "title": title,
                        "content": dedent(content).strip(),
                        "order": l_order,
                    },
                )
                lesson_total += 1

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} '{course.title}': {len(MODULES)} modules, {lesson_total} lessons (all free)."
            )
        )