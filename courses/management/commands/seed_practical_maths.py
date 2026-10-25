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
        "how long a trip will take and when to leave, converting cups, grams, feet, "
        "kilograms and temperatures, and more. Short lessons with worked examples, practice and a quick "
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

KITCHEN = """
GOAL: Convert cups, tablespoons, teaspoons, millilitres, ounces and grams so any recipe from any country works in your kitchen.

WHY THIS MATTERS
Recipes online come from all over the world. An American recipe says "1 cup of flour" and "2 sticks of butter", a British one says "200 g", and an Australian one uses a different-sized tablespoon. Getting conversions wrong is the main reason a cake sinks or a sauce is too salty. Once you know a few key numbers, you can cook from any recipe.

KEY WORDS
- Volume: how much space something takes up. Measured in millilitres (mL), litres (L), cups, tablespoons (tbsp) and teaspoons (tsp).
- Weight (mass): how heavy something is. Measured in grams (g), kilograms (kg), ounces (oz) and pounds (lb).
- Fluid ounce (fl oz): a measure of volume, not weight.
- Ounce (oz): a measure of weight. A fluid ounce and an ounce are different things.

THE NUMBERS TO REMEMBER
- 1 teaspoon (tsp) = 5 mL
- 1 tablespoon (tbsp) = 15 mL, which is 3 teaspoons
- 1 cup = 16 tablespoons
- 1/2 cup = 8 tablespoons
- 1/4 cup = 4 tablespoons
- 1 US cup = about 240 mL (237 mL exactly)
- 1 metric cup = 250 mL (used in Australia, New Zealand and Canada)
- 1 US fluid ounce = about 30 mL (29.6 mL exactly)
- 8 fluid ounces = 1 US cup

WATCH OUT: THE AUSTRALIAN TABLESPOON
In Australia, a tablespoon is 20 mL (4 teaspoons), not 15 mL. If you use an Australian tablespoon for an American recipe, you add a third more than intended. That matters for salt, baking powder and baking soda. For small amounts of strong ingredients, measure in teaspoons to be safe: 1 US tablespoon = 3 teaspoons.

AMERICAN LIQUID MEASURES
- 2 cups = 1 pint
- 2 pints = 1 quart
- 4 quarts = 1 gallon
- 16 cups = 1 gallon
- 128 fluid ounces = 1 US gallon
- 1 US gallon = about 3.8 litres

CUPS TO GRAMS: IT DEPENDS WHAT'S IN THE CUP
A cup measures volume, but different foods weigh different amounts. A cup of flour is much lighter than a cup of sugar. These are typical weights for one US cup:
- Water or milk: about 240 g
- Plain (all-purpose) flour: about 125 g
- White sugar: about 200 g
- Brown sugar, packed: about 220 g
- Uncooked rice: about 185 g
- Butter: about 227 g (1 cup = 2 American "sticks", and 1 stick = 113 g)
Flour weights vary depending on how tightly the cup is filled, so for baking, weighing is more accurate than cups.

OUNCES AND POUNDS TO GRAMS
- 1 ounce (oz) = 28.35 g, so roughly 28 g or "about 30 g" for quick estimates
- 1 pound (lb) = 16 ounces = 454 g
- 1 kg = 2.2 lb
- Example: a recipe asks for 12 oz of chicken. 12 × 28.35 = 340 g.

SCALING A RECIPE UP OR DOWN
To change the number of servings, find the scale factor: new servings ÷ original servings. Multiply every ingredient by it.
- A recipe serves 4 and you need to feed 6. Scale factor: 6 ÷ 4 = 1.5.
- 2 cups of rice becomes 2 × 1.5 = 3 cups.
- 3 tablespoons of oil becomes 3 × 1.5 = 4.5 tablespoons.
Cooking times usually change less than the ingredients do, so check food is cooked rather than multiplying the time.

REAL-LIFE CASE STUDY: GRACE BAKES AN AMERICAN BANANA BREAD IN SYDNEY
The recipe says: 2 cups flour, 3/4 cup sugar, 1 stick butter, 1 tsp baking soda, 1/2 tsp salt.
Grace has kitchen scales and Australian spoons.
- Flour: 2 × 125 g = 250 g
- Sugar: 3/4 × 200 g = 150 g
- Butter: 1 stick = 113 g
- Baking soda: 1 teaspoon is 5 mL everywhere, so her teaspoon is fine.
- Salt: 1/2 teaspoon, also fine.
Because the recipe uses teaspoons, not tablespoons, her Australian spoons cause no problem. If it had said 1 tablespoon of baking soda, she would use 3 teaspoons instead of her 20 mL tablespoon.

PRACTICE
Complete the sentences.
1. One tablespoon is the same as ___ teaspoons in a US recipe.
2. A quarter cup is ___ tablespoons.
3. One US gallon holds ___ fluid ounces.
4. One pound is ___ ounces.
5. In Australia, a tablespoon holds ___ mL.

ANSWERS: 1. 3  2. 4  3. 128  4. 16  5. 20

QUIZ: Check Your Understanding
Q: How many tablespoons are in 1/4 cup?
- 2 tablespoons
- 3 tablespoons
* 4 tablespoons
- 8 tablespoons
Explanation: A cup is 16 tablespoons, so a quarter cup is 16 ÷ 4 = 4 tablespoons. (8 tablespoons is half a cup.)

Q: How many grams are in one ounce?
* About 28 grams
- About 16 grams
- About 100 grams
- About 454 grams
Explanation: One ounce is 28.35 grams. (16 is the number of ounces in a pound, and 454 grams is a whole pound.)

Q: A recipe needs 2 cups of plain flour. Roughly how many grams is that?
- 480 g
- 400 g
* 250 g
- 125 g
Explanation: A US cup of plain flour weighs about 125 g, so 2 cups is about 250 g. (480 g would be right for 2 cups of water, because water is much heavier than flour for the same volume.)

Q: An American recipe uses 1 tablespoon of salt. You only have an Australian tablespoon. What should you use?
- 1 Australian tablespoon
- 2 Australian tablespoons
- 4 teaspoons
* 3 teaspoons
Explanation: A US tablespoon is 15 mL, or 3 teaspoons. An Australian tablespoon is 20 mL, which would add a third too much salt. Three 5 mL teaspoons gives exactly 15 mL.

Q: A soup recipe serves 4 and uses 6 cups of stock. How much stock do you need to serve 10 people?
- 12 cups
* 15 cups
- 10 cups
- 24 cups
Explanation: Scale factor = 10 ÷ 4 = 2.5. Then 6 cups × 2.5 = 15 cups.
"""

LENGTH_WEIGHT = """
GOAL: Switch between metric and imperial units for height, weight and distance, quickly in your head or exactly with a calculator.

WHY THIS MATTERS
Most of the world uses the metric system (metres, kilograms), but the United States uses imperial units (feet, pounds, miles), and the UK uses a mix: road signs in miles, body weight often in stones. Online shopping, travel, job forms, medical forms and sports all make you switch between the two.

KEY WORDS
- Metric system: millimetres (mm), centimetres (cm), metres (m), kilometres (km), grams (g) and kilograms (kg). Every step is a multiple of 10.
- Imperial system: inches (in), feet (ft), yards (yd), miles (mi), ounces (oz), pounds (lb) and stones (st).
- Conversion factor: the number you multiply or divide by to change units.

METRIC STEPS: JUST MOVE THE DECIMAL POINT
- 10 mm = 1 cm
- 100 cm = 1 m
- 1,000 m = 1 km
- 1,000 g = 1 kg
Example: 2.5 m = 250 cm. And 750 g = 0.75 kg.

THE KEY CONVERSION FACTORS
Length and height:
- 1 inch = 2.54 cm (exactly)
- 1 foot = 12 inches = 30.48 cm
- 1 metre = about 3.28 feet, or 39.4 inches
- 1 yard = 3 feet = 0.91 m

Distance:
- 1 mile = 1.609 km
- 1 km = 0.621 miles

Weight:
- 1 kg = 2.205 lb
- 1 lb = 0.454 kg
- 1 stone = 14 lb = 6.35 kg

WHICH WAY DO I MULTIPLY OR DIVIDE
A simple check: when you change to a smaller unit, you get a bigger number. Centimetres are smaller than inches, so inches to centimetres means the number gets bigger: multiply by 2.54. Centimetres to inches means the number gets smaller: divide by 2.54.

QUICK MENTAL ESTIMATES
- Kilograms to pounds: double it and add 10%. 70 kg → 140 + 14 = 154 lb (exact: 154.3 lb).
- Pounds to kilograms: halve it and take off 10%. 200 lb → 100 − 10 = 90 kg (exact: 90.7 kg).
- Miles to kilometres: multiply by 1.6. 50 miles → 80 km.
- Kilometres to miles: multiply by 0.6. 100 km → 60 miles (exact: 62.1 miles).
- Handy pairs to remember: 5 miles ≈ 8 km, and 8 miles ≈ 13 km.

HEIGHT: FEET AND INCHES TO CENTIMETRES
1. Turn everything into inches: feet × 12, plus the extra inches.
2. Multiply by 2.54.
Example: 5 feet 10 inches = (5 × 12) + 10 = 70 inches. Then 70 × 2.54 = 177.8 cm, so about 178 cm.

Going back: 165 cm ÷ 2.54 = 65 inches. Then 65 ÷ 12 = 5 remainder 5, so 5 feet 5 inches.

SPEED
- 100 km/h = about 62 mph
- 60 mph = about 97 km/h
- Speed conversions use the same factors as distance: multiply mph by 1.609 to get km/h.

THE CONVERSION-FACTOR METHOD (FOR TRICKY CHAINS)
Write each conversion as a fraction that equals 1, then multiply. Units on the top and bottom cancel out, so you can check you haven't flipped anything.
Example: how many centimetres in 3 yards?
- 3 yards × (3 feet ÷ 1 yard) = 9 feet
- 9 feet × (12 inches ÷ 1 foot) = 108 inches
- 108 inches × (2.54 cm ÷ 1 inch) = 274.32 cm

REAL-LIFE CASE STUDY: DAVID FILLS IN A VISA MEDICAL FORM
The form asks for height in centimetres and weight in kilograms. David knows he is 6 feet 1 inch and 185 lb.
- Height: (6 × 12) + 1 = 73 inches. Then 73 × 2.54 = 185.4 cm, so he writes 185 cm.
- Weight: 185 × 0.454 = 84 kg (exact: 83.9 kg).
Funny coincidence: his height in centimetres and his weight in pounds are both about 185.

PRACTICE
Complete the sentences.
1. One foot is ___ inches.
2. One inch is ___ cm.
3. One stone is ___ pounds.
4. A distance of 50 miles is about ___ km.
5. One metre is ___ cm.

ANSWERS: 1. 12  2. 2.54  3. 14  4. 80  5. 100

QUIZ: Check Your Understanding
Q: Someone is 5 feet 8 inches tall. What is that in centimetres, to the nearest whole number?
- 147 cm
* 173 cm
- 177 cm
- 158 cm
Explanation: 5 feet 8 inches = (5 × 12) + 8 = 68 inches. Then 68 × 2.54 = 172.7 cm, which rounds to 173 cm. (177 cm comes from mistakenly treating "5 feet 8" as 5.8 feet, and 147 cm from treating it as 58 inches.)

Q: A suitcase limit is 23 kg. Roughly what is that in pounds?
- 10 lb
- 46 lb
* 51 lb
- 32 lb
Explanation: Double 23 kg to get 46, then add 10% (4.6) to get about 51 lb. The exact answer is 23 × 2.205 = 50.7 lb. (46 is a common answer from doubling only.)

Q: A road sign in the UK says 30 miles. About how far is that in kilometres?
- 19 km
- 30 km
- 36 km
* 48 km
Explanation: Multiply miles by 1.6: 30 × 1.6 = 48 km (exact: 48.3 km). Miles are longer than kilometres, so the number of kilometres must be bigger. (19 km comes from multiplying by 0.621, which is the factor for going the other way, from km to miles.)

Q: A TV screen is 55 inches across. How many centimetres is that?
* About 140 cm
- About 22 cm
- About 55 cm
- About 110 cm
Explanation: Inches to centimetres means multiply by 2.54: 55 × 2.54 = 139.7 cm. Centimetres are smaller than inches, so the number gets bigger. (22 cm comes from dividing instead of multiplying.)

Q: A friend says they weigh 11 stone. How much is that in kilograms?
- About 50 kg
- About 64 kg
* About 70 kg
- About 154 kg
Explanation: 11 stone × 14 = 154 lb, and 154 × 0.454 = 69.9 kg, so about 70 kg. (154 is the weight in pounds, not kilograms.)
"""

TEMP_TIME = """
GOAL: Convert Celsius and Fahrenheit, and answer everyday time questions like how many weeks are in a year or seconds in a day.

WHY THIS MATTERS
Weather apps, oven dials, thermometers and recipes may use Celsius or Fahrenheit depending on where they come from. And questions like "how many weeks are in a year?" are among the most searched maths questions on the internet. Knowing how to work them out means you never have to look them up again.

KEY WORDS
- Celsius (°C): water freezes at 0 °C and boils at 100 °C. Used in most countries.
- Fahrenheit (°F): water freezes at 32 °F and boils at 212 °F. Used mainly in the United States.
- Leap year: a year with 366 days instead of 365. February gets an extra day, the 29th.

CELSIUS TO FAHRENHEIT
Formula: °F = (°C × 9 ÷ 5) + 32
You can use 1.8 instead of 9 ÷ 5.
Example: 25 °C → 25 × 1.8 = 45, then 45 + 32 = 77 °F.

FAHRENHEIT TO CELSIUS
Formula: °C = (°F − 32) × 5 ÷ 9
Example: 86 °F → 86 − 32 = 54, then 54 × 5 ÷ 9 = 30 °C.
Order matters: always subtract 32 first.

QUICK ESTIMATE: DOUBLE AND ADD 30
- Celsius to Fahrenheit: double it, then add 30. 20 °C → 40 + 30 = 70 °F (exact: 68 °F).
- Fahrenheit to Celsius: take away 30, then halve it. 80 °F → 50 ÷ 2 = 25 °C (exact: 26.7 °C).
This is close for everyday weather, but not accurate enough for cooking or a fever.

TEMPERATURES WORTH KNOWING
- 0 °C = 32 °F: water freezes
- 20 °C = 68 °F: a comfortable room
- 30 °C = 86 °F: a hot day
- 37 °C = 98.6 °F: normal body temperature
- 38 °C = 100.4 °F: a fever, generally
- 100 °C = 212 °F: water boils
- 180 °C = 356 °F: a moderate oven (recipes usually round this to 350 °F)
- −40 °C = −40 °F: the one temperature where both scales match

TIME FACTS PEOPLE SEARCH FOR
- 60 seconds = 1 minute, and 60 minutes = 1 hour
- 1 day = 24 hours = 1,440 minutes = 86,400 seconds
- 1 week = 7 days = 168 hours
- 1 year = 365 days (366 in a leap year)
- Weeks in a year: 365 ÷ 7 = 52 weeks and 1 day (52 weeks and 2 days in a leap year)
- Weeks in a month: on average 52 ÷ 12, which is about 4.3 weeks. A month is never exactly 4 weeks, except February in a normal year.
- Hours in a year: 365 × 24 = 8,760
- Seconds in a year: 365 × 86,400 = 31,536,000

LEAP YEARS
A year is a leap year if it can be divided by 4, for example 2024 and 2028. The exception: years ending in 00 are only leap years if they can be divided by 400. So 2000 was a leap year, but 1900 was not.

USING THIS AT WORK: WEEKLY, FORTNIGHTLY AND MONTHLY PAY
- Weekly to yearly: multiply by 52.
- Fortnightly to yearly: multiply by 26.
- Monthly to yearly: multiply by 12.
- Yearly to weekly: divide by 52.
Example: a rent of $400 a week is 400 × 52 = $20,800 a year. Divided by 12, that's about $1,733 a month, not $1,600. Using "4 weeks in a month" makes monthly costs look lower than they really are.

REAL-LIFE CASE STUDY: MARIA CHECKS HER CHILD'S TEMPERATURE
Maria's thermometer was bought in the United States and shows 101.3 °F. Her doctor's advice sheet says to call if a child's temperature is above 38.5 °C.
- 101.3 − 32 = 69.3
- 69.3 × 5 ÷ 9 = 38.5 °C
Her child's temperature is right at the level on the sheet, so she calls the doctor for advice. The quick "take away 30 and halve" estimate gives 35.7 °C, which would have been badly wrong here. For health and cooking, always use the exact formula.

PRACTICE
Complete the sentences.
1. Water freezes at 0 °C, which is ___ °F.
2. Water boils at 100 °C, which is ___ °F.
3. One day has ___ hours.
4. A normal year has 52 weeks and ___ day.
5. A leap year has ___ days.

ANSWERS: 1. 32  2. 212  3. 24  4. one  5. 366

QUIZ: Check Your Understanding
Q: The weather forecast says 35 °C. What is that in Fahrenheit?
- 67 °F
- 63 °F
* 95 °F
- 85 °F
Explanation: 35 × 1.8 = 63, then 63 + 32 = 95 °F. (63 °F is what you get if you forget to add 32, and 67 °F comes from adding 32 without multiplying.)

Q: An American recipe says to bake at 400 °F. What is that in Celsius, roughly?
* About 200 °C
- About 368 °C
- About 222 °C
- About 180 °C
Explanation: 400 − 32 = 368, then 368 × 5 ÷ 9 = 204 °C, so set the oven to about 200 °C. (222 °C comes from multiplying by 5 ÷ 9 without subtracting 32 first, and 368 °C from subtracting 32 but not multiplying. Always subtract first, then multiply.)

Q: How many weeks are in a normal (non-leap) year?
- Exactly 52 weeks
- 48 weeks
- 50 weeks
* 52 weeks and 1 day
Explanation: 365 ÷ 7 = 52 remainder 1, so a year is 52 weeks and 1 day. That extra day is why your birthday moves one day of the week later each year (two days after a 29 February).

Q: How many seconds are in one day?
- 3,600
- 1,440
* 86,400
- 8,760
Explanation: 24 hours × 60 minutes × 60 seconds = 86,400 seconds. (3,600 is the number of seconds in an hour, 1,440 is minutes in a day, and 8,760 is hours in a year.)

Q: Your rent is $350 a week. What is it per month on average?
- $1,400
* About $1,517
- $1,050
- About $1,750
Explanation: First find the yearly rent: $350 × 52 = $18,200. Then divide by 12 months: $18,200 ÷ 12 ≈ $1,517. Using 4 weeks a month gives $1,400, which is too low, because most months are longer than 4 weeks.
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
    (
        "Module 2: Measurements and Conversions",
        True,
        [
            ("cooking-measurement-conversions", "Cooking Conversions: Cups, Tablespoons, Grams and Ounces", KITCHEN),
            ("metric-imperial-conversions", "Metric and Imperial: Height, Weight and Distance", LENGTH_WEIGHT),
            ("temperature-and-time-conversions", "Celsius, Fahrenheit and Everyday Time Calculations", TEMP_TIME),
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
