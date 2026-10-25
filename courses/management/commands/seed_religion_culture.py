"""
Seed the "Religion and Culture in Africa" course.

Run with:  python manage.py seed_religion_culture

Safe to run more than once (updates instead of duplicating). Every module is
free. Each lesson has picture DIAGRAMs, a drag-and-drop PRACTICE and a
multiple-choice QUIZ ("Check Your Understanding"); see courses/lesson_format.py.

Sources: Pew Research Center, "Tolerance and Tension: Islam and Christianity
in Sub-Saharan Africa" (2010; survey of 19 countries, 2008-09); University of
Warsaw "Virtual Nubia" project (Nubian kingdoms); Jesse A. Zink, "Christianity
and Catastrophe in South Sudan" (2018); John S. Mbiti, "African Religions and
Philosophy" (1969).

The essay lesson presents the argument that Christianity and Islam were
imposed on Africa in its strongest form, then the evidence on the other side,
so readers can weigh it for themselves.

Writing rules for this file (so the lesson parser reads it correctly):
- A line written entirely in capitals (before any colon) becomes a heading,
  so start ordinary lines with a normal word, never an all-caps abbreviation
  or a bare date like "AD 640:". Put dates inside bullet lines instead.
- A DIAGRAM's caption is every line until the next heading.
- PRACTICE answers must be short and contain no "/".
- In PRACTICE and ANSWERS, never write a number followed by ". ".
"""
from django.core.management.base import BaseCommand

from courses.seeding import seed_course

COURSE = {
    "slug": "religion-and-culture-in-africa",
    "title": "Religion and Culture in Africa",
    "description": (
        "A respectful look at faith in Africa: the traditional religions that came "
        "first, how Christianity and Islam arrived, the big debate over whether they "
        "were imposed or chosen, and how millions of Africans blend old and new "
        "beliefs today. Based on historical research and large surveys. Free for everyone."
    ),
}

TRADITIONAL = """
GOAL: Understand the main beliefs and practices shared by many African traditional religions, and why they are still important today.

WHY THIS MATTERS
Long before Christianity or Islam reached most of Africa, African peoples had rich religious traditions of their own. They explained where the world came from, how to live well, how to heal the sick and how to stay connected to family members who had died. These traditions were often dismissed by outsiders as "pagan" or "primitive". In fact, they are complex systems of belief that still shape how hundreds of millions of Africans think about life, death, family and community.

KEY WORDS
- Supreme Being: the one great God or creator found in most African traditions.
- Divinities: spirits or lesser gods who look after particular things, such as rain, rivers, a clan or a family.
- Ancestors: family members who have died but are believed to remain part of the family and to watch over the living.
- Diviner: a religious specialist who seeks guidance from the spirit world, to find the cause of problems and how to solve them.
- Oral tradition: knowledge passed down by speaking, through stories, songs, proverbs and rituals, rather than written in books.

THERE ARE MANY TRADITIONS: NOT JUST ONE
Africa has thousands of ethnic groups, and each has its own religious tradition. Scholars talk about "African traditional religions" (plural) because they differ from place to place. Unlike Christianity and Islam, they usually have no single founder and no single holy book. But many share common features.

COMMON FEATURE 1: ONE SUPREME GOD
Most African traditions believe in one Supreme Being who created the world. People often see this God as great and far away, approached through spirits and ancestors rather than directly. Some examples:
- Nhialic among the Dinka of South Sudan
- Kwoth among the Nuer of South Sudan
- Olodumare among the Yoruba of Nigeria
- Ngai among the Kikuyu of Kenya, traditionally associated with Mount Kenya
- Onyame among the Akan of Ghana
- uNkulunkulu among the Zulu of South Africa

COMMON FEATURE 2: SPIRITS AND DIVINITIES
Between God and people are many spirits. Among the Dinka, these are called jak; among the Yoruba, the orisha. Some are linked to forces of nature such as rain, thunder or rivers. Others protect a clan, a place or a family.

COMMON FEATURE 3: THE ANCESTORS
In many African cultures, death does not end a person's place in the family. The Kenyan scholar John Mbiti called the recently dead "the living dead", because they are remembered by name and still thought to be present. Families honour ancestors by pouring drinks or offering food, and ask for their protection and blessing. Ancestors who are respected are believed to protect the family; those who are forgotten may cause trouble.

DIAGRAM: traditional-beliefs
The spiritual world in many African traditions. The Supreme God is at the top, then spirits and divinities, then the ancestors, and the living community at the base. People send prayers and offerings upward and receive protection and blessing in return.

COMMON FEATURE 4: RELIGION IS PART OF EVERYDAY LIFE
In many African languages there is no separate word for "religion", because faith isn't kept to one day a week or one building. It is part of farming, cattle keeping, marriage, naming a baby, healing and leadership. John Mbiti famously wrote that "Africans are notoriously religious", meaning that religion runs through every part of life.

COMMON FEATURE 5: RELIGIOUS SPECIALISTS
Communities have people with special religious roles:
- Diviners, who seek guidance from the spirit world.
- Traditional healers, who use herbs and rituals to treat illness.
- Rain-makers and priests of particular divinities.
- Among the Dinka, "masters of the fishing spear" (bany bith), hereditary spiritual leaders who pray for the community, help settle disputes and lead sacrifices.

COMMON MISUNDERSTANDINGS
- "They had no idea of God." False. Most traditions believe in one Supreme Being.
- "It's all witchcraft." False. Most traditions see harmful witchcraft as evil and something to be protected against.
- "Ancestor veneration is worshipping the dead instead of God." Many believers see it more like showing respect to elders who are still part of the family, while God remains supreme.

REAL-LIFE CASE STUDY: AN OX FOR A WEDDING
Among the Dinka, cattle are at the centre of life, both economically and spiritually. When a marriage is agreed, cattle are given by the groom's family to the bride's family, linking the two families together. On important occasions, such as a serious illness or a time of danger, a family may dedicate or sacrifice an ox, praying to Nhialic and the jak for help. The meat is then shared, so the ritual also brings the community together. Today many Dinka are Christians, yet cattle and their meaning remain central to marriage and family life, a sign of how old and new traditions sit side by side.

PRACTICE
Complete the sentences.
1. The Dinka name for the Supreme God is ___.
2. Family members who have died but are still honoured are called ___.
3. A specialist who seeks guidance from the spirit world is a ___.
4. Knowledge passed down by speaking, not writing, is called ___ tradition.
5. The Yoruba divinities are called the ___.

ANSWERS: 1. Nhialic  2. ancestors  3. diviner  4. oral  5. orisha

QUIZ: Check Your Understanding
Q: Which statement about African traditional religions is most accurate?
- They are all exactly the same across Africa
* There are many traditions, but most share beliefs such as one Supreme God, spirits and ancestors
- They have one founder and one holy book
- They have no belief in God
Explanation: Africa has thousands of peoples with their own traditions, so scholars speak of religions in the plural. Most share common features, including belief in a Supreme Being, spirits and ancestors.

Q: Who did John Mbiti call "the living dead"?
- Ghosts who frighten people
- People who are very sick
* Ancestors who have recently died but are remembered and believed to still be present in the family
- Religious specialists
Explanation: Mbiti used "the living dead" for ancestors who are still remembered by name and believed to be part of the family, watching over the living.

Q: Kwoth is the name for the Supreme God among which people?
- The Yoruba
- The Zulu
- The Kikuyu
* The Nuer
Explanation: Kwoth is the Nuer name for God. The Dinka name is Nhialic, the Yoruba Olodumare, the Kikuyu Ngai and the Zulu uNkulunkulu.

Q: Why do many African languages have no separate word for "religion"?
* Because faith was part of all of life, including farming, family, healing and leadership, not a separate activity
- Because people had no beliefs
- Because religion was banned
- Because only priests were allowed to talk about it
Explanation: In traditional African life, spiritual beliefs ran through everything. That's what John Mbiti meant when he wrote that "Africans are notoriously religious".

Q: Among the Dinka, who are the "masters of the fishing spear"?
- Soldiers in the army
* Hereditary spiritual leaders who pray for the community and help settle disputes
- Fishermen who sell fish at the market
- Christian missionaries
Explanation: The masters of the fishing spear (bany bith) are traditional Dinka spiritual leaders. They lead prayers and sacrifices and help keep peace in the community.
"""

ARRIVAL = """
GOAL: Learn when and how Christianity and Islam arrived in different parts of Africa, from ancient kingdoms to the colonial era and independence.

WHY THIS MATTERS
Many people assume Christianity arrived in Africa with European missionaries in the 1800s, and that Islam came only by conquest. The real story is longer and more surprising. Christianity reached North and East Africa almost 2,000 years ago, before it reached much of Europe. Islam arrived in some places by conquest and in others through traders and scholars. Knowing this timeline helps you judge the big question in the next lesson: were these religions imposed, or chosen?

KEY WORDS
- Missionary: a person sent to spread a religion.
- Convert: to change from one religion to another, or a person who has done so.
- Jihad: an Arabic word meaning "struggle". It can mean a personal spiritual struggle, and in history it was also used for wars fought in the name of Islam.
- Colonialism: when a foreign power takes control of a territory and its people.
- Independence: when a colony becomes a self-governing country.

DIAGRAM: religion-timeline
A timeline of faith in Africa. Traditional religions were always there. Christianity reached Egypt by AD 50 to 300, Aksum in Ethiopia in the 330s, and the Nubian kingdoms of Sudan in the 540s. Islam reached North Africa in the 640s and spread through trade from about 1000 to 1500. Missions and jihads came in the 1800s, then colonial rule from 1885 to 1960. The fastest growth came after independence, led by Africans.

ANCIENT AFRICAN CHRISTIANITY
- Egypt: Christianity spread in Egypt in the first centuries after Christ. Alexandria became one of the great centres of the early Church, and Egypt's Coptic Church is one of the oldest in the world.
- North Africa: some of the most important early Christian thinkers were Africans, including Augustine of Hippo, born in AD 354 in what is now Algeria.
- Ethiopia: in the AD 330s, King Ezana of Aksum adopted Christianity. The Ethiopian Orthodox Tewahedo Church has continued ever since, and Ethiopia kept its Christian identity for more than 1,600 years.
- Nubia (today's Sudan): the Nubian kingdoms became Christian in the 6th century. The king of Nobadia converted officially in AD 543. These Christian kingdoms lasted for centuries, with churches and cathedrals along the Nile.

HOW ISLAM ARRIVED
- An early welcome: around AD 615, some of the Prophet Muhammad's first followers fled persecution in Mecca and were sheltered by the Christian king of Aksum in Ethiopia. Africa's link with Islam began with protection, not conquest.
- Conquest in the north: in the AD 640s, Arab Muslim armies conquered Egypt and then spread across North Africa. Over the following centuries, most people there gradually became Muslim.
- A long peace with Nubia: the Nubians defeated Arab invasions in AD 641 and 652, and the two sides signed a treaty, the baqt, which kept peace and trade going for around 500 years.
- Trade and scholarship in West Africa: Islam spread across the Sahara with camel caravans of traders. Rulers of the Ghana and Mali empires adopted it. Mansa Musa of Mali made a famous pilgrimage to Mecca in 1324, and Timbuktu became a great centre of Islamic learning.
- The Swahili coast: on the East African coast, trade across the Indian Ocean brought Islam to towns like Kilwa, Mombasa and Zanzibar, creating the Swahili culture.

THE 1800s: JIHADS AND MISSIONS
- In West Africa, Islamic reform movements led by scholars such as Usman dan Fodio, who launched a jihad in 1804 and founded the Sokoto Caliphate in today's Nigeria, spread Islam further, partly by war.
- European Christian missionaries arrived in large numbers, opening churches, schools and hospitals.
- Earlier, some African rulers had chosen Christianity themselves: King Afonso I of Kongo, in today's Angola and DR Congo, ruled as a Christian king in the early 1500s, and his son Henrique became one of the first African Catholic bishops.

THE COLONIAL ERA (ABOUT 1885 TO 1960)
After the Berlin Conference of 1884 to 1885, European powers divided most of Africa between them. Missionaries often worked alongside colonial governments, and mission schools became the main way to get an education and a job in the colonial system.

AFTER INDEPENDENCE: AFRICAN-LED GROWTH
In 1900, there were only about 7 million Christians and 11 million Muslims in sub-Saharan Africa; most people followed traditional religions. By 2010, there were about 470 million Christians and 234 million Muslims, according to the Pew Research Center. Much of this growth happened in the second half of the 20th century, after most countries became independent, when churches and mosques were increasingly led by Africans.

DIAGRAM: religion-growth
In sub-Saharan Africa there were about 7 million Christians and 11 million Muslims in 1900, when most people followed traditional religions. By 2010, there were about 470 million Christians and 234 million Muslims.

REAL-LIFE CASE STUDY: SUDAN AND SOUTH SUDAN, A SHORT HISTORY OF FAITH
The land along the Nile that is now Sudan and South Sudan shows the whole story in one place. In the north, the Christian kingdoms of Nubia lasted for centuries until Islam gradually became the main religion of northern Sudan. In the south, most people followed traditional religions, such as those of the Dinka and Nuer, well into the 20th century. Christian missions arrived in the colonial period but at first won relatively few converts. After independence, Sudan's governments in Khartoum pushed Islamic law and Arabic culture across the country, especially after the 1983 "September Laws" introduced sharia nationally. Many southerners resisted, and during the long civil wars, Christianity grew rapidly in the south. Today, South Sudan is a mainly Christian country where traditional beliefs and practices remain strong.

PRACTICE
Complete the sentences.
1. In the AD 330s, King Ezana made Christianity the religion of ___.
2. The Christian kingdoms along the Nile in today's Sudan were called the kingdoms of ___.
3. In West Africa, Islam spread mainly with ___ crossing the Sahara.
4. Mansa Musa, who made a famous pilgrimage to Mecca, ruled the empire of ___.
5. The coastal culture of East Africa shaped by Indian Ocean trade is called ___.

ANSWERS: 1. Aksum  2. Nubia  3. traders  4. Mali  5. Swahili

QUIZ: Check Your Understanding
Q: When did Christianity first become established in Ethiopia?
- In the 1800s, with European missionaries
- In 1960, at independence
* In the AD 330s, when King Ezana of Aksum adopted it
- In 1884, at the Berlin Conference
Explanation: Ethiopia became Christian in the 4th century, under King Ezana of Aksum, more than 1,500 years before European colonisation of Africa.

Q: How did Islam mainly spread in West Africa, in places like Mali?
- Only through European colonisers
* Through traders crossing the Sahara and rulers who chose to adopt it
- Through the Berlin Conference
- It never reached West Africa
Explanation: Camel caravans of traders brought Islam across the Sahara. Rulers of empires like Ghana and Mali adopted it, and Timbuktu became a great centre of Islamic learning.

Q: What happened around AD 615 that links early Islam with Africa?
- Arab armies conquered Ethiopia
- Mansa Musa travelled to Mecca
* Early followers of the Prophet Muhammad were sheltered by the Christian king of Aksum
- The Sokoto Caliphate was founded
Explanation: Fleeing persecution in Mecca, some of the first Muslims found protection with the Christian ruler of Aksum in Ethiopia.

Q: Roughly how many Christians lived in sub-Saharan Africa in 1900, according to Pew?
- About 470 million
- About 234 million
- About 100 million
* About 7 million
Explanation: There were about 7 million Christians and 11 million Muslims in 1900. By 2010 the numbers had grown to about 470 million and 234 million.

Q: What were the 1983 "September Laws" in Sudan?
- A peace treaty with Nubia
* Laws that introduced Islamic sharia law across Sudan, which many southerners resisted
- The laws that ended colonial rule
- A law allowing traditional religions only
Explanation: The September Laws imposed sharia nationally. Many people in the south, who followed Christianity or traditional religions, opposed them, and the issue fuelled the civil war.
"""

ESSAY = """
GOAL: Weigh the evidence on one of the most debated questions about faith in Africa: were Christianity and Islam imposed on Africans, or did Africans choose and reshape them?

THE QUESTION
Today, most Africans are Christian or Muslim. Yet only a few generations ago, most people south of the Sahara followed the religions of their ancestors. Many people ask: is it really believable that a whole continent freely abandoned its own beliefs and embraced religions from far away? Or were these faiths forced on Africa by conquerors, slave traders and colonial rulers?
This essay sets out the strongest case for imposition, then the strongest case against, then looks at what the evidence suggests. You can decide for yourself.

DIAGRAM: imposed-debate
A balance weighing the question. Signs of imposition: conquest and colonial rule, mission schools as the only route to education and jobs, bans on traditional rituals, and Islamisation policies such as Sudan's 1983 sharia laws. Signs of African choice: ancient African churches in Egypt, Ethiopia and Nubia, Islam spreading through trade, and most growth coming after independence, led by Africans.

PART 1: THE CASE THAT THEY WERE IMPOSED
Conquest came first in many places. Arab armies conquered Egypt and North Africa in the 7th century. Under Muslim rule, non-Muslims usually paid a special tax called the jizya, which gave people a strong financial reason to convert over the generations. In the 1800s, jihads in West Africa, such as the one that created the Sokoto Caliphate, spread Islam partly by war.

The cross followed the flag. In the colonial era, missionaries often arrived alongside, or just ahead of, colonial rule. A famous saying, often attributed to Kenya's Jomo Kenyatta and also to Desmond Tutu, puts it sharply: "When the missionaries came to Africa, they had the Bible and we had the land. They said, let us pray. We closed our eyes. When we opened them, we had the Bible and they had the land."

Schools came with conditions. In many colonies, mission schools were almost the only way to learn to read, get a job as a clerk or teacher, or rise in society. Often, to attend, children had to be baptised and take a new "Christian" name. This was pressure, even if no one was physically forced.

Traditional religion was attacked. Many missionaries called African beliefs "pagan" or "devil worship". Converts were told to destroy shrines, stop honouring ancestors and give up customs such as polygamy. Colonial governments passed laws against some traditional practices, labelling them "witchcraft".

Slavery left deep wounds. Both the Atlantic slave trade, run largely by Christian Europeans, and the slave trades across the Sahara and the Indian Ocean, run largely by Muslim traders, tore millions of Africans from their homes. Enslaved people were often pressured or forced to adopt their owners' religion.

The pattern continued after independence. In Sudan, governments in Khartoum pushed Islamic law and Arabic culture onto the south, especially with the 1983 September Laws. For many South Sudanese, this was imposition within living memory.

Seen this way, it is hard to call the spread of these religions a free choice.

PART 2: THE CASE AGAINST
African Christianity is older than European colonialism by over a thousand years. Egypt's Coptic Church, Ethiopia's Orthodox Church from the AD 330s and the Christian kingdoms of Nubia from the 540s were African, not European, creations. Ethiopia was never a European colony, apart from a brief Italian occupation from 1936 to 1941, yet it remained Christian.

Islam often spread peacefully. In West Africa and along the Swahili coast, Islam came mainly with traders and scholars. Rulers such as those of the Mali Empire chose it, and Timbuktu became one of the world's great centres of Islamic learning. Africans helped spread Islam, they weren't only receivers of it.

Some African rulers chose Christianity themselves. In the early 1500s, King Afonso I of Kongo ruled as a Christian king, wrote letters to the King of Portugal as a fellow monarch, and sent his son Henrique to Europe, where he became a bishop.

The biggest growth came after colonialism. In 1900, after decades of missionary work, there were only about 7 million Christians in sub-Saharan Africa. Most of the growth to around 470 million by 2010 came in the 20th century, much of it after independence, when Europeans had left and Africans led the churches. If Christianity depended on colonial power, it should have shrunk when that power ended. Instead it grew faster.

Africans created their own churches, sometimes against colonial rulers. African-led churches broke away from mission control. Simon Kimbangu, a Congolese preacher, started a movement in 1921 that the Belgian colonial authorities saw as a threat. They jailed him, and he died in prison. His followers founded the Kimbanguist Church, now one of Africa's largest independent churches.

Africans had their own reasons. Research among the Dinka of South Sudan found that early missionaries won few converts, partly because they demanded a complete break with traditional religion. Large-scale conversion came decades later, during the civil wars. According to the scholar Jesse Zink, many Dinka felt their traditional divinities had not helped them in the crisis, while churches offered education, health care and hymns in the Dinka language. Local Dinka church leaders, cut off from foreign church officials by the war, adapted Christianity to Dinka life. This was a choice made under terrible pressure, but it was the Dinka's own choice.

PART 3: NOT ABANDONED, BUT BLENDED
Here the question itself may need rethinking. It assumes Africans either kept their old religions or abandoned them. Large surveys suggest that, for many, neither is true.
In a 2008 to 2009 survey of 19 sub-Saharan countries, the Pew Research Center found that many people who are deeply committed Christians or Muslims also keep traditional beliefs and practices:
- In 14 of the 19 countries, more than 30% of people said they sometimes consult traditional healers.
- In Senegal, 75% said they believe that charms (juju) and other sacred objects can protect them.
- In four countries, half or more of the people believed that sacrifices to ancestors or spirits can protect them from harm.
- In most countries, at least 30% believed in reincarnation.
So the instinct that a whole continent could not simply drop its beliefs is supported by evidence, but in an unexpected way. Many Africans didn't drop their old beliefs; they combined them with the new religions.

CONCLUSION
The evidence suggests that "imposed" is part of the truth, but not all of it. Conquest, colonial power, unequal schooling, slavery and, in Sudan, state Islamisation policies all pushed Africans towards Christianity and Islam. But Africans also chose these faiths, sometimes centuries before Europeans arrived, spread them themselves, built their own churches and mosques, and reshaped them with African music, languages and beliefs. Today, sub-Saharan Africa is home to more Christians than any other region of the world, about 697 million in 2020 according to Pew, and Africa is one of the great heartlands of Islam.
Perhaps the best word is not "imposed" or "chosen", but "transformed": Africans transformed these religions as much as the religions transformed Africa. Historians, theologians and Africans themselves still debate where the balance lies. What do you think?

PRACTICE
Complete the sentences.
1. A special tax paid by non-Muslims under early Muslim rule was called the ___.
2. The Congolese preacher jailed by Belgian colonial authorities was Simon ___.
3. Ethiopia's ancient church is the Ethiopian ___ Tewahedo Church.
4. Combining traditional beliefs with Christianity or Islam is often called ___.
5. Most growth of Christianity in Africa came after ___.

ANSWERS: 1. jizya  2. Kimbangu  3. Orthodox  4. blending  5. independence

QUIZ: Check Your Understanding
Q: Which of these is evidence used to argue that Christianity was imposed on Africa?
- Ethiopia became Christian in the AD 330s
- Most growth came after independence
* Mission schools were often the only way to get an education, and pupils were usually expected to be baptised
- The Kimbanguist Church was founded by Africans
Explanation: Making baptism a condition for schooling and jobs put strong pressure on people to convert. The other options are evidence for the opposite view: that Africans chose and led their own faith.

Q: Which fact challenges the idea that Christianity in Africa simply came from European colonialism?
* Christian kingdoms existed in Ethiopia and Nubia more than 1,000 years before European colonisation
- Missionaries opened schools in the colonial era
- The Berlin Conference divided Africa in 1884 to 1885
- Some colonial laws banned traditional practices
Explanation: African Christianity in Egypt, Ethiopia and Nubia is ancient, so it cannot be explained only by European colonial rule.

Q: Why is it significant that Christianity grew fastest after independence?
- It shows colonial rulers forced more people to convert after they left
* If the religion depended only on colonial power, it would be expected to shrink when that power ended, but instead it grew
- It shows traditional religions disappeared completely
- It proves that no one was ever pressured to convert
Explanation: Growth after colonial rule suggests many Africans had their own reasons for joining churches. It doesn't erase the pressures of the colonial era, but it complicates the "imposed" argument.

Q: What did the Pew survey of 19 African countries suggest about traditional beliefs?
- They have completely disappeared
- Only people with no religion keep them
* Many committed Christians and Muslims also keep traditional beliefs, such as consulting traditional healers or believing in protective charms
- They exist only in Senegal
Explanation: Pew found that traditional beliefs and practices remain widespread, even among people deeply committed to Christianity or Islam, showing that many people blend old and new.

Q: According to research among the Dinka of South Sudan, why did many Dinka become Christians during the civil wars?
- Because foreign missionaries forced them at gunpoint
- Because the government of Khartoum required it
* Many felt traditional divinities hadn't helped in the crisis, while churches offered education, health care and hymns in Dinka, and local Dinka leaders adapted the faith
- Because they were paid to convert
Explanation: Jesse Zink's research found the Dinka made the choice for their own reasons in a time of crisis, and Dinka church leaders shaped Christianity to fit Dinka life.
"""

TODAY = """
GOAL: Explore how Africans practise faith today: blending traditions, the boom in new churches, how religion shapes public life, and the role of faith in South Sudan.

WHY THIS MATTERS
Africa is now one of the most religious places on earth. In the Pew Research Center's survey of 19 sub-Saharan countries, in many of them about nine in ten people or more said religion is very important in their lives. Faith shapes how people vote, how they settle disputes, how they treat illness and how communities rebuild after war. To understand modern Africa, you need to understand its faith.

KEY WORDS
- Syncretism: blending beliefs and practices from different religions.
- Pentecostal: a type of Christianity that emphasises the Holy Spirit, healing, lively worship and personal experience of God.
- Prosperity gospel: the teaching that faith and giving to the church will bring wealth and health.
- Interfaith: involving people of different religions.
- Secular: not connected with religion.

BLENDING OLD AND NEW
Many Africans see no conflict between going to church or mosque and honouring ancestors, consulting a traditional healer or wearing a protective charm. A person might pray in church on Sunday, then pour a drink for the ancestors at a family ceremony. Funerals and weddings often mix Christian or Muslim prayers with traditional customs. Some religious leaders welcome this, saying faith should be at home in African culture; others condemn it and ask believers to choose.

DIAGRAM: faith-blend
Two overlapping circles. Traditional beliefs include ancestors, spirits, healers and charms. Christianity or Islam include church or mosque, prayer, scripture and festivals. In the overlap, many people combine both, for example at funerals and in healing. In Senegal, 75 percent believe charms can protect them.

THE CHURCH BOOM
Since the 1970s, Pentecostal and charismatic churches have spread rapidly across Africa, from Nigeria and Ghana to Kenya, Uganda and South Africa. Their lively music, prayers for healing and miracles, use of local languages and young leaders appeal to many people, especially in fast-growing cities. Some have become very large, with television channels and branches abroad.

THE PROSPERITY GOSPEL DEBATE
Some churches teach that giving money to the church will bring blessings of wealth and health. Supporters say this message gives hope and encourages hard work. Critics, including many African church leaders, say it can be used to take money from poor people, and that some preachers become very rich while their members stay poor. It is one of the most debated issues in African Christianity today.

RELIGION AND PUBLIC LIFE
- Peace and reconciliation: churches and mosques often help mediate conflicts and support victims of war.
- Health and education: faith groups run many schools and hospitals across Africa.
- Politics: politicians often seek the support of religious leaders, and religion can unite or divide voters.
- Living together: in many countries, Christians and Muslims live side by side, marry each other and share celebrations. In some places, though, religion has become mixed up with violent conflict.

YOUNG AFRICANS AND FAITH TODAY
Many young Africans remain deeply religious, often joining newer churches or Islamic movements. Others are questioning religion, especially online, and some, in Africa and among Africans living abroad, are rediscovering traditional spirituality as part of their cultural identity. Cities, the internet and education are all changing how people practise and talk about faith.

REAL-LIFE CASE STUDY: FAITH IN SOUTH SUDAN
South Sudan became independent in 2011 after decades of war. Churches played a major role during and after the conflict. Church leaders spoke out for peace, organised meetings between rival communities and provided food, schools and health care when the state could not. The South Sudan Council of Churches, which brings together different Christian churches, has been involved in efforts to promote peace and reconciliation.
At the same time, traditional beliefs remain important. Many South Sudanese Christians still give cattle in marriage, respect the role of spiritual leaders such as the Dinka masters of the fishing spear, and keep traditional ceremonies at funerals. Faith in South Sudan, like much of Africa, is both new and very old at once.

PRACTICE
Complete the sentences.
1. Blending beliefs from different religions is called ___.
2. Christianity that emphasises the Holy Spirit and healing is called ___.
3. The teaching that giving to the church brings wealth is the prosperity ___.
4. Involving people of different religions is described as ___.
5. South Sudan became independent in the year ___.

ANSWERS: 1. syncretism  2. Pentecostal  3. gospel  4. interfaith  5. 2011

QUIZ: Check Your Understanding
Q: What does syncretism mean?
- Rejecting all religions
* Blending beliefs and practices from different religions
- Following only traditional religion
- Moving to a different country
Explanation: Syncretism is the mixing of religious traditions, such as combining church attendance with honouring ancestors.

Q: In Pew's survey of 19 sub-Saharan countries, how important did people say religion was?
- Most said it was not important
- About half said it was somewhat important
* In many countries, about nine in ten or more said religion is very important in their lives
- Only older people said it was important
Explanation: Pew found very high levels of religious commitment across sub-Saharan Africa, making it one of the most religious regions in the world.

Q: Why have Pentecostal and charismatic churches grown so fast in Africa?
- Because the government requires everyone to join
- Because they ban all music
* Lively worship, prayers for healing, local languages and young leaders appeal to many people, especially in cities
- Because they only accept older members
Explanation: These churches feel lively and relevant to many Africans, especially young people in growing cities, and they often use local languages and music.

Q: What is a main criticism of the prosperity gospel?
* It can be used to take money from poor people while some preachers become very rich
- It forbids people from working
- It is only practised outside Africa
- It bans traditional ceremonies
Explanation: Critics, including many African church leaders, argue that promising wealth in return for giving can exploit poor believers.

Q: How have churches contributed in South Sudan?
- They have stayed out of public life completely
* They have spoken out for peace, brought rival communities together and provided food, schools and health care
- They replaced the national government
- They banned traditional ceremonies everywhere
Explanation: Churches, including through the South Sudan Council of Churches, have worked for peace and reconciliation and filled gaps in services during and after the war.
"""

MODULES = [
    (
        "Module 1: Faith in Africa, Past and Present",
        True,
        [
            ("african-traditional-religions", "African Traditional Religions: God, Spirits and Ancestors", TRADITIONAL),
            ("how-christianity-and-islam-came-to-africa", "How Christianity and Islam Came to Africa: A Timeline", ARRIVAL),
            ("were-christianity-and-islam-imposed-on-africa", "Were Christianity and Islam Imposed on Africa? The Case For and Against", ESSAY),
            ("religion-in-africa-today", "Religion in Africa Today: Blending Old and New Faith", TODAY),
        ],
    ),
]


class Command(BaseCommand):
    help = "Creates or updates the 'Religion and Culture in Africa' course (all modules free)."

    def handle(self, *args, **options):
        course, created, lessons = seed_course(COURSE, MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} '{course.title}': {len(MODULES)} modules, {lessons} lessons."
            )
        )
