# 5 Topic Modeling State Archives of Assyria

*Topic modeling* is an unsupervised technique for identifying abstract topics in a set of documents.  In this chapter we will exemplify the process with the corpus of texts published in the series State Archives of Assyria ([SAAo](http://oracc.org/saao)). Notebook 5.1 will download and parse the text material, using the techniques discussed in section 2.1. Notebook 5.2 will build the actual topic model and 5.3 will demonstrate several types of visualizations that may help in exploring and analyzing the model.

Typically, the output of a topic model will list words and probabilities - the high probability words characterize the topic. Such an output may look like this (five out of ten topics displayed):

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

The process is unsupervised and language agnostic - it is the task of the researcher to make some sense of the results. The visualizations (section 5.3) are designed to help with that process.

The most commonly used topic modeling technique is called LDA, or Latent Dirichlet Allocation. LDA takes each document in a corpus as a so-called Bag of Words, that is, it abstracts from word order, and syntax, taking into account only the frequencies of  words in that document. Usually, LDA is performed on a corpus that is lemmatized or stemmed, so that it also abstracts from morphology.

Prior to running the LDA process one has to estimate a reasonable number of topics. This is a somewhat arbitrary aspect of topic modeling. A low number of topics will likely result in strange mixtures of words that may represent multiple topics. A high number of topics may result in some very clear topics, with high-ranking words that clearly cohere around a theme, and then a good number of other topics that seem to collect random words.

Once the number of topics is chosen three basic quantities are known: the number of Topics (K), the number of unique lemmas (L), and the number of documents (D). The goal of the LDA process is to construct two tables: the Topic-Term table (a matrix of dimensions K x L), where each row represents a topic and each column a lemma, and the Document-Topic table (a matrix of dimensions D x K), where each row represents a document and each column a topic. Each cell in the Topic-Term table indicates the probability of a particular lemma in a particular topic.  Each cell in the Document-Topic table indicates the probability of a particular topic in a particular document. 

The table is built by, initially, assigning a random topic to each word (each token) in the entire corpus. If there are 10 topics and the lemma abnu[stone]N appears 100 times, we may expect approximately 10 abnu[stone]N tokens in each topic, and the initial probability for this lemma is approximately 0.1 (10/100) for each topic. However, since the allocation is random, some topics will have only 7 tokens, others 12 or 13, meaning that the initial probability of this lemma in each of the topics will vary between, for instance, 0.07 and 0.13. Similarly, since each word is allocated to a topic randomly, on average each document has 10% of its words allocated to each topic. But again, this only on average - in practice in each document some topics will have a slightly higher prevalence and others a somewhat lower. In a second round each word (token) is again allocated to a topic, but now the allocation uses two weighting factors: first, the prominence of each topic in the document and second the probability of the lemma in each topic. Assume that document n had an initial (random) topic distribution as follows (note that the sum of the row is always 1):

|       | Topic 0 | Topic 1 | Topic 2 | Topic 3 | Topic 4 | Topic 5 | Topic 6 | Topic 7 | Topic 8 | Topic 9 |
| ----- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| Doc n | 0.1     | 0.08    | 0.07    | 0.13    | 0.11    | 0.09    | 0.08    | 0.12    | 0.1     | 0.12    |

In allocating a token to a topic in this second round, chances that a token in this document will end up in Topic 3, 7, or 9 are higher than that it will end up in 2, 1, or 6. Similarly, the lemma abnu[stone]N may (by chance) have been allocated more frequently to one topic or another and that will also influence the weights when the token abnu[stone]N in document n is re-allocated.

State Archives of Assyria ([SAAo](http://oracc.org/saao)) is an interesting test case for topic modeling because it includes a wide variety of genres and text types, while at the same time deriving from the same, well-defined origin - the Assyrian court. The corpus includes diplomatic letters, letters by scholars on ritual matters, observations of astronomical phenomena, contracts, administrative text, divinatory requests, etc.

Each of these text groups may be characterized by a particular vocabulary, a set of words that is typically used to talk about astronomy, war, health,  or divination. Or, to be more precise, the *probability* of a word like sisu[horse]N is higher in military contexts than it is in the context of an inquiry about the king's health and topic modeling should be able to figure that out.

Topic modeling may thus be used to divide a large corpus into groups (documents that share a preference for words scoring high in a particular topic) or to get a rough idea of what a corpus is about - what themes (topics) are present in the corpus.

A few words of caution are in order. First, the requirement to select the number of topics beforehand is one of the Achilles heals of LDA.  Changing K will changes the probability distributions and changes everything that is done with the model downstream (for instance text classification). Second, LDA is a non-deterministic process. That means that a new run with the same data and the same K will still produce a somewhat different result. Although the topics may be fairly similar, the order in which the topics are assigned are certainly not (that is, what was topic 5 in one run, may become topic 8 in the next). In order to make the process reproducible one may choose a `seed`, a number that will ensure that the process starts at the same point. This 'solution' however, inserts a rather arbitrary element in the whole process. Choosing a different seed results in a different model. It is worth experimenting with both K and the seed, to see how much the models differ from each other.