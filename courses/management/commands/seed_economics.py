"""
Seed the "Economics and Money Made Simple" course.

Run with:  python manage.py seed_economics

Safe to run more than once (updates instead of duplicating). Every module is
free. Each lesson has picture DIAGRAMs, a drag-and-drop PRACTICE and a
multiple-choice QUIZ ("Check Your Understanding"); see courses/lesson_format.py.

Sources: Bank of England, "Money creation in the modern economy" (2014);
Pew Research Center middle-income definition (2023 data); African Development
Bank, "The Middle of the Pyramid" (2011); IMF projections reported by Eye Radio
(South Sudan inflation, 2025). Re-check current figures before major updates.

Writing rules for this file (so the lesson parser reads it correctly):
- A line written entirely in capitals (before any colon) becomes a heading,
  so start ordinary lines with a normal word, never an all-caps abbreviation.
  Headings can't end in "?" unless the question is after a colon.
- A DIAGRAM's caption is every line until the next heading, so always put a
  heading straight after the caption.
- PRACTICE answers must be short and contain no "/".
- In PRACTICE and ANSWERS, never write a number followed by ". ".
"""
from django.core.management.base import BaseCommand

from courses.seeding import seed_course

COURSE = {
    "slug": "economics-and-money",
    "title": "Economics and Money Made Simple",
    "description": (
        "How money really works, explained in plain language with pictures: how "
        "money flows round the economy, where new money comes from, what inflation "
        "does to your wages and savings, what working, middle and upper class mean, "
        "and how to make a budget that works. Free for everyone."
    ),
}

CIRCULATION = """
GOAL: Understand how money moves between households, businesses, banks and the government, and why one person's spending is another person's income.

WHY THIS MATTERS
Have you noticed that when a big mine opens or a factory closes, the whole town feels it, from the market sellers to the bus drivers? That's because money flows in a circle. Every shilling, pound or dollar you spend becomes someone else's income, and they spend it again. Understanding this flow explains why recessions spread, why governments spend money to help the economy, and why buying local helps your community.

KEY WORDS
- Economy: all the buying, selling, making and working that happens in a place.
- Household: a person or family that earns income and spends it.
- Business (firm): an organisation that makes goods or provides services to sell.
- Income: money you receive, such as wages, profits or rent.
- Goods and services: things you can buy. Goods are objects (rice, phones); services are work done for you (a haircut, a bus ride).

THE CIRCULAR FLOW
The simplest picture of an economy has two groups:
1. Households work for businesses, and businesses pay them wages.
2. Households spend those wages buying goods and services from businesses.
3. Businesses use that money to pay wages again, and the circle continues.

DIAGRAM: circular-flow
Money flows in a circle. Households spend money at businesses, and businesses pay wages to households. Banks keep savings and make loans, and the government collects taxes and pays for services.

MONEY LEAVING AND JOINING THE CIRCLE
Real economies are more complicated. Some money leaves the circle, and some joins it.
Money leaves the circle when people:
- Save it in a bank or under the mattress instead of spending it.
- Pay taxes to the government.
- Buy imported goods, because the money goes to businesses in another country.
Money joins the circle when:
- Banks lend money to businesses and households to spend or invest.
- The government spends on roads, schools, hospitals and salaries.
- People in other countries buy our exports, such as oil, gold, coffee or cattle.
If more money joins than leaves, the economy grows. If more leaves than joins, the economy shrinks.

THE MULTIPLIER: WHY SPENDING SPREADS
Imagine a new road project pays a builder $100. The builder spends $80 of it at the market and saves $20. The market seller then spends $64 of that $80 on school fees and saves $16. The school spends $51.20 on salaries, and so on.
Each time, the money keeps moving, a little smaller each round. Add up all the rounds, and that first $100 creates about $500 of spending in total.
Quick formula: total spending = first amount ÷ (the part each person saves)
- Here each person saves 20%, or 0.2. So $100 ÷ 0.2 = $500.
This is called the multiplier. It works in reverse too: when a big employer closes, the loss of spending spreads through the whole community.

WHY BUYING LOCAL HELPS
When you buy tomatoes from a local farmer, the money stays in your area: the farmer pays a local worker, who buys bread from a local baker. When you buy imported goods, much of the money leaves the country. Imports are not bad, since they bring things we can't make ourselves, but local spending keeps more money circulating at home.

REAL-LIFE CASE STUDY: THE GOLD MINE TOWN
When a new gold mine opened near a small town, it hired 300 local workers. Those workers spent their wages in town. Food sellers and shops had more customers, so they hired helpers. Bus companies added routes to take workers to the mine. New guesthouses opened for visitors. A few years later, gold prices fell and the mine cut half its workers. Within months, shops lost customers, some guesthouses closed, and the bus company cut routes, even though none of them worked at the mine. This is the circular flow and the multiplier in action, both on the way up and on the way down.

PRACTICE
Complete the sentences.
1. Businesses pay households ___ for their work.
2. Money you put aside instead of spending is called ___.
3. Goods bought from another country are called ___.
4. Goods sold to another country are called ___.
5. One person's spending is another person's ___.

ANSWERS: 1. wages  2. savings  3. imports  4. exports  5. income

QUIZ: Check Your Understanding
Q: In the simple circular flow, what do households give businesses?
- Taxes and loans
* Work, and money spent on goods and services
- Only savings
- Imports and exports
Explanation: Households work for businesses (earning wages) and then spend that money buying goods and services from businesses, which keeps the money flowing in a circle.

Q: Which of these takes money out of the local circular flow?
- The government building a new school
- A bank lending to a small business
* A family saving money under the mattress
- A foreign company buying local coffee
Explanation: Money that is saved and not spent or lent leaves the circle. Government spending, bank loans and exports all add money to the circle.

Q: A road project pays a worker $1,000. Everyone who receives the money spends 75% of it and saves 25%. About how much total spending does the first $1,000 create?
- $1,750
- $1,250
* $4,000
- $750
Explanation: Use the multiplier: first amount ÷ the part saved. $1,000 ÷ 0.25 = $4,000. Each round of spending is smaller, but together they add up to four times the original amount.

Q: A large factory closes. Why do shops in the town also lose business?
* The factory workers lose their wages and spend less in the shops
- Shops have to pay the factory's debts
- The government closes the shops too
- Shops only sell to factories
Explanation: One person's spending is another's income. When workers lose their wages, they spend less, so shop owners earn less and may cut their own staff, spreading the effect.

Q: Why does buying from local producers help a community's economy?
- Local goods are always cheaper
- It stops the government collecting taxes
* More of the money stays in the area and is spent again locally
- It increases imports
Explanation: When money goes to local producers, they pay local workers and suppliers, so it keeps circulating nearby. Money spent on imports mostly leaves the area.
"""

MONEY_CREATION = """
GOAL: Learn where new money really comes from: the central bank, which issues notes and coins and sets interest rates, and commercial banks, which create most money when they lend.

WHY THIS MATTERS
Many people think banks lend out money that other customers have saved. That's only part of the story. In modern economies, most new money is created by ordinary commercial banks every time they make a loan. Understanding this explains how interest rates affect your loans and why printing too much money causes prices to rise.

KEY WORDS
- Central bank: the country's main bank, owned by the government, which issues the currency and manages the money supply. Examples: the Bank of South Sudan, the Bank of Uganda, the Central Bank of Kenya and the Reserve Bank of Australia.
- Commercial bank: an ordinary bank where people and businesses keep accounts and borrow money.
- Deposit: money held in your bank account.
- Loan: money you borrow and must pay back, usually with interest.
- Interest rate: the price of borrowing money, shown as a percentage per year.

TWO KINDS OF MONEY
Most money isn't cash at all.
- Cash: notes and coins, issued by the central bank. In a country like the United Kingdom, this is only about 3% of the money people hold.
- Bank deposits: the numbers in bank accounts. About 97% of money in the UK is this kind of money.
Mobile money balances, such as M-Pesa, are backed by real money held in banks, so they move existing money around quickly rather than creating new money.

WHAT THE CENTRAL BANK DOES
1. Issues the currency. It decides how many notes and coins to put into circulation.
2. Sets the main interest rate. This affects how expensive it is for banks, and so for you, to borrow money.
3. Acts as the bank for banks. Commercial banks keep accounts at the central bank and can borrow from it in an emergency.
4. Keeps prices stable. Many central banks aim to keep inflation low and steady, for example around 2% to 3% a year.

HOW COMMERCIAL BANKS CREATE MONEY
Here's the surprising part. When a bank lends you money, it doesn't take cash out of a vault or out of someone else's account. It simply adds the amount to your account. The Bank of England puts it this way: whenever a bank makes a loan, it creates a matching deposit in the borrower's account.
Example: Amina borrows $1,000 from her bank to buy a sewing machine.
1. The bank writes down a loan: Amina owes the bank $1,000.
2. At the same moment, it types $1,000 into Amina's account. That $1,000 didn't exist before. It is new money.
3. Amina pays the seller, and the money moves into the seller's bank account. It keeps circulating.
4. When Amina pays the loan back, the money is cancelled and disappears from the economy.

DIAGRAM: money-creation
The central bank prints notes and coins, about 3 percent of money, and sets interest rates. Commercial banks create about 97 percent of money by making loans. When a bank lends, it creates a new deposit. When the loan is repaid, that money disappears.

WHAT STOPS BANKS CREATING UNLIMITED MONEY
- Banks must lend to people who can pay them back, or they lose money.
- Rules from the central bank require banks to hold enough of their own funds to cover losses.
- The central bank's interest rate: when it raises rates, loans cost more, so people borrow less and less new money is created.
- People must actually want to borrow.

WHEN GOVERNMENTS PRINT TOO MUCH MONEY
If a government pays its bills by creating huge amounts of new money, without more goods being produced, there is more money chasing the same amount of goods. Prices shoot up. In Zimbabwe in 2008, prices were doubling roughly every day at the worst point, and the central bank issued a 100 trillion dollar note that couldn't buy a loaf of bread for long. You'll learn more about this in the next lesson on inflation.

REAL-LIFE CASE STUDY: JOSEPH'S BUSINESS LOAN
Joseph runs a small bakery and wants a second oven costing $3,000. The bank checks his business records and agrees to lend him the money at 18% interest per year. It adds $3,000 to his account, which is new money. Joseph pays the oven supplier, who pays her workers, who spend at the market. Joseph's bakery now makes twice as much bread, so he hires a helper. A year later, the central bank raises its interest rate because prices are rising fast. Joseph's bank raises his loan rate too, so his monthly repayments go up. He decides not to borrow for a third oven yet. This shows how central bank decisions travel through commercial banks to ordinary businesses.

PRACTICE
Complete the sentences.
1. Notes and coins are issued by the ___ bank.
2. When a bank makes a loan, it creates a new ___ in the borrower's account.
3. Most money today is bank deposits, not ___.
4. The price of borrowing money is the interest ___.
5. When a loan is paid back, that money ___.

ANSWERS: 1. central  2. deposit  3. cash  4. rate  5. disappears

QUIZ: Check Your Understanding
Q: Who issues a country's banknotes and coins?
- Commercial banks
- Mobile money companies
* The central bank
- Large businesses
Explanation: The central bank, such as the Bank of South Sudan or the Bank of Uganda, issues the national currency. Commercial banks hand out cash, but they don't issue it.

Q: When a commercial bank gives Amina a $1,000 loan, where does the money in her account come from?
- From a pile of cash in the bank vault
- From another customer's savings account, which goes down by $1,000
* The bank creates it as a new deposit when it makes the loan
- From the government's tax money
Explanation: As the Bank of England explains, a bank creates a matching deposit when it makes a loan. The $1,000 is new money that didn't exist before.

Q: In a modern economy like the UK's, roughly what share of money is notes and coins?
* About 3%
- About 50%
- About 75%
- About 97%
Explanation: About 97% of money is bank deposits, the numbers in accounts. Notes and coins are only about 3%.

Q: The central bank raises its main interest rate. What is the most likely effect?
- Loans become cheaper, so people borrow more
- Banks must give away free money
- Prices immediately fall by half
* Loans become more expensive, so people borrow less and less new money is created
Explanation: Higher interest rates make borrowing cost more, so fewer loans are made. Fewer loans means less new money, which helps slow down rising prices.

Q: What usually happens if a government prints huge amounts of money to pay its bills, without more goods being produced?
- Everyone becomes richer
* Prices rise quickly, because more money is chasing the same goods
- The currency becomes more valuable
- Banks stop lending forever
Explanation: More money with the same amount of goods means each note buys less. This is what happened in Zimbabwe in 2008, when prices doubled roughly every day at the worst point.
"""

INFLATION = """
GOAL: Understand what inflation is, how it's measured, what causes it, and how it shrinks the value of your wages and savings.

WHY THIS MATTERS
Have you heard someone say "when I was young, a loaf of bread cost just a few coins"? That's inflation: prices going up over time, so the same money buys less. Low, steady inflation is normal. But when inflation is high, families struggle to afford food and rent, and savings lose value fast. In 2025, South Sudan's inflation was close to 100%, according to IMF projections reported in the local media, meaning prices were roughly doubling in a year.

KEY WORDS
- Inflation: a general rise in prices over time.
- Inflation rate: how fast prices are rising, as a percentage per year.
- Purchasing power: how much your money can buy.
- Consumer price index (CPI): a measure of the price of a "basket" of things households usually buy.
- Deflation: when prices fall over time (rare).

HOW INFLATION IS MEASURED
Government statisticians track the prices of a typical "basket" of things households buy: food, fuel, rent, transport, clothes, school fees and so on. They compare the cost of the same basket each month or year.
Formula: inflation rate = (new price − old price) ÷ old price × 100
Example: the basket cost 10,000 last year and costs 10,800 this year.
- Increase: 10,800 − 10,000 = 800
- 800 ÷ 10,000 = 0.08
- 0.08 × 100 = 8% inflation

DIAGRAM: inflation-basket
Inflation means the same money buys less. In year 1, 100 dollars buys 8 items. In year 2, it buys 6 items. In year 3, only 4 items. When prices go up, each note is worth less.

WHAT CAUSES INFLATION
- Too much money: if the amount of money grows faster than the goods being produced, prices rise. This is the main cause of very high inflation.
- Rising costs: when fuel, transport or imported goods get more expensive, businesses raise their prices to cover their costs.
- Strong demand: when lots of people want to buy more than businesses can produce, sellers can raise prices.
- A falling currency: if your currency loses value against the US dollar, imported goods such as fuel, medicine and cooking oil cost more. This is a big cause of inflation in countries that import much of what they use, such as South Sudan.

HOW INFLATION AFFECTS YOU
Your savings lose value. If you keep $100 at home and prices rise by 10% in a year, it will only buy about what $91 bought last year ($100 ÷ 1.10 = $90.91).

Your wages may fall in real terms. If your pay rises by 5% but prices rise by 8%, you can actually buy about 3% less than last year. Economists call this a fall in your "real wage".

DIAGRAM: real-wage
If your pay rises 5 percent but prices rise 8 percent, your money buys about 3 percent less than last year. A pay rise smaller than inflation is really a pay cut.

People on fixed incomes, such as pensioners, are hurt most, because their income doesn't rise with prices. People who owe money can benefit a little, because they repay with money that's worth less, but lenders usually raise interest rates to make up for it.

THE RULE OF 70
To estimate how many years it takes for prices to double, divide 70 by the inflation rate.
- At 7% inflation: 70 ÷ 7 = 10 years for prices to double.
- At 2% inflation: 70 ÷ 2 = 35 years.
- At 35% inflation: 70 ÷ 35 = 2 years.
At close to 100% a year, as in South Sudan in 2025, prices roughly double within a single year.

WAYS FAMILIES PROTECT THEMSELVES
These are common approaches people use. They aren't personal financial advice, and the right choice depends on your situation.
- Keep savings in an account that pays interest, ideally at a rate close to or above inflation, rather than as cash at home.
- When inflation is high, avoid holding large amounts of a fast-falling currency for long. Some families buy useful goods they'll need anyway, such as bags of grain, when prices are lower.
- Ask for pay rises that keep up with inflation, and compare your pay rise with the inflation rate.
- Be careful with loans: when inflation is high, interest rates often rise too.

REAL-LIFE CASE STUDY: GRACE'S SCHOOL FEES
Grace sells vegetables at a market. Last year she saved 120,000 at home to pay her daughter's school fees this year. But during the year, prices rose by 40%, and the school raised its fees by the same amount. The fees, which were 120,000, are now 120,000 × 1.4 = 168,000. Grace's savings didn't grow at all, so she is 48,000 short.
Her neighbour Mary saved the same amount in a savings group that paid interest and bought two bags of seed early in the year, before prices rose. When she planted and sold her crop, her income kept up better with rising prices.
The lesson: in times of high inflation, money kept as cash at home loses value quickly.

PRACTICE
Complete the sentences.
1. A general rise in prices over time is called ___.
2. How much your money can buy is its purchasing ___.
3. Prices rising from 100 to 110 is an inflation rate of ___ percent.
4. When prices fall over time, it is called ___.
5. To estimate how long prices take to double, divide ___ by the inflation rate.

ANSWERS: 1. inflation  2. power  3. ten  4. deflation  5. seventy

QUIZ: Check Your Understanding
Q: A bag of rice cost 2,000 last year and costs 2,500 this year. What is the rate of inflation for rice?
- 20%
* 25%
- 50%
- 5%
Explanation: The increase is 500. Then 500 ÷ 2,000 = 0.25, and 0.25 × 100 = 25%. Always divide by the old price, not the new one. (Dividing by 2,500 gives the wrong answer of 20%.)

Q: Your pay goes up by 4%, but inflation is 10%. What has happened to your real wage?
- It went up by 4%
- It went up by 14%
* It went down, because prices rose faster than your pay
- It stayed the same
Explanation: Prices rose 10% while your pay rose only 4%, so you can buy about 6% less than before. A pay rise smaller than inflation is really a pay cut.

Q: Who is usually hurt most by high inflation?
- People whose wages rise faster than prices
* People who keep their savings as cash and people on fixed incomes, like pensioners
- People who own lots of goods that are rising in price
- Nobody is affected
Explanation: Cash savings and fixed incomes don't grow when prices rise, so they buy less and less. That's why high inflation is especially hard on savers and retired people.

Q: Using the rule of 70, how long would it take prices to double at 5% inflation per year?
- 5 years
- 7 years
- 35 years
* 14 years
Explanation: Divide 70 by the inflation rate: 70 ÷ 5 = 14 years.

Q: South Sudan imports much of its fuel, food and medicine. Why does a falling South Sudanese pound make prices rise?
* Imported goods are priced in foreign currency, so they cost more pounds when the pound loses value
- A falling currency makes local farmers grow less
- Shops are not allowed to change prices
- It has no effect on prices
Explanation: Imports are paid for in currencies like the US dollar. When the local currency is worth less, it takes more pounds to buy the same dollar's worth of goods, so prices in the shops go up.
"""

SOCIAL_CLASS = """
GOAL: Understand what people mean by working class, middle class and upper class, the different ways class is measured, and why the definitions vary between countries.

WHY THIS MATTERS
You'll hear politicians promise to help "the middle class" and news stories about "the working class". But what do these words actually mean? There isn't one official definition. Economists, sociologists and governments measure class in different ways: by income, by type of job, by wealth or by education. Understanding these helps you make sense of the news and of debates about fairness and opportunity.

KEY WORDS
- Social class: a group of people with a similar economic and social position in society.
- Income: money received regularly, such as wages, salary, profits or rent.
- Wealth: the total value of what you own, such as land, houses, savings, livestock and businesses, minus what you owe.
- Wage: pay usually calculated by the hour, day or week, often for manual or service work.
- Salary: a fixed yearly amount paid in regular instalments, often for professional jobs.
- Social mobility: moving between classes, for example a child of farm workers becoming a doctor.

THREE CLASSES: THE COMMON DEFINITIONS
Working class: people who earn their living mainly from wages, often in manual, routine or service jobs such as farm work, factory work, construction, cleaning, driving or shop work. They usually have limited savings and own little property, so losing a job can quickly cause hardship.
Middle class: people in professional, managerial, technical or skilled jobs, such as teachers, nurses, engineers, office managers and many small-business owners. They often have a salary, some savings, more education and may own a home with a loan.
Upper class: people whose income comes mainly from wealth rather than work, such as owning land, large businesses, property or investments. Their wealth is often inherited and passed down through families. Very high earners such as top executives are sometimes included.

DIAGRAM: class-ladder
A simple guide to social class. The upper class lives mainly on wealth, such as land, businesses and investments. The middle class has professional, managerial or skilled jobs and some savings. The working class earns wages from manual, routine or service work, with little savings or property.

WAY 1: CLASS BY INCOME
Many researchers group households by income compared with the typical (median) household in their country.
- The Pew Research Center in the United States calls a household "middle income" if it earns between two-thirds and double the national median income, adjusted for household size. By that measure, about half of US households (51%) were middle income in 2023, about 30% lower income and 19% upper income.
- The African Development Bank used a different measure for Africa: people spending between $2 and $20 a day. By that definition, about 34% of Africans, or 313 million people, were middle class in 2010. The bank pointed out that many people at the bottom of that range, spending $2 to $4 a day, could easily fall back into poverty.
This shows why "middle class" means very different things in different countries.

WAY 2: CLASS BY JOB AND WEALTH
Some researchers focus on the type of work people do and whether they own things that produce income:
- The philosopher Karl Marx divided society mainly into those who own businesses, land and factories, and those who sell their labour for wages.
- The sociologist Max Weber argued class also depends on skills and qualifications, and that social status and political power matter too.
- A large British study in 2013, the Great British Class Survey, used income, wealth, social connections and cultural activities and found seven classes, from an "elite" at the top to a "precariat" of people with insecure work and low income at the bottom.

WHY CLASS IS DIFFERENT IN EACH COUNTRY
A teacher in Juba and a teacher in Sydney may both feel middle class, but their incomes are very different. Class depends on how your income and lifestyle compare with others around you, not on a single number for the whole world. In many African countries, people also mix sources of income: a civil servant may also farm, keep cattle and run a small shop, which makes simple labels harder to apply.

SOCIAL MOBILITY
Social mobility means moving up or down between classes, within your life or across generations. Things that often help people move up include education and training, access to loans to start a business, good health, and fair access to jobs. Things that can push people down include job loss, illness, conflict, and high inflation that wipes out savings. How easy it is to move between classes is a big topic of political debate in many countries.

REAL-LIFE CASE STUDY: THREE GENERATIONS OF ONE FAMILY
Deng's grandfather was a cattle keeper and farm labourer who never went to school. He earned little money but owned some cattle. Deng's mother finished secondary school and became a nurse with a regular salary. She saved enough to build a small brick house. Deng studied engineering at university and now works for a construction company, earning a good salary, and he has bought land outside the city. In two generations, the family moved from what many would call working class into the middle class, mainly through education and steady saving. But Deng knows that if he lost his job or fell ill, his family could lose their position, which is why he keeps an emergency fund.

PRACTICE
Complete the sentences.
1. Everything you own, minus what you owe, is your ___.
2. People whose income comes mainly from owning land and businesses are usually called upper ___.
3. A fixed yearly amount paid for professional work is called a ___.
4. Moving between social classes is called social ___.
5. The middle of all incomes in a country is called the ___ income.

ANSWERS: 1. wealth  2. class  3. salary  4. mobility  5. median

QUIZ: Check Your Understanding
Q: What is the main difference between income and wealth?
- They mean the same thing
* Income is money you receive regularly; wealth is the value of everything you own minus what you owe
- Wealth is only money in the bank
- Income only comes from owning land
Explanation: Income is a flow of money, like wages or rent. Wealth is a stock of things you own, like land, houses, savings and livestock, minus your debts.

Q: Which description best matches the common idea of the upper class?
- People who earn hourly wages in manual jobs
- People who work as teachers and nurses
* People whose income comes mainly from owning wealth such as land, businesses or investments, often inherited
- People who have just started their first job
Explanation: The upper class is usually defined by wealth and ownership rather than by work. Teachers and nurses are commonly seen as middle class, and manual wage workers as working class.

Q: How does the Pew Research Center define a middle-income household in the United States?
- Any household that owns a car
- A household earning exactly the median income
* A household earning between two-thirds and double the national median income
- A household with a university graduate
Explanation: Pew uses income compared with the national median, from two-thirds of the median up to double it, adjusted for household size. By this measure, about half of US households were middle income in 2023.

Q: The African Development Bank counted people spending $2 to $20 a day as middle class. What warning did it give?
* Many people at the lower end ($2 to $4 a day) could easily fall back into poverty
- Everyone in that group was rich
- The definition only worked in Europe
- Nobody in Africa was middle class
Explanation: The bank said people spending $2 to $4 a day were vulnerable: a small shock like illness or a bad harvest could push them back into poverty. That's why definitions of class need care.

Q: Why might a teacher in Juba and a teacher in Sydney both be called middle class, even though their incomes are very different?
- Because all teachers in the world earn the same
* Because class depends on how your income, job and lifestyle compare with others in your own country
- Because class is only about the type of building you work in
- Because Juba and Sydney use the same currency
Explanation: Class is relative. It depends on your position compared with others in the same society, not on one worldwide income figure.
"""

BUDGET = """
GOAL: Make a simple monthly budget using the 50/30/20 rule, so you know where your money goes and can start saving.

WHY THIS MATTERS
Many people get to the end of the month and wonder where their money went. A budget is simply a plan for your money. It helps you pay for what you need, avoid debt, and save for emergencies and goals like school fees, a business or a house. "How to make a budget" is one of the most common money questions people search for, and the 50/30/20 rule is one of the easiest places to start.

KEY WORDS
- Budget: a plan for how you will spend and save your income.
- Needs: things you must pay for to live and work, such as rent, food, transport, school fees and bills.
- Wants: things that are nice to have but not essential, such as eating out, new clothes beyond what you need, or entertainment.
- Emergency fund: savings kept aside for unexpected costs, such as illness or job loss.
- Net income: your pay after tax and other deductions, the amount you actually receive.

THE 50/30/20 RULE
Split your net income into three parts:
- 50% for needs
- 30% for wants
- 20% for savings and paying off debt
Example: you take home $1,000 a month.
- Needs: $1,000 × 0.5 = $500
- Wants: $1,000 × 0.3 = $300
- Savings and debt: $1,000 × 0.2 = $200

DIAGRAM: budget-50-30-20
The 50 30 20 budget. Half your income, 50 percent, goes to needs like rent, food and transport. 30 percent goes to wants. 20 percent goes to savings and paying off debt.

MAKE YOUR OWN BUDGET IN 5 STEPS
1. Write down your monthly net income. If your income changes, use a low, typical month.
2. List all your needs and their costs.
3. List your wants and what you usually spend on them.
4. Decide how much you'll save. Treat savings like a bill: put it aside as soon as you're paid.
5. Track your spending for a month, then adjust.

WHEN 50/30/20 DOESN'T FIT
For many families, especially on low incomes or where food and rent are expensive, needs take far more than half. That's normal. Adjust the rule to fit your life:
- A common alternative is 70/20/10: 70% needs, 20% savings and debt, 10% wants.
- Even saving 5% or 10% is a great start. The habit matters more than the exact number.
- Look for the biggest costs first. Saving a little on rent or transport often matters more than cutting small treats.

BUILDING AN EMERGENCY FUND
Aim to save enough to cover about 3 months of your needs. If your needs cost $600 a month, that's $600 × 3 = $1,800. It takes time, so start small. An emergency fund stops one bad month, like a hospital bill or a broken phone, from pushing you into expensive debt.

SAVINGS GROUPS
In many communities, people save together in savings groups, such as village savings and loan associations, where members put in a fixed amount each week and can borrow from the group. They are a good way to save regularly and get small loans without high interest, but choose a group you trust and that keeps clear records.

REAL-LIFE CASE STUDY: PETER'S FIRST BUDGET
Peter, a bus driver, takes home $2,400 a month. Using 50/30/20 as a guide, he aims for $1,200 on needs, $720 on wants and $480 on savings.
When he tracks his spending, he finds his needs are actually $1,500: rent $900, food $400 and transport $200. He's also spending $800 on wants, mostly takeaway meals and phone credit, and saving only $100.
So he adjusts:
- He cooks at home more and switches to a cheaper phone plan, bringing his wants down from $800 to $500.
- That frees up $300, so he now saves $400 a month instead of $100.
His new budget is about 62% needs, 21% wants and 17% savings. It isn't exactly 50/30/20, but it works for him. Within 4 months he has saved $1,600, enough to cover one month of his needs, the first step towards his emergency fund.

PRACTICE
Complete the sentences.
1. In the 50/30/20 rule, half your income goes on ___.
2. Eating out and entertainment are examples of ___.
3. Savings kept for unexpected costs are called an emergency ___.
4. With an income of $1,000, the 20% savings share is $___.
5. A good emergency fund covers about ___ months of needs.

ANSWERS: 1. needs  2. wants  3. fund  4. 200  5. three

QUIZ: Check Your Understanding
Q: You take home $1,500 a month. Using the 50/30/20 rule, how much should go to savings and debt?
- $150
* $300
- $450
- $750
Explanation: 20% of $1,500 is $1,500 × 0.2 = $300. Needs would be $750 (50%) and wants $450 (30%).

Q: Which of these is a need rather than a want?
- A new pair of designer trainers
- Eating at a restaurant every weekend
* Your child's school fees
- A streaming subscription
Explanation: Needs are costs you must pay to live and work, such as rent, food, transport and school fees. The others are wants: nice to have, but not essential.

Q: Your needs cost $800 a month. How much should your emergency fund be, using the 3-month guide?
- $800
- $1,600
- $3,200
* $2,400
Explanation: 3 months × $800 = $2,400. This covers essential costs if you lose income or face an unexpected bill.

Q: Your rent and food already take 70% of your income. What's the best approach?
- Give up on budgeting because the rule doesn't fit
* Adjust the rule, for example 70/20/10, and save what you can
- Borrow money to pay for wants
- Stop paying rent
Explanation: The 50/30/20 rule is a guide, not a law. Many families need a different split. Saving even a small amount regularly builds a valuable habit.

Q: When is the best time to put money into savings?
- At the end of the month, if anything is left over
- Only when you get a bonus
* As soon as you're paid, before spending on wants
- Never, because inflation makes saving pointless
Explanation: Paying yourself first means savings actually happen. If you wait until the end of the month, there's often nothing left. And interest-paying savings help protect against inflation.
"""

MODULES = [
    (
        "Module 1: How the Economy Works",
        True,
        [
            ("how-money-circulates-in-the-economy", "How Money Flows Round the Economy", CIRCULATION),
            ("how-money-is-created-central-and-commercial-banks", "Where Money Comes From: Central Banks and Commercial Banks", MONEY_CREATION),
            ("what-is-inflation", "What Is Inflation? How Rising Prices Affect Your Money", INFLATION),
        ],
    ),
    (
        "Module 2: Money, Society and You",
        True,
        [
            ("working-middle-upper-class-explained", "Working Class, Middle Class and Upper Class Explained", SOCIAL_CLASS),
            ("how-to-make-a-budget-50-30-20-rule", "How to Make a Budget: The 50/30/20 Rule", BUDGET),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the 'Economics and Money Made Simple' course (all modules free)."

    def handle(self, *args, **options):
        course, created, lessons = seed_course(COURSE, MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} '{course.title}': {len(MODULES)} modules, {lessons} lessons."
            )
        )
