"""
Seed the "Practical Maths for Everyday Life" course.

Run with:  python manage.py seed_practical_maths

Safe to run more than once (updates instead of duplicating). Every module is
free. Each lesson ends with a drag-and-drop PRACTICE and a multiple-choice
QUIZ ("Check Your Understanding"); see courses/lesson_format.py for the layout.

Writing rules for this file (so the lesson parser reads it correctly):
- A line written entirely in capitals (before any colon) becomes a heading,
  so start ordinary lines with a normal word, never an all-caps abbreviation.
- PRACTICE answers must be short and contain no "/".
- In PRACTICE and ANSWERS, never write a number followed by ". " (e.g. "is 80. Then"),
  or it is read as a new numbered item.
"""
from django.core.management.base import BaseCommand

from courses.seeding import seed_course

COURSE = {
    "slug": "practical-maths",
    "title": "Practical Maths for Everyday Life",
    "description": (
        "The maths you actually use: working out sale prices and real bargains, "
        "how long a trip will take and when to leave, how many pavers or tiles to "
        "buy, and more. Short lessons with worked examples, practice and a quick "
        "quiz at the end of every lesson. Free for everyone."
    ),
}

DISCOUNTS = """
GOAL: Work out sale prices in your head, compare deals and spot bargains that aren't really bargains.

WHY THIS MATTERS
Shops know that most people don't stop to check the maths. "Up to 50% off", "buy 2 get 1 free" and "extra 20% off at checkout" are designed to feel like big savings. In a few seconds you can work out what you will actually pay, and which deal really is cheaper.

KEY WORDS
- Original price: the normal price before the sale (sometimes called the RRP, or recommended retail price).
- Discount: the amount taken off the price.
- Percentage (%): "out of 100". 25% means 25 out of every 100.
- Sale price: what you actually pay after the discount.
- Unit price: the price for one unit, such as per kilogram, per litre or per item.

METHOD 1: FIND THE DISCOUNT, THEN SUBTRACT
1. Turn the percentage into a decimal by dividing by 100. For example, 25% becomes 0.25.
2. Multiply the original price by that decimal. This is your saving.
3. Subtract the saving from the original price.

Example: a jacket costs $80 and is 25% off.
- Saving: 0.25 × $80 = $20
- Sale price: $80 − $20 = $60

METHOD 2: THE ONE-STEP SHORTCUT
If something is 25% off, you pay the other 75%. So multiply by what you pay:
- 0.75 × $80 = $60
This is faster, and it's the method that works best on a phone calculator.
- 10% off → multiply by 0.9
- 20% off → multiply by 0.8
- 30% off → multiply by 0.7
- 15% off → multiply by 0.85

MENTAL MATHS TRICKS: no calculator needed
- 10%: move the decimal point one place left. 10% of $64 = $6.40
- 5%: half of 10%. 5% of $64 = $3.20
- 20%: double 10%. 20% of $64 = $12.80
- 25%: divide by 4. 25% of $64 = $16
- 50%: halve it. 50% of $64 = $32
- 15%: 10% plus 5%. 15% of $64 = $6.40 + $3.20 = $9.60

Example: a pair of shoes costs $240 with 15% off. 10% is $24 and 5% is $12, so the discount is $36. You pay $240 − $36 = $204.

WORKING BACKWARDS
What percentage off is it? Divide the saving by the original price, then multiply by 100.
- A $120 kettle is on sale for $90. The saving is $30. 30 ÷ 120 = 0.25, so it's 25% off.

What was the original price? Divide the sale price by the part you paid.
- You paid $63 after 30% off, so you paid 70% of the price. $63 ÷ 0.7 = $90.
- A common mistake is to add 30% of $63 back on. That gives $81.90, which is wrong, because the 30% was taken from the original price, not from $63.

TRAP 1: STACKED DISCOUNTS DON'T ADD UP
"20% off, plus an extra 10% off at the checkout" is not 30% off. The second discount comes off the already-reduced price.
- Start with $100. After 20% off: $100 × 0.8 = $80.
- After another 10% off: $80 × 0.9 = $72.
- Total saving: $28, which is 28%, not 30%.
Quick method: multiply the parts you pay. 0.8 × 0.9 = 0.72, so you pay 72%.

TRAP 2: "BUY 2, GET 1 FREE" VS "30% OFF"
Buy 2, get 1 free means you get 3 items for the price of 2. You pay 2 ÷ 3 = 0.667, or about 66.7% of the normal price, which is a 33.3% discount on each item. That beats 30% off, but only if you actually need 3.

TRAP 3: THE BIGGER PACK ISN'T ALWAYS CHEAPER
Always compare the unit price.
- Shampoo A: 400 mL for $6.00. Per 100 mL: $6.00 ÷ 4 = $1.50
- Shampoo B: 750 mL for $10.50. Per 100 mL: $10.50 ÷ 7.5 = $1.40
Shampoo B is cheaper per 100 mL. Many supermarkets print the unit price in small type on the shelf label. Look for it.

TRAP 4: THE INFLATED "WAS" PRICE
Some sellers raise the "was" price just before a sale so the discount looks bigger. "Was $99, now $59" means nothing if it normally sold for $65. Before a big purchase, check the price at two or three other shops or online.

REAL-LIFE CASE STUDY: AMINA BUYS A FRIDGE
Amina sees the same fridge in two shops.
- Shop A: $1,200 with 25% off.
- Shop B: $1,100 with 15% off, plus free delivery (Shop A charges $60 delivery).

Shop A: $1,200 × 0.75 = $900, plus $60 delivery = $960.
Shop B: $1,100 × 0.85 = $935, with free delivery = $935.

The bigger percentage looked better, but Shop B saves Amina $25. Lesson: compare the final price you will pay, including extras, not the percentage.

PRACTICE
Complete the sentences.
1. 10% of $70 is ___.
2. A $50 shirt with 20% off costs ___.
3. If something is 25% off, you pay ___ of the price.
4. Going from $200 down to $150 is a ___ discount.
5. Taking 20% off and then a further 10% off saves ___ in total.

ANSWERS: 1. $7  2. $40  3. 75%  4. 25%  5. 28%

QUIZ: Check Your Understanding
Q: A television costs $650 and is 20% off. What is the sale price?
- $630
- $130
* $520
- $580
Explanation: 10% of $650 is $65, so 20% is $130. The sale price is $650 − $130 = $520. Or in one step: $650 × 0.8 = $520. ($630 comes from taking off $20 instead of 20%, and $130 is the saving, not the price.)

Q: Which is the better deal for the same pair of jeans?
* Shop A: $45 with 10% off
- Shop B: $48 with 15% off
- They cost exactly the same
Explanation: Shop A: $45 × 0.9 = $40.50. Shop B: $48 × 0.85 = $40.80. Shop A is 30 cents cheaper, even though Shop B has the bigger percentage off.

Q: A shop offers 30% off, then an extra 20% off at the checkout. What is the total discount?
- 50%
* 44%
- 46%
- 40%
Explanation: Discounts stack by multiplying, not adding. You pay 0.7 × 0.8 = 0.56, or 56% of the original price, so the total discount is 100% − 56% = 44%.

Q: You paid $36 for a toaster after a 25% discount. What was the original price?
- $45
- $27
* $48
- $61
Explanation: After 25% off you paid 75% of the original price, so the original was $36 ÷ 0.75 = $48. Check: 25% of $48 is $12, and $48 − $12 = $36. ($45 comes from adding 25% of $36, which is the common mistake.)

Q: Rice comes in a 5 kg bag for $9.50 or a 2 kg bag for $4.20. Which is cheaper per kilogram?
* The 5 kg bag, at $1.90 per kg
- The 2 kg bag, at $2.10 per kg
- They cost the same per kg
Explanation: 5 kg bag: $9.50 ÷ 5 = $1.90 per kg. 2 kg bag: $4.20 ÷ 2 = $2.10 per kg. The 5 kg bag saves 20 cents on every kilogram.
"""

TRAVEL = """
GOAL: Work out how long a trip will take, how fast you need to travel, and what time to leave so you arrive on time.

WHY THIS MATTERS
Whether you're driving to a job interview, catching a bus to another town or walking to school, the same simple formula tells you how long it will take. Knowing it helps you plan, avoid being late, and check whether a map app's estimate makes sense.

KEY WORDS
- Distance: how far you travel, for example in kilometres (km) or miles.
- Speed: how far you travel in one hour, for example kilometres per hour (km/h).
- Time: how long the trip takes.
- Average speed: your overall speed for the whole trip, including slow parts, traffic and stops.

THE THREE FORMULAS
- Distance = Speed × Time
- Time = Distance ÷ Speed
- Speed = Distance ÷ Time

Memory trick: draw a triangle with D at the top, and S and T at the bottom. Cover the one you want to find. If D is on top of S, divide. If S and T sit side by side, multiply.

Important: the units must match. If distance is in km and speed is in km/h, the time comes out in hours.

TURNING HOURS INTO HOURS AND MINUTES
Calculators give time as a decimal, like 2.75 hours. That does not mean 2 hours and 75 minutes.
1. Keep the whole number: 2 hours.
2. Multiply the decimal part by 60: 0.75 × 60 = 45 minutes.
3. So 2.75 hours = 2 hours 45 minutes.

Useful ones to remember:
- 0.25 hours = 15 minutes
- 0.5 hours = 30 minutes
- 0.75 hours = 45 minutes
- 0.1 hours = 6 minutes

Going the other way, divide minutes by 60 to get hours: 45 minutes = 45 ÷ 60 = 0.75 hours.

EXAMPLE 1: HOW LONG WILL IT TAKE?
A town is 240 km away and you expect to average 80 km/h.
Time = 240 ÷ 80 = 3 hours.

EXAMPLE 2: HOW FAST WERE YOU GOING?
A bus travels 50 km in 1 hour 15 minutes. First change the time into hours: 1 hour 15 minutes = 1.25 hours.
Speed = 50 ÷ 1.25 = 40 km/h.

EXAMPLE 3: HOW FAR CAN YOU WALK?
Most adults walk at about 5 km/h. In 36 minutes (0.6 hours) you can walk about 5 × 0.6 = 3 km.

WHAT TIME SHOULD I LEAVE?
1. Work out the travel time.
2. Add time for stops (fuel, food, rest breaks).
3. Add a safety buffer for traffic or delays, often 10 to 20 minutes.
4. Count back from the time you need to arrive.

Example: you need to arrive at 2:00 pm. The drive takes 3 hours, you plan one 30-minute rest stop, and you add a 15-minute buffer. Total: 3 hours 45 minutes. Counting back from 2:00 pm, leave by 10:15 am.

TRAP: AVERAGE SPEED IS NOT THE SPEED LIMIT
On a 100 km/h highway, your average speed is usually lower because of towns, roadworks, traffic and stops. In busy city traffic, 25 to 40 km/h is common. Use a realistic average, not the speed limit.

TRAP: YOU CAN'T JUST AVERAGE TWO SPEEDS
You drive 60 km to a market at 60 km/h, and come back at 40 km/h because of traffic. Your average speed is not 50 km/h.
- Going: 60 ÷ 60 = 1 hour
- Coming back: 60 ÷ 40 = 1.5 hours
- Total: 120 km in 2.5 hours, so 120 ÷ 2.5 = 48 km/h
You spend longer at the slower speed, so it pulls the average down.

REAL-LIFE CASE STUDY: JOSEPH'S DELIVERY RUN
Joseph delivers goods to three villages in one day.
- Leg 1: 36 km on a good road at 60 km/h → 36 ÷ 60 = 0.6 hours = 36 minutes
- Leg 2: 20 km on a rough road at 25 km/h → 20 ÷ 25 = 0.8 hours = 48 minutes
- Leg 3: 44 km back on a tar road at 80 km/h → 44 ÷ 80 = 0.55 hours = 33 minutes

Driving time: 36 + 48 + 33 = 117 minutes = 1 hour 57 minutes. With 20 minutes unloading at each of the three stops, the whole run takes about 2 hours 57 minutes. If he leaves at 8:00 am, he'll be back just before 11:00 am, in time to take an afternoon booking.

PRACTICE
Complete the sentences.
1. Travelling 150 km at 50 km per hour takes ___ hours.
2. Half an hour is ___ minutes.
3. A time of 1.25 hours is 1 hour and ___ minutes.
4. Covering 120 km in 2 hours is an average speed of ___ km per hour.
5. Walking at 5 km per hour for 2 hours covers ___ km.

ANSWERS: 1. 3  2. 30  3. 15  4. 60  5. 10

QUIZ: Check Your Understanding
Q: A town is 210 km away. If you average 70 km/h, how long will the trip take?
* 3 hours
- 2 hours 10 minutes
- 3.5 hours
- 140 hours
Explanation: Time = Distance ÷ Speed = 210 ÷ 70 = 3 hours. (140 comes from subtracting the speed from the distance, which doesn't give a time at all.)

Q: Your map app says the trip will take 2.4 hours. How long is that in hours and minutes?
- 2 hours 40 minutes
* 2 hours 24 minutes
- 2 hours 4 minutes
- 2 hours 14 minutes
Explanation: Multiply the decimal part by 60: 0.4 × 60 = 24 minutes. So 2.4 hours is 2 hours 24 minutes, not 2 hours 40 minutes.

Q: Your job interview is at 9:00 am, 45 km away. In morning traffic you'll average 30 km/h, and you want to arrive 15 minutes early. What is the latest time you should leave?
- 7:30 am
* 7:15 am
- 7:45 am
- 8:15 am
Explanation: Travel time = 45 ÷ 30 = 1.5 hours = 1 hour 30 minutes. You want to arrive at 8:45 am, and 1 hour 30 minutes before 8:45 am is 7:15 am.

Q: A bus travels 18 km in 36 minutes. What is its average speed?
- 0.5 km/h
- 50 km/h
* 30 km/h
- 54 km/h
Explanation: First change minutes to hours: 36 ÷ 60 = 0.6 hours. Then Speed = 18 ÷ 0.6 = 30 km/h. (0.5 comes from dividing 18 by 36 without converting the minutes to hours.)

Q: You drive 100 km to town at 100 km/h and return the same way at 50 km/h. What is your average speed for the whole trip?
- 75 km/h
- 50 km/h
- 60 km/h
* About 67 km/h
Explanation: Going takes 100 ÷ 100 = 1 hour and returning takes 100 ÷ 50 = 2 hours. That's 200 km in 3 hours, so the average is 200 ÷ 3 ≈ 66.7 km/h. You spend more time at the slower speed, so the average is below 75.
"""

MODULES = [
    (
        "Module 1: Money and Time",
        True,
        [
            ("how-to-calculate-discounts", "How to Calculate Discounts and Sale Prices", DISCOUNTS),
            ("travel-time-speed-and-distance", "Travel Time, Speed and Distance", TRAVEL),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the 'Practical Maths for Everyday Life' course (all modules free)."

    def handle(self, *args, **options):
        course, created, lessons = seed_course(COURSE, MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} '{course.title}': {len(MODULES)} modules, {lessons} lessons."
            )
        )
