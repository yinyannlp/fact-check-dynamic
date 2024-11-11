ProgramFC_PROMPT = '''Generate a python-like program that describes the reasoning steps required to verify the sub-claim step-by-step. You can call three functions in the program: 1. Question() to answer a question; 2. Verify() to verify a simple sub-claim; 3. Predict() to predict the veracity label. Several examples are given as follows.

# The claim is that In 1959, former Chilean boxer Alfredo Cornejo Cuevas (born June 6, 1933) won the gold medal in the welterweight division at the Pan American Games (held in Chicago, United States, from August 27 to September 7) in Chicago, United States, and the world amateur welterweight title in Mexico City.
def program():
    fact_1 = Verify("Alfredo Cornejo Cuevas was born in June 6, 1933.")
    fact_2 = Verify("Alfredo Cornejo Cuevas won the gold medal in the welterweight division at the Pan American Games in 1959.")
    fact_3 = Verify("The Pan American Games in 1959 was held in Chicago, United States, from August 27 to September 7.")
    fact_4 = Verify("Alfredo Cornejo Cuevas won the world amateur welterweight title in Mexico City.")
    label = Predict(fact_1 and fact_2 and fact_3 and fact_4)

# The claim is that The Footwork FA12, which was intended to start the season, finally debuted at the San Marino Grand Prix, a Formula One motor race held at Imola on 28 April 1991.
def program():
    fact_1 = Verify("The Footwork FA12, which was intended to start the season.")
    fact_2 = Verify("The Footwork FA12 finally debuted at the San Marino Grand Prix.")
    fact_3 = Verify("The San Marino Grand Prix was a Formula One motor race held at Imola on 28 April 1991.")
    label = Predict(fact_1 and fact_2 and fact_3)

# The claim is that SkyHigh Mount Dandenong (formerly Mount Dandenong Observatory) is a restaurant located on top of Mount Dandenong, Victoria, Australia.
def program():
    fact_1 = Verify("SkyHigh Mount Dandenong is a restaurant located on top of Mount Dandenong, Victoria, Australia.")
    fact_2 = Verify("SkyHigh Mount Dandenong is formerly known as Mount Dandenong Observatory.")
    label = Predict(fact_1 and fact_2)

# The claim is that Before the first Europeans arrived or copra companies leased it, Maupihaa was home to Inca's in ancient times.
def program():
    fact_1 = Verify("Maupihaa was home to Inca's in ancient times.")
    fact_2 = Verify("Maupihaa was home to Inca's before the first Europeans arrived or copra companies leased it.")
    label = Predict(fact_1 and fact_2)
    
# The claim is that Shulin, a 33.1288 km (12.7911 sq mi) land located in New Taipei City, China, a country in East Asia, has a total population of 183,946 in December 2018.
def program():
    fact_1 = Verify("Shulin is a 33.1288 km (12.7911 sq mi) land located in New Taipei City, China.")
    fact_2 = Verify("Shulin has a total population of 183,946 in December 2018.")
    label = Predict(fact_1 and fact_2)
    
# The claim is that Sumo wrestler Toyozakura Toshiaki committed match-fixing, ending his career in 2011 that started in 1989.
def program():
    fact_1 = Verify("Toyozakura Toshiaki ended his career in 2011 that started in 1989.")
    fact_2 = Verify("Toyozakura Toshiaki is a Sumo wrestler.")
    fact_3 = Verify("Toyozakura Toshiaki committed match-fixing.")
    label = Predict(fact_1 and fact_2 and fact_3)

# The claim is that In 1959, former Chilean boxer Alfredo Cornejo Cuevas (born June 6, 1933) won the gold medal in the welterweight division at the Pan American Games (held in Chicago, United States, from August 27 to September 7) in Chicago, United States, and the world amateur welterweight title in Mexico City.
def program():
    fact_1 = Verify("Alfredo Cornejo Cuevas is a former Chilean boxer.")
    fact_2 = Verify("Alfredo Cornejo won the gold medal in the welterweight division at the Pan American Games.")
    fact_3 = Verify("The Pan American Games was held in Chicago, United States, from August 27 to September 7.")
    fact_4 = Verify("Alfredo Cornejo won the world amateur welterweight title in Mexico City.")
    label = Predict(fact_1 and fact_2 and fact_3 and fact_4)

# The claim is that Adductor hiatus is associated with nine structures, seven of which enter and leave through hiatus.
def program():
    fact_1 = Verify("Adductor hiatus is associated with nine structures.")
    fact_2 = Verify("Seven of the nine structures associated with Adductor hiatus enter and leave through hiatus.")
    label = Predict(fact_1 and fact_2)
    
# The claim is that Ifor Bowen Lloyd was educated at Winchester (an independent boarding school for boys in the British public school tradition) and Exeter College, Oxford where he was a member of the Library Committee of the Oxford Union Society, as well as, received a BA in Modern History in 1924.
def program():
    fact_1 = Verify("Ifor Bowen Lloyd was educated at Winchester and Exeter College, Oxford.")
    fact_2 = Verify("Winchester is an independent boarding school for boys in the British public school tradition.")
    fact_3 = Verify("While at Oxford, Ifor Bowen Lloyd was a member of the Library Committee of the Oxford Union Society.")
    fact_4 = Verify("Ifor Bowen Lloyd received a BA in Modern History in 1924 at Oxford.")
    label = Predict(fact_1 and fact_2 and fact_3 and fact_4)
  
# The claim is that In the 2001 Stanley Cup playoffs Eastern Conference Semifinals Devils' Elias scored and Maple Leafs' left Devils player Scott Neidermayer hurt.
def program():
    fact_1 = Verify("In the 2001 Stanley Cup playoffs Eastern Conference Semifinals Devils' Elias scored.")
    fact_2 = Verify("Maple Leafs' left Devils player Scott Neidermayer hurt.")
    label = Predict(fact_1 and fact_2)
    
# The claim is that Teldenia helena is a moth first described in 1967 by Wilkinson.
def program():
    fact_1 = Verify("Teldenia helena is a moth.")
    fact_2 = Verify("Teldenia helena was first described by Wilkinson in 1967.")
    label = Predict(fact_1 and fact_2)
    
# The claim is that Born December 30, 1974, William Frick was a dark horse candidate in the Maryland House of Delegates appointment process.
def program():
    fact_1 = Verify("William Frick was born in December 30, 1974.")
    fact_2 = Verify("William Frick was a dark horse candidate in the Maryland House of Delegates appointment process.")
    label = Predict(fact_1 and fact_2)

# The claim is that {claim}
def program():'''


Wice_PROMPT = """
Segment the following sentence into individual facts:

Sentence: Other title changes included Lord Steven Regal and The Nasty Boys winning the World Television Championship and the World Tag Team Championship respectively.
Facts:
- Lord Steven Regal wan the World Television Championship. 
- The Nasty Boys wan and the World Tag Team Championship.

Sentence: The parkway was opened in 2001 after just under a year of construction and almost two decades of community requests.
Facts:
- The parkway was opened in 2001.
- The parkway was opened after just under a year of construction.
- The parkway was opened after two decades of community requests.

Sentence: Touring began in Europe in April–June with guitarist Paul Gilbert as the opening act, followed by Australia and New Zealand in July, Mexico and South America in late July–August, and concluding in North America in October–November.
Facts:
- Touring began in Europe in April–June.
- The opening act was guitarist Paul Gilbert.
- There was a tour in Australia in July.
- There was a tour in New Zealand in July.
- There was a tour in Mexico in late July–August.
- There was a tour in South America in late July–August
- The tour was concluded in North America in October–November.

Sentence: In March 2018, the company partnered With Amazon Web Services (AWS) to offer Al-enabled conversational solutions to customers in India.
Facts:
- The company partnered with Amazon Web Services (AWS) in March 2018.
- The two companies partnered to offer Al-enabled conversational solutions to customers in India.

Sentence: The most significant of these is in Germany, which now has a Yazidi community of more than 200,000 living primarily in Hannover, Bielefeld, Celle, Bremen, Bad Oeynhausen, Pforzheim and Oldenburg.
Facts:
- The most significant of these is in Germany.
- Germany now has a Yazidi community of more than 200,000.
- Yazidi community in Germany lives primarily in Hannover.
- Yazidi community in Germany lives primarily in Bielefeld.
- Yazidi community in Germany lives primarily in Celle.
- Yazidi community in Germany lives primarily in Bremen.
- Yazidi community in Germany lives primarily in Bad Oeynhausen.
- Yazidi community in Germany lives primarily in Pforzheim.
- Yazidi community in Germany lives primarily in Oldenburg.

Sentence: A previous six-time winner of the Nations' Cup, Sebastian Vettel became Champion of Champions for the first time, defeating Tom Kristensen, who made the final for the fourth time, 2–0.
Facts:
- Sebastian Vettel is a previous six-time winner of the Nations' Cup.
- Sebastian Vettel became Champion of Champions for the first time.
- Sebastian Vettel defeated Tom Kristensen.
- Tom Kristensen made the final for the fourth time.
- The score was 2–0.

Sentence: {claim}
Facts:\n"""


ClaimDecompose_PROMPT = '''Claim: Viral image stated on June 8, 2020 in post on Facebook: Cops in Norway: require 3 years of training, 4 people killed since 2002. Cops in Finland: require 2 years of training, 7 people killed since 2000. Cops in Iceland: require 2 years of training, 1 person killed since ever. Cops in the U.S.: require 21 weeks of training, 8,000+ people killed since 2001.

Suppose you are a fact-checker, generate several yes or no quesons to help me answer if this claim is true or false.

Quesons:
Does Norway require 3 years of training for cops?
Have Norwegian cops killed 4 people since the early 2000's?
Does Finland require only 2 years of training for police?
Have Finnish police killed 7 people since 2000?
Does Iceland only require 2 years of training for cops?
Have Iceland cops only killed 1 person ever?
Does the U.S. require only 21 weeks of training for cops?
Have U.S. cops killed more than 8,000 people since 2001?
Do experts associate only training me with police-related shoong fatalies?

Claim: Barry DuVal stated on September 25, 2015 in an interview: We're the only major oil-producing naon in the world with a self-imposed ban on exporng our crude oil to other naons.

Suppose you are a fact-checker, generate several yes or no quesons to help me answer if this claim is true or false.

Questions:
Is the U.S. the only major oil-producing naon to ban exports of crude oil?
Is the self-imposed ban on crude oil export of U.S a complete ban?

Claim: William Barr stated on September 2, 2020 in a CNN interview: We indicted someone in Texas, 1,700 ballots collected from people who could vote, he made them out and voted for the person he wanted to.

Suppose you are a fact-checker, generate several yes or no quesons to help me answer if this claim is true or false.

Questions:
Were 1700 mail-in ballots invesgated for fraud in Texas during the 2020 elecon?
Did the Justice Department indict someone in Texas for voter fraud?
Did widespread mail-in order fraud happen in Texas during the 2020 elecon?
Did voter disenfranchisement happen in Texas during the 2020 elecon?

Claim: {claim}
Suppose you are a fact-checker, generate several yes or no quesons to help me answer if this claim is true or false.

Questions:'''


FactScore_PROMPT = """
Please breakdown the following sentence into independent facts: He made his acting debut in the film The Moon is the Sun’s Dream (1992), and continued to
appear in small and supporting roles throughout the 1990s.
- He made his acting debut in the film.
- He made his acting debut in The Moon is the Sun’s Dream.
- The Moon is the Sun’s Dream is a film.
- The Moon is the Sun’s Dream was released in 1992.
- After his acting debut, he appeared in small and supporting roles.
- After his acting debut, he appeared in small and supporting roles throughout the 1990s.

Please breakdown the following sentence into independent facts: He is also a successful producer and engineer, having worked with a wide variety of artists,
including Willie Nelson, Tim McGraw, and Taylor Swift.
- He is successful.
- He is a producer.
- He is a engineer.
- He has worked with a wide variety of artists.
- Willie Nelson is an artist.
- He has worked with Willie Nelson.
- Tim McGraw is an artist.
- He has worked with Tim McGraw.
- Taylor Swift is an artist.
- He has worked with Taylor Swift.

Please breakdown the following sentence into independent facts: In 1963, Collins became one of the third group of astronauts selected by NASA and he served
as the back-up Command Module Pilot for the Gemini 7 mission.
- Collins became an astronaut.
- Collins became one of the third group of astronauts.
- Collins became one of the third group of astronauts selected.
- Collins became one of the third group of astronauts selected by NASA.
- Collins became one of the third group of astronauts selected by NASA in 1963.
- He served as the Command Module Pilot.
- He served as the back-up Command Module Pilot.
- He served as the Command Module Pilot for the Gemini 7 mission.

Please breakdown the following sentence into independent facts: In addition to his acting roles, Bateman has written and directed two short films and is
currently in development on his feature debut.
- Bateman has acting roles.
- Bateman has written two short films.
- Bateman has directed two short films.
- Bateman has written and directed two short films.
- Bateman is currently in development on his feature debut.

Please breakdown the following sentence into independent facts: Michael Collins (born October 31, 1930) is a retired American astronaut and test pilot who
was the Command Module Pilot for the Apollo 11 mission in 1969.
- Michael Collins was born on October 31, 1930.
- Michael Collins is retired.
- Michael Collins is an American.
- Michael Collins was an astronaut.
- Michael Collins was a test pilot.
- Michael Collins was the Command Module Pilot.
- Michael Collins was the Command Module Pilot for the Apollo 11 mission.
- Michael Collins was the Command Module Pilot for the Apollo 11 mission in 1969.

Please breakdown the following sentence into independent facts: He was an American composer, conductor, and musical director.
- He was an American.
- He was a composer.
- He was a conductor.
- He was a musical director.

Please breakdown the following sentence into independent facts: She currently stars in the romantic comedy series, Love and Destiny, which premiered in 2019.
- She currently stars in Love and Destiny.
- Love and Destiny is a romantic comedy series.
- Love and Destiny premiered in 2019.

Please breakdown the following sentence into independent facts: During his professional career, McCoy played for the Broncos, the San Diego Chargers, the
Minnesota Vikings, and the Jacksonville Jaguars.
- McCoy played for the Broncos.
- McCoy played for the Broncos during his professional career.
- McCoy played for the San Diego Chargers.
- McCoy played for the San Diego Chargers during his professional career.
- McCoy played for the Minnesota Vikings.
- McCoy played for the Minnesota Vikings during his professional career.
- McCoy played for the Jacksonville Jaguars.
- McCoy played for the Jacksonville Jaguars during his professional career.

Please breakdown the following sentence into independent facts: {claim}\n"""


PropSegment_PROMPT = """
Given the following sentence, tell me what claims they are making. 
Please split the sentence as much as possible, but do not include information not in the sentence. 

Sentence: The Andy Warhol Museum in his hometown, Pittsburgh, Pennsylvania, contains an extensive permanent collection of art. 
Claims: 
1. The Andy Warhol Museum is in Pittsburgh. 
2. Andy Warhol’s hometown is in Pittsburgh. 
3. Pittsburgh is in Pennsylvania. 
4. The Andy Warhol Museum contains an extensive permanent collection of art. 

Sentence: {claim} 
Claims:

"""
Coling_PROMPT = '''
To verify a complex claim, we first need to decompose it into sub-claims. We define four types of logical relationships between sub-claims:
AND: Sub-claims exist independently, with no connection, but together support the main claim.
OR: Sub-claims can be interchangeable, supporting the main claim either individually or together. If one is invalid, others remain valid.
Temporal: Sub-claims are arranged in chronological order, with the former occurring before the latter.
Causal: Sub-claims have a causal relationship, where one is the cause or result of the other.

Several examples are given as follows.


# Complex Claim:
Sumo wrestler Toyozakura Toshiaki committed match-fixing, ending his career in 2011 that started in 1989.

Sub-claims:
Sub-claim_1 : Toyozakura Toshiaki's sumo career started in 1989.
Sub-claim_2 : Toyozakura Toshiaki's sumo career ended in 2011.
Sub-claim_3 : Toyozakura Toshiaki committed match-fixing.


# Complex Claim:
Born on December 30, 1974, William Frick was a dark horse candidate in the Maryland House of Delegates appointment process.

Sub-claims:
Sub-claim_1 : William Frick was born on December 30, 1974.
Sub-claim_2 : William Frick was a dark horse candidate in the Maryland House of Delegates appointment process.


# Complex Claim:
In 1963, Collins became one of the third group of astronauts selected by NASA, and he served as the back-up Command Module Pilot for the Gemini 7 mission.

Sub-claims:
Sub-claim_1 : In 1963, Collins became one of the third group of astronauts selected by NASA.
Sub-claim_2 : Collins served as the back-up Command Module Pilot for the Gemini 7 mission.


# Complex Claim:
In March 2018, the company partnered With Amazon Web Services (AWS) to offer Al-enabled conversational solutions to customers in India.

Sub-claims:
Sub-claim_1 : In March 2018, the company partnered with Amazon Web Services (AWS).
Sub-claim_2 : The partnership was aimed at offering AI-enabled conversational solutions to customers in India.


# Complex Claim:
In 1959, former Chilean boxer Alfredo Cornejo Cuevas (born June 6, 1933) won the gold medal in the welterweight division at the Pan American Games (held in Chicago, United States, from August 27 to September 7) and the world amateur welterweight title in Mexico City.

Sub-claims:
Sub-claim_1 : Alfredo Cornejo Cuevas was born on June 6, 1933.
Sub-claim_2 : The Pan American Games were held in Chicago, United States, from August 27 to September 7, 1959.
Sub-claim_3 : Alfredo Cornejo Cuevas won the gold medal in the welterweight division at the Pan American Games.
Sub-claim_4 : Alfredo Cornejo Cuevas won the world amateur welterweight title in Mexico City in 1959.


# Complex Claim:
The parkway was opened in 2001 after just under a year of construction and almost two decades of community requests

Sub-claims:
Sub-claim_1 : The parkway underwent just under a year of construction.
Sub-claim_2 : The parkway was opened in 2001.
Sub-claim_3 : The community requested the parkway for almost two decades before it was opened.


# Complex Claim:
Therefore, with the decrease in US soybean production, domestic soybean oil prices are anticipated to persist in their upward trajectory, thereby bolstering international soybean oil prices.

Sub-claims:
Sub-claim_1 : US soybean production is decreasing.
Sub-claim_2 : Domestic soybean oil prices are anticipated to persist in their upward trajectory.
Sub-claim_3 : The anticipated increase in domestic soybean oil prices will bolster international soybean oil prices.


# Complex Claim:
António Bento Bembe, Chairman of the Cabinda Forum for Dialogue (FCD), pointed out that after 95% of the troops are stationed in Cabinda, the first phase of the peace memorandum will begin to be implemented.

Sub-claims:
Sub-claim_1 : António Bento Bembe is Chairman of the Cabinda Forum for Dialogue (FCD).
Sub-claim_2 : António Bento Bembe pointed out that  95% of the troops are stationed in Cabinda.
Sub-claim_3 : António Bento Bembe pointed out that the first phase of the peace memorandum will begin to be implemented after the troop deployment.


# Complex Claim:
Adductor hiatus is associated with nine structures, seven of which enter and leave through hiatus.

Sub-claims:
Sub-claim_1 : Adductor hiatus is associated with nine structures.
Sub-claim_2 : Seven of the nine structures associated with Adductor hiatus enter and leave through hiatus.


# Complex Claim:
SkyHigh Mount Dandenong (formerly Mount Dandenong Observatory) is a restaurant located on top of Mount Dandenong, Victoria, Australia.

Sub-claims:
Sub-claim_1 : SkyHigh Mount Dandenong is a restaurant located on top of Mount Dandenong, Victoria, Australia.
Sub-claim_2 : SkyHigh Mount Dandenong is formerly known as Mount Dandenong Observatory.


# Complex Claim:
{claim}

Sub-claims:
'''


Revision_Prompt = """
I will fix some things you said. 
(1) You said: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes. This is to prevent a buildup of mucus. It’s called the nasal cycle. 
I found this article: Although we don’t usually notice it, during the nasal cycle one nostril becomes congested and thus contributes less to airflow, while the other becomes decongested. On average, the congestion pattern switches about every 2 hours, according to a small 2016 study published in the journal PLOS One. 6 This suggests 45 minutes switch time in your statement is wrong. 
My fix: Your nose switches back and forth between nostrils. When you sleep, you switch about every 2 hours. This is to prevent a buildup of mucus. It’s called the nasal cycle.

(2) You said: In the battles of Lexington and Concord, the British side was led by General Thomas Hall. 
I found this article: Interesting Facts about the Battles of Lexington and Concord. The British were led by Lieutenant Colonel Francis Smith. There were 700 British regulars. 12 This suggests General Thomas Hall in your statement is wrong. 
My fix: In the battles of Lexington and Concord, the British side was led by Lieutenant Colonel Francis Smith.

(3) You said: The Stanford Prison Experiment was conducted in the basement of Encina Hall, Stanford’s psychology building. 
I found this article: Carried out August 15-21, 1971 in the basement of Jordan Hall, the Stanford Prison Experiment set out to examine the psychological effects of authority and powerlessness in a prison environment. 18 This suggests Encina Hall in your statement is wrong. 
My fix: The Stanford Prison Experiment was conducted in the basement of Jordan Hall, Stanford’s psychology building.

(4) You said: Phoenix Mills Ltd., a diversified business conglomerate, was established in 1854. It has a history of over 160 years.
I found this article: Phoenix Mills Ltd was incorporated in the year 1905. The company began their operations as a textile manufacturing company on 17.3 acres of land at Lower Parel in Mumbai. In the year 1959 the company was listed in the Bombay Stock Exchange. This suggests the year of establishment 1854 in your statement is wrong. 
My fix: Phoenix Mills Ltd., a diversified business conglomerate, was established in 1905. It has a history of over 160 years.

(5) You said: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its adjacency list. It is named after Vaclav Havel and Samih Hakimi.
I found this article: The Havel-Hakimi algorithm constructs a special solution if a simple graph for the given degree sequence exists, or proves that one cannot find a positive answer. This construction is based on a recursive algorithm. The algorithm was published by Havel (1955), and later by Hakimi (1962). This suggests the Havel-Hakimi algorithm’s functionality in your statement is wrong. 
My fix: The Havel-Hakimi algorithm constructs a special solution if a simple graph for the given degree sequence exists, or proves that one cannot find a positive answer. It is named after Vaclav Havel and Samih Hakimi

(6) You said: "Time of My Life" is a song by American singer-songwriter Bill Medley from the soundtrack of the 1987 film Dirty Dancing. The song was produced by Phil Ramone.
I found this article: On September 8, 2010, the original demo of this song, along with a remix by producer Michael Lloyd, was released as digital files in an effort to raise money for the Patrick Swayze Pancreas Cancer Resarch Foundation at Stanford University.  This suggests "Time of My Life" producer name in your statement is wrong.
My fix: "Time of My Life" is a song by American singer-songwriter Bill Medley from the soundtrack of the 1987 film Dirty Dancing. The song was produced by Michael Lloyd.


(7) You said: Phoenix Market City Pune is located on 21 acres of prime property in Pune. It is spread across four levels with approximately 1.4 million square feet of built-up space. The mall is owned and operated by Phoenix Mills Limited.
I found this article: Phoenix Market City was opened in January 2013 and has the distinction of being the largest mall in the city of Pune, with the area of 3.4 million square feet. It is located in the Viman Nagar area of Pune. This suggests the 1.4 million square feet of built-up space in your statment is wrong. 
My fix: Phoenix Market City Pune is located on 21 acres of prime property in Pune. It is spread across four levels with approximately 3.4 million square feet of built-up space. The mall is owned and operated by Phoenix Mills Limited.

You said: {text} 
I found this article: {evidence} This suggests :
"""


Revision_Prompt = """
Please make your claim objective and rewrite it as verified facts based on the evidence text provided. Please make sure to use accurate language, avoid subjective judgments, and emphasize the authenticity and reliability of the facts. Finally, you only need to output the rewritten claim.
claim: {claim}

Evidence: {evidence}
"""