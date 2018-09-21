[TOC]

# 3. Lexical and Literary Vocabularies

In the Old Babylonian period (around 1,800 BCE) scribal students learned how to read and write by copying longs lists of signs and words (lexical lists). In a second stage they would start copying a broad variety of Sumerian literary texts, including hymns to gods and kings, narrative texts about gods and heroes of the past, and whimsical texts in which hoe and plow (or other non-human entities) dispute their utility for mankind.

Since Sumerian by this time was a dead language, the whole curriculum (lexical lists and literary texts together) has been interpreted as looking back at a golden age, and creating an "invented tradition" - a period when all of Babylonia was united under a single king, speaking a single language - Sumerian.

The sequence lexical exercises - literary exercises suggests that the literary material embodies the real goal of this education and that the lexical texts, enumerating thousands of Sumerian words and expressions, function in support of the students' ability to read, copy, and understand the literary texts. Yet, it has often been noticed that many words in the lexical repertoire never appear in literary texts - and the other way around. In the [list of domestic animals](http://oracc.org/dcclt/Q000001), for instance, we find the entry **udu gug-ga-na₂** (sheep for a *guqqanû* offering; line 98). The expression is known from administrative texts in the Ur III period, several centuries earlier (see, for instance, [TLB 03, 095](http://oracc.org/epsd2/admin/u3adm/P134236) o 9), but in the literary corpus the word **gug-ga-na₂** is absent. Many other such examples could be quoted here.

One may draw the conclusion that the "invented tradition" that was the subject of this curriculum not only involved the literary corpus, but also the Sumerian language itself. The lexical corpus not only functioned in support of the literary corpus - it also had a function of its own in preserving as much as possible of Sumerian writing and vocabulary.

Research on bird vocabulary showed that of the ### entries in the Old Babylonian list of birds, only ##% can be found in the literary corpus. This research was mainly done by hand, based on the author's reconstruction of the Old Babylonian bird list and a thorough survey of Sumerian literature - primarily based on the Electronic Text Corpus of Sumerian Literature ([ETCSL][]; more on [ETCSL][] below). The challenge of this chapter is: can we scale this comparison up, to include the entire Old Babylonian lexical corpus by using computational methods? And is it possible to use such methods to dig deeper into the relationship between these two vocabularies?

## 3.1 A First Attempt

As a first attempt, we may simply take all Old Babylonian lexical lists, extract the full vocabulary and compare that vocabulary to the inventory of words in [ETCSL][]. This approach will not be concerned with word frequencies - the issues simply is: is this particular word (lemma) attested in literary texts (in [ETCSL][]), in (Old Babylonian) lexical texts, or in both.

We load the [ETCSL][] dataset as extracted in the file `alltexts.csv`(see section ###) in a Pandas DataFrame, and create a `lemma`column (combining Citation Form, Guide Word, and Part of Speech), and extract the unique elements with the command `set()` (a `set`in Python is an unordered list of unique elements).

Loading the file: 

```Python
file = "../2_4_Data_Acquisition_ETCSL/Output/alltexts.csv"
etcsl = pd.read_csv(file, keep_default_na=False)
etcsl = etcsl.loc[etcsl["lang"].str.contains("sux")]  # throw out non-Sumerian words
```
The command `read_csv` in the Pandas module reads a `csv`file directly into a Pandas DataFrame. It will interpret entries such as "NA", "na", or "NaN" as conventional representations of "Missing Value" ("NaN" = "Not a Number"). This is going to create problems in particular in badly preserved text areas, where a "word" may consist simply of the sign "NA." In order to prevent this behaviour the option `keep_default_na` is set to `False`.

Creating a `lemma`column simply means adding up Citation Form (**lugal**), Guide Word (**king**), and Part of Speech (**N**), to create the format **lugal[king]N**. However, there are words (broken, or not understood) that have no Guide Word, Citation Form, or Part of Speech. For the present analysis we could simply throw those out (words that are broken or not understood cannot be compared across corpora) - and we will do so later on. For now, however, we keep them in because they will become important when we consider multiple-word expressions (section ##). They will be represented by their `form`(transliteration) instead of Citation Form and "NA" as Guide Word and Part of Speech (e.g. **KAŠ₄[NA]NA**). This results in a rather longish `apply()` with a temporary function (`lambda`) and an `if` statement, applied over each row (`axis = 1`). This function will also create "lemmas" for entries that merely mark breakage ("8 lines broken"). Such entries have no `form`and will result in the lemma **[NA]NA**. Those entries are eliminated. Finally, all lemmas are lowercased.

```python
etcsl["lemma"] = etcsl.apply(lambda r: (r["cf"] + '[' + r["gw"] + ']' + r["pos"]) 
           if r["cf"] != '' else r['form'] + '[NA]NA', axis=1)
etcsl['lemma'] = [lemma if not lemma == '[NA]NA' else '' for lemma in etcsl['lemma'] ] 
# kick out empty forms
etcsl["lemma"] = etcsl["lemma"].str.lower()
```

Reading the lexical data is very similar - essentially using the same code as used above for reading in the data, creating a `lemma`column, etc. In order to restrict the dataset to Old Babylonian lexical texts we need to access the catalog which is available in `JSON`format in the `dcclt.zip` (see section ####). From the catalog we select only the fields `id_text` and `period` and then select the rows where `period`equals "Old Babylonian". This yields a list of P, Q, and X numbers that have been assigned to the Old Babylonian period in the [DCCLT][] catalog. This list includes lexical texts that have not (yet) been transliterated and those that have been transliterated but have not been lemmatized. Since the code in this section is based on lemmatized texts, those documents will be ignored. The `JSON`file set includes a file (`metadata.json`) that provides information about the status of transliteration and lemmatization of a particular document and one could use that information to further pare down the list of P/Q/X numbers to consider. Here we will simply work with all Old Babylonian text numbers.

After extracting the list of Old Babylonian P/Q/X numbers we can use that list to filter the rows in the DataFrame that holds the lexical data: 

```python
keep = list(cat['id_text'])
keep = ['dcclt/' + id for id in keep]
lexical = lexical.loc[lexical["id_text"].isin(keep)]
```





[ETCSL]: http://etcsl.orinst.ox.ac.uk
[DCCLT]: http://oracc.org/dcclt