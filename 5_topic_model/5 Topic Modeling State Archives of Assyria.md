# 5 Topic Modeling State Archives of Assyria

*Topic modeling* is an unsupervised technique for identifying abstract topics in a set of documents. Typically, the output of a topic model will list words and probabilities - the high probability words characterize the topic. Such an output may look like this:

```python
[(0,
  '0.044*"qû[unit]n" + 0.027*"šikaru[beer]n" + 0.027*"ilu[god]n" + 0.025*"karānu[vine]n" + 0.022*"šamnu[oil]n" + 0.020*"kusāpu[bread]n" + 0.018*"zamāru[sing]v" + 0.016*"naqû[pour-(a-libation)]v" + 0.015*"dišpu[honey]n" + 0.014*"qātu[hand]n"'),
 (1,
  '0.069*"nišu[people]n" + 0.064*"imēru[unit]n" + 0.048*"eqlu[field]n" + 0.043*"immeru[sheep]n" + 0.042*"ikkaru[farmer]n" + 0.035*"alpu[ox]n" + 0.029*"kirû[garden]n" + 0.029*"sinništu[woman]n" + 0.023*"lawû[surround]v" + 0.022*"qabūtu[bowl]n"'),
 (2,
  '0.076*"rabû[big-one]n" + 0.069*"sisû[horse]n" + 0.036*"pīhātu[responsibility]n" + 0.025*"ša-rēši[eunuch]n" + 0.024*"ša-qurbūti[close-follower]n" + 0.021*"ṣābu[people]n" + 0.018*"ēkallu[palace]n" + 0.018*"kiṣru[knot]n" + 0.018*"šaknu[appointee]n" + 0.017*"qātu[hand]n"'),
 (3,
  '0.063*"rabû[big]aj" + 0.040*"ilūtu[divinity]n" + 0.029*"šalmu[intact]aj" + 0.027*"immeru[sheep]n" + 0.026*"luʾʾû[sullied]aj" + 0.021*"pû[mouth]n" + 0.019*"bīru[divination]n" + 0.016*"qātu[hand]n" + 0.015*"kīnu[permanent]aj" + 0.014*"apālu[pay]v"'),
 (4,
  '0.069*"mātu[land]n" + 0.048*"ilu[god]n" + 0.031*"rabû[big]aj" + 0.024*"pû[mouth]n" + 0.017*"kīnu[permanent]aj" + 0.017*"damqu[good]aj" + 0.015*"ridûtu[appropriation]n" + 0.013*"qaqqaru[ground]n" + 0.013*"abu[father]n" + 0.012*"qarnu[horn]n"'),
```

Each topic (indicated here with the numbers 0 to 4) is characterized by a number of words, listed in descending probability. Each word that is available in the corpus is assigned some probability in each topic - only the highest scoring words are shown here. One can see that in topic 0 words that relate to food and drink, and other provisions for the god score high. Topic 2, on the other hand, seems concerned with the military.

The process is unsupervised and language agnostic - it is the task of the researcher to make some sense of the results. In this chapter we will look at various ways in which a topic model can be visualized. One such visualization essentially comes out-of-the-box in the form of the pyLDAvis package, which does an excellent job in creating graphs that clarify the relationship between words and topics. In addition, we will create custom visualization that focus on the relationship between topics and documents.

The main topic modeling technique is called LDA, or Latent Dirichlet Allocation. 

In this chapter we will create a topic model for the documents in the State Archives of Assyria ([SAAo](http:oracc.org/saao)). This is a group of more than 4,000 documents that derive from a particular context (the Assyrian royal court), but include a wide variety of text types, such as letters on military or political matters, letters by scholars on ritual affairs, astronomical reports, administrative texts, contracts, and divinatory queries. We wull use various types of visualizations to help explore the model.

The most common topic modeling technique is called LDA, short for Latent Dirichlet Allocation. LDA takes each document in a corpus as a so-called Bag of Words, that is, it abstracts from morphology, word order, and syntax, taking into account only the frequencies of  words in that document. In most topic modeling projects the first step is preprocessing the data: removing punctuation and other extraneous elements and reducing the words to their stems or lemmas. Since we work with lemmatized data from [ORACC](http://oracc.org) those steps will be unnecessary.

In order to run the LDA process one has to estimate a reasonable number of topics. This is a somewhat arbitrary aspect of topic modeling. A low number of topics will likely result in strange mixtures that are difficult to interpret. A high number of topics may result in some very clear topics, with high-ranking words that clearly cohere around a theme, and then some other topics that seem to collect random words.

Each group of texts may be characterized by a particular vocabulary, a set of words that is typically used to talk about astronomy, war, health,  or divination. Or, to be more precise, the *probability* of a word like sisu[horse]N is higher in military contexts than it is in the context of an inquiry about the king's health. Topic Modeling will distribute the probability of each word that appears in the corpus over *N* topics. The value of *N* is chosen by the user. The process is non-deterministic in that a repeated run of the same script leads to different results. The 'topics essentially consist of hte words with the highest scoring probability in that topic.

Topic modeling may thus be used to divide a large corpus into groups (documents that share a preference for words scoring high in a particular topic) or to get a rough idea of what a corpus is about - what themes (topics) are present in the corpus.

 Words that frequently appear together in the same documents are more likely to appear in the same topic.

LDA results in two tables with probability distributions. The Topic/Term table indicates for each term (or word) available in the corpus the probability that this word belongs to a particular topic. If there are N topics and the corpus has M unique terms, the Topic/Term table is a M by N matrix. The sum of each row (representing a topic) in the matrix is 1, that is, the probability of the word is distributed over all topics [**#CHECK is this correct?**]. Probabilities in this matrix are never 0 or 1 - each word has some probability (even if minimal) to appear in each topic. The second table is the Document/Topic table which indicates for each topic the probability that it appears in a particular document. If there are N topics and D documents, this is a N by D matrix.  