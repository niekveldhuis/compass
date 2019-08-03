[TOC]

# 3. Lexical and Literary Vocabularies

In the Old Babylonian period (around 1,800 BCE) scribal students learned how to read and write by copying longs lists of signs and words (lexical lists). In a second stage they would start copying a broad variety of Sumerian literary texts, including hymns to gods and kings, narrative texts about gods and heroes of the past, and whimsical texts in which non-human entities (such as hoe and plow) dispute their utility for mankind.

Sumerian by this time was a dead language and the whole curriculum has been interpreted as an "invented tradition" - a golden age, projected in the distant past, when all of Babylonia was united under a single king, speaking a single language - Sumerian[^1].

The sequence lexical exercises - literary exercises may suggest that the literary material embodies the real goal of this education and that the lexical texts, enumerating thousands of Sumerian words and expressions, function in support of the students' ability to read, copy, and understand the literary compositions. Yet, it has often been noticed that many words and expressions in the lexical repertoire never appear in literary texts - and the other way around. In the [list of domestic animals](http://oracc.org/dcclt/Q000001), for instance, we find the entry **udu gug-ga-na₂** (sheep for a *guqqanû* offering; line 98). The expression is known from administrative texts in the Ur III period, several centuries earlier (see, for instance, [TLB 03, 095](http://oracc.org/epsd2/admin/u3adm/P134236) o 9), but in the literary corpus the word **gug-ga-na₂** is absent. Many other such examples could be quoted here.

One may draw the conclusion that the "invented tradition" that was the subject of this curriculum not only involved the literary corpus, but also the Sumerian language itself. The lexical corpus not only functioned in support of the literary corpus - it also had a function of its own in preserving as much as possible of Sumerian writing and vocabulary.

Research on bird vocabulary showed that of the 116 entries in the Old Babylonian [list of birds](http://oracc.org/dcclt/Q000041.405), only 39 can be found in the literary corpus.[^2] This research was mainly done by hand, based on the author's reconstruction of the Old Babylonian bird list and a survey of Sumerian literature - primarily based on the Electronic Text Corpus of Sumerian Literature ([ETCSL][]; more on [ETCSL][] below). The challenge of this chapter is: can we scale this analysis up, to include the entire Old Babylonian lexical and literary corpus by using computational methods? And is it possible to use such methods to dig deeper into the relationship between these two vocabularies?

## 3.1 A First Attempt

As a first attempt, we may simply take all Old Babylonian lexical lists from [DCCLT][], extract the full vocabulary and compare that vocabulary to the inventory of words (lemmas) in [ETCSL][]. In this approach we are not concerned with word frequencies - the issue simply is: is this particular word (lemma) attested in literary texts (in [ETCSL][]), in (Old Babylonian) lexical texts, or in both.

In order to do so we read the  [ETCSL][] and the [DCCLT][] datasets into Pandas DataFrames. The first step is to create a field `lemma` by adding Citation Form, Guide Word, and Part of Speech in the format **du[build]V/t**, or **lugal[king]N**. Next, we restrict the [DCCLT][] dataset to only Old Babylonian documents. We read the `catalogue.json` file from the `dcclt.zip` and isolate the text ID numbers that have the value "Old Babylonian" in the field `period`.  From both datasets we eliminate words that are not in Sumerian (e.g. Akkadian glosses). Finally we extract the new `lemma` field from both datasets and reduce them to their unique elements with the `set()` function: a `set` in Python is an unordered list of unique elements. 

From the two sets, which we call `etcsl_words_s` and `lexical_words_s` we eliminate all words that have not been lemmatized (unknown words or broken words). We will see in the next section that we will need unlemmatized words in a slightly more sophisticated analysis - but not here. Collections of unique elements can be visualized in a Venn diagram, that shows the two sets as two partly overlapping circles. The intersection of the two sets represents the overlap. This is done with the function `venn2` from the `matplotlib_venn` package, which allows us to select colors and define captions. The result looks like this:

![venn diagram 1](viz/venn_1.png)

The Old Babylonian lexical corpus currently has 4,165 distinct lemmas, of which 2,033 (or almost half) are shared with the literary corpus. The vocabulary of the literary corpus is only slightly larger with 4,345 distinct lemmas. The number of items in the literary set should be stable, because it is based on the archival set of [ETCSL][] files. The number on the right (set of lexical lemmas), however, may vary, because it is based on [DCCLT][] and its subcorpora, and those are still in the process of being edited.

For a number of reasons, this is a very rough estimate and perhaps not exactly what we were looking for. A lexical entry like **udu diŋir-e gu₇-a**  (sheep eaten by a god) consists of three very common lemmas (**udu[sheep]N**, **diŋir[deity]N**, **gu[eat]V/t**). This lexical entry, therefore, will result in three matches, three correspondences between the lexical and literary vocabulary. But what about the lexical *entry*? Does the nominal phrase **udu diŋir-e-gu₇-a** or, more precisely, the sequence of the lemmas **udu[sheep]N, diŋir[deity]N, gu[eat]V/t**) ever appear in a literary text? 

## 	3.1.2 Lexical Entries in Literary Context

In order to perform the comparison of lexical and literary vocabularies on the lexical *entry* level we first need to represent the data (lexical and literary) as lines, rather than as individual words. The line in a lexical texts will become our unit of comparison by defining those as Multiple Word Expressions (or MWEs). Lines in literary texts will serve as boundaries, since we do not expect an MWE to continue from one line to the next. 

The first step, therefore, is to group the data by line. This is done with the Pandas commands `groupby()`and `aggregate()` (abbreviated as `agg()`) . Once the lexical data are grouped by line the lexical dataframe will look like this (from the Old Babylonian [list of animals](http://oracc.org/dcclt/Q000001)):

| id_text       | id_line | lemma                                            |
| :------------ | :------ | :----------------------------------------------- |
| dcclt/Q000001 | 1       | udu\[sheep\]n niga\[fattened\]v/i                |
| dcclt/Q000001 | 2       | udu\[sheep\]n niga\[fattened\]v/i sag\[rare\]v/i |

We can use this data to look through the literary compositions to see whether there are places where the lemma **udu[sheep]n** is followed by the lemma **niga[fattened]v/i**, or whether we can find the sequence **udu[sheep]n niga[fattened]v/i sag[rare]v/i**, corresponding to the second line in the list of animals. When such a match is found in a literary composition, the lemmas are connected to each other with underscores, so that the sequence can be treated as a unit. Finding and marking such sequences is done with the MWETokenizer from the Natural Language Toolkit (NLTK) package. The MWETokenizer is initialized with a list of Multiple Word Expressions, which we can easily derive from the lexical data. It then applies this list to the corpus to be tokenized (in this case the [ETCSL][] corpus) to connect elements of MWEs by underscores.

Once this is done the lexical entries are treated the same: each space is replaced by an underscore. Now we have the same two sets of data in a slightly different representation and we can do essentially the same analysis as we did above by creating sets (called `etcsl_words_s2` and `lexical_words_s2`) and then visualize those sets in a Venn diagram: 

![venn diagram 2](viz/venn_2.png)

We see that this approach essentially doubles the number of unique elements on the lexical side; on the literary side the increase is much less drastic. It turns out that many of the lexical entries (some 70%) never appear as such in the literary corpus.

## 3.1.3. Add them Up

Finally we can add the two approaches discussed above into a single Venn diagram. There are words that appear as modifiers in lexical *entries* but never appear on their own in a lexical composition. Similarly, there are words in the literary corpus that occur in phrases known from the lexical corpus, but never outside of such phrases (we will see examples below). Such words, one may argue, potentially add to the intersection between the lexical and literary corpus, but are not represented in the second Venn diagram.

In order to do so we create the *union* of the first lexical set (individual words) and the second one (lexical expressions), and the same for the literary corpus and then draw a new Venn diagram. The union of two sets is a new set, with all the unique elements from the two original sets. The union sets are called `etcsl_words_s3` and `lexical_words_s3`.

![venn diagram 3](viz/venn_3.png)

The new diagram shows some increase on both sides, and a little increase in overlap as well - but the change is not very dramatic.

So which words are found on the literary side that only appear in MWEs known from lexical sources? We can easily find those by subtracting `etcsl_s2` from `etcsl_s3`. It turns out there are about thirty such words, most of them appearing just once

```
'ašgar[kid]n',
 'bazbaz[bird]n',
 'bur[grass]n',
 'burgia[offering]n',
 'ebgal[oval]n',
 'ebir[vessel-stand]n',
 'giʾiziʾešta[~bread]n',
 'guʾeguʾe[fatty?]aj',
 'hub[cvve]v/t',
 'huz[cvve]v/t',
 'kašu[~plow]n',
 'kiʾuš[waste]n',
 'ligidba[plant]n',
 'lillan[grain]n',
 'manzila[foot]n',
 'mer[cvve]v/t',
 'mur[noise]n',
 'namaʾa[unmng]n',
 'namniŋir[herald]n',
 'nim[high]v/i',
 'sa.ku[arm]n',
 'saharŋar[silt]n',
 'sala[bug-ridden]aj',
 'tuhul[hip]n',
 'tutu[cvve]v/t',
 'u[cvne]n',
 'ugudili[scalp]n',
 'uzudirig[mushroom]n',
 'zana[doll]n',
 'še[cone]n'}
```

An example is the word **ašgar[kid]n** (a female kid) that is very common in administrative and lexical texts, but appears only once in our literary corpus. The context, in Gudea Cylinder A vii 9, is where Gudea uses the hide of a virgin kid (**{munus}aš₂-gar₃ ŋeš nu-zu**) for a ritual purpose (the same expression appears in some Old Babylonian incantations). This expression, written slightly differently but representing the same series of lemmas, is found in the lexical corpus.

Our investigation so far has shown that a very considerable portion of lexical words and lexical expressions are not found in the literary corpus as represented by [ETCSL][]. Chances are that a good number of them will be found in literary texts that are not in [ETCSL][] or that are not even known today. However, the lexical corpus is likely to increase, too, and chances that the intersection between those two vocabularies will increase significantly seem slim. Other forces may actually decrease the overlap. The example of **ašgar[kid]n**, above, derives from the Gudea Cylinders which is a royal inscription from several centuries before the Old Babylonian period. It is often included in presentations of Sumerian literature because it is, indeed, one of the high points of Sumerian literary language. But is has nothing to do with the Old Babylonian schools that our research started with and a good argument can be made for excluding it from our investigation.

## 3.2 Digging Deeper

We can take our analysis several steps further by looking for *important* words,  or *rare* words, or by investigating the relative contribution of individual lexical and literary compositions to the intersection. The lemmas **šag[heart]n** and **igi[eye]n** appear in the lexical composition Ugumu (the list of body parts). They also appear in virtually every literary composition, because there are many common verbal and nominal expressions that use these lemmas. On the other hand, the list of stones includes the entry {na₄}e-gu₂-en-sag₉ (with many variant writings), a very rare word that is know from the literary composition Lugal-e (or [Ninurta's Exploits](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.6.2&display=Crit&charenc=gcirc&lineid=c162.619#c162.619)) line 619 in the form **{na₄}en-ge-en**.  Since part of this composition is an enumeration of many types of stones (and their fates), there is a good chance that this particular match is significant - that the stone name is included in the list because it appears in Lugal-e, for instance.

The sets used in the previous sections are not useful for such investigations. First, we have no idea where words/expressions that match (or do not match) appear and second, we have no information about how frequent a word is or its importance in a particular composition. 

In order to address such questions we will use a Document Term Matrix (DTM): a huge matrix, where each row represents a (lexical or literary) composition (Document) and each column represents a lemma (Term). The number of columns will thus equal the number of individual lemmas available in our corpus. 

In order to do so we will use the Pandas  `groupby()` and `aggregate()` commands again to represent each composition (lexical or literary) as one long string of lemmas.  We will use the data representation where lemmas in lexical expressions are connected by underscores.

Once we have the data represented this way we can use `Countvecorizer()` from the `sklearn` package to create the DTM. The `countvectorizer()` function essentially vectorizes a document by counting the number of times each word appears. In an artificial example we can vectorize the sentences (documents)

> **lugal[king]n e[house]n du[build]v/t** 
>
>  **lugal[king]n egal[palace]n du[build]v/t** 

as follows: 

| sentence | du[build]v/t | e[house]n | egal[palace]n | lugal[king]n |
| -------- | ------------ | --------- | ------------- | ------------ |
| one      | 1            | 1         | 0             | 1            |
| two      | 1            | 0         | 1             | 1            |

We can now say that sentence one is represented by the vector `[1, 1, 0, 1]` and sentence two by the vector `[1, 0, 1, 1]`. That means that we can apply vector operations and vector mathematics on these two sentences - for instance we can compute their cosine similarity (0.66). In real-world examples many slots in the matrix are 0 (there are many words in the corpus that do not appear in this particular composition) and many slots are higher than 1 (a word that appears in a document is likely to appear more than once). Note that each *word* (or lemma) is now also characterized by a vector, represented by the numbers in a column.

We can use various types of DTMs to investigate in more complex ways the relationships between the lexical and the literary vocabulary. Instead of a full DTM, in which all occurrences of all words are represented, we will first build a *binary* DTM of the literary corpus (the [ETCSL][] corpus), using the lexical vocabulary. Our DTM will have one row for each document/composition (as in any DTM), and one column for each lemma or expression attested in the Old Babylonian *lexical* corpus. Because this is a *binary* DTM, each cell has either a 0 or a 1, to indicate that the word/expression in question does or does not appear in that particular literary composition. How many times a lemma is attested in the composition is not indicated - only *that* it appears, or not.

Because each column represents a word in the lexical corpus, there are many columns that have only zeroes (lexical entries that do not occur in [ETCSL][]). In terms of our Venn diagrams, the zeros in our DTM represent the blue area to the right, the ones represent the middle area (overlap between lexical and literary vocabulary). 
![venn diagram 3](viz/venn_3.png)

The main difference between the Venn diagram and the DTM is that the DTM shows in which compositions the shared words are attested. By computing the sum of a row we get an integer that represents the number of lexically attested lemmas in a particular composition, and this gives us a (numerical) measuring for comparing between compositions. Not surprisingly, longer compositions, such as the [Gudea Cylinders](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.7&display=Crit&charenc=gcirc#) (1363 lines), or the Ninurta narrative [Lugale](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.6.2&display=Crit&charenc=gcirc#) (726 lines) have more such matches than shorter ones. In fact, the very short ones (some consist of only a few words) are not very useful for the comparison - we will restrict the analysis to texts that are at least 200 words (lemmas/expressions) long. In addition to text length, other (related) characteristics that we may want to pay attention to are lexical richness (how many unique lemmas/expressions are attested in this composition?) and type-token-ration (TTR), which is defined as the number of unique lemmas (types) divided by the length of the text (number of tokens).  TTR is considered a rather poor measurement for lexical diversity (because it has it strong negative correlation with text length), but for compositions of approximately even length it may give some idea of the creativity vs. repetitiveness of the text.

The table below gives the first ten compositions, sorted by `norm2` (descending). Of the 97 unique lemmas that are attested in Inana E no less than 94 are also attested in the Old Babylonian lexical corpus - a norm2 score of 0.969.

| id_text                                                      | text_name                                                    | length | mtld    | ttr   | lex_var | n_matches | norm1 | norm2 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------ | ------- | ----- | ------- | --------- | ----- | ----- |
| [c.4.07.5](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.4.07.5&display=Crit&charenc=gcirc#) | A tigi to Inana (Inana E)                                    | 292    | 23.982  | 0.332 | 97      | 94        | 0.322 | 0.969 |
| [c.2.3.1](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.3.1&display=Crit&charenc=gcirc#) | An adab to Bau for Luma (Luma A)                             | 232    | 20.212  | 0.336 | 78      | 75        | 0.323 | 0.962 |
| [c.4.15.3](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.4.15.3&display=Crit&charenc=gcirc#) | A tigi to Nergal (Nergal C)                                  | 213    | 60.425  | 0.451 | 96      | 91        | 0.427 | 0.948 |
| [c.2.5.4.23](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.5.4.23&display=Crit&charenc=gcirc#) | A hymn to Nibru and Išme-Dagan (Išme-Dagan W)                | 331    | 62.805  | 0.465 | 154     | 144       | 0.435 | 0.935 |
| [c.5.2.4](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.5.2.4&display=Crit&charenc=gcirc#) | A man and his god                                            | 564    | 85.109  | 0.418 | 236     | 218       | 0.387 | 0.924 |
| [c.4.13.01](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.4.13.01&display=Crit&charenc=gcirc#) | A balbale to Suen (Nanna A)                                  | 245    | 48.75   | 0.478 | 117     | 108       | 0.441 | 0.923 |
| [c.2.5.6.5](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.5.6.5&display=Crit&charenc=gcirc#) | An adab to An for Ur-Ninurta (Ur-Ninurta E)                  | 216    | 58.974  | 0.602 | 130     | 120       | 0.556 | 0.923 |
| [c.4.12.1](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.4.12.1&display=Crit&charenc=gcirc#) | A šir-gida to Martu (Martu A)                                | 286    | 110.755 | 0.615 | 176     | 162       | 0.566 | 0.92  |
| [c.5.1.3](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.5.1.3&display=Crit&charenc=gcirc#) | The advice of a supervisor to a younger scribe (E-dub-ba-a C) | 407    | 90.529  | 0.521 | 212     | 195       | 0.479 | 0.92  |
| [c.2.5.4.11](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.5.4.11&display=Crit&charenc=gcirc#) | A hymn to Inana for Išme-Dagan (Išme-Dagan K)                | 233    | 135.139 | 0.635 | 148     | 136       | 0.584 | 0.919 |

Note that changes in the [DCCLT][] data may change the numbers and the arrangement of the table.

The top-ten for `norm2` does not favor typical school compositions. Typical school compositions are found in large numbers of exemplars or have other characteristics that make it likely that they played an important role in literary education in scribal school. Several such groups of texts, labeled the *tetrad*, the *decad* and the *House F Fourteen* have been identified in the past[^3]. Of these compositions only [Eduba C](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.5.1.3&display=Crit&charenc=gcirc#)  (which belongs to the *House F Fourteen*) appears in our list appears at number 9. 

In the notebook one may manipulate the table to sort it by different columns (ascending or descending) and by displaying a larger or smaller number of rows. We can manipulate the various columns to get a sense of what these numbers mean.

Ordering by text *length* we see that the Gudea cylinders are by far the longest composition in this group at 4,387 lemmas. The next composition is Ninurta's exploits (or Lugal-e) at 3,160, followed by The Lament for Sumer and Ur (2,701). From there on composition gradually get shorter, but the first two stand out. 

As expected, this is correlated with a low TTR (Gudea: 0.209). It is interesting to note, however, that there are four compositions that are (much) shorter, but have an even lower TTR. These are: 

| id_text                                                      | text_name                            | length | ttr   |
| ------------------------------------------------------------ | ------------------------------------ | ------ | ----- |
| [c.1.3.1](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.3.1&display=Crit&charenc=gcirc#) | Inana and Enki                       | 2085   | 0167  |
| [c.1.5.1](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.5.1&display=Crit&charenc=gcirc#) | Nanna-Suen's journey to Nibru        | 1219   | 0.187 |
| [c.1.8.1.4](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.8.1.4&display=Crit&charenc=gcirc#) | Gilgameš Enkidu and the nether world | 2145   | 0.191 |
| [c.1.4.1](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&display=Crit&charenc=gcirc#) | Inana's descent to the nether world  | 1827   | 0.205 |

These four compositions are characterized by wholesale repetitions of passages, which probably explains their low TTR.

Ordering our texts by MTLD yields some surprising and perhaps irregular results. MTLD measures the mean number of words needed to lower the TTR to the default threshold of 0.720. There are no less than 50 compositions for which this average is above 100, with a maximum of 239.19 (Enlil-bāni A) and a median of 65.23 (Song of the Hoe). The validity of the result for Enlil-bāni A is questionable, because the text is only 316 lemmas long - which means that the average is based on only one full factor and a partial one. Still, the rest of the numbers for Enlil-bāni A confirm that there is something remarkable about this composition. 



Examples are Gilgameš Enkidu and the Netherword (length 2145; TTR 0.191) or Inana and Enki (length 2,085; TTR 0.166).  Both of these compositions have long repeated sequences, which may explain their low TTR.

Here the highest score is for Sîn-iddinam E, which has 130 matches on a text length of 207 - a score of 0.628. 

These ten texts that score highest on lexical matches per lemma include a very large number of hymns to Isin kings, including Ur-Ninurta, Enlil-bani, Lipit-Eštar, Sin-Iddinam, and Išme-Dagan. The list includes some texts that are considered typical school compositions, such as [Enlil-bani A](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.5.8.1&display=Crit&charenc=gcirc#), [Lipit-Eštar A](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.5.5.1&display=Crit&charenc=gcirc#), [Lipit-Eštar B](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.5.5.2&display=Crit&charenc=gcirc#), and [Šulgi A](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.4.2.01&display=Crit&charenc=gcirc#). 

Although the two "top tens" do not have any composition in common, it seems that hymns to gods and (in particular) to kings score high in both categories. The only narrative text to show in either table is Gilgameš and Aga, with the 10th highest score on`norm2`; proverbs and disputations are absent.

We can look in more detail at the highest scoring text in the `norm2` column to see what is going on.  




[^1]: 	N. Veldhuis, *Religion, Literature, and Scholarship: The Sumerian Composition "Nanše and the Birds"*. Cuneiform Monographs 22. Leiden: Brill 2004.
[^2]:	N. Veldhuis, *Religion, Literature, and Scholarship: The Sumerian Composition "Nanše and the Birds"*. Cuneiform Monographs 22. Leiden: Brill 2004.
[^3]:	For tetrad, decad and House F Fourteen, see E. Robson, The tablet House: a scribal school in old Babylonian Nippur, in: *Revue d'Assyriologie* 93 (2001) 39-66, [doi:10.3917/assy.093.0039](https://doi.org/10.3917/assy.093.0039); and Paul Delnero, *The Textual Criticism of Sumerian Literature*, Journal of Cuneiform Studies Supplementary Series 3 (2012); both with further literature.

[ETCSL]: http://etcsl.orinst.ox.ac.uk
[DCCLT]: http://oracc.org/dcclt
```

```