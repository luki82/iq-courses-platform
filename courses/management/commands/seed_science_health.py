"""
Seed the "Practical Science and Public Health" course.

Run with:  python manage.py seed_science_health

Safe to run more than once (updates instead of duplicating). Every module is
free. Each lesson ends with a drag-and-drop PRACTICE and a multiple-choice
QUIZ ("Check Your Understanding"); see courses/lesson_format.py for the layout.

Facts are drawn from WHO and CDC fact sheets, WHO AFRO's South Sudan malaria
vaccine announcement (August 2025) and IFRC volunteer guidance. Re-check
figures against the latest WHO World Malaria Report before major updates.

Writing rules for this file (so the lesson parser reads it correctly):
- A line written entirely in capitals (before any colon) becomes a heading,
  so start ordinary lines with a normal word, never an all-caps abbreviation.
- PRACTICE answers must be short and contain no "/".
- In PRACTICE and ANSWERS, never write a number followed by ". ".
"""
from django.core.management.base import BaseCommand

from courses.seeding import seed_course

COURSE = {
    "slug": "science-and-health",
    "title": "Practical Science and Public Health",
    "description": (
        "Science you can use to protect your family and community: how mosquitoes "
        "breed and how to stop them, how to prevent and recognise malaria, and how "
        "to keep water and food safe from typhoid. Written with communities in "
        "South Sudan and East Africa in mind. General health information only; "
        "always see a health worker if someone is sick. Free for everyone."
    ),
}

LIFE_CYCLE = """
GOAL: Understand how a mosquito grows from an egg to a biting adult, and why that tells us exactly where and when to fight it.

WHY THIS MATTERS
Mosquitoes kill more people than any other animal, because they carry diseases such as malaria, dengue and yellow fever. But for most of its life a mosquito cannot fly or bite: it lives in water. If you understand its life cycle, you can stop mosquitoes before they ever reach your home.

KEY WORDS
- Life cycle: the stages an animal goes through from birth to adult.
- Larva (plural larvae): the young, worm-like stage that lives in water. People sometimes call them "wigglers".
- Pupa (plural pupae): the resting stage in water, when the larva changes into an adult.
- Breeding site: any water where mosquitoes lay eggs, from a pond to a bottle cap.
- Vector: a living thing that carries a disease from one person or animal to another.

THE FOUR STAGES
1. Egg. A female lays a batch of 50 to 200 eggs on the surface of water. Malaria mosquitoes lay their eggs one at a time, and each egg has tiny floats on its sides.
2. Larva. The egg hatches into a larva that lives in the water, eats tiny bits of food and breathes air at the surface. It sheds its skin four times as it grows.
3. Pupa. The larva becomes a pupa. It does not eat. Inside, its body is changing into an adult mosquito.
4. Adult. The adult breaks out of the pupa, rests on the water for a moment while its wings dry, and flies away.

From egg to flying adult usually takes 10 to 14 days for malaria mosquitoes, and can be faster in hot weather. That's why emptying or removing standing water once a week breaks the cycle: the young mosquitoes die before they can fly.

ONLY THE FEMALE BITES
Male mosquitoes feed on plant juices and nectar. Only females bite, because they need the protein in blood to make their eggs. After a blood meal, a female rests for a few days in a dark, sheltered place while her eggs develop, then looks for water to lay them. She can repeat this many times in her life, and each time she bites, she can pick up or pass on a disease.

THREE KINDS OF MOSQUITO TO KNOW
- Anopheles carries malaria. It usually bites in the late evening and at night, often indoors. Its larvae prefer clean, sunlit, shallow water such as puddles, hoof prints, tyre tracks, rice fields and the edges of streams. At rest, the adult sits with its body tilted, bottom in the air.
- Aedes carries dengue, yellow fever, chikungunya and Zika. It bites mainly in the daytime and breeds in small containers: buckets, old tyres, water jars, flower pots and plastic rubbish. It has black-and-white striped legs.
- Culex is the common night-time "buzzing" mosquito. It breeds in dirty water such as blocked drains and latrines, and can spread diseases such as lymphatic filariasis (elephantiasis).

HOW TO SPOT MALARIA MOSQUITO LARVAE
Scoop some water from a puddle into a clear cup or a white bowl and look closely.
- Anopheles larvae lie flat, parallel to the water surface, like a floating stick.
- Most other mosquito larvae hang down at an angle from the surface, breathing through a tube at their tail.
If you find larvae lying flat, malaria mosquitoes are breeding close to your home.

HOW FAR DO MOSQUITOES FLY
Malaria mosquitoes usually stay within about 2 km of where they hatched. That's good news: if a whole village or neighbourhood removes breeding sites together, it can make a real difference. One household alone helps, but a community helps much more.

REAL-LIFE CASE STUDY: THE SCHOOL WATER TANK
At a primary school, teachers noticed many children were sick with malaria after the rainy season started. A science class searched the school grounds with white bowls. They found larvae in a leaking water tank overflow, in tyre ruts by the gate, and in old containers behind the kitchen. The class drained the overflow into a soak pit, filled the ruts with soil and gravel, and collected the containers. They repeated the search every Friday. After a few weeks, staff and pupils noticed far fewer mosquitoes in the classrooms in the evenings, and the class reported their findings to the local health office.

PRACTICE
Complete the sentences.
1. A mosquito lays its eggs on ___.
2. The worm-like young stage of a mosquito is called a ___.
3. The stage that does not eat while it changes into an adult is the ___.
4. Only the ___ mosquito bites.
5. The mosquito that carries malaria is called ___.

ANSWERS: 1. water  2. larva  3. pupa  4. female  5. Anopheles

QUIZ: Check Your Understanding
Q: What are the four stages of the mosquito life cycle, in order?
- Larva, egg, adult, pupa
* Egg, larva, pupa, adult
- Egg, pupa, larva, adult
- Adult, egg, pupa, larva
Explanation: A mosquito starts as an egg on water, hatches into a larva, becomes a pupa while its body changes, and then emerges as a flying adult.

Q: Why do female mosquitoes bite people?
- They drink blood for water when it's hot
- They bite to defend their breeding site
* They need protein from blood to make their eggs
- Both males and females bite to feed
Explanation: Females need the protein in blood to develop their eggs. Males never bite; they feed on plant juices and nectar.

Q: Why does emptying standing water once a week help so much?
- Mosquitoes only lay eggs on one day of the week
* Young mosquitoes need about 10 to 14 days in water to become adults, so weekly emptying kills them before they can fly
- Adult mosquitoes drink the water and die without it
- It makes the water too cold for eggs
Explanation: Eggs, larvae and pupae all live in water. If the water is gone within a week, they die before they can become flying adults, which breaks the cycle.

Q: You scoop water from a puddle and see larvae lying flat along the surface, like little floating sticks. What does this tell you?
- They are harmless water insects
- They are Culex larvae from dirty water
- They are Aedes larvae, which carry dengue
* They are probably Anopheles larvae, the kind that carries malaria
Explanation: Anopheles larvae lie parallel to the water surface because they have no breathing tube. Most other mosquito larvae hang down at an angle.

Q: Which mosquito mostly bites during the day and breeds in small containers such as buckets and old tyres?
- Anopheles
* Aedes
- Culex
- None of them bite during the day
Explanation: Aedes mosquitoes bite mainly in the daytime and breed in containers. They carry dengue, yellow fever, chikungunya and Zika. Anopheles, which carries malaria, mostly bites in the evening and at night.
"""

HOME_CONTROL = """
GOAL: Use cheap, proven methods to cut down mosquitoes around your home and protect your family from bites, especially at night.

WHY THIS MATTERS
You don't need expensive sprays or gadgets. The methods that work best are mostly free or low-cost: sleeping under a treated net, getting rid of standing water, and blocking the ways mosquitoes get into your house. Used together, they protect your family from malaria and other mosquito-borne diseases.

KEY WORDS
- Insecticide-treated net (ITN): a bed net treated with insecticide that kills or drives away mosquitoes that land on it. Long-lasting nets keep working for about three years.
- Indoor residual spraying (IRS): spraying insecticide on inside walls, usually done by health teams.
- Repellent: a cream or spray that stops mosquitoes from biting your skin.
- Eaves: the gap between the top of a wall and the roof, a common way for mosquitoes to get in.

METHOD 1: SLEEP UNDER A TREATED NET, EVERY NIGHT
This is the single most important step against malaria, because malaria mosquitoes bite late at night when people are asleep.
- Everyone should sleep under a net, especially children under five and pregnant women.
- Hang the net over the sleeping place and tuck the edges under the mattress or mat.
- Air a new net outside in the shade for a day before first use.
- Get into bed and close the net before it gets dark, and keep it closed during the day.
- Mend holes as soon as you see them, by sewing them closed or adding a patch. Even small holes let mosquitoes in.
- Wash it only when it's dirty, with mild soap and cool water, and dry it flat in the shade. Washing too often and drying in strong sun weakens the insecticide.
- Replace your net every three to five years, or sooner if it's badly damaged.
- Never use treated nets for fishing or to protect crops. The insecticide harms fish and the net no longer protects your family.

METHOD 2: REMOVE BREEDING SITES EVERY WEEK
Mosquitoes need standing water to breed. Walk around your home once a week, especially during the rainy season:
- Empty, scrub and turn over buckets, basins, pots and old containers.
- Cover water storage drums and jerrycans tightly with a lid or cloth.
- Fill puddles, ruts and hoof prints near the house with soil or sand.
- Clear blocked drains so water flows away.
- Store old tyres under cover or fill them with soil, and collect plastic rubbish, bottles and tins.
- Change water in animal drinking troughs and flower vases at least once a week.
- For ponds or water you can't drain, local fish such as tilapia eat mosquito larvae.

METHOD 3: KEEP MOSQUITOES OUT OF THE HOUSE
- Close the eaves gap between the wall and roof with mud, wood or mesh.
- Fit wire or plastic mesh screens on windows and vents.
- Close doors and windows from dusk, when mosquitoes start looking for people.
- Let health teams spray inside walls during indoor spraying campaigns, and don't repaint or plaster over the walls afterwards, or the insecticide stops working.

METHOD 4: PROTECT YOURSELF IN THE EVENING
- Wear long sleeves and long trousers when sitting outside after dark.
- Use an insect repellent containing DEET, picaridin or oil of lemon eucalyptus on exposed skin, following the label.
- Light-coloured clothes make it easier to see and brush off mosquitoes.

WHAT DOESN'T WORK (OR WORKS POORLY)
- Ultrasonic "mosquito repeller" devices and phone apps: studies show they don't stop bites.
- Eating garlic or taking vitamin B: no good evidence that they repel mosquitoes.
- Burning leaves, cow dung or mosquito coils indoors: smoke may chase some mosquitoes away for a while, but the smoke damages lungs, especially children's. If you use coils, use them outdoors or in well-ventilated places, never instead of a net.
- Cutting all the grass and bushes: tidiness helps a little, but mosquitoes breed in water, not grass. Removing water matters much more.

REAL-LIFE CASE STUDY: A COMPOUND IN BOR
Deng's family of seven lives in a compound near the Nile. Two children had malaria twice in one rainy season. The local health volunteer visited and found three problems: the family had only two nets for seven people, one net had large holes, and water was collecting in a broken water drum and in cattle hoof prints near the huts.
The family took these low-cost steps:
- They collected free nets from the next distribution, so every sleeping place had one, and sewed up the torn net.
- They turned the broken drum over and filled the hoof prints with soil every few days during the rains.
- They packed mud into the eaves gap of the main hut.
- The children now go under their nets before dark.
By the end of the next rainy season, nobody in the family had needed malaria treatment. Their neighbours copied the same steps.

PRACTICE
Complete the sentences.
1. The most important protection against malaria is sleeping under a treated ___ every night.
2. Check for and empty standing water at least once a ___.
3. Dry a washed net in the ___, not in strong sun.
4. Close the gap between the wall and roof, called the ___.
5. Children under five and ___ women most need to sleep under nets.

ANSWERS: 1. net  2. week  3. shade  4. eaves  5. pregnant

QUIZ: Check Your Understanding
Q: Why is sleeping under a treated net so effective against malaria?
* Malaria mosquitoes mostly bite late at night while people sleep, and the net blocks and kills them
- It keeps the room cooler so mosquitoes stay away
- The smell of the net attracts mosquitoes away from the house
- Malaria mosquitoes only bite in the daytime
Explanation: Anopheles mosquitoes, which carry malaria, mostly bite in the late evening and at night. A treated net forms a barrier and the insecticide kills or drives away mosquitoes that land on it.

Q: Your net has a small hole. What should you do?
- Nothing, small holes don't matter
- Throw it away and sleep without one
* Sew it closed or patch it straight away
- Wash it in hot water to tighten the threads
Explanation: Mosquitoes can get through even small holes. Mend holes quickly with a needle and thread or a patch, and keep using the net.

Q: Which of these is a breeding site for malaria mosquitoes?
- Dry, dusty ground
* Rainwater collected in cattle hoof prints near the house
- A tightly covered water drum
- A bag of dry maize
Explanation: Anopheles mosquitoes breed in shallow, sunlit water such as puddles and hoof prints. Filling them with soil removes the breeding site. A tightly covered drum keeps mosquitoes out.

Q: A neighbour wants to buy an ultrasonic mosquito repeller instead of using nets. What would you tell them?
- It works better than a net
- It works only for children
- It's fine if used with mosquito coils indoors
* Studies show these devices don't stop bites, so keep using a net
Explanation: Research has found that ultrasonic repellers don't prevent mosquito bites. Treated nets, removing standing water and screening the house are proven to work.

Q: Health workers have just sprayed the inside walls of your house. What should you avoid doing?
- Sleeping under a net
- Closing the eaves gap
- Emptying containers of water
* Repainting or plastering the walls soon afterwards
Explanation: Indoor spraying leaves insecticide on the walls that kills mosquitoes when they rest there. Repainting or plastering covers it up so it stops working. Keep using your net too.
"""

MALARIA = """
GOAL: Know how malaria spreads, recognise the warning signs, and act fast to get tested and treated, and know how to prevent it, especially in children and pregnant women.

WHY THIS MATTERS
Malaria is one of the biggest killers of children in Africa. In 2024 there were about 282 million malaria cases and 610,000 deaths worldwide, and around 95% of them were in Africa. Most of the people who die are children under five. In South Sudan, malaria causes about 5.5 million cases and more than 4,000 deaths every year, and about half of young children tested in 2023 had malaria parasites in their blood. Malaria can be prevented, and it can be cured if it's treated early.

KEY WORDS
- Parasite: a tiny living thing that lives inside another living thing and harms it. Malaria is caused by Plasmodium parasites.
- Rapid diagnostic test (RDT): a quick finger-prick blood test for malaria that gives a result in about 15 to 20 minutes.
- Severe malaria: malaria that has started to damage the body, such as the brain, blood or kidneys. It is an emergency.
- Prevention: actions that stop a disease before it starts.

HOW MALARIA SPREADS
1. An Anopheles mosquito bites a person who has malaria and sucks up parasites with the blood.
2. The parasites grow inside the mosquito for about one to two weeks.
3. The mosquito bites another person and passes the parasites into their blood.
4. The parasites travel to the liver, multiply, then attack red blood cells.
Malaria does not spread through the air, by touching, or by sharing food. It can pass from a mother to her unborn baby and, rarely, through blood transfusions.

SIGNS AND SYMPTOMS
Early signs usually appear 10 to 15 days after an infected bite:
- Fever, which may come and go
- Chills and shivering
- Headache
- Sweating, body aches and tiredness
- In children: vomiting, poor feeding, being unusually sleepy or cranky

DANGER SIGNS: GO TO A HEALTH FACILITY IMMEDIATELY
- Convulsions (fits)
- Very sleepy, confused or cannot be woken
- Difficulty breathing
- Unable to drink, eat or breastfeed, or vomiting everything
- Dark or very little urine
- Yellow eyes or skin
- Unusual bleeding
The most dangerous type of malaria can become severe and kill within 24 hours, so never wait to see if a fever goes away on its own.

IF SOMEONE HAS A FEVER: TEST, THEN TREAT
- Get tested the same day, ideally within 24 hours of the fever starting. A health worker can do a finger-prick RDT or look at the blood under a microscope.
- Not every fever is malaria. Testing makes sure you get the right medicine, and if the test is negative, the health worker will look for other causes.
- If the test is positive, take the full course of the medicine the health worker gives you, even if you feel better after a day or two. Stopping early can let the malaria come back and helps the parasites become resistant to medicine.
- Don't use leftover tablets, share medicine or buy unlabelled medicine from the market. The wrong dose or fake medicine can be deadly.
- Keep a child with fever cool with light clothes, and give plenty of fluids or breastfeed more often on the way to the clinic.

PROTECTING THOSE MOST AT RISK
- Children under five: sleep under a treated net every night. In South Sudan, the R21 malaria vaccine is now part of routine childhood vaccinations. Babies get three doses at 5, 6 and 7 months, and a fourth at 18 months. Take children to the clinic for every dose.
- Pregnant women: malaria in pregnancy can cause anaemia, miscarriage and low birth weight. Go to antenatal care early, ask about preventive malaria medicine during pregnancy, and always sleep under a net.
- Visitors from areas without malaria: they have little or no immunity, so they get very sick. They should use nets and repellent, and travellers should see a doctor before travelling about preventive medicine.

COMMON MYTHS
- "Malaria comes from drinking dirty water or eating mangoes." False. It only comes from the bite of an infected mosquito (or from mother to baby).
- "Adults who've had malaria many times are immune." Partly false. Repeated infections give some protection, but adults can still get sick and pass malaria to mosquitoes, and protection fades if you move away for a while.
- "If the fever goes away, the malaria is gone." False. Fever can come and go. Only finishing the full treatment cures it.
- "Every fever is malaria and typhoid together." Often false. This is common in East Africa, but many people are told they have typhoid because of an unreliable test. See the next lesson.

REAL-LIFE CASE STUDY: NYANDENG'S DAUGHTER
Nyandeng's three-year-old daughter developed a fever and stopped eating in the evening. Nyandeng remembered the health volunteer's advice: test within 24 hours. The next morning she took her daughter to the nearest health post. The RDT was positive. The health worker gave the correct medicine for the child's weight and explained how to give every dose. On the second day, the girl felt better and wanted to play, but Nyandeng finished the full course anyway. She also noticed their family net had a hole near the child's sleeping place and sewed it that night. A week later, her daughter was completely well. Acting early made the difference: she never developed danger signs.

PRACTICE
Complete the sentences.
1. Malaria is caused by a tiny ___ carried by mosquitoes.
2. Early signs of malaria usually start 10 to 15 ___ after an infected bite.
3. Anyone with a fever should get a malaria ___ the same day.
4. Always take the ___ course of medicine, even if you feel better.
5. In South Sudan, babies get the first malaria vaccine dose at ___ months.

ANSWERS: 1. parasite  2. days  3. test  4. full  5. five

QUIZ: Check Your Understanding
Q: How does malaria spread from one person to another?
- Through coughing and sneezing
- By sharing food or cups with a sick person
* Through the bite of an infected female Anopheles mosquito
- By drinking dirty water
Explanation: Malaria parasites pass from person to person through bites from infected female Anopheles mosquitoes. It can also pass from mother to unborn baby, but it does not spread through the air, food or water.

Q: A child has had a fever since last night. What is the best thing to do?
* Take the child for a malaria test today
- Wait three days to see if the fever goes away
- Give leftover malaria tablets from last year
- Buy any malaria medicine from the market
Explanation: Test within 24 hours of the fever starting. The most dangerous kind of malaria can become severe within a day, and testing makes sure the child gets the right medicine for their illness.

Q: Which of these is a danger sign that means a person with malaria needs a health facility immediately?
- A mild headache
- Feeling tired in the afternoon
- Sweating after the fever
* Convulsions, or being very hard to wake
Explanation: Convulsions, confusion, difficulty breathing, being unable to drink, dark urine, yellow eyes and unusual bleeding are signs of severe malaria. These are emergencies.

Q: After two days of malaria medicine, a man feels much better. What should he do?
- Stop taking the medicine and save the rest for next time
* Finish the full course exactly as the health worker said
- Give the rest of the tablets to his brother
- Take a double dose to finish faster
Explanation: Feeling better doesn't mean all the parasites are gone. Finishing the full course cures the infection and helps stop malaria medicines from becoming less effective.

Q: In South Sudan, at what ages do children receive the R21 malaria vaccine?
- One dose at birth
- Two doses at 9 and 12 months
* Three doses at 5, 6 and 7 months, and a fourth at 18 months
- Only when a child first gets malaria
Explanation: South Sudan's schedule is three doses at 5, 6 and 7 months, plus a fourth dose at 18 months alongside the second measles dose. The vaccine works best alongside nets, not instead of them.
"""

TYPHOID = """
GOAL: Understand that typhoid spreads through dirty water, food and hands, not mosquitoes, and learn simple ways to make water and food safe for your family.

WHY THIS MATTERS
Typhoid fever makes about 9 million people sick and kills about 110,000 every year around the world, most of them children in places without safe water and toilets. Many people believe typhoid and malaria come together from mosquitoes. They don't. Typhoid comes from swallowing germs from human waste. That means the ways to prevent it are completely different: clean water, toilets, handwashing and safe food.

KEY WORDS
- Bacteria: tiny living germs. Typhoid is caused by a bacterium called Salmonella Typhi.
- Faeces: human waste (poo). Typhoid germs leave the body in the faeces of an infected person.
- Contaminated: made dirty or unsafe by germs.
- Carrier: a person who feels healthy but still carries typhoid germs and can spread them.
- Antibiotic: a medicine that kills bacteria. Antibiotics don't work against malaria or viruses.

HOW TYPHOID SPREADS
Typhoid follows a simple path, sometimes called the "faecal-oral" route: from one person's faeces to another person's mouth.
- Faeces get into water when people defecate in the open, near rivers or wells, or when latrines leak.
- Germs get onto hands if people don't wash with soap after using the toilet.
- Unwashed hands then touch food, cups or water containers.
- Flies can carry germs from faeces to food.
- Someone eats or drinks the contaminated food or water, and the germs multiply in their body.

SIGNS AND SYMPTOMS
Typhoid usually starts slowly, often 1 to 3 weeks after swallowing the germs:
- A high fever that keeps rising over several days and lasts a long time
- Headache, weakness and tiredness
- Stomach pain
- Constipation or diarrhoea
- Loss of appetite and nausea
- Sometimes a faint rash of rose-coloured spots
Without treatment, typhoid can cause serious problems such as a hole in the gut. Anyone with a long-lasting fever should see a health worker.

THE TESTING PROBLEM: WHY SO MANY PEOPLE ARE TOLD THEY HAVE TYPHOID
In many clinics in East Africa, typhoid is tested with the Widal test. It's cheap and fast, but often wrong. In a study of 158 people with suspected typhoid in Dar es Salaam, Tanzania, the Widal test was positive in about 8 out of 10 of them, but a blood culture (the reliable test) showed that only about 1 in 10 actually had typhoid. That means most people told "you have typhoid" did not.
This matters because people take antibiotics they don't need. Unnecessary antibiotics cost money, cause side effects and help germs become resistant, so the medicines stop working when they're really needed. If you have a fever, make sure you're tested for malaria first, and ask the health worker whether a blood or stool culture is possible if typhoid is suspected.

IF A HEALTH WORKER DIAGNOSES TYPHOID
- Take all of the antibiotics exactly as prescribed, even after you feel better.
- Wash your hands with soap after using the toilet and before touching food.
- Don't prepare food for other people until a health worker says the infection has cleared. Some people keep carrying germs after they feel well.

MAKING DRINKING WATER SAFE
Water from rivers, ponds, open wells and even some taps can carry typhoid germs. Low-cost ways to make it safe:
- Boiling: bring water to a full, rolling boil (big bubbles) for at least one minute, then let it cool in a clean, covered container. This kills typhoid germs.
- Chlorine: use water treatment tablets or liquid chlorine sold for drinking water. Follow the instructions on the packet exactly, and wait at least 30 minutes before drinking.
- Sunlight (solar disinfection): fill clear plastic bottles of 2 litres or less with clear water and leave them lying in full sunlight for at least 6 hours, or for two days if it's cloudy. This works only with clear water, so let cloudy water settle and pour it through a clean cloth first.
- Safe storage: keep treated water in a container with a lid and a tap or narrow opening, so hands and cups don't go into the water.

HANDWASHING: THE SIMPLEST MEDICINE
Wash hands with soap and water:
- After using the toilet or cleaning a child
- Before preparing food, before eating and before feeding a child
A simple "tippy tap", made from a jerrycan hung on a stick and tipped with a foot pedal, lets a family wash hands with very little water. If there's no soap, ash is better than water alone.

TOILETS AND SANITATION
- Use a latrine or toilet every time, and stop open defecation. If one family's faeces get into the water, the whole community is at risk.
- Build latrines at least 30 metres from water sources such as wells and boreholes, and downhill from them.
- Keep latrines covered to stop flies.

SAFE FOOD
- Cook food thoroughly and eat it while it's hot.
- Peel fruit yourself, or wash it in safe water.
- Avoid ice and drinks unless you know the water is safe.
- Boil milk unless it's pasteurised.
- Cover food to keep flies away.
- Remember the rule: "Boil it, cook it, peel it, or forget it."

THE TYPHOID VACCINE
A typhoid conjugate vaccine can protect children from 6 months of age with a single injection. Some countries in Africa have added it to routine childhood vaccinations. Ask your local health centre whether it's available.

REAL-LIFE CASE STUDY: THE COOK WHO DIDN'T FEEL SICK
In New York over 100 years ago, a cook named Mary Mallon moved from family to family, and in each home people fell ill with typhoid. She felt perfectly healthy. Investigators discovered she was a carrier: typhoid germs lived in her body and passed onto the food she made, because she didn't wash her hands well after using the toilet. She became known as "Typhoid Mary". Her story shows why handwashing before preparing food matters, even for people who feel fine, and why someone who has had typhoid should be checked before cooking for others.

PRACTICE
Complete the sentences.
1. Typhoid is caused by ___, not by a mosquito bite.
2. Typhoid germs leave the body in a sick person's ___.
3. Boil water at a rolling boil for at least one ___.
4. Wash your hands with ___ after using the toilet.
5. A person who feels healthy but still spreads typhoid is called a ___.

ANSWERS: 1. bacteria  2. faeces  3. minute  4. soap  5. carrier

QUIZ: Check Your Understanding
Q: How do people catch typhoid?
- From the bite of an Anopheles mosquito
- From cold weather and rain
* By swallowing food or water contaminated with germs from human faeces
- By standing near someone who is coughing
Explanation: Typhoid spreads through the faecal-oral route: germs from an infected person's faeces get into water, onto hands or into food, and someone swallows them. Mosquitoes do not spread typhoid.

Q: A clinic tells a man he has both malaria and typhoid after a quick Widal test. Why should he be careful about this result?
- The Widal test is always correct
* The Widal test often gives false positives, so many people are wrongly told they have typhoid
- Typhoid and malaria are the same disease
- Only children can get typhoid
Explanation: Studies in East Africa show the Widal test is positive for many people who don't have typhoid. A blood culture is more reliable. Unneeded antibiotics cost money and help germs become resistant.

Q: Which is a safe way to treat river water for drinking at home?
- Let it stand overnight in an open bucket
- Add a little sugar and stir
- Pour it through a cloth and drink it straight away
* Bring it to a rolling boil for at least one minute, then store it covered
Explanation: A rolling boil for at least one minute kills typhoid germs. Pouring through a cloth removes dirt but not germs, so it should be followed by boiling, chlorine or sunlight treatment.

Q: When is it most important to wash your hands with soap to prevent typhoid?
- Only when they look dirty
* After using the toilet and before preparing or eating food
- Once a day in the morning
- Only after touching animals
Explanation: Germs from faeces can't be seen. Washing with soap after the toilet and before handling food breaks the path from faeces to mouth.

Q: Why should a latrine be built well away from a well or borehole?
- So it's easier to find at night
- Because latrines attract mosquitoes
* So germs from faeces don't seep into the drinking water
- It doesn't matter where a latrine is built
Explanation: Germs from a latrine can seep through the soil into nearby water. Build latrines at least 30 metres from water sources and downhill from them.
"""

MODULES = [
    (
        "Module 1: Mosquitoes and Malaria",
        True,
        [
            ("mosquito-life-cycle", "The Mosquito Life Cycle: Where Mosquitoes Come From", LIFE_CYCLE),
            ("how-to-get-rid-of-mosquitoes-at-home", "How to Reduce Mosquitoes Around Your Home (Low-Cost Methods)", HOME_CONTROL),
            ("malaria-prevention-and-symptoms", "Malaria: Prevention, Warning Signs and Early Treatment", MALARIA),
        ],
    ),
    (
        "Module 2: Clean Water and Food Safety",
        True,
        [
            ("typhoid-prevention-safe-water-and-food", "Typhoid: How It Spreads and How to Prevent It", TYPHOID),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the 'Practical Science and Public Health' course (all modules free)."

    def handle(self, *args, **options):
        course, created, lessons = seed_course(COURSE, MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} '{course.title}': {len(MODULES)} modules, {lessons} lessons."
            )
        )
