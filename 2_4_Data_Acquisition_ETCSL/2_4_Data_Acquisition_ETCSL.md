**Preliminary version**

This is a preliminary version of Chapter 2.4 of [ComPass][] (Computational Assyriology). The associated [notebook](https://github.com/niekveldhuis/CompAss/blob/master/2_4_Data_Acquisition_ETCSL/2_4_Data_Acquisition_ETCSL.ipynb) should work as advertised (Python 3; tested for Windows and Mac), but the text below still needs polishing and editing for clarity. Comments are very welcome.

Back to the main [COMPASS][] page on [ORACC][]

Back to [COMPASS Chapter 2](http://build-oracc.museum.upenn.edu/compass/2dataacquisition/index.html)

To the [Data Acquisition ETCSL](https://github.com/niekveldhuis/CompAss/blob/master/2_4_Data_Acquisition_ETCSL/2_4_Data_Acquisition_ETCSL.ipynb) notebook on Github.

## 2.4 Data Acquisition: ETCSL

[TOC]
The Electronic Text Corpus of Sumerian Literature ([ETCSL][]) provides editions and translations of almost 400 Sumerian literary texts, mostly from the Old Babylonian period (around 1800 BCE). The project was led by Jeremy Black (Oxford University) and was active until 2006, when it was archived. Information about the project, its stages, products and collaborators may be found in the project's [About](http://etcsl.orinst.ox.ac.uk/edition2/general.php) page. By the time of its inception [ETCSL][] was a pioneering effort - the first large digital project in Assyriology, using well-structured data according to the standards and best practices of the time. [ETCSL][] allows for various kinds of searches in Sumerian and in English translation and provides lemmatization for each individual word. Numerous scholars contributed data sets to the [ETCSL][] project (see [Acknowledgements](http://etcsl.orinst.ox.ac.uk/edition2/credits.php#ack)). The availability of [ETCSL][] has fundamentally altered the study of Sumerian literature and has made this literature available for undergraduate teaching.

The original [ETCSL][] files in TEI XML are stored in the [Oxford Text Archive][] from where they can be downloaded as a ZIP file under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License ([by-nc-sa 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/)). The copyright holders are Jeremy Black, Graham Cunningham, Jarle Ebeling, Esther Flückiger-Hawker, Eleanor Robson, Jon Taylor, and Gábor Zólyomi.

The [Oxford Text Archive][] page offers the following description:

> The Electronic Text Corpus of Sumerian Literature (ETCSL) comprises transliterations and English translations of 394 compositions attested on sources dating to the period from approximately 2100 to 1700 BCE. The compositions are divided into seven categories: ancient literary catalogues; narrative compositions; royal praise poetry and hymns to deities on behalf of rulers; literary letters and letter-prayers; divine and temple hymns; proverbs and proverb collections; and a more general category including compositions such as debates, dialogues and riddles. The numbering of the compositions within the corpus follows Miguel Civil's unpublished catalogue of Sumerian literature (etcslfullcat.html).Files with an initial c are composite transliterations (a reconstructed text editorially assembled from the extant exemplars but including substantive variants) in which the cuneiform signs are represented in the Roman alphabet. Files with an initial t are translations. The composite files include full references for the cuneiform sources and author-date references for the secondary sources (detailed in bibliography.xml). The composite and translation files are in XML and have been annotated according to the TEI guidelines. In terms of linguistic information, each word form in the composite transliterations has been assigned to a lexeme which is specified by a citation form, word class information and basic English translation.

Since [ETCSL][] is an archival site, the editions are not updated to reflect new text finds or new insights in the Sumerian language. Many of the [ETCSL][] editions were based on standard print editions that itself may have been 10 or 20 years old by the time they were digitized. Any computational analysis of the [ETCSL][] corpus will have to deal with the fact that: 

- the text may not represent the latest standard
- the [ETCSL][] corpus is extensive - but does not cover all of Sumerian literature known today

In terms of data acquisition, the way to deal with these limitations is to make the [ETCSL][] data as much as possible compatible with the data standards of the Open Richly Annotated Cuneiform Corpus ([ORACC][]). [ORACC][] is an active project where new or updated editions can be produced. If compatible, if [ETCSL][] and [ORACC][] data may be freely mixed and matched, then the [ETCSL][] data set can effectively be updated and expanded.

The [ETCSL][] text corpus was one of the core data sets for the development of of [ePSD1](http://psd.museum.upenn.edu/epsd1/index.html) and [ePSD2][] (currently in a Beta version) and this version of the [ETCSL][] data is available at [ePSD2/ETCSL][] and can be parsed with the ORACC parser, discussed in section 2.3. In order to include the data in ePSD the lemmatization is adapted there to [ORACC][] standards and thus this version of the [ETCSL][] dataset is fully compatible with any [ORACC][] dataset.

Parsing the original [ETCSL][] XML TEI files has, therefore, become somewhat redundant. The reason to include and discuss the [ETCSL][] parser here is, first, to offer users the opportunity to work with the original data set. The various transformations included in the current parser may be adapted and adjusted to reflect the preferences and research questions of the user. Second, [ETCSL][] distinguishes between main text, secondary text, and additional text, to reflect different types of variants between manuscripts (see below 2.4.4). The [ePSD2/ETCSL][] data set does not include this distinction. The output of the parser will indicate for each word whether it is "secondary" or "additional" (according to [ETCSL][] criteria) and offer the possibility to include such words or exclude them from the  analysis.

In order to achieve compatability between [ETCSL][] and [ORACC][] the code uses a number of equivalence dictionaries, that enable replacement of characters, words, or names. These equivalence dictionaries are stored in JSON format (for JSON see section 2.3) in the file `equivalancies.json`  in the directory `equivalencies`.

### 2.4.1 TEI XML format

The [ETCSL][] files as distributed by the [Oxford Text Archive](http://ota.ox.ac.uk/desc/2518) are encoded in a dialect of `XML` (Extensible Markup Language) that is referred to as `TEI` (Text Encoding Initiative). In this encoding each word (in transliteration) is an *element* that is surrounded by `<w>` and `</w>` tags. Inside the start-tag the word may receive several attributes, encoded as name/value pairs, as in the following random examples:

```xml
<w form="ti-a" lemma="te" pos="V" label="to approach">ti-a</w>
<w form="e2-jar8-bi" lemma="e2-jar8" pos="N" label="wall">e2-jar8-bi</w>
<w form="ickila-bi" lemma="ickila" pos="N" label="shell"><term id="c1813.t1">ickila</term><gloss lang="sux" target="c1813.t1">la</gloss>-bi</w>
```

The `form` attribute is the full form of the word, omitting flags (such as question marks), indication of breakage, or glosses. The `lemma` attribute is the form minus morphology (corresponding to `citation form` in [ORACC][]). Some lemmas may be spelled in more than one way in Sumerian; the `lemma` attribute will use a standard spelling (note, for instance, that the `lemma` of "ti-a" is "te"). The `lemma` in [ETCSL][]](unlike `Citation Form` in [ORACC][]) uses actual transliteration with hyphens and sign index numbers (as in `lemma = e2-jar8`, where the corresponding [ORACC][] `citation form` is egar).

The `label` attribute gives a general indication of the meaning of the Sumerian word but is not context-sensitive. That is, the `label` of "lugal" is always "king", even if in context the word means "owner". The `pos` attribute gives the Part of Speech, but again the attribute is not context-sensitive. Where a verb (such as sag₉, to be good) is used as an adjective the `pos` is still "V" (for verb). Together `lemma`, `label`, and `pos` define a Sumerian lemma (dictionary entry).

In parsing the [ETCSL] files we will be looking for the `<w>` and `</w>` tags to isolate words and their attributes. Higher level tags identify lines (`<l>` and `</l>`), versions, secondary text (found only in a minority of sources), etcetera.

The [ETCSL] file set includes the file [etcslmanual.html](http://etcsl.orinst.ox.ac.uk/edition2/etcslmanual.php) with explanations of the tags, their attributes, and their proper usage.

Goal of the parsing process is to get as much information as possible out of the `XML` tree in a format that is useful for computational text analysis. What "useful" means depends, of course, on the particular project. The output of the parser is a word-by-word (or rather lemma-by-lemma) representation of the entire [ETCSL][] corpus in a format that is as close as possible to the output of the [ORACC][] parser. For most computational projects it will be necessary to group words into lines or compositions, or to separate out a particular group of compositions. The data is structured in such a way that that can be achieved with a standard set of Python commands of the `Pandas` library..

### 2.4.2 `lxml` and `Xpath`

There are several Python libraries specifically for parsing `XML`, among them the popular `ElementTree` and its twin `cElementTree`. The library `lxml` is largely compatible with `ElementTree` and `cElementTree` but differs from those in its full support of `Xpath`. `Xpath` is a language for finding and retrieving elements and attributes in XML trees. `Xpath` is not a program or a library, but a set of specifications that is implemented in a variety of software packages in different programming languages. 

`Xpath` uses the forward slash to describe a path through the hierarchy of the the `XML` tree. The expression `"/body/l/w"` will select all the `w` (word) elements that are children of `l` (line) elements that are children of the `body` element in the top level of `XML` hierarchy.

The expression `'//w'`means: all the `w` nodes, wherever in the hierarchy of the `XML` tree. The expression may be used to create a list of all the `w` nodes with all of their associated attributes. The attributes of a node are addressed  with the `@` sign, so that `//w/@label` refers to the `label` attributes of all the `w` nodes at any level in the hierarchy. 

```python
words = tree.xpath('//w')
labels = tree.xpath('//w/@label')
```

Predicates are put between square brackets and describe conditions for filtering a node set. The expression  `//w[@emesal]` will return all the `w` elements that have an attribute `emesal`. 

`Xpath` also defines hundreds of functions. An important function is `'string()'` which will return the string value of a node or an attribute.  Once all `w` nodes are listed in the list `words` (with the code above) one may extract the transliteration and Guide Word (`label` in [ETCSL][]) of each word as follows:

```python
form_l = []
gw_l = []
for node in words:
    form = node.xpath('string(.)') 
    form_l.append(form)
    gw = node.xpath('string(@label)')
    gw_l.append(gw)
```

The dot in `node.xpath('string(.)')` refers to the current node.

For proper introductions to `Xpath` and `lxml` see the [Wikipedia](https://en.wikipedia.org/wiki/XPath) article on `Xpath` and the homepage of the [`lxml`](https://lxml.de/) library, respectively.

### 2.4.3 Pre-processing: HTML entities

Before the XML files can be parsed, it is necessary to remove character sequences that are not allowed in XML proper (so-called HTML entities). 

In non-transliteration contexts (bibliographies, text titles, etc.) [ETCSL][] uses so-called HTML entities to represent non-ASCII characters such as,  á, ü, or š. These entities are encoded with an opening ampersand (`&`) and a closing semicolon (`;`). For instance, `&C;` represents the character `Š`. The HTML entities are for the most part project-specific and are declared in the file `etcsl-sux.ent` which is part of the file package and is used by the [ETCSL][] project in the process of validating and parsing the XML for online publication.

For purposes of data acquisition these entities need to be resolved, because XML parsers will not recognize these sequences as valid XML. 

The key `ampersands`in the file `equivalences.json` includes a dictionary, listing all the HTML entities that appear in the [ETCSL][] files with their Unicode counterparts:

```json
{'&C;': 'Š',
 '&Ccedil;': 'Ç',
 '&Eacute;': 'É',
 '&G;': 'Ŋ',
 '&H;': 'H',
 '&Imacr;': 'Î',
 '&X;': 'X',
 '&aacute;': 'á',
 etc.  
```

This dictionary is used to replace each HTML entity with its unicode (UTF-8) counterpart in each of the data files (the original files are, of course, left untouched). The function `ampersands()` is called in the main process. 

```python
import json
with open("equivalencies/equivalencies.json") as f:
    eq = json.load(f)
def ampersands(x):
    for amp in eq["ampersands"]:
        x = x.replace(amp, eq["ampersands"][amp])
    return x
```

### 2.4.4 Pre-Processing: Additional Text and Secondary Text

In order to be able to preserve the [ETCSL][] distinctions between main text (the default), secondary text, and additional text, such information needs to be added as an attribute to each `w` node (word node). This must take place in pre-processing, before the `XML` file is parsed.

[ETCSL][] transliterations represent composite texts, put together (in most cases) from multiple exemplars. The editions include substantive variants, which are marked either as "additional" or as "secondary". Additional text consists of words or lines that are *added* to the text in a minority of sources. In the opening passage of [Inana's Descent to the Netherworld][], for instance, there is a list of temples that Inana leaves behind. One exemplar extends this list with eight more temples; in the composite text these lines are marked as "additional" and numbered lines 13A-13H. Secondary text, on the other hand, is variant text (words or lines) that are found in a minority of sources *instead of* the primary text. An example in [Inana's Descent to the Netherworld][] is lines 30-31, which are replaced by 30A-31A in one manuscript (text and translation as in [ETCSL][]):

| line | text                                       | translation                                                  |
| ---- | ------------------------------------------ | ------------------------------------------------------------ |
| 30   | sukkal e-ne-eĝ₃ sag₉-sag₉-ga-ĝu₁₀          | my minister who speaks fair words,                           |
| 31   | ra-gaba e-ne-eĝ₃ ge-en-gen₆-na-ĝu₁₀        | my escort who speaks trustworthy words                       |
| 30A  | [na] ga-e-de₅ na de₅-ĝu₁₀ /ḫe₂\\-[dab₅]    | I am going to give you instructions: my instructions must be followed; |
| 31A  | [inim] ga-ra-ab-dug₄ ĝizzal [ḫe₂-em-ši-ak] | I am going to say something to you: it must be observed      |

"Secondary text" and "additional text" can also consist of a single word and there are even cases of "additional text" within "additional text" (an additional word within an additional line).

In [ETCSL][] TEI XML secondary/additional text is introduced by a tag of the type:

```xml
<addSpan to="c141.v11" type="secondary"/>
```

or

```xml
<addSpan to="c141.v11" type="additional"/>
```

The number c141 represents the text number in [ETCSL][] (in this case [Inana's Descent to the Netherworld][], text c.1.4.1). The return to the primary text is indicated by a tag of the type:

```xml
<anchor id="c141.v11"/>
```

Note that the `id` attribute in the `anchor` tag is identical to the `to` attribute in the `addSpan` tag.

We can collect all the `w` tags (words) between `addSpan` and its corresponding `anchor` tag wih the following `xpath` expression:

```python
secondary = tree.xpath('//w[preceding::addSpan[@type="secondary"]/@to = following::anchor/@id]')
```

In the expression `preceding` and `following` are so-called `axes` (plural of `axis`) which describe the relationship of an element to another element in the tree. The expression means: get all `w` tags that are preceded by an `addSpan` tag and followed by an `anchor` tag. The `addSpan` tag has to have an attribute `type` with value `secondary` , and the value of the `to` attribute of this `addSpan` tag is to be equal to the `id` attribute of the following `anchor` tag.

Once we have collected all the "secondary" `w` tags this way, we can add an attribute to each of these words in the following way:

```python
for word in secondary:
    word.attrib["status"] = "secondary"
```

In the process of parsing we can retrieve this new `status` attribute to mark all of these words as `secondary`.

Since we can do exactly the same for "additional text" we can slightly adapt the above expression for use in a function:

```python
def mark_extra(tree, which):
    extra = tree.xpath('//w[preceding::addSpan[@type="' + which + '"]/@to = following::anchor/@id]')
    
    for word in extra:
        word.attrib["status"] = which
	return tree
```

In the main process the function `mark_extra()`is called with the entire `XML` tree as its first argument, and  "additional" or "secondary" as its second argument.

###  2.4.5 Gaps

Gaps of one or more lines in the composite text, due to damage to the original cuneiform tablet, is encoded as follows:

```xml
<gap extent="8 lines missing"/>
```

In order to be able to process this information and keep it at the right place in the data we will parse the `gap` tags together with the `l` (line) tags and process the gap as a line. In [ORACC][] gaps are described with the fields `extent` (a number, or `n` for unknown),  and`scope` (line, column, obverse, etc.) . [ORACC][] uses a restricted vocabulary for these fields, but [ETCSL][] does not. The code currently does not try to make the [ETCSL][] encoding of gaps compatible with the [ORACC][] encoding.

### 2.4.6 Parsing the XML Tree

The Python library `lxml`, includes a module`etree`, specialized in parsing XML trees. The code basically works from the highest level of the hierarchy  to the lowest, in the following way:

```
text							parsetext()
	version						getversion()
		section					getsection()
			line				getline()
				word			getword()
					format		etcsl_to_oracc()
```

The main process calls the function `parsetext()` which calls the pre-processing functions discussed in section [2.4.3](#2.4.3-Pre-processing:-HTML-entities) and [2.4.4](#2.4.4-Pre-Processing:-Additional-Text-and-Secondary-Text). It then calls `getversion()`, which calls `getsection()`, which calls `getline()`, which, calls `getword()`, which calls `etcsl_to_oracc()`. These functions do not return anything. Instead, they modify the dictionaries `meta_d` (which collects meta data on various levels) and `word`, which contains all the information (including meta data) of an individual word. The function `etcsl_to_oracc()`, the last one in the hierarchy, appends the dictionary `word` to the list `alltexts` (which was created as an empty list in the main process) before the whole cycle starts again.

The word `šeŋ₆-ŋa₂` in the file `c.1.2.2.xml` ([Enlil and Sud](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.2.2&display=Crit&charenc=gcirc#)), in Version A, section A line 115, looks as follows in the original XML file: 

```xml
<w form="cej6-ja2" lemma="cej6" pos="V" label="to be hot">cej6-ja2</w>
```

The dictionary that is created in `etcsl_to_oracc()` represents that same word as follows:

```python
{'id_text': 'c.1.2.2', 
 'text_name': 'Enlil and Sud',
 'version': 'A', 
 'lang': 'sux',
 'cf': 'šeŋ',
 'gw': 'cook',
 'pos': 'V/t',
 'form': 'šeŋ₆-ŋa₂',
 'line_no' : 'A115',
 'line_ref': 109,
 'extent': ''}
```

Note that in the process the transliteration and lemmatization data have been replaced by [epsd2][] style data. The function `tounicode()` replaces `j` by `ŋ` , `c` by `š`, etc. and substitutes Unicode subscript numbers for the regular numbers in sign indexes. The function `etcsl_to_oracc()`replaces [ETCSL][] style lemmatization with [epsd2][] style (`gw` 'cook' instead of `label= "to be hot"`). Both replacements use dictionaries in the `equivalencies.json` file.  

The sections below will discuss in some detail the various functions, starting with `parsetext()` and going down the hierarchy to `etcsl_to_oracc()`. In the notebook, the functions are defined in the opposite order, because a function cannot be called before it has been defined.

### 2.4.7 Parsetext()

For each `XML` file, the function `parsetext()` is called by the main process. After opening the `XML` file `parsetext()` first calls the function `ampersands()` in order to replace HTML entities by their unicode counterparts ([2.4.3](#2.4.3-Pre-processing:-HTML-entities)). The module `etree` from the `lxml` library is used to read the `XML` tree. Since `etree` does not read the `XML` directly from file, but rather reads the output of the `ampersands()` function, we need the function `fromstring()`:

```python
tree = etree.fromstring(xmltext)
```

After creating the tree the function `mark_extra()` ([2.4.4](#2.4.4-Pre-Processing:-Additional-Text-and-Secondary-Text)) is called in order to explicitly mark "additional" and "secondary" words.  The composition name is found in the node `title`. This name is slightly adjusted in two ways. First, all [ETCSL][] text names include the phrase " -- a composite transliteration". This is useful for online presentation, but not for computational text analysis. Second, some titles include commas, which create problems when data are saved in `cvs`. These two elements are removed from the title.

```python
name = tree.xpath('string(//title)')
name = name.replace(' -- a composite transliteration', '')
name = name.replace(',', '')
```



The dictionary `meta_d`, which was created as an empty dictionary in the main process, is now filled with meta data on the composition level: the text ID (the [ETCSL][] text number, for instance c.1.4.1 for Inana's Descent) and the text name. Finally, the line reference count is set to 0. This line reference will be used and manipulated in the function `getline()`.

The `XML` tree is now forwarded to the function `getversion()`.

### 2.4.8 Getversion()

In some cases an [ETCSL][] file contains different versions of the same composition. The versions may be distinguished as 'Version A' vs. 'Version B' or may indicate the provenance of the version ('A version from Urim' vs. 'A version from Nibru'). In the edition of the proverbs the same mechanism is used to distinguish between numerous tablets (often lentils) that contain just one proverb (or a few), and are collected in the files "Proverbs from Susa," "Proverbs from Nibru," etc. ([ETCSL][] c.6.2.1 - c.6.2.5).

The function `getversion()` is called by the function `parsetext()` and receives one argument: `tree` (the `etree` object). The function updates`meta_d`, a dictionary of meta data. The function checks to see if versions are available in the file that is being parsed. Versions are marked by a node `body`with a child `head`. The node `head` contains the name of the version. For each set of `XML` nodes that represents one version the code adds the version name to the `meta_d` dictionary and then calls the `getsection()` dictionary. The sole argument is the portion of the tree that represents the version that is being parsed. If a composition is not divided into versions the entire tree is passed to `getsection()` and the version name is the empty string.

### 2.4.9 Getsection()

Some compositions in [ETCSL][] are divided into *sections*. This is usually the case when there are gaps of unknown length. Section B supposedly follows section A, but how much text is missing between these sections cannot be reconstructed.
The function `getsection()` works essentially in the same way as `getversion()`. The code will check whether the composition (or a version of the composition) is divided into sections. Sections are indicated in the `XML` with a node `div1`. If such nodes are detected, the function will pull the name of that section (an attribute of `div1` called `n`) and store it in a temporary variable. Section names are usually capital letters that are prefixed to the line number. The function will now collect all `l` (line) *and* `gap` nodes. The Xpath expression that is used for that is `.//l|.//gap`. In some regards gaps are treated as lines - they need to be placed after the last extant line and before the first line after the break. If the node is an `l` node the `meta_d`dictionary is updated with a line number (or section + line number, if the text is divided into sections)The function then calls `getline()`. The only argument of `getline()` is the part of the `XML` tree that belongs to a single line or gap. 

### 2.4.10 Getline()

The function `getline()`first updates the field `line_ref` in `meta_d`, increasing it by 1. The data type `line_ref` is integer - it is used to keep lines and gaps in correct order.

If `getline()` receives a `gap` node it copies all the metadata in the dictionary meta_d into the dictionary `line` and adds a field `extent` (the length of the gap). This data is found in the attribute `extent` of the `gap` node.

If `getline()` receives an `l` node it will collect `w` nodes (words) and `gloss` nodes with the language attribute `akk`. The Xpath expression looks as follows: './/w|.//gloss[@lang="akk"]'. This will find both Sumerian and Akkadian words in the text.

The found nodes are sent to `getword()`.

### 2.4.11 Getword()

The function `getword()` is the most complex of the series of functions because different types of words are processed in different ways.

As a first step `getword()` will copy all the meta-data in the dictionary `meta_d` into the dictionary `word`. This dictionary will hold all the data for one individual word token.

If `getword()` receives a `gloss` node, this is an Akkadian word, or an entire Akkadian phrase or sentence, that is inserted in a Sumerian text as a translation gloss. Akkadian words are not lemmatized in [ETCSL][], so all we can collect is the `form` (the transliteration) and the language. These fields are added to the `word` dictionary, `word` is appended to the list `alltexts` and control is returned to the previous function (`getline()`), which will send the next word.

If `getword()` receives a `w` node (a word) it will assign different attributes of that node to different fields in the `word` dictionary. The Citation Form (`cf`) is found in the attribute `lemma`. 

The Guide Word (`gw`) is found in the attribute `label` and the Part of Speech (`pos`) in the attribute `pos`.  

The rest of the code takes care of some special situations:

* If there is no attribute `pos`, this indicates that the word was not lemmatized (because it is broken or unknown). In such cases `pos` and `gw` are both assigned 'NA'. Note that 'NA' is a string, not Missing Value.
* if the word has an attribute `emesal`, then the citation form is found in that attribute and the language is "sux-x-emesal". If there is no such attribute the language is "sux" (for Sumerian).
* In [ETCSL][] **proper nouns** are nouns (`pos` = "N"), which are qualified by an additional attribute `type` (Divine Name, Personal Name, Geographical Name, etc.; abbreviated as DN, PN, GN, etc.). In [ORACC][] a word has a single `pos`; for proper nouns this is DN, PN, GN, etc. - so what is `type` in [ETCSL][] becomes `pos` in [ORACC][]. [ORACC][] proper nouns usually do not have a guide word (only a number to enable disambiguation of namesakes). The [ETCSL][] guide words (`label`) for names come pretty close to [ORACC][] citation forms. Proper nouns are therefore formatted differently from other nouns.
* Finally, in pre-processing we added to some `w` nodes an attribute `status`, which is either 'additional' or 'secondary'. If the attribute exists, it is added to the `word` dictionary.

The dictionary `word` now has all the information it needs, but Citation Form, Guide Word, and Part of Speech are still mostly in [ETCSL][] format. The function `getword()` calls `tounicode()`to change (Sumerian) text from ASCII to Unicode representation. The argument of `tounicode()` is a string, the `form` or the `cf` (Citation Form) of the word that is being processed. The function returns the same string in Unicode representation.

The function `getword()`, finally sends the `word` dictionary to `etcsl_to_oracc` for final formatting of these data elements.

### 2.4.12 tounicode()

The main function of `tounicode()` is to change 'c' into  'š', 'j' into 'ŋ', 'e2' into 'e₂', etc. This is done in two steps. First sign index numbers are changed from regular numbers into Unicode index numbers (du3 > du₃). The replacement of sign index numbers is complicated by the fact that `Citation Forms` and `Forms` may include real numbers, as in **7-ta-am3** where the **7** should remain unchanged, while **am3** should become **am₃**. The replacement routine for numbers, therefore, uses a "look-behind" [regular expression](http://www.regular-expressions.info/) to check what character is found before the digit to be replaced. If this is a letter (a-z or A-Z) the digit is replaced by its Unicode subscript counterpart. Otherwise it is left unchanged. In a second run the same code is used to take care of the second digit in 2-digit indexes (as in šeg₁₂), now with the unicode index digits in the look behind regular expression. The routine uses the dictionary `index_no` in `equivalencies.json`, which lists the digits 0-9 (and x) as keys, and their unicode counterparts as values.

```python
for key in eq["index_no"]: 
	x = re.sub(r'(?<=[a-zA-Z])'+key, eq["index_no"][key], x)
for key in eq["index_no"]: 
	x = re.sub(r'(?<=[₀-₉])'+key, eq["index_no"][key], x)
```
Finally,  `tounicode()` use the dictionary `ascii_unicode` (also in the file `equivalencies.json` to replace 'c' by 'š', 'j' by 'ŋ', etc.

### 2.4.13 etcsl_to_oracc()

The function receives a single argument, the dictionary `word` that was created in `getword()`. The function will look up each lemma (a combination of Citation Form, Guide Word, and Part of Speech) in the dictionary `equiv`. This dictionary is a combination of three dictionaries in the file `equivalecies.json`, namely `suxwords`, `emesalwords` and `propernouns`. If the lemma is found in equiv, the [ETCSL][] forms of `cf`, `gw`, and `pos` are replaced by their [ORACC][] counterparts.
In the `equiv` dictionary the lemmas are stored in the following format:
```json
"taka₄[to leave behind]V": {
            "gw": "abandon",
            "pos": "V/t",
            "cf": "taka"
        },
 "me-te-ŋal₂[seemly]AJ": {
            "gw": "seemly",
            "pos": "AJ",
            "cf": "meteŋal"
        }
```
The keys in this dictionary are combinations of `cf`, `gw`, and `pos` ([ETCSL][]-style) in a single string. The `etcsl_to_oracc()` function, therefore first has to create the `lemma` from the fields `cf`, `gw`, and `pos` before it can look the word up in `equiv`. 

In a few cases a single word in [ETCSL][] is represented by a sequence of two words in [EPSD2][] style. This is represented as follows in the `JSON`:

```json
 "maš₂-sa-la₂[bug-ridden goat]N": {
            "cf": "maš",
     		"pos": "N",
            "gw": "goat",
     		"cf2": "sala",
            "pos2": "AJ",
		    "gw2": "bug-ridden" 
        },
```

The code checks for the existence of a `cf2`key. If present, a new dictionary is created (`word2`) and both dictionaries (`word` and `word2`) are appended to the list `alltexts`.

If the lemma is not found in the `equiv` list the `word` dictionary is left unchanged and appended to the list `alltexts`.

### 2.4.14 Post-processing

The DataFrame that is the result of the notebook is saved as a `csv` file named `alltexts.csv`, where each word form occupies a single row. In many cases, however, we may want to represent the data in a line-by-line or composition-by-composition format and/or filter out certain words (for instance: use only lemmatized words, remove Akkadian words, remove "additional" and/or "secondary" text - etc.). Such transformations can be done most easily in our `Pandas` DataFrame. The code for doing so is essentially the same as the code for structuring [ORACC][] data discussed in Chapter 2.3: Data Acquisition ORACC (see the [Basic ORACC-JSON Parser](https://github.com/niekveldhuis/CompAss/blob/master/2_3_Data_Acquisition_ORACC/2_3_2_basic_ORACC-JSON_parser.ipynb)).


[ETCSL]:                               http://etcsl.orinst.ox.ac.uk
[ORACC]:                             http://oracc.org
[epsd2]:                               http://oracc.org/epsd2/sux
[epsd2/etcsl]: http://oracc.museum.upenn.edu/epsd2/etcsl/
[Inana's Descent to the Netherworld]: http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&amp;amp;amp;display=Crit&amp;amp;amp;charenc=gcirc#
[Oxford Text Archive]:       http://ota.ox.ac.uk/desc/2518
[COMPASS]:	http://oracc.org/compass

