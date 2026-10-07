"""
Seed the "English for School Students" course.

Run with:  python manage.py seed_school_english

Safe to run more than once (updates instead of duplicating).
Module 1 is a free preview; the other modules require Premium.
"""
from django.core.management.base import BaseCommand

from courses.seeding import seed_course

COURSE = {
    "slug": "english-for-school-students",
    "title": "English for School Students",
    "description": (
        "Build the English skills you need for high school (about Years 7-10): "
        "clear sentences and punctuation, reading between the lines, persuasive "
        "and narrative writing, and analytical essays. Great for students "
        "learning English as an additional language. Module 1 is free."
    ),
}

MODULES = [
    (
        "Module 1: Sentence Power",
        True,
        [
            (
                "complete-sentences",
                "Writing Complete Sentences",
                """
                GOAL: Avoid the two most common sentence mistakes -- fragments and run-ons.

                A COMPLETE SENTENCE needs a subject (who/what) and a verb (action/state),
                and it must make sense on its own.
                - The bus arrived late. (subject: The bus, verb: arrived)

                MISTAKE 1: THE FRAGMENT (an incomplete sentence)
                - "Because I missed the bus." -- Because what? It doesn't finish the idea.
                - Fix: "I was late because I missed the bus."

                MISTAKE 2: THE RUN-ON (two sentences joined with nothing or just a comma)
                - "I love basketball, I play every Saturday."
                Three fixes:
                1. Full stop: "I love basketball. I play every Saturday."
                2. Joining word: "I love basketball, so I play every Saturday."
                3. Semicolon: "I love basketball; I play every Saturday."

                JOINING WORDS (conjunctions) -- remember FANBOYS:
                for, and, nor, but, or, yet, so

                PRACTICE
                Write F (fragment), R (run-on) or C (correct):
                1. Running to the canteen before the bell.
                2. The test was hard, I studied all week.
                3. Although it rained, we still played.
                4. My sister likes maths she wants to be an engineer.

                ANSWERS: 1. F  2. R  3. C  4. R
                Fix for 4: "My sister likes maths, and she wants to be an engineer."
                """,
            ),
            (
                "punctuation-essentials",
                "Punctuation Essentials: Commas and Apostrophes",
                """
                GOAL: Use commas and apostrophes correctly.

                COMMAS
                1. In lists: "I need a pen, a ruler, a calculator and a USB."
                2. After an opening word or phrase: "However, the results were different."
                   "After lunch, we went to the library."
                3. Before a joining word that links two full sentences:
                   "It was cold, but we went swimming anyway."

                APOSTROPHES -- only two jobs
                1. Missing letters (contractions): do not -> don't, it is -> it's, they are -> they're
                2. Ownership (possession):
                   - one owner: the dog's bowl, Sam's phone
                   - plural owner ending in s: the students' books, the teachers' lounge

                APOSTROPHES ARE NEVER FOR PLURALS
                - Wrong: "Apple's for sale"  - Right: "Apples for sale"

                IT'S vs ITS
                - it's = it is / it has: "It's raining."
                - its = belongs to it: "The school changed its uniform."
                Test: can you say "it is"? If yes, use it's.

                PRACTICE
                Correct the sentences:
                1. The cat licked it's paw.
                2. Both team's coaches were angry.
                3. We bought chips drinks and lollies.

                ANSWERS
                1. its paw  2. Both teams' coaches  3. chips, drinks and lollies
                """,
            ),
            (
                "keeping-tense-consistent",
                "Keeping Your Tense Consistent",
                """
                GOAL: Stay in the same tense when you write, unless the time really changes.

                Stories are usually written in the PAST tense.
                Essays about texts are usually written in the PRESENT tense.

                INCONSISTENT: "Maya walked into the room. She sees a strange box and picks it up."
                CONSISTENT: "Maya walked into the room. She saw a strange box and picked it up."

                WHY PRESENT TENSE FOR ESSAYS?
                The events in a book are always "happening" when someone reads them.
                - "In the novel, the main character learns that ..." (not "learned")

                COMMON IRREGULAR PAST VERBS
                go-went, see-saw, take-took, run-ran, think-thought, bring-brought,
                catch-caught, begin-began, write-wrote, find-found

                PRACTICE
                Rewrite in the past tense:
                "Leo runs to the station. He thinks he is late, but the train is not there yet."

                ANSWER
                "Leo ran to the station. He thought he was late, but the train was not there yet."
                """,
            ),
        ],
    ),
    (
        "Module 2: Reading Between the Lines",
        False,
        [
            (
                "main-idea-skimming-scanning",
                "Main Ideas, Skimming and Scanning",
                """
                GOAL: Find the main idea of a text quickly and locate details.

                SKIMMING = reading fast for the general idea.
                Read the title, the first and last paragraphs, and the first sentence of each paragraph.

                SCANNING = searching for one specific detail (a name, date, number).
                Move your eyes quickly and look only for the key word.

                FINDING THE MAIN IDEA
                Ask: "What is the writer mostly saying about the topic?"
                The main idea is often in the first sentence (the topic sentence) of a paragraph.

                SAMPLE PARAGRAPH
                "Kangaroos are well suited to Australia's dry climate. They can survive for long
                periods without drinking, getting much of their water from the plants they eat.
                In very hot weather, they lick their forearms so that evaporation cools their blood."

                Main idea: Kangaroos are adapted to dry conditions.
                Supporting details: little drinking; water from plants; licking forearms to cool down.

                PRACTICE
                1. Scan: how do kangaroos cool their blood?
                2. Which sentence is the topic sentence?

                ANSWERS
                1. By licking their forearms (evaporation cools them).  2. The first sentence.
                """,
            ),
            (
                "making-inferences",
                "Making Inferences",
                """
                GOAL: Work out what the writer suggests but doesn't say directly.

                INFERENCE = clues in the text + what you already know = a reasonable conclusion.

                EXAMPLE
                "Jacob stared at the floor. His report card was still in his bag, unopened,
                and he hadn't touched his dinner."
                The text doesn't say Jacob is worried, but the clues (staring at the floor,
                hiding the report card, not eating) suggest he is nervous about his results.

                HOW TO WRITE AN INFERENCE ANSWER
                "The writer suggests that ... because ..." + a quote or detail as evidence.
                "The writer suggests Jacob is anxious about his results because he leaves his
                report card 'unopened' and hasn't eaten."

                DON'T GO TOO FAR
                An inference must be supported by the text. "Jacob failed every subject" goes
                too far -- we don't know that.

                PRACTICE
                "Mrs Hill looked at the clock for the third time, tapping her pen. The empty seat
                in the front row stayed empty."
                What can you infer? Give evidence.

                SAMPLE ANSWER: Mrs Hill is impatient or worried because a student is late or
                absent -- she keeps checking the clock and tapping her pen, and a seat is empty.
                """,
            ),
            (
                "language-techniques",
                "Spotting Language Techniques",
                """
                GOAL: Identify language techniques and explain their effect.

                TECHNIQUES
                - Simile: compares using "like" or "as" -- "as cold as ice"
                - Metaphor: says something IS something else -- "The classroom was a zoo."
                - Personification: gives human qualities to objects -- "The wind howled."
                - Alliteration: repeated first sounds -- "slippery, slimy snake"
                - Hyperbole: deliberate exaggeration -- "I've told you a million times."
                - Rhetorical question: asked for effect, not an answer -- "Isn't our planet worth saving?"
                - Onomatopoeia: words that sound like the noise -- "crash", "sizzle"

                THE KEY SKILL: NAME IT + EXPLAIN THE EFFECT
                Just naming a technique earns few marks. Explain what it makes the reader see or feel.
                - Weak: "This is personification."
                - Strong: "The personification in 'the wind howled' makes the storm sound like a wild
                  animal, creating a frightening mood."

                PRACTICE
                Name the technique and explain the effect:
                1. "The stars were diamonds scattered across the sky."
                2. "Do we really want our children breathing this air?"

                SAMPLE ANSWERS
                1. Metaphor -- comparing stars to diamonds makes the night sky seem precious and beautiful.
                2. Rhetorical question -- it makes the reader feel responsible and agree that action is needed.
                """,
            ),
        ],
    ),
    (
        "Module 3: Persuasive Writing",
        False,
        [
            (
                "persuasive-structure",
                "Structuring a Persuasive Text",
                """
                GOAL: Plan and structure a persuasive text.

                STRUCTURE
                1. Introduction: hook + your position (contention) + preview of your reasons
                2. Body paragraphs (usually 3): one reason each, using PEEL
                3. Conclusion: restate your position + strong final sentence (call to action)

                PEEL PARAGRAPHS
                P - Point: your reason in one sentence
                E - Evidence: facts, examples, expert opinion
                E - Explain: how the evidence supports your point
                L - Link: back to your main argument

                EXAMPLE BODY PARAGRAPH (topic: schools should have a later start time)
                (P) Firstly, a later start would improve students' health. (E) Sleep researchers
                report that many teenagers' body clocks shift later during adolescence, making
                early nights difficult. (E) This means that a 7 am alarm can leave students
                short of sleep, which affects their mood and concentration. (L) Clearly, starting
                school later is a simple way to support student wellbeing.

                PLANNING (spend 5 minutes on this!)
                Position: ______
                Reason 1: ______   Evidence: ______
                Reason 2: ______   Evidence: ______
                Reason 3: ______   Evidence: ______

                PRACTICE
                Plan a persuasive text on: "Mobile phones should be banned at school."
                Choose your position and fill in the planning table.
                """,
            ),
            (
                "persuasive-devices",
                "Persuasive Devices",
                """
                GOAL: Use persuasive language to convince your reader.

                DEVICES (and an example of each)
                - Inclusive language: "We all want a cleaner town."
                - Emotive language: "Innocent animals are suffering needlessly."
                - Rhetorical question: "How many more warnings do we need?"
                - Statistics: "Nearly half of students say ..." (only use real figures!)
                - Rule of three: "It is cheap, simple and effective."
                - Expert opinion: "Doctors agree that ..."
                - Modal verbs (strength of position): must, should, need to, will

                HIGH vs LOW MODALITY
                - Low: "Maybe we could think about recycling."
                - High: "We must start recycling now."
                Persuasive writing usually uses HIGH modality.

                REBUTTAL: answer the other side
                "Some people argue that uniforms are expensive. However, uniforms actually save
                families money, because students don't need many different outfits."

                PRACTICE
                Improve this weak sentence using at least two devices:
                "Littering is bad and people should stop."

                SAMPLE ANSWER: "Every day, our beaches are choked with plastic that kills turtles and
                seabirds. Isn't it time we all took responsibility and stopped littering for good?"
                """,
            ),
            (
                "persuasive-model-piece",
                "Model Persuasive Text and Checklist",
                """
                GOAL: Study a full model and check your own writing.

                MODEL: "Every school should have a vegetable garden"

                Imagine a lunchtime where students pick the tomatoes for their own salad. A school
                vegetable garden is not a luxury -- it is one of the best investments a school can
                make, because it improves health, teaches real science and builds community.

                Firstly, gardens encourage healthy eating. Students who grow vegetables are often
                keener to taste them. When a Year 7 student has spent weeks watering a carrot,
                they are far more likely to eat it than to throw it in the bin.

                Secondly, a garden is a living science lab. Students can measure plant growth,
                test soil and observe insects -- learning that sticks because they can see and touch it.

                Some argue that gardens cost too much. However, a few raised beds and seedlings cost
                very little, and many local hardware stores and community groups support school
                gardens.

                Finally, gardens bring people together. Parents, grandparents and students can work
                side by side on weekends.

                Healthier students, better science and a stronger community: surely that is worth a
                few seedlings. Let's dig in.

                CHECKLIST FOR YOUR WRITING
                [ ] Clear position in the introduction
                [ ] Each body paragraph has one main reason (PEEL)
                [ ] At least one rebuttal
                [ ] Three or more persuasive devices
                [ ] Strong ending with a call to action
                [ ] Checked spelling, punctuation and paragraphs

                PRACTICE
                Write your own persuasive text (about 400 words) using your plan from the
                "Structuring a Persuasive Text" lesson.
                """,
            ),
        ],
    ),
    (
        "Module 4: Narrative Writing",
        False,
        [
            (
                "show-dont-tell",
                "Show, Don't Tell",
                """
                GOAL: Make your writing vivid by showing emotions and settings through details.

                TELLING: "Ella was scared."
                SHOWING: "Ella's hands shook as she reached for the door handle. Her heart thudded
                so loudly she was sure the whole house could hear it."

                HOW TO SHOW
                - Actions and body language (shaking hands, a forced smile)
                - The five senses (what she hears, smells, feels)
                - Dialogue ("Is... is anyone there?")
                - Thoughts

                SETTINGS: use specific details
                - Telling: "It was a hot day in town."
                - Showing: "Heat shimmered above the road, and the red dust clung to everything --
                  the parked utes, the shop windows, the back of my neck."

                PRACTICE
                Rewrite each sentence to SHOW instead of TELL:
                1. Max was angry.
                2. The classroom was messy.
                3. It was a cold morning.
                """,
            ),
            (
                "story-structure-and-openings",
                "Story Structure and Strong Openings",
                """
                GOAL: Plan a story with a clear structure and a hook at the start.

                STRUCTURE
                1. Orientation -- who, where, when (keep it short!)
                2. Complication -- the problem
                3. Rising action -- things get harder
                4. Climax -- the most intense moment
                5. Resolution -- how it ends (it doesn't need to be happy, but it should feel finished)

                TIP: In a short story, use ONE main character, ONE problem and a small number of settings.

                STRONG OPENING TYPES
                - Action: "I was halfway up the water tower when the ladder groaned."
                - Dialogue: "'Don't open that,' Gran whispered."
                - Mystery: "The letter had my name on it, but it was dated fifty years ago."
                - Setting: "Nothing moved on the salt lake except the heat."

                AVOID
                - "One day ..." / "Hi, my name is ..." / waking up to an alarm
                - Ending with "... and then I woke up. It was all a dream."

                PRACTICE
                Write three different opening sentences for a story called "The Last Bus".
                """,
            ),
            (
                "writing-dialogue",
                "Writing and Punctuating Dialogue",
                """
                GOAL: Punctuate dialogue correctly and use it to show character.

                THE RULES
                1. Put spoken words inside quotation marks: "I'm hungry," said Ali.
                2. Punctuation goes INSIDE the quotation marks.
                3. Use a comma (not a full stop) before the speaker tag: "Let's go," she said.
                4. Start a new line each time a new person speaks.
                5. Questions and exclamations keep their mark: "Where are you going?" asked Mum.

                EXAMPLE
                "Did you finish the project?" asked Mr Chen.
                Noah stared at his shoes. "Nearly."
                "Nearly?"
                "I'll have it tomorrow. I promise."

                SAID IS NOT DEAD -- but use variety when it adds meaning:
                whispered, muttered, snapped, called, admitted, shouted

                DIALOGUE SHOULD DO A JOB
                Use it to show character or move the story forward -- not for long chats about nothing.

                PRACTICE
                Punctuate correctly:
                1. where is my phone asked Leah
                2. it's on the table said Tom
                3. thanks she said grabbing it

                ANSWERS
                1. "Where is my phone?" asked Leah.
                2. "It's on the table," said Tom.
                3. "Thanks," she said, grabbing it.
                """,
            ),
        ],
    ),
    (
        "Module 5: Essays and Exams",
        False,
        [
            (
                "analytical-paragraphs-teel",
                "Analytical Paragraphs with TEEL",
                """
                GOAL: Write a strong analytical paragraph about a text.

                TEEL
                T - Topic sentence: your point about the text
                E - Evidence: a short quote or specific example
                E - Explanation: how the evidence proves your point (this is the most important part)
                L - Link: connect back to the essay question

                EXAMPLE (question: How does the author show that friendship changes the main character?)
                (T) At the start of the novel, Sam is lonely and closed off. (E) He describes
                himself as "a ghost in the corridors". (E) This metaphor suggests Sam feels
                invisible and disconnected from others, as though he doesn't really exist at school.
                (L) This early loneliness makes the change caused by his friendship with Ari more
                powerful later in the text.

                QUOTING TIPS
                - Keep quotes short and embed them in your sentence.
                - Never leave a quote on its own -- always explain it.

                PHRASES FOR EXPLAINING
                This suggests ... / This shows ... / The word "..." implies ... /
                This makes the reader feel ...

                PRACTICE
                Choose a book or film you know. Write one TEEL paragraph about a main character.
                """,
            ),
            (
                "essay-structure",
                "Structuring a Text Response Essay",
                """
                GOAL: Organise a whole essay that answers the question.

                STEP 1: UNPACK THE QUESTION
                Underline the key words. "How does the author use setting to create tension?"
                -> key words: author, setting, tension.

                STEP 2: WRITE A CONTENTION (your answer in one sentence)
                "The author uses the isolated outback setting, the harsh weather and the
                abandoned house to steadily build tension."

                STEP 3: STRUCTURE
                Introduction
                - Text title and author
                - Contention
                - Three main points (in order)
                Body paragraph 1, 2, 3 -- TEEL, one point each
                Conclusion
                - Restate the contention in new words
                - Summarise the main points
                - Final thought about the text's message

                LINKING WORDS
                Firstly, Furthermore, In addition, Similarly, In contrast, Finally, Ultimately

                PRACTICE
                Unpack this question and write a contention:
                "How does the writer show the importance of family?" (use any text you know)
                """,
            ),
            (
                "writing-tests-and-time",
                "Writing Tests and Managing Your Time",
                """
                GOAL: Plan your time and check your work in writing tests and exams.

                A SIMPLE TIME PLAN (for a 40-minute writing task)
                - 5 minutes: read the prompt carefully and plan
                - 30 minutes: write
                - 5 minutes: check and fix

                READ THE PROMPT CAREFULLY
                - What type of writing is it -- persuasive, narrative, or analytical?
                - Who is the audience?
                - Are there any images or ideas you must use?

                WHAT MARKERS USUALLY LOOK FOR
                - Ideas that are relevant and developed
                - Clear structure and paragraphs
                - Varied, precise vocabulary
                - Correct sentences, punctuation and spelling

                LAST-5-MINUTE CHECK
                [ ] Does each paragraph have one main idea?
                [ ] Capital letters and full stops on every sentence?
                [ ] Any run-on sentences?
                [ ] Did I answer the actual question?

                IF YOU RUN OUT OF TIME
                Write a short, clear conclusion -- an ending matters more than one extra body paragraph.

                PRACTICE
                Set a 40-minute timer and write a persuasive text on: "Homework should be optional."
                Use the time plan above.

                Congratulations -- you have finished English for School Students!
                """,
            ),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the 'English for School Students' course (module 1 free, the rest Premium)."

    def handle(self, *args, **options):
        course, created, lessons = seed_course(COURSE, MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} '{course.title}': {len(MODULES)} modules, {lessons} lessons."
            )
        )
