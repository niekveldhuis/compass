[TOC]

# 3. Lexical and Literary Vocabularies

In the Old Babylonian period (around 1,800 BCE) scribal students learned how to read and write by copying longs lists of signs and words (lexical lists). In a second stage they would start copying a broad variety of Sumerian literary texts, including hymns to gods and kings, narrative texts about gods and heroes of the past, and whimsical texts in which hoe and plow (or other non-human entities) dispute their utility for mankind.

Since Sumerian by this time was a dead language, the whole curriculum (lexical lists and literary texts together) has been interpreted as looking back at a golden age, and creating an "invented tradition" - a period when all of Babylonia was united under a single king, speaking a single language - Sumerian.

The sequence lexical exercises - literary exercises suggests that the literary material embodies the real goal of this education and that the lexical texts, enumerating thousands of Sumerian words and expressions, function in support of the students' ability to read, copy, and understand the literary texts. Yet, it has often been noticed that many words in the lexical repertoire never appear in literary texts - and the other way around. In the [list of domestic animals](http://oracc.org/dcclt/Q000001), for instance, we find the entry **udu gug-ga-na₂** (sheep for a *guqqanû* offering; line 98). The expression is known from administrative texts in the Ur III period, several centuries earlier (see, for instance, [TLB 03, 095](http://oracc.org/epsd2/admin/u3adm/P134236) o 9), but in the literary corpus the word **gug-ga-na₂** is absent. Many other such examples could be quoted here.

One may draw the conclusion that the "invented tradition" that was the subject of this curriculum not only involved the literary corpus, but also the Sumerian language itself. The lexical corpus not only functioned in support of the literary corpus - it also had a function of its own in preserving as much as possible of Sumerian writing and vocabulary.

Research on bird vocabulary showed that of the ### entries in the Old Babylonian list of birds, only ##% can be found in the literary corpus. This research was mainly done by hand, based on the author's reconstruction of the Old Babylonian bird list and a thorough survey of Sumerian literature - primarily based on the Electronic Text Corpus of Sumerian Literature ([ETCSL][]; more on [ETCSL][] below). The challenge of this chapter is: can we scale this comparison up, to include the entire Old Babylonian lexical corpus by using computational methods? And is it possible to use such methods to dig deeper into the relationship between these two vocabularies?

## 3.1 A First Attempt

As a first attempt, we may simply take all Old Babylonian lexical lists from [DCCLT][], extract the full vocabulary and compare that vocabulary to the inventory of words in [ETCSL][]. This approach will not be concerned with word frequencies - the issues simply is: is this particular word (lemma) attested in literary texts (in [ETCSL][]), in (Old Babylonian) lexical texts, or in both.

In order to do so we read the  [ETCSL][] and the [DCCLT][] datasets into Pandas DataFrame. The first step is to create a field `lemma` by adding Citation Form, Guide Word, and Part of Speech in the format **du[build]V/t**, or **lugal[king]N**. Next, we restrict the [DCCLT][] dataset to only Old Babylonian documents. We read the `catalogue.json` file from the `dcclt.zip` and isolate the text ID numbers that have the value "Old Babylonian" in the field `period`.  From both datasets we eliminate words that are not in Sumerian (e.g. Akkadian glosses). Finally we extract the new `lemma` field from both datasets and reduce them to their unique elements with the `set()` function.  A `set` in Python is an unordered list of unique elements. 

From the two sets, which we call `etcsl_words_s` and `lexical_words_s` we eliminate all words that have not been lemmatized (unknown words or broken words). We will see in the next section that we will need unlemmatized words in a slightly more sophisticated analysis - but not here. Collections of unique elements can be visualized in a Venn diagram, that shows the two sets as two partly overlapping circles. The intersection of the two sets represent the overlap. The function `plot_venn`  calls the function `venn2` from the `matplotlib_venn` library and defines the colors and captions. The result looks like this:

![venn diagram 1](viz/venn_1.png)

The Old Babylonian lexical corpus currently has 4,165 distinct lemmas, of which 2,033 (or almost half) are shared with the literary corpus. The vocabulary of the literary corpus is slightly larger with 4,345 distinct lemmas.

For a number of reasons, this is a very rough estimate and perhaps not exactly what we were looking for. A lexical entry like **udu diŋir-e gu₇-a**  (sheep eaten by a god) consists of three very common lemmas (**udu[sheep]N**, **diŋir[deity]N**, **gu[eat]V/t**) but the lexical *entry* (the sequence of these three lemmas in this order) may well be very rare or non-existent in the literary corpus. 

## 	3.2 Lexical Entries in Literary Context

The Old Babylonian list of animals ([OB Ura 3](http://oracc.org/dcclt/Q000001)) has 106 entries that begin with **udu** (sheep), including

| text                    | translation           |
| ----------------------- | --------------------- |
| 23. udu diŋir-e gu₇-a   | sheep eaten by a god  |
| 24. udu ur-mah-e gu₇-a  | sheep eaten by a lion |
| 25. udu ur-bar-ra gu₇-a | sheep eaten by a wolf |

The individual lemmas here are all fairly to very common and it is not a surprise to see them appear in the literary corpus. But what about the full entries? 



[ETCSL]: http://etcsl.orinst.ox.ac.uk
[DCCLT]: http://oracc.org/dcclt