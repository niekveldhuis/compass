[TOC]

# 3. Lexical and Literary Vocabularies

In the Old Babylonian period (around 1,800 BCE) scribal students learned how to read and write by copying long lists of cuneiform signs and Sumerian words (lexical lists). In a second stage they copied a broad variety of Sumerian literary texts, including hymns to gods and kings, narrative texts about gods and heroes of the past, and whimsical texts in which non-human entities (such as hoe and plow) dispute their utility for mankind.

By this time Sumerian was a dead language and the whole curriculum has been interpreted as an "invented tradition" - a vision of a golden age, projected in a distant past, when all of Babylonia was imagined to be united under a single king, speaking a single language - Sumerian[^1].

The curricular sequence with lexical exercises followed by literary exercises may suggest that the literary material embodies the real goal of this education and that the lexical texts, enumerating thousands of Sumerian words and expressions, function in support of the students' ability to read, copy, and understand the literary compositions. Yet, it has often been noticed that many words and expressions in the lexical repertoire never appear in literary texts - and the other way around. In the [list of domestic animals](http://oracc.org/dcclt/Q000001), for instance, we find the entry **udu gug-ga-na₂** (sheep for a *guqqanû* offering; line 98). The expression is known from administrative texts in the Ur III period, several centuries earlier (see, for instance, [TLB 03, 095](http://oracc.org/epsd2/admin/u3adm/P134236) o 9), but in the literary corpus the word **gug-ga-na₂** is absent. Many other such examples could be quoted here.

One may draw the conclusion that the "invented tradition" that was the subject of this curriculum not only involved the literary corpus, but also the Sumerian language itself. The lexical corpus functioned in support of the literary corpus but also had a function of its own in preserving as much as possible of Sumerian writing and vocabulary.

Research on bird vocabulary has shown that of the 116 entries in the Old Babylonian [list of birds](http://oracc.org/dcclt/Q000041.405), only 39 can be found in the literary corpus.[^2] This research was mainly done by hand, based on the author's reconstruction of the Old Babylonian bird list and a survey of Sumerian literature - primarily the compositions edited in the Electronic Text Corpus of Sumerian Literature ([ETCSL][]). The challenge of this chapter is: can we scale this analysis up, to include the entire Old Babylonian lexical and literary corpus by using computational methods? And is it possible to use such methods to dig deeper into the relationship between these two corpora and their vocabularies?

## 3.1 Venn Diagrams

In order to compare lexical and literary vocabulary we will draw [Venn diagrams](https://en.wikipedia.org/wiki/Venn_diagram). One circle in the diagram represents all the lemmas found in the literary corpus, the other circle represents all the lemmas of the lexical corpus. The overlap of the two circles indicates the intersection of both.

### 3.1.1 A First Attempt

As a first attempt, we may simply take all Old Babylonian lexical lists from the Digital Corpus of Cuneiform Lexical Texts ([DCCLT][]), extract the full vocabulary and compare that vocabulary to the inventory of words (lemmas) in Sumerian literary texts. The corpus of Sumerian literary texts that we will use is formed by the material currently in [epsd2/literary][]. This includes the compositions edited in [ETCSL][] (excluding the [Gudea Cylinders](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.7&display=Crit&charenc=gcirc#), which were moved to [epsd2/royal](http://oracc.org/epsd2/royal)), the (Sumerian) literary texts published in Ur Excavations Texts Vol. 6/1-3, edited by Jeremiah Peterson, and a somewhat random collection of recently published texts, including most of CUSAS 38.[^3] The [epsd2/literary][] corpus, however, is not frozen (nor is [DCCLT][]) so that repeating this process in the future will necessarily lead to somewhat different results.

We are not concerned with word frequencies - the issue simply is: is this particular word (lemma) attested in literary texts (in [epsd2/literary][]), in (Old Babylonian) lexical texts, or in both.

In order to do so we read the  [epsd2/literary][] and the [DCCLT][] datasets into Pandas DataFrames, using the code developed in section 2.1. The first step is to create a field `lemma` by adding Citation Form,  Guide Word, and Part of Speech in the format **du[build]V/t**, or **lugal[king]N**. Next, we restrict the [DCCLT][] dataset to only Old Babylonian documents by utilizing the catalog. From both datasets we eliminate words that are not in Sumerian (e.g. Akkadian glosses). Finally we extract the new `lemma` field from both datasets and reduce them to their unique elements with the `set()` function: a `set` in Python is an unordered list of unique elements. 

From the two sets, which we call `lit_words_s` and `lexical_words_s` we eliminate all words that have not been lemmatized (unknown words or broken words). We will see in the next section that we will need unlemmatized words in a slightly more sophisticated analysis - but not here. Collections of unique elements can be visualized in a Venn diagram, that shows the two sets as two partly overlapping circles. The overlap represents the intersection of the two sets. This is done with the function `venn2` from the `matplotlib_venn` package, which allows us to select colors and define captions. The result looks like this:

<img src="viz/venn_1.png" alt="venn diagram 1" style="zoom:150%;" />

The Old Babylonian lexical corpus currently has more than 4,000 distinct lemmas, of which almost 60% are shared with the literary corpus. The vocabulary of the literary corpus is only slightly larger. The number of items (lemmas) in both sets will change, because of ongoing improvements and additions in both the literary and the lexical corpus. The Venn diagram above is redrawn whenever Notebook 3_1 is run, and this will update the numbers.

For a number of reasons, this is a very rough estimate and perhaps not exactly what we were looking for. A lexical entry like **udu diŋir-e gu₇-a**  (sheep eaten by a god) consists of three very common lemmas (**udu[sheep]N**, **diŋir[deity]N**, **gu[eat]V/t**). This lexical entry, therefore, will result in three matches, three correspondences between the lexical and literary vocabulary. But what about the lexical *entry*? Does the nominal phrase **udu diŋir-e gu₇-a** or, more precisely, the sequence of the lemmas **udu[sheep]N, diŋir[deity]N, gu[eat]V/t**) ever appear in a literary text? 

### 	3.1.2 Lexical Entries in Literary Context

In order to perform the comparison of lexical and literary vocabularies on the lexical *entry* level we first need to represent the data (lexical and literary) as lines, rather than as individual words. The line in a lexical text will become our unit of comparison by defining each line as a Multiple Word Expression (or MWE). Lines in literary texts will serve as boundaries. Lines in Sumerian literary texts tend to coincide with meaningful semantic (and poetic) units and therefore we will not allow an MWE to continue from one line to the next. 

The first step, therefore, is to group the data by line. This is done with the Pandas functions `groupby()`and `aggregate()`. Once the lexical data are grouped by line the lexical DataFrame will look like this (from the Old Babylonian [list of animals](http://oracc.org/dcclt/Q000001)):

| id_text       | id_line | lemma                                     |
| :------------ | :------ | :---------------------------------------- |
| dcclt/Q000001 | 1       | udu\[sheep\]N niga\[fattened\]V/i             |
| dcclt/Q000001 | 2       | udu\[sheep\]N niga\[fattened\]V/i sag\[rare\]V/i |

We can use this data to look through the literary compositions to see whether there are places where the lemma **udu[sheep]N** is followed by the lemma **niga[fattened]V/i**, or whether we can find the sequence **udu[sheep]N niga[fattened]V/i sag[rare]V/i**, corresponding to the second line in the list of animals. When such a match is found in a literary composition, the lemmas are connected to each other with underscores, so that the sequence can be treated as a unit. Finding and marking such sequences is done with the MWETokenizer from the Natural Language Toolkit ([NLTK](https://www.nltk.org/)) package. The MWETokenizer is initialized with a list of Multiple Word Expressions, which we can easily derive from the lexical data. It then applies this list to the corpus to be tokenized (in this case the [epsd2/literary][] corpus) to connect elements of MWEs by underscores.

Once this is done the lexical entries are treated the same: each space is replaced by an underscore. Now we have the same two sets of data in a slightly different representation and we can do essentially the same analysis as we did above by creating sets (called `lit_words_s2` and `lexical_words_s2`) and then visualize those sets in a Venn diagram: 

<img src="viz/venn_2.png" alt="venn diagram 2" style="zoom:150%;" />

We see that this approach essentially doubles the number of unique elements on the lexical side; on the literary side the increase is much less drastic. It turns out that many of the lexical entries (more than 65%) never appear as such in the literary corpus.

### 3.1.3. Add them Up

Finally we can add the two approaches discussed above into a single Venn diagram. There are words that appear as modifiers in lexical *entries* but never appear on their own in a lexical composition. Similarly, there are words in the literary corpus that occur in phrases known from the lexical corpus, but never outside of such phrases (we will see examples below). Such words, one may argue, potentially add to the intersection between the lexical and literary corpus, but are not represented in the second Venn diagram.

In order to do so we create the union of the first lexical set (individual words) and the second one (lexical expressions), and the same for the literary corpus and then draw a new Venn diagram. The union of two sets is a new set, with all the unique elements from the two original sets. The union sets are called `lit_words_s3` and `lexical_words_s3`.

<img src="viz/venn_3.png" alt="venn diagram 3" style="zoom:150%;" />

The new diagram shows some increase on both sides, and a little increase in overlap as well - but the change is not very dramatic.

So which words are found on the literary side that only appear in MWEs known from lexical sources? We can easily find those by subtracting `lit_words_s2` from `lit_words_s3`. It turns out there are about thirty such words, most of them appearing just once or a few times.

```
{'ašrinna[object]n',
 'ašša[perfect]aj',
 'babbardili[~stone]n',
 'bur[grass]n',
 'burgia[offering]n',
 'du[hold]v/t',
 'ebir[vessel-stand]n',
 'giʾiziʾešta[~bread]n',
 'gub[bathe]v/i',
 'hub[cvve]v/t',
 'huldim[rotten]aj',
 'kašu[~plow]n',
 'kiŋ[pointed]v/i',
 'ligidba[plant]n',
 'manzila[foot]n',
 'maʾu[barge]n',
 'mud[rabid]aj',
 'nir[trust]n',
 'nisaba[1]dn',
 'niŋkalaga[strong]aj',
 'sa.ku[arm]n',
 'sar[shave]v/t',
 'saŋa[priest]n',
 'tuhul[hip]n',
 'tutu[cvve]v/t',
 'ugudili[scalp]n',
 'uzudirig[mushroom]n',
 'zaga[part-of-the-face]n',
 'zana[doll]n',
 'zidsig[flour]n',
 'še[cone]n'}
```

The word `ašrinna[object]n`, for instance, appears only a few times in the current literary corpus: in one of the Eduba dialogues and in proverbs. In each case the word is preceded by `kid[mat]n` and this word sequence is also found in [Old Babylonian Nippur Ura 2](http://oracc.org/dcclt/Q000040), line 20. As a result, the lemma sequence `kid[mat]n_ašrinna[object]n` was treated as a unit, a Multiple Word Expression, and the word `ašrinna[object]n` was found in `lit_words_s1` , but not in `lit_words_s2`.

Our investigation so far has shown that a very considerable portion of lexical words and lexical expressions are not found in the literary corpus as represented by [epsd2/literary][]. Chances are that a good number of them will be found in literary texts that are currently not in [epsd2/literary][] or that are not even known today. However, the lexical corpus is likely to increase, too, and chances that the intersection between those two vocabularies will increase significantly seem slim. Quite puzzling is the large amount of vocabulary on the literary side that is not represented in the lexical corpus. We will investigate the origins of that in the next section.

## 3.2 Literary Compositions and their Relation to Lexical Vocabulary

In order to research the relationship between lexical and literary material in more detail, we will look at individual literary texts. Which compositions have more and which have less overlap with the lexical vocabulary? Is it possible to make meaningful distinctions between literary texts that primarily use vocabulary that is found in the lexical corpus, vs. compositions that do not do so?

### 3.2.1 The Document Term Matrix

In order to address this question we will use a [Document Term Matrix](https://en.wikipedia.org/wiki/Document-term_matrix) (DTM): a huge table, that describes the frequency of terms that occur in a collection of documents. Each row in our DTM represents a literary composition (Document) and each column represents a lemma (Term).

In an artificial example we can transform the following sentences (documents) into a DTM:

> lugal-e e₂ mu-un-du₃ (the king built the temple)
> 
> lugal-e e₂ mu-un-du₃ e₂-gal mu-un-du₃ (the king built the temple and he built the palace)

The DTM, in our case, uses the lemmatized representation of those sentences:

| sentence | du[build]v/t | e[house]n | egal[palace]n | lugal[king]n |
| -------- | --------- | -------- | ------------ | ----------- |
| one      | 1         | 1        | 0            | 1           |
| two      | 2        | 1       | 1            | 1           |

We can now say that sentence one is represented by the vector `[1, 1, 0, 1]` and sentence two by the vector `[2, 1, 1, 1]`. The sum of all the elements in the vector gives us the length of the document in lemmas (3 and 5 respectively) and the number of non-zero elements in the vector gives us the number of unique lemmas in the document (3 and 4, respectively). We may now apply vector operations and vector mathematics on these two sentences - for instance we can compute their cosine similarity (0.873). In real-world examples many slots in the matrix are 0 (there are many words in the corpus that do not appear in this particular document) and many slots are higher than 1 (a word that appears in a document is likely to appear more than once). Note that each *word* (or lemma) is now also characterized by a vector, represented by the numbers in a column.

In our case, we will use the DTM to count the number of matches between each literary composition and the lexical vocabulary. In building the DTM of the [epsd2/literary][] corpus we will use the lexical vocabulary: the columns of the DTM represent words and MWEs present in the lexical corpus, the rows represent the documents in the literary corpus. Because each column in the DTM represents a word or MWE in the lexical corpus, there are many columns that have only zeros (lexical entries that do not occur in [epsd2/literary][]). In terms of the Venn diagrams discussed in 3.1, the zero-value columns in our DTM represent the blue area to the right, the non-zero ones represent the middle area (intersection of the lexical and literary vocabulary); the yellow area (words in [epsd2/literary][] that do not appear in the Old Babylonian lexical corpus) is not represented in the DTM. 
<img src="viz/venn_3.png" alt="venn diagram 3" style="zoom:150%;" />

The main difference between the Venn diagram and the DTM is that the DTM shows in which compositions the shared words are attested. By counting the number of non-zero cells in a row we get an integer that represents the number of unique lexically attested lemmas in a particular composition, and this gives us a (numerical) measure for comparing between compositions. Not surprisingly, a longer composition, such as [Ninurta's Exploits](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.6.2&display=Crit&charenc=gcirc#) (726 lines) has more such matches than shorter ones. In fact, the very short ones (some consist of only a few words) are not very useful for the comparison - we will restrict the analysis to texts that are above a certain threshold in length. We will therefore include in the table below for each literary document its *text length* (number of lemmas and MWES) and *lexical variation* (number of unique lemmas and MWEs). The column `norm` represents the number of matches divided by the number of unique lemmas. `Norm` may therefore be interpreted as the percentage of lemmas and MWEs present in a literary document that are attested lexically in the Old Babylonian period.

### 3.2.2 Exploring Results

The table below gives the first ten compositions, sorted by `norm` (descending), at a minimum text length of 200 lemmas and MWEs . Of the 96 unique lemmas that are attested in [Inana E](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.4.07.5&display=Crit&charenc=gcirc#) no less than 95 are also attested in the Old Babylonian lexical corpus - a `norm` score of 0.99.

| id_text                                            | designation                                               |   length |   lex_var |   n_matches |   norm |
|----------------------------------------------------|-----------------------------------------------------------|----------|-----------|-------------|--------|
| [Q000626](http://oracc.org/epsd2/literary/Q000626) | A tigi to Inana (Inana E)                                 |      296 |        96 |          95 |  0.99  |
| [Q000695](http://oracc.org/epsd2/literary/Q000695) | A tigi to Nergal (Nergal C)                               |      209 |        96 |          94 |  0.979 |
| [P346203](http://oracc.org/epsd2/literary/P346203) | ETCSL 2.05.04.23 Ishme-Dagan W (witness)                  |      214 |       124 |         120 |  0.968 |
| [Q000818](http://oracc.org/epsd2/literary/Q000818) | Proverbs: collection 26                                   |      238 |       158 |         153 |  0.968 |
| [Q000756](http://oracc.org/epsd2/literary/Q000756) | The advice of a supervisor to a younger scribe (Edubba C) |      401 |       211 |         204 |  0.967 |
| [Q000668](http://oracc.org/epsd2/literary/Q000668) | A šir-gida to Martu (Martu A)                             |      279 |       182 |         176 |  0.967 |
| [Q000785](http://oracc.org/epsd2/literary/Q000785) | The three ox-drivers from Adab                            |      268 |        91 |          88 |  0.967 |
| [Q000384](http://oracc.org/epsd2/literary/Q000384) | An adab to Bau for Luma (Luma A)                          |      232 |        78 |          75 |  0.962 |
| [Q000494](http://oracc.org/epsd2/literary/Q000494) | An adab to An for Ur-Ninurta (Ur-Ninurta E)               |      211 |       133 |         128 |  0.962 |
| [Q000788](http://oracc.org/epsd2/literary/Q000788) | A man and his god                                         |      560 |       235 |         226 |  0.962 |

> Note that changes in the [epsd2/literary][] and [DCCLT][] data may change the numbers and the arrangement of the table.

In the notebook one may manipulate the table to sort by different columns (ascending or descending), adjust minimum text length or display a larger or smaller number of rows. Looking at the descriptive statistics of the `norm` variable may give us some idea of how the values are distributed.

```
count    203.000000
mean       0.911294
std        0.052470
min        0.359833
25%        0.898747
50%        0.918182
75%        0.934008
max        0.989583
Name: norm, dtype: float64
```

The 25%, 50%, and 75% point are all very close to each other - the great majority of values are on the (very) high side of the scale, with only a few outliers at the bottom. A histogram of the values visualizes that: 

<img src="viz/hist_norm.png" alt="Histogram of norm" style="zoom:150%;" />

Looking at the bottom of the table we find that the compositions ranking lowest on `norm` are the following:

| id_text                                            | designation                                                          |   length |   lex_var |   n_matches |   norm |
|----------------------------------------------------|----------------------------------------------------------------------|----------|-----------|-------------|--------|
| [Q000371](http://oracc.org/epsd2/literary/Q000371) | The Sumerian king list                                               |     1049 |       239 |          86 |  0.36  |
| [Q000372](http://oracc.org/epsd2/literary/Q000372) | The rulers of Lagaš                                                  |      405 |       179 |         131 |  0.732 |
| [Q000752](http://oracc.org/epsd2/literary/Q000752) | A hymn to the E-kur                                                  |      244 |        61 |          46 |  0.754 |
| [Q000559](http://oracc.org/epsd2/literary/Q000559) | Letter from Puzur-Šulgi to Ibbi-Suen about Išbi-Erra's claim on Isin |      205 |       107 |          82 |  0.766 |
| [Q000336](http://oracc.org/epsd2/literary/Q000336) | Enlil and Ninlil                                                     |      674 |       169 |         140 |  0.828 |
| [Q000632](http://oracc.org/epsd2/literary/Q000632) | A balbale to Inana (Dumuzid-Inana A)                                 |      212 |        59 |          49 |  0.831 |
| [Q000750](http://oracc.org/epsd2/literary/Q000750) | The temple hymns                                                     |     2490 |       696 |         582 |  0.836 |
| [Q000651](http://oracc.org/epsd2/literary/Q000651) | A kungar to Inana (Dumuzid-Inana T)                                  |      236 |       113 |          97 |  0.858 |
| [Q000746](http://oracc.org/epsd2/literary/Q000746) | A šir-namšub to Utu (Utu E)                                          |      331 |       127 |         109 |  0.858 |
| [Q000380](http://oracc.org/epsd2/literary/Q000380) | The lament for Sumer and Ur                                          |     2646 |       739 |         634 |  0.858 |

[The Sumerian King List](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.1&display=Crit&charenc=gcirc#) is the outlier with only 86 matches on 239 unique lemmas and a `norm` score of 0.36. [The Sumerian King List](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.1&display=Crit&charenc=gcirc#) is a rather repetitive composition that enumerates the names of kings and the cities from which they reigned, recording regnal years with, occasionally, a brief (one-line) anecdote about one of those kings. Proper nouns, including royal names and city names, are currently underrepresented in the (lemmatized) lexical corpus. The proper nouns in [The Sumerian King List](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.1&display=Crit&charenc=gcirc#) explain the large number of lemmas not attested in the Old Babylonian lexical corpus in [DCCLT][]. The next composition ([The Rulers of Lagaš](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.2&display=Crit&charenc=gcirc#)) has a `norm` score that is significantly higher, but still low comparatively speaking. [The Rulers of Lagaš](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.2&display=Crit&charenc=gcirc#) is molded on the pattern of the [The Sumerian King List](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.1&display=Crit&charenc=gcirc#) and equally features a relatively large number of proper nouns.

After these two lowest scoring texts, the rest of the [epsd2/literary][] corpus scores at least 0.75, with a median value of 0.92 and a mean of 0.91. In the great majority of cases more than ninety percent of the words and expressions in a literary composition are represented in the lexical corpus. Some of the non-overlap between the two corpora, moreover, may be explained by Proper Nouns, or the use of Emesal, a variety of Sumerian used in liturgical laments and by female speakers (Emesal is very rare in the Old Babylonian lexical corpus).

This yields a picture that is rather different from the Venn diagrams in section 3.1, where we looked at the intersection of the full vocabulary of [epsd2/literary][] against the full vocabulary of (lemmatized) Old Babylonian lexical texts in [DCCLT][]. The Venn diagrams showed that only between 55 and 65% (depending on how we count) of the [epsd2/literary][] vocabulary is found in the Old Babylonian lexical corpus in [DCCLT][], but looking in more detail we realize that the relationship between literary compositions and the contemporary lexical corpus is much tighter and that each composition by itself, on average, shares more than 90% of its vocabulary with the lexical corpus. 

### 3.2.3 Dumuzid's Dream

How is it possible to arrive at such different percentages, using the same data set? It means that for any particular composition a good deal of the 90% of vocabulary items that is shared with the lexical corpus is also shared with at least some other compositions, whereas the 10% of items not shared may well be unique to that composition.

in order to investigate this further we may look at one particular composition, known as [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#). This composition is well-preserved with about 60 exemplars that derive from Nippur, Ur, and other places.[^4] This composition is fairly well preserved and has a `norm` value of 0.94, slightly above the median value of 0.92.

This is the set of lemmas (n = 16) currently not found in the lexical corpus:
```python
{'amaŋeštinanak[1]dn',
 'arali[1]gn',
 'dubban[fence]n',
 'durtur[1]dn',
 'kubireš[1]gn',
 'kubirešdildareš[1]gn',
 'mašuzudak[goat]n',
 'men[go]v/i',
 'ne[cvne]n',
 'sug[full]v/i',
 'zipatum[cord]n',
 'ŋeštindudu[1]dn',
 'šarag[dry]v/t',
 'še[tear]n',
 'širkalkal[subscript]n',
 'šudu[handcuffs]n'}
```
We may notice, first, that there are three geographical names (Arali, Kubireš and Kubirešdildareš) and three divine names (Amaŋeštinanak, Durtur, and Ŋeštindudu) in this list, as well as an Emesal word (**men\[go\]v/i**). The geographical name Arali is, in fact, to be found in [Old Babylonian Nippur Izi](http://oracc.org/dcclt/Q000050) I 394 among other terms that denote the realm of the dead. In Izi it has been lemmatized as a noun, rather than as a geographical name, preventing the match.

The divine name Amaŋeštinanak appears in line 83 of [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#), where it is written **ama-{d}ŋeštin-an-na**. Although this Divine Name is known from a number of instances in third millennium administrative and royal texts, this is the only place in the Old Babylonian corpus where it appears. The placement of the divine determinative (in the transliteration represented by {d}) indicates that **ama** is more probably a separate word, not part of the name. The Sumerian word **ama** means mother and is likely a honorific here (see, for instance, the translation by [P. Attinger](https://doi.org/10.5281/zenodo.2599639)). The Divine Name Ŋeštinanak ({d}ŋeštin-an-na) is well known, and is attested in Old Babylonian lexical texts (for instance in the [Nippur God List](http://oracc.org/dcclt/Q000261) line 185). In fact, she is one of the main characters in [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#).

The lemma **men[go]v/i** is an example of an Emesal lemma. It appears in [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#) in the imperative plural form **ŋa₂-nam-ma-an-ze₂-en** "You all go!" (line 140 and parallels) in an address spoken by the demons in search of Dumuzid. That this really is an Emesal form, however, is questionable and most likely an error in the transformation from the [ETCSL][] source data to the [epsd2/literary][] format. Treating this form as a regular form of the Sumerian lemma **ŋen\[go\]v/i** (as [ETCSL][] does) makes it into a very common lemma that is found all over the place in the Old Babylonian lexical corpus (although this particular form is currently not found there).

There are, in other words, a good number of instances where the particularities and mistakes of the edited corpora prevent additional matches, and the `norm`value of 0.94 may well underestimate the role of lexically attested words in [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#).

This is not say that there are no such non-matching words or expressions in [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#). The lemma **zipatum\[cord\]n** is one such example. This word appears three times in [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#) (in the same repeated phrase) and in Enki and the Turtle (not in the current corpus), but is not currently found in the Old Babylonian lexical corpus. More remarkable is the absence of **še[tear]n**, a word that only appears in the expression **šeₓ(SIG₇)-šeₓ(SIG₇) ... ŋa₂-ŋa₂** which means to sob or to cry. This is a fairly common, perhaps onomatopoetic, representation of the sound of sobbing.[^5]

The discussion of the non-matching words in [Dumuzid's Dream](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.3&display=Crit&charenc=gcirc#) suggests that the average `norm` value of 0.91 may well be an underestimation and that the literary corpus sticks very close to the vocabulary found in the contemporary literary corpus. As a corollary, there is little chance that we can find meaningful distinctions between different groups of literary compositions based on lexically attested vocabulary. 



## 3.3 Distinctions between Lexical Compositions

In the previous section it was shown that there are few significant differences between Old Babylonian literary texts in the way their vocabulary connects to contemporary lexical sources. In this section we will change the perspective and ask whether there are such differences that can be detected among lexical texts - in other words: are some lexical texts more attuned to the literary vocabulary than others?

In order to do so we will approach the lexical corpus more or less in the same way as we did the literary corpus in the previous section, using  much of the same code. Instead of using Multiple Word Expressions we will use [ngrams](https://en.wikipedia.org/wiki/N-gram) - a ngram is a sequence of *n* consecutive words (or lemmas). The function that builds the DTM can also count ngrams of any length.

For this analysis we will count ngrams from n=1 to n=5. That will create a DTM with a column for each lemma (ngram n=1), but also for each sequence of two lemmas (bigram; n=2), three lemmas (trigram; n=3), etc. - up to five. The entry **amar ga gu₇-a** ([OB Nippur Ura 3](http://oracc.org/dcclt/Q000001) line 225), lemmatized as `amar[young]n ga[milk]n gu[eat]v/t` ("suckling calf") will be represented as :

| type    | representation                          |
| ------- | --------------------------------------- |
| unigram | amar\[young\]n                          |
|         | ga\[milk\]n                             |
|         | gu\[eat\]v/t                            |
| bigram  | amar\[young\]n ga\[milk\]n              |
|         | ga\[milk\]n gu\[eat\]v/t                |
| trigram | amar\[young\]n ga\[milk\]n gu\[eat\]v/t |

For longer entries we will also get 4-grams and 5-grams. 

A three word entry which was treated as a single unit in 3.1 and 3.2 now results in 6 columns in the Document Term Matrix. 

Similar to the process in section 3.2, we will compute for each lexical document the number of lemmas and ngrams that are attested in the literary corpus. 

In the notebook one may manipulate the table to sort by different columns (ascending or descending), adjust minimum text length, display a larger or smaller number of rows, and select for composites only, exemplars only, or all.

| id_text                                   | designation     | subgenre               | n_matches | length | norm     |
| ----------------------------------------- | --------------- | ---------------------- | --------- | ------ | -------- |
| [P228842](http://oracc.org/dcclt/P228842) | MSL 14, 018 Bb  | OB Nippur Ea           | 333       | 410    | 0.812195 |
| [Q000055](http://oracc.org/dcclt/Q000055) | OB Nippur Ea    | Sign Lists             | 599       | 779    | 0.768935 |
| [Q000056](http://oracc.org/dcclt/Q000056) | OB Nippur Aa    | Sign Lists             | 231       | 408    | 0.566176 |
| [P447992](http://oracc.org/dcclt/P447992) | OECT 04, 152    | OB Diri Oxford         | 145       | 293    | 0.494881 |
| [Q000050](http://oracc.org/dcclt/Q000050) | OB Nippur Izi   | Acrographic Word Lists | 688       | 1400   | 0.491429 |
| [P247810](http://oracc.org/dcclt/P247810) | IB 1514         | OB Lu                  | 133       | 274    | 0.485401 |
| [Q002268](http://oracc.org/dcclt/Q002268) | OB Nippur Ugumu | Thematic Word Lists    | 163       | 348    | 0.468391 |
| [Q000057](http://oracc.org/dcclt/Q000057) | OB Nippur Diri  | Sign Lists             | 278       | 594    | 0.468013 |
| [Q000052](http://oracc.org/dcclt/Q000052) | Nippur Nigga    | Acrographic Word Lists | 391       | 844    | 0.46327  |
| [Q000048](http://oracc.org/dcclt/Q000048) | OB Nippur Kagal | Acrographic Word Lists | 447       | 1015   | 0.440394 |

When ordered by `norm` the top of the list is formed by lexical compositions such as the sign lists [OB Nippur Ea](http://oracc.org/dcclt/Q000055) and [OB Nippur Diri](http://oracc.org/dcclt/Q000057), the acrographic list/list of professions [OB Nippur Lu](http://oracc.org/dcclt/Q000047), and the acrographic lists [OB Nippur Izi](http://oracc.org/dcclt/Q000050), and [OB Nippur Kagal](http://oracc.org/dcclt/Q000048), or (large) exemplars of such compositions. All these lexical texts belong to what Jay Crisostomo has labeled "ALE": Advanced Lexical Exercises[^4]. These exercises were studied in the advanced first stage of education, just before students would start copying literary compositions. If we restrict the DataFrame to composites (Q numbers) only, this comes out even clearer. 

| id_text                                   | designation       | subgenre               | n_matches | length | norm     |
| ----------------------------------------- | ----------------- | ---------------------- | --------- | ------ | -------- |
| [Q000055](http://oracc.org/dcclt/Q000055) | OB Nippur Ea      | Sign Lists             | 599       | 779    | 0.768935 |
| [Q000056](http://oracc.org/dcclt/Q000056) | OB Nippur Aa      | Sign Lists             | 231       | 408    | 0.566176 |
| [Q000050](http://oracc.org/dcclt/Q000050) | OB Nippur Izi     | Acrographic Word Lists | 688       | 1400   | 0.491429 |
| [Q002268](http://oracc.org/dcclt/Q002268) | OB Nippur Ugumu   | Thematic Word Lists    | 163       | 348    | 0.468391 |
| [Q000057](http://oracc.org/dcclt/Q000057) | OB Nippur Diri    | Sign Lists             | 278       | 594    | 0.468013 |
| [Q000052](http://oracc.org/dcclt/Q000052) | Nippur Nigga      | Acrographic Word Lists | 391       | 844    | 0.46327  |
| [Q000048](http://oracc.org/dcclt/Q000048) | OB Nippur Kagal   | Acrographic Word Lists | 447       | 1015   | 0.440394 |
| [Q000047](http://oracc.org/dcclt/Q000047) | OB Nippur Lu      | Thematic Word Lists    | 608       | 1459   | 0.416724 |
| [Q000302](http://oracc.org/dcclt/Q000302) | OB Lu₂-azlag₂ B-C | Thematic Word Lists    | 363       | 1040   | 0.349038 |
| [Q000041](http://oracc.org/dcclt/Q000041) | OB Nippur Ura 04  | Thematic Word Lists    | 343       | 983    | 0.348932 |

The thematic lists collected in [Ura](http://oracc.org/dcclt/Q000039,Q000040,Q000001,Q000041,Q000042,Q000043) (lists of trees, wooden objects, reeds, reed objects, clay, pottery, hides, metals and metal objects, animals, meat cuts, fish, birds, plants, etc.) have much lower `norm` values and thus less overlap with literary vocabulary. The lists that belong to [Ura](http://oracc.org/dcclt/Q000039,Q000040,Q000001,Q000041,Q000042,Q000043) are studied in a more elementary phase of scribal education and are further removed from the literary corpus, both in vocabulary and in curricular terms.

One might entertain the possibility that the vocabulary of [Ura](http://oracc.org/dcclt/Q000039,Q000040,Q000001,Q000041,Q000042,Q000043) is closer to the administrative corpus, whereas the ALE compositions tend to be closer to the literary vocabulary. In 1959, J.B. Curtis and W.W. Hallo already noticed that the great majority of the commodities in the Ur III merchants' accounts that they edited is found in Ura. Anecdotally, the idea of a connection between Ur III accounts and the contents of Ura may be supported by a number of striking observations. For instance, the Old Babylonian entry **ha-zi-in gu₂ bir₅-ra{mušen}{zabar}** (axe made of locust-neck bronze) is found in two Ur III texts, one from Umma ([TCL 05, 6055](http://oracc.org/epsd2/admin/ur3/P131769)) and one from Drehem ([MMFM 2005, 24, 5](http://oracc.org/epsd2/admin/ur3/P113021)). More than sixty years after the article by Curtis and Hallo was published, we are now in a position to approach such an idea systematically.

For com parison it is useful to look at matches between administrative documents and lexical compositions. The administrative corpus selected is the Ur III corpus, dating, approximately, to the twenty-first century BCE. It would be more ideal to use the Old Babylonian administrative corpus, in particular texts from Isin, Nippur, and other Southern cities that were still composed in Sumerian. This corpus, however, has not been fully edited on [ORACC][] and is much smaller than the Ur III corpus. For a rough impression it may not make a big difference.

| id_text                                   | designation      | subgenre               | length | n_matches | norm     |
| ----------------------------------------- | ---------------- | ---------------------- | ------ | --------- | -------- |
| [Q000055](http://oracc.org/dcclt/Q000055) | OB Nippur Ea     | Sign Lists             | 779    | 439       | 0.563543 |
| [Q000056](http://oracc.org/dcclt/Q000056) | OB Nippur Aa     | Sign Lists             | 408    | 180       | 0.441176 |
| [Q000040](http://oracc.org/dcclt/Q000040) | OB Nippur Ura 02 | Thematic Word Lists    | 1182   | 434       | 0.367174 |
| [Q000047](http://oracc.org/dcclt/Q000047) | OB Nippur Lu     | Thematic Word Lists    | 1459   | 485       | 0.332419 |
| [Q000039](http://oracc.org/dcclt/Q000039) | OB Nippur Ura 01 | Thematic Word Lists    | 1289   | 423       | 0.328161 |
| [Q000041](http://oracc.org/dcclt/Q000041) | OB Nippur Ura 04 | Thematic Word Lists    | 983    | 314       | 0.31943  |
| [Q000048](http://oracc.org/dcclt/Q000048) | OB Nippur Kagal  | Acrographic Word Lists | 1015   | 324       | 0.319212 |
| [Q000052](http://oracc.org/dcclt/Q000052) | Nippur Nigga     | Acrographic Word Lists | 866    | 259       | 0.299076 |
| [Q000001](http://oracc.org/dcclt/Q000001) | OB Nippur Ura 03 | Thematic Word Lists    | 1034   | 300       | 0.290135 |
| [Q002268](http://oracc.org/dcclt/Q002268) | OB Nippur Ugumu  | Thematic Word Lists    | 348    | 96        | 0.275862 |

## 3.4 Some Final Thoughts

The issue of the intersection between lexical and literary vocabulary turns out to be more complex than a simple count of words. In all computational work issues of definition become central: what counts as a match, and how do we make sure that we exclude, as much as possible, false positives and false negatives?   I took advantage of the undefined nature of what a "match" is (a word? a lemma? an entry?) to introduce two different ways of considering matches that consist of more than one word, Multiple Word Expressions (essentially reducing such an expression to a single token) and ngrams (counting both the individual words and combinations of words found in sequence). Both of these approaches will identify and match compound nouns and compound verbs, with or without morphology - but neither of them will be able to match the expression **mi₂ dug₄** (to care for) with **mi₂ zid dug₄** (to truly care for), because of the intervening lemma. Other types of analysis could be developed to take care of such situations. For now, the point is: each technique has its limitations and it will never completely match the interpretation of a human reader.

Moreover, computational results can never be more reliable than the data on which they are based. Inconsistencies in large datasets are unavoidable - as we have seen - but still the computations lead to interpretable results. The volume of the data is canceling out a few errors or inconsistencies here or there. This is a line of reasoning that is still uncommon in Assyriology where errors are regarded with great suspicion. 

# Footnotes

[^1]: 	N. Veldhuis, *Religion, Literature, and Scholarship: The Sumerian Composition "Nanše and the Birds"*. Cuneiform Monographs 22. Leiden: Brill 2004.
[^2]:	N. Veldhuis, *Religion, Literature, and Scholarship: The Sumerian Composition "Nanše and the Birds"*. Cuneiform Monographs 22. Leiden: Brill 2004.
[^3]:	C. Metcalf, *Sumerian Literary Texts in the Schøyen Collection: Volume 1: Literary Sources on Old Babylonian Religion*. Cornell University Studies in Assyriology and Sumerology. Winona Lake: Eisenbrauns 2019. 
[^4]: 	Attinger, Pascal. (2019, March 1). Edubba'a A (5.1.1). Zenodo. https://doi.org/10.5281/zenodo.2599639.
[^5]:	George, Andrew (2002) 'How women weep? Reflections on a passage of Bilgames and the Bull of Heaven.' In: Parpola, S and Whiting, R, (eds.), *Sex and Gender in the Ancient Near East.* Helsinki: University Helsinki (Finland), pp. 141-150.
[^6]: 	J. Crisostomo, *Translation as Scholarship. Language, Writing, and Bilingual Education in Ancient Babylonia*. Studies in Ancient Near Eastern Records (SANER), 22. De Gruyter 2019; https://doi.org/10.1515/9781501509810.


[ETCSL]: http://etcsl.orinst.ox.ac.uk
[DCCLT]: http://oracc.org/dcclt
[epsd2/literary]: http://oracc.org/epsd2/literary
```

```