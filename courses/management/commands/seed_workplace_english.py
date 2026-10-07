"""
Seed the "Workplace English" course.

Run with:  python manage.py seed_workplace_english

Safe to run more than once (updates instead of duplicating).
Module 1 is a free preview; the other modules require Premium.
"""
from django.core.management.base import BaseCommand

from courses.seeding import seed_course

COURSE = {
    "slug": "workplace-english",
    "title": "Workplace English",
    "description": (
        "Practical English for working in Australia. Understand instructions, "
        "write clear emails and messages, speak up about safety, take part in "
        "meetings and prepare for job interviews. For learners who can already "
        "hold a simple conversation. Module 1 is free."
    ),
}

MODULES = [
    (
        "Module 1: Starting at Work",
        True,
        [
            (
                "introducing-yourself-at-work",
                "Introducing Yourself at Work",
                """
                GOAL: Introduce yourself to new colleagues and explain your role.

                KEY PHRASES
                - Hi, I'm Daniel. I've just started in the warehouse.
                - I'm the new receptionist / driver / apprentice.
                - I'll be working with the night shift.
                - How long have you been here?
                - Who should I ask if I have a question?

                DIALOGUE
                Supervisor: Everyone, this is Maria. She starts in admin today.
                Maria: Hi everyone. I'm Maria. I'll be looking after bookings and invoices.
                Ken: Welcome, Maria. I'm Ken -- I run the workshop. Shout if you need anything.
                Maria: Thanks, Ken. Who do I talk to about my roster?
                Ken: That's Sue in the office. She does all the rosters.

                GRAMMAR TIP: talking about your job
                - Present simple for routines: "I work Monday to Friday." "I drive the airport run."
                - "I'll be + -ing" for plans in your new job: "I'll be working on reception."
                - Present perfect for time up to now: "I've worked in hospitality for five years."

                AUSTRALIAN WORKPLACE WORDS
                - roster = the timetable of who works when
                - shift = your block of working time (day shift, night shift)
                - smoko = a short break (informal)
                - induction = your first training session at a new job

                PRACTICE
                Write three sentences to introduce yourself at a new job: your name,
                your role, and something about your experience.

                Choose the correct form:
                1. I (have worked / am working) here since March.
                2. Next week I'll be (train / training) the new staff.
                3. I usually (start / starting) at 6 am.

                ANSWERS: 1. have worked ("since" + a starting point needs the present perfect)
                2. training  3. start
                """,
            ),
            (
                "understanding-instructions",
                "Understanding and Checking Instructions",
                """
                GOAL: Follow instructions and check you have understood them correctly.

                At work, it is always better to check than to guess. Australians often
                give instructions quickly and informally, so these phrases are important.

                ASKING TO REPEAT OR SLOW DOWN
                - Sorry, could you say that again?
                - Could you slow down a little, please?
                - Could you show me how to do that?

                CHECKING (repeat it back in your own words)
                - So, you want me to ... first, and then ...?
                - Just to check: the boxes go on the top shelf, not the bottom?
                - Do you mean today or tomorrow?

                DIALOGUE
                Manager: Can you restock aisle four, then do the cardboard before you knock off?
                Ahmed: Sorry, "knock off"?
                Manager: Finish work -- go home.
                Ahmed: Ah, OK. So I restock aisle four first, then flatten the cardboard, and then I can go?
                Manager: Spot on.

                IMPERATIVES: the grammar of instructions
                Instructions usually start with the verb:
                - Put on your gloves. / Don't lift that by yourself. / Make sure the door is locked.
                "Make sure" means: check that something is done.

                PRACTICE
                Your boss says: "Grab the keys off Tony, fuel up the van and have it out the front by eight."
                Write a sentence to check you understood.

                SAMPLE ANSWER: "So I get the keys from Tony, fill the van with fuel, and park it
                at the front by 8 o'clock?"
                """,
            ),
            (
                "small-talk-with-colleagues",
                "Small Talk with Colleagues",
                """
                GOAL: Have short, friendly conversations at break time.

                Small talk builds good relationships at work. Safe topics: the weekend,
                the weather, sport, food, holidays, the drive to work. Avoid at first:
                salary, religion, politics, someone's age or weight.

                STARTING A CONVERSATION
                - How was your weekend?
                - Hot one today, isn't it?
                - Did you watch the footy?
                - Got any plans for the long weekend?

                KEEPING IT GOING: answer + add + ask
                Don't just say "Good." Give a little more, then ask back.
                "Good, thanks. We went to the lake with the kids. How about you?"

                DIALOGUE
                Jess: Morning! How was your weekend?
                Tran: Pretty good, thanks. I finally finished painting the fence. You?
                Jess: Quiet one. Just caught up on sleep after nights.
                Tran: Fair enough. Are you back on days now?
                Jess: Yeah, for two weeks. Thank goodness.

                ENDING POLITELY
                - Anyway, I'd better get back to it.
                - Good chatting -- catch you later.

                PRACTICE
                Answer each question using "answer + add + ask":
                1. How was your weekend?
                2. Busy day?
                3. Got any holidays coming up?

                SAMPLE ANSWER for 1: "Really nice. My cousin visited from Perth. Did you do anything fun?"
                """,
            ),
        ],
    ),
    (
        "Module 2: Emails, Calls and Messages",
        False,
        [
            (
                "writing-professional-emails",
                "Writing Clear Professional Emails",
                """
                GOAL: Write short, clear, polite emails at work.

                STRUCTURE
                1. Subject line -- say what the email is about: "Leave request: 14-18 July"
                2. Greeting -- "Hi Sarah," (most workplaces) or "Dear Ms Lee," (very formal)
                3. Purpose in the first line -- "I'm writing to request leave from 14 to 18 July."
                4. Details -- one idea per short paragraph
                5. Action -- what do you need? "Could you please confirm by Friday?"
                6. Close -- "Thanks," / "Kind regards," + your name

                EXAMPLE
                Subject: Forklift licence renewal

                Hi Mark,

                I'm writing about my forklift licence, which expires on 30 August.

                Could the company book me into a renewal course before then? I'm available
                any weekday except Thursdays.

                Please let me know if you need a copy of my current licence.

                Thanks,
                Ravi

                POLITE REQUESTS (softer = more polite)
                - Send me the roster. (too direct)
                - Can you send me the roster? (OK)
                - Could you please send me the roster when you get a chance? (polite)

                COMMON MISTAKES
                - No subject line, or "Hi" as the subject
                - One long paragraph
                - Writing all in CAPITALS (it looks like shouting)

                PRACTICE
                Write an email to your supervisor asking to swap your Saturday shift with a
                colleague, Lin. Include a subject line and a clear request.
                """,
            ),
            (
                "phone-calls-and-voicemail",
                "Phone Calls and Voicemail",
                """
                GOAL: Answer the phone professionally, take a message and leave a voicemail.

                ANSWERING
                "Good morning, Goldfields Plumbing, this is Amy speaking. How can I help?"

                TAKING A MESSAGE
                - I'm sorry, he's not available at the moment. Can I take a message?
                - Could I have your name and number, please?
                - Could you spell that for me?
                - I'll make sure he gets the message.

                A GOOD PHONE MESSAGE HAS: who called, their number, what it's about, what they want.

                Message for: Steve    From: Carol (Ace Hire)    Number: 0412 555 019
                About: excavator return    Action: please call back before 3 pm

                LEAVING A VOICEMAIL (keep it under 30 seconds)
                "Hi Steve, it's Carol from Ace Hire. I'm calling about the excavator you hired.
                Can you give me a call back before 3 today on 0412 555 019? That's 0412 555 019. Thanks."
                Tip: say your number twice, slowly.

                CALLING IN SICK
                "Hi Sue, it's Daniel. I'm sorry, I'm not well and won't be able to come in today.
                I'll let you know about tomorrow by this afternoon."

                PRACTICE
                Write a voicemail for this situation: you are running 20 minutes late for a 9 am
                site meeting because of a flat tyre.
                """,
            ),
            (
                "team-chat-and-text-messages",
                "Team Chat and Text Messages",
                """
                GOAL: Write clear, short work messages in group chats and texts.

                Work chats are informal, but they still need to be clear. A good message
                answers: what, when, where, and what you need.

                UNCLEAR: "can someone do sat"
                CLEAR: "Hi team, can anyone swap my Saturday 7am-3pm shift? I can do your Sunday in return."

                USEFUL SHORT PHRASES
                - Heads up: the loading dock is closed till 10.
                - Running 10 mins late, sorry.
                - Thanks, all sorted.
                - Can you confirm?
                - On my way.

                COMMON ABBREVIATIONS AT WORK
                - ETA = estimated time of arrival ("ETA 5 mins")
                - ASAP = as soon as possible
                - FYI = for your information
                - OOO = out of office

                RULES OF THUMB
                - Don't send private or angry messages to a group chat.
                - Reply to questions directed at you, even with just "Got it, thanks."
                - Use full words for anything important (safety, pay, times).

                PRACTICE
                Rewrite these unclear messages:
                1. "truck broke"
                2. "need someone 2moro"

                SAMPLE ANSWERS
                1. "Heads up: truck 3 has a flat battery at the depot. Can someone bring the jump starter?"
                2. "Can anyone help me move stock tomorrow from 8 to 10 am? It's a two-person job."
                """,
            ),
        ],
    ),
    (
        "Module 3: Safety at Work",
        False,
        [
            (
                "safety-words-and-signs",
                "Safety Words and Signs",
                """
                GOAL: Understand key work health and safety (WHS) words and signs.

                In Australia, everyone at work has a legal duty to work safely and to report
                hazards. You must understand safety language -- if you don't, ask.

                KEY WORDS
                - hazard = something that could cause harm (a wet floor, a loose cable)
                - risk = how likely and how serious the harm could be
                - PPE = personal protective equipment (hi-vis, hard hat, gloves, safety glasses, steel caps)
                - near miss = something that almost caused an injury
                - exclusion zone = an area you must not enter
                - isolate / lock out = turn off power or machinery so it can't start

                SIGN COLOURS
                - Red = prohibition or danger: "No entry", "Do not operate"
                - Yellow = warning: "Caution: forklifts operating"
                - Blue = must do: "Hearing protection must be worn"
                - Green = safety information: "First aid", "Emergency exit"

                MODAL VERBS IN SAFETY RULES
                - must / have to = required: "You must wear a hard hat on site."
                - must not = not allowed: "You must not enter without a permit."
                - should = strongly advised: "You should take regular breaks in the heat."

                PRACTICE
                Match the sign to the colour:
                1. "Fire extinguisher"  2. "Danger: high voltage"  3. "Eye protection must be worn"
                4. "Caution: slippery floor"

                ANSWERS: 1. red (fire equipment signs are red)  2. red  3. blue  4. yellow
                """,
            ),
            (
                "reporting-a-hazard-or-incident",
                "Reporting a Hazard or Incident",
                """
                GOAL: Report a hazard or incident clearly, in speech and in writing.

                SPEAKING UP
                - I need to report a hazard.
                - There's oil on the floor near bay two -- someone could slip.
                - I'm not comfortable doing this. Can someone check it first?
                Saying "stop" when something is unsafe is your right.

                WRITING AN INCIDENT REPORT: answer the 5 Ws + H
                - Who was involved?   - What happened?   - When?   - Where?
                - Why (if known)?     - How was it handled?
                Write facts, not opinions. Use the past simple.

                EXAMPLE
                On Tuesday 3 June at about 2:15 pm, I was walking past bay two in the workshop.
                I slipped on a patch of oil near the hoist but did not fall. There was no warning
                sign. I put a cone over the oil and told the supervisor, Mark. He arranged for the
                area to be cleaned. No one was injured.

                FACT vs OPINION
                - Opinion: "Someone was lazy and left a mess."
                - Fact: "There was oil on the floor and no warning sign."

                PRACTICE
                Write a short report: this morning in the car park you saw a reversing truck nearly
                hit a pedestrian. The truck's reversing beeper was not working.
                """,
            ),
            (
                "pre-starts-and-toolbox-talks",
                "Pre-Start Meetings and Toolbox Talks",
                """
                GOAL: Understand and take part in short safety meetings before work.

                Many sites -- mines, construction, transport -- start each shift with a
                pre-start meeting or a toolbox talk. The supervisor explains the day's work
                and hazards, and workers can ask questions or raise concerns.

                WHAT YOU WILL HEAR
                - "Today we're working near the crusher, so hearing protection on at all times."
                - "Watch out for heavy vehicles on the haul road."
                - "Any issues from last shift?"
                - "Has everyone done their vehicle pre-start checks?"

                VEHICLE PRE-START CHECK WORDS
                tyres, lights, indicators, brakes, horn, mirrors, fluid levels, seatbelts, fire extinguisher, two-way radio

                TAKING PART
                - Raising an issue: "The lights on unit 12 were flickering last night."
                - Asking: "Is the east gate still closed today?"
                - Confirming: "Got it -- channel 2 for the radio."

                RADIO LANGUAGE
                - Copy / Received = I heard and understood.
                - Say again = repeat, please.
                - Over = I've finished talking, your turn.
                Keep radio calls short: who you're calling, who you are, the message.
                "Light vehicle 4 to control, entering the haul road at gate 2, over."

                PRACTICE
                At the pre-start, you want to report that the passenger-side mirror on your
                bus is cracked. Write what you would say.

                SAMPLE ANSWER: "Just a heads up -- the passenger-side mirror on bus 7 is cracked.
                Can we get it looked at before it goes out?"
                """,
            ),
        ],
    ),
    (
        "Module 4: Meetings and Problem Solving",
        False,
        [
            (
                "speaking-up-in-meetings",
                "Speaking Up in Meetings",
                """
                GOAL: Give your opinion, agree and disagree politely in meetings.

                GIVING AN OPINION
                - I think ... / In my view ...
                - From what I've seen on the floor, ...

                AGREEING
                - I agree. / Good point. / That makes sense.

                DISAGREEING POLITELY (soften first, then give a reason)
                - I see what you mean, but ...
                - That's true, although ...
                - I'm not sure that would work, because ...

                INTERRUPTING POLITELY
                - Sorry to interrupt, but ...
                - Can I just add something?

                ASKING FOR CLARIFICATION
                - What do you mean by ...?
                - Could you give an example?

                DIALOGUE
                Manager: I'm thinking of moving the stocktake to Friday afternoons.
                Lena: I see what you mean, but Friday afternoon is our busiest delivery time.
                Could we do Thursday instead?
                Manager: Good point. Let's try Thursday for a month.

                PRACTICE
                Your manager suggests that everyone starts at 5:30 am in summer to avoid the heat.
                Write one polite agreement and one polite disagreement with a reason.
                """,
            ),
            (
                "dealing-with-customers",
                "Dealing with Customers and Complaints",
                """
                GOAL: Stay calm and professional when a customer is unhappy.

                THE LAST METHOD
                L - Listen without interrupting.
                A - Apologise for the experience: "I'm sorry this happened."
                S - Solve, or say what you will do: "Let me check that for you."
                T - Thank them: "Thanks for letting us know."

                USEFUL PHRASES
                - I understand why you're frustrated.
                - Let me see what I can do.
                - I'll need to check with my manager, but I'll get back to you by 3 pm.
                - Is there anything else I can help with?

                AVOID
                - "That's not my job." -> "Let me find the right person for you."
                - "Calm down." -> "I can see this is really frustrating."
                - "I don't know." -> "I'm not sure, but I'll find out."

                DIALOGUE
                Customer: I booked a pick-up for 6 and nobody came!
                Staff: I'm really sorry about that. Can I get your booking name?
                Customer: Patel.
                Staff: Thanks, Mr Patel. I can see the booking. The next bus is leaving in 15 minutes --
                I'll put you on it and let the driver know. Thanks for your patience.

                PRACTICE
                A customer says: "My order is a week late and nobody has called me." Write a
                reply using the LAST method.
                """,
            ),
            (
                "explaining-a-problem-to-your-boss",
                "Explaining a Problem to Your Boss",
                """
                GOAL: Explain a problem clearly and suggest a solution.

                A clear problem report has four parts:
                1. What the problem is
                2. Why it matters (the effect)
                3. What you've already tried
                4. What you suggest or need

                EXAMPLE
                "Hi Mark, the label printer has stopped working (problem). We can't send any
                orders until it's fixed (effect). I've restarted it and changed the roll, but it
                still jams (tried). Could we borrow the one from the front office for today
                and call the repair company? (suggestion)"

                USEFUL LANGUAGE
                - There's a problem with ...
                - This means that ... / As a result, ...
                - I've already tried ...
                - Would it be OK if I ...? / Could we ...?

                CAUSE AND EFFECT WORDS
                because, so, as a result, which means

                PRACTICE
                Explain this problem to your supervisor using the four parts: two people called
                in sick, and you have 40 deliveries today with only one driver.
                """,
            ),
        ],
    ),
    (
        "Module 5: Getting the Job",
        False,
        [
            (
                "writing-your-resume",
                "Writing an Australian-Style Resume",
                """
                GOAL: Write a clear resume that Australian employers expect.

                AUSTRALIAN RESUME BASICS
                - 2-3 pages is normal.
                - No photo, age, date of birth or marital status.
                - Most recent job first.
                - Use action verbs: managed, operated, trained, improved, delivered.

                SECTIONS
                1. Name and contact details (phone, email, suburb)
                2. Career summary -- 2-3 lines about who you are and what you offer
                3. Licences and tickets (driver's licence, forklift, White Card, first aid)
                4. Work history -- job title, company, dates, 3-5 achievements
                5. Education and training
                6. Referees -- or "Available on request"

                WEAK vs STRONG BULLET POINTS
                - Weak: "Responsible for deliveries."
                - Strong: "Delivered 30+ orders a day across the metro area with a 99% on-time record."

                CAREER SUMMARY EXAMPLE
                "Reliable heavy-rigid driver with six years' experience in mining and passenger
                transport. Strong safety record, current HR licence and first aid certificate."

                PRACTICE
                Rewrite these as strong bullet points:
                1. "Did cleaning."
                2. "Helped new staff."

                SAMPLE ANSWERS
                1. "Cleaned and restocked 12 hotel rooms per shift to brand standards."
                2. "Trained five new team members on the till and safety procedures."
                """,
            ),
            (
                "job-interview-questions",
                "Answering Job Interview Questions",
                """
                GOAL: Answer common interview questions with confidence.

                THE STAR METHOD (for "Tell me about a time when ..." questions)
                S - Situation: where and when
                T - Task: what you needed to do
                A - Action: what YOU did (use "I", not "we")
                R - Result: what happened -- numbers help

                EXAMPLE: "Tell me about a time you dealt with a difficult customer."
                S: "At my last job in a hardware store, a customer was angry about a wrong delivery."
                T: "I needed to fix it quickly and keep him as a customer."
                A: "I listened, apologised, and arranged the right part by courier that afternoon."
                R: "He was happy and he came back the next week to order more."

                COMMON QUESTIONS
                - Tell me about yourself. (2 minutes: past, present, why this job)
                - Why do you want to work here?
                - What are your strengths?
                - What is one area you are working to improve?
                - Do you have any questions for us?

                GOOD QUESTIONS TO ASK
                - What does a typical day look like?
                - What training do new staff get?
                - What's the roster like?

                PRACTICE
                Use STAR to answer: "Tell me about a time you had to learn something new quickly."
                """,
            ),
            (
                "phone-interviews-and-follow-up",
                "Phone Interviews and Following Up",
                """
                GOAL: Handle a phone screening and follow up after an interview.

                PHONE SCREENING TIPS
                - Find a quiet place and have your resume in front of you.
                - Smile when you speak -- people can hear it.
                - If you didn't hear: "Sorry, the line dropped out. Could you repeat the question?"

                QUESTIONS YOU MAY HEAR
                - When could you start?
                - Are you able to work weekends / do FIFO / a 2:1 roster?
                - What are your salary expectations?
                Answer for salary: "I understand the award rate for this role is around ..., and I'm
                happy to discuss."

                THANK-YOU EMAIL (send within 24 hours)
                Subject: Thank you -- Warehouse Supervisor interview

                Hi Karen,

                Thank you for meeting with me today. I enjoyed learning about the new
                distribution centre, and I'm even more interested in the role.

                Please let me know if you need anything else from me.

                Kind regards,
                Thanh

                FOLLOWING UP (if you haven't heard back after a week)
                "Hi Karen, I'm just following up on my interview last Tuesday. I'm still very
                interested in the role and wondered if there was any update. Thanks, Thanh"

                PRACTICE
                Write a thank-you email after an interview for a bus driver role.

                Congratulations -- you have finished Workplace English!
                """,
            ),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the 'Workplace English' course (module 1 free, the rest Premium)."

    def handle(self, *args, **options):
        course, created, lessons = seed_course(COURSE, MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} '{course.title}': {len(MODULES)} modules, {lessons} lessons."
            )
        )
