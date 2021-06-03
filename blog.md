# ParlaMint Showcase Blog



## Introduction to the topic

Scientific knowledge and expertise stands at the center of recent government responses to the current SARS-CoV-2 pandemic. Containment strategies, vaccination efforts and economic policies are informed and shaped by experts and scientists. The power of medical-scientific experts and institutions is, in the eyes of many, unprecedented. Especially after years of populist discontent in many democracies, the corona epidemic has produced a narrative of a "return of science". Science has regained its public trust and centrality in policy-making (Windholz 2020; Bertsou 2020). However, the opposite argument could also be true. Conspiracy theories flourish like never before (Shelton 2020; Duarte 2020). The suddenness of the pandemic’s spread and the gravity of the containment measures reinforced existing suspicions against scientific and political authorities and the spread of “fake news” pertaining to a “plandemic” has accelerated. It appears that the corona crisis has produced a heightened polarity between the technocratic adoption of scientific knowledge on the one hand and the conspiratory rejection of (institutionalized) scientific knowledge on the other. For democratic decision-making, this begs the question how to navigate between these poles. This question is relevant because it has proved hard to wage politics during the corona crisis (Amat et al. 2020; Bekker, Ivankovic, and Biermann 2020). Political opposition against government strategies has been obscured by a 'rally around the flag'-effect in the first months of the pandemic, and the spectre of conspiratory post-truth soon after.

## Data: Parliaments in Pandemic Times

Parliamentary debates are highly specific forms of textual data. Compared to other often-used forms of public discourse, parliamentary transcripts stand out for several reasons. Parliamentary interaction, in an ideal-typical setting, is an exchange of arguments *pro* and *contra*. Deviation from this ideal type is part of the day-to-day rhetoric, but in its *argumentative* nature, parliamentary language differs fundamentally from other types of political discourse found in for example social media data or newspapers. 

The nature of parliamentary language also changes in times of crisis. Political scientists often refer to the so-called "rally around the flag effect" when analyzing crisis politics. Political actors, so the idea runs, "rally" around the flag - in the case of parliaments the incumbent government and/or the coalition parties -, temporally suspending the enmities that mark the political landscape.  

## Approach



## More Crisis, More Experts? Frequency Patterns

The research departed from the hypothesis that the corona crisis provoked more references to expertise in European parliaments. Frequency patterns quickly disprove this expected general pattern of increasing frequencies. In this section I use a lexicon of terms related to expertise ("expert","science" and "expertise", translated in all participating languages) to inspect frequencies as a first step. Figure X, for example, shows the relative frequencies of the lemma "expert" in eight different countries. Only the patterns in Dutch, Italian, Polish and Spanish suggest change as a result of the corona pandemic (the dashed gray line marks the first week of March 2020 during which infections grew rapidly in many countries).

[subplots of frequency / week]

Before taking a deep dive into the speeches that mention expertise, it is worthwhile to further investigate other frequency patterns. One way of getting a better idea of national differences and commonalities is investigating the coalition-opposition distribution of the frequency of 'expert'. I plotted the frequency of this term in the first five months of the pandemic (March - July) by coalition and opposition, normalized by the total number of tokens for opposition and coalition (to control for the overall differences in speech size between both groups). The resulting charts shows that there is not common pattern. In Latvia and the Netherlands, the coalition speaks relatively more of experts. In Great Britain, Italy, Czech Republic, Poland and Spain, the opposition speaks more about experts. 

[bar chart of coal/opp uses of 'expert']

The divergent patterns in coalition-opposition distributions prompted me to investigate the individual speakers in their uses of "expert". Inspecting the top "users" of the term shows how in several countries it is the Health Minister (or persons with a comparable position) that utter "expert" the most. James Bethell in Great Britain, Hugo de Jonge in the Netherlands, Aurelijus Veryga in Lithuania and Magnus Heunicke in Denmark use the term the most in their parliaments.  In Italy, Poland and Spain, the prime minister uses the lemma the most. The high rankings of these persons is not surprising. As the crisis unfolded, (prime) ministers drew on experts in their decision-making. However, in multiple countries, opposition figures also use the term frequently. In the Netherlands, the health minister is closely followed by two MPs from the opposition. In Czech Republic two opposition party members occupy the top positions (although we must be careful to draw conclusions from the low frequencies). Similarly, in Spain, Pablo Casado Blanco, leader of the largest opposition party (Partido Popular) follows Pedro Sánchez in the top users of the term.

The relatively low frequencies of the top users of "expert" hints at a large spread of users. The prime minister of Spain uses 'expert' only 38 times. Because the total number of references is far bigger, a large number of other MPs must have mentioned it. An overview of the distribution of the references over the different speakers is visualised below. The figure shows the number of different speakers that mention 'expert', divided by the monthly total number of different speakers (to compensate for the fact that in some months a high number of different speakers speaks in parliament). Especially the temporal development visible in the figure is interesting. It shows that in Czech Republic, Denmark, Spain, Italy, Lithuania and the Netherlands, the relative number of speakers using 'expertise' increases with the spread of the coronavirus (in the months after February 2020). This means that the lemma "expert" was not only used by prime ministers and health ministers, but also by an increasing number of other MPs. In the case of Spain and the Netherlands this sudden upsurge in topicality declines after April 2020. In other countries the relative number of different speakers mentioning 'expert' seems to return to pre-covid levels.



## Expertise in Context: TF-IDF Timelines and Topic Models

Since frequency patterns show only a limited picture, the next step in this research was the mapping of the context of mentions of "expert(ise)" or "science". Two methods were used to do so. First, I used basic TF-IDF for keyword extraction. This enabled the composition of a timeline with key terms from speeches that mention terms such as "virus" and "pandemic". In this way we can reconstruct the contents of the debates that contain words such as 'expertise'.

## Narratives of Expertise: Collocation Analysis

Frequency patterns only reveal the diachronic patterns in the parliamentary 'lifes' of individual words. Topic modelling on the other hand is a more data-driven type of method that is also not the optimal fit for exploring narratives in which terms surrounding 'expert' were used. However, by leveraging the premise of word co-occurrence that underlies topic modelling (and so many other methods in NLP) we can strike a balance between the not-so-informative individual frequencies and the overall topics present in a (subsetted) corpus. 

Collocation analysis revolves around the co-occurrence of units, in this case words. With information on the (relative) frequency of words and their lexical contexts, several measures can be used to calculate association scores. In this research, ````nltk```` was used to generate bigram collocations. The window size was increased to 15 in order to increase the degree to which the algorithm searches for paradigmatic, instead of syntagmatic relations. If we take a more common window of 5, we get high-ranking word pairs such as "corona" + "virus", "global" + "epidemic" or simply "the" + "virus". By increasing the window, words that are related to the seed term but are not necessarily its direct neighbours are also considered.

