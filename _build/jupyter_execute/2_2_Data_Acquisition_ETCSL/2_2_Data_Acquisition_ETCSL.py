#!/usr/bin/env python
# coding: utf-8

# (2.2)=
# # 2.2 Data Acquisition ETCSL
# ## 2.2.1. Introduction
# 
# The Electronic Text Corpus of Sumerian Literature ([ETCSL](http://etcsl.orinst.ox.ac.uk)) provides editions and translations of 394 Sumerian literary texts, mostly from the Old Babylonian period (around 1800 BCE). The project was founded by Jeremy Black (Oxford University), who sadly passed away in 2004; it was active from 1998 to 2006, when it was archived. Information about the project, its stages, products and collaborators may be found in the project's [About](http://etcsl.orinst.ox.ac.uk/edition2/general.php) page. By the time of its inception [ETCSL](http://etcsl.orinst.ox.ac.uk) was a pioneering effort - the first large digital project in Assyriology, using well-structured data according to the standards and best practices of the time. [ETCSL](http://etcsl.orinst.ox.ac.uk) allows for various kinds of searches in Sumerian and in English translation and provides lemmatization for each individual word. Numerous scholars contributed data sets to the [ETCSL](http://etcsl.orinst.ox.ac.uk) project (see [Acknowledgements](http://etcsl.orinst.ox.ac.uk/edition2/credits.php#ack)). The availability of [ETCSL](http://etcsl.orinst.ox.ac.uk) has fundamentally altered the study of Sumerian literature and has made this literature available for undergraduate teaching.
# 
# ```{figure} ../images/JeremyBlack.jpg
# :figclass: margin
# [Jeremy Black](https://cdli.ox.ac.uk/wiki/doku.php?id=black_jeremy_allen) 1951-2004
# ```
# 
# The original [ETCSL](http://etcsl.orinst.ox.ac.uk) files in TEI XML are stored in the [Oxford Text Archive](http://hdl.handle.net/20.500.12024/2518) from where they can be downloaded as a ZIP file under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License ([by-nc-sa 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/)). The copyright holders are Jeremy Black, Graham Cunningham, Jarle Ebeling, Esther Flückiger-Hawker, Eleanor Robson, Jon Taylor, and Gábor Zólyomi.
# 
# The [Oxford Text Archive](http://hdl.handle.net/20.500.12024/2518) page offers the following description:
# 
# > The Electronic Text Corpus of Sumerian Literature (ETCSL) comprises transliterations and English translations of 394 compositions attested on sources dating to the period from approximately 2100 to 1700 BCE. The compositions are divided into seven categories: ancient literary catalogues; narrative compositions; royal praise poetry and hymns to deities on behalf of rulers; literary letters and letter-prayers; divine and temple hymns; proverbs and proverb collections; and a more general category including compositions such as debates, dialogues and riddles. The numbering of the compositions within the corpus follows Miguel Civil's unpublished catalogue of Sumerian literature (etcslfullcat.html). Files with an initial c are composite transliterations (a reconstructed text editorially assembled from the extant exemplars but including substantive variants) in which the cuneiform signs are represented in the Roman alphabet. Files with an initial t are translations. The composite files include full references for the cuneiform sources and author-date references for the secondary sources (detailed in bibliography.xml). The composite and translation files are in XML and have been annotated according to the TEI guidelines. In terms of linguistic information, each word form in the composite transliterations has been assigned to a lexeme which is specified by a citation form, word class information and basic English translation.
# 
# Since [ETCSL](http://etcsl.orinst.ox.ac.uk) is an archival site, the editions are not updated to reflect new text finds or new insights in the Sumerian language. Many of the [ETCSL](http://etcsl.orinst.ox.ac.uk) editions were based on standard print editions that itself may have been 10 or 20 years old by the time they were digitized. Any computational analysis of the [ETCSL](http://etcsl.orinst.ox.ac.uk) corpus will have to deal with the fact that: 
# 
# - the text may not represent the latest standard
# - the [ETCSL](http://etcsl.orinst.ox.ac.uk) corpus is extensive - but does not cover all of Sumerian literature known today
# 
# ```{figure} ../images/P346466.jpg
# :scale: 50%
# Sumerian literary fragment: [UET 6, 427](http://cdli.ucla.edu/P346466) with a few lines of [Inana's Descent to the Netherworld](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&amp;amp;amp;display=Crit&amp;amp;amp;charenc=gcirc#)
# ```
# 
# In terms of data acquisition, one way to deal with these limitations is to make the [ETCSL](http://etcsl.orinst.ox.ac.uk) data as much as possible compatible with the data standards of the Open Richly Annotated Cuneiform Corpus ([ORACC](http://oracc.org)). [ORACC](http://oracc.org) is an active project where new or updated editions can be produced. If compatible, if [ETCSL](http://etcsl.orinst.ox.ac.uk) and [ORACC](http://oracc.org) data may be freely mixed and matched, then the [ETCSL](http://etcsl.orinst.ox.ac.uk) data set can effectively be updated and expanded.
# 
# The [ETCSL](http://etcsl.orinst.ox.ac.uk) text corpus was one of the core data sets for the development of of [ePSD1](http://psd.museum.upenn.edu/epsd1/index.html) and [ePSD2](http://oracc.org/epsd2), and the ePSD version of the [ETCSL](http://etcsl.orinst.ox.ac.uk) data forms the core of the literary corpus collected in [ePSD2/literary](http://oracc.org/epsd2/literary). In order to harvest the [ETCSL](http://etcsl.orinst.ox.ac.uk) data for [ePSD2](http://oracc.org/epsd2) the lemmatization was adapted to [ORACC](http://oracc.org) standards and thus the [ePSD2/literary](http://oracc.org/epsd2/literary) version of the [ETCSL](http://etcsl.orinst.ox.ac.uk) dataset is fully compatible with any [ORACC](http://oracc.org) dataset, and can be parsed with the ORACC parser, discussed in section [2.1](2.1). However, [ePSD2/literary](http://oracc.org/epsd2/literary) is not identical with the [ETCSL](http://etcsl.orinst.ox.ac.uk) data set. Several compositions have been replaced by more recent editions (for instance the Sumerian disputations edited in the [ORACC](http://oracc.org) project [Datenbank Sumerischer Streitliteratur](http://oracc.org/dsst)); a significant number of texts that were not available in [ETCSL](http://etcsl.orinst.ox.ac.uk) have been added (many of them published after 2006) and the Gudea Cylinders have been moved to [epsd2/royal](http://oracc.org/epsd2/royal/Q000377), where they more properly belong.
# 
# For some applications, therefore, parsing the original [ETCSL](http://etcsl.orinst.ox.ac.uk) XML TEI files has become redundant since a fuller and more up-to-date version of the data set is available in [epsd2/literary](http://oracc.org/epsd2/literary). . However, any data transformation implies choices and it is hard to know what the needs will be of future computational approaches to the [ETCSL](http://etcsl.orinst.ox.ac.uk) dataset. The reason to include and discuss the [ETCSL](http://etcsl.orinst.ox.ac.uk) parser here is, first, to offer users the opportunity to work with the original data set. The various transformations included in the current parser may be adapted and adjusted to reflect the preferences and research questions of the user. As a concrete example of choices to be made, [ETCSL](http://etcsl.orinst.ox.ac.uk) distinguishes between main text, secondary text, and additional text, to reflect different types of variants between manuscripts (see below [2.2.4](2.2.4)). The [ePSD2/literary](http://oracc.org/epsd2/literary) data set does not include this distinction. The output of the current parser will indicate for each word whether it is "secondary" or "additional" (according to [ETCSL](http://etcsl.orinst.ox.ac.uk) criteria) and offer the possibility to include such words or exclude them from the analysis. Similarly, the translations are not included in the [ePSD2/literary](http://oracc.org/epsd2/literary) dataset, nor are they considered by the present parser. Translation data are, however, available in the [ETCSL](http://etcsl.orinst.ox.ac.uk) XML TEI file set and the XML of the transcription files marks the beginning and end of translation paragraphs. Such data, therefore, is available and one may well imagine research questions for which the translation files are relevant (e.g. translation alignment). Although the present code does not deal with translation, one may use the same techniques and the same approach exemplified here to retrieve such data.
# 
# In order to achieve compatibility between [ETCSL](http://etcsl.orinst.ox.ac.uk) and [ORACC](http://oracc.org) the code uses a number of equivalency dictionaries, that enable replacement of characters, words, or names. These equivalency dictionaries are made available in JSON format (for JSON see section [2.1.1](2.1.1) in the file `equivalencies.json` in the directory `equivalencies`.

# ### 2.2.1.1 XML
# The [ETCSL](http://etcsl.orinst.ox.ac.uk) files as distributed by the [Oxford Text Archive](http://hdl.handle.net/20.500.12024/2518) are encoded in a dialect of XML (Extensible Markup Language) that is referred to as `TEI` (Text Encoding Initiative). In this encoding each word (in transliteration) is an *element* that is surrounded by `<w>` and `</w>` tags. Inside the start-tag the word may receive several attributes, encoded as name/value pairs, as in the following random examples:
# 
# ```xml
# <w form="ti-a" lemma="te" pos="V" label="to approach">ti-a</w>
# <w form="e2-jar8-bi" lemma="e2-jar8" pos="N" label="wall">e2-jar8-bi</w>
# <w form="ickila-bi" lemma="ickila" pos="N" label="shell"><term id="c1813.t1">ickila</term><gloss lang="sux" target="c1813.t1">la</gloss>-bi</w>
# ```
# 
# The `form` attribute is the full form of the word, including morphology, but omitting flags (such as question marks), indication of breakage, or glosses. The `lemma` attribute is the form minus morphology (similar to `Citation Form` in [ORACC](http://oracc.org). Some lemmas may be spelled in more than one way in Sumerian; the `lemma` attribute will use a standard spelling (note, for instance, that the `lemma` of "ti-a" is "te"). The `lemma` in [ETCSL](http://etcsl.orinst.ox.ac.uk) (unlike `Citation Form` in [ORACC](http://oracc.org)) uses actual transliteration with hyphens and sign index numbers (as in `lemma = "e2-jar8"`, where the corresponding [ORACC](http://oracc.org) `Citation Form` is [egar](http://oracc.org/epsd2/o0026723).
# 
# :::{note} ETCSL vs ORACC: terminology and conventions
# :class: tip, dropdown
# 
# | Data Type  | ETCSL term | ETCSL example  | ORACC term    | ORACC example |
# | --- | --- | --- | --- | ---- |
# | Transliteration | form | e2-jar8-bi | form | e₂-gar₈-bi |
# | Dictionary Form | lemma  | e2-jar8  | citation form | egar | 
# | Part of Speech | pos  | N  | pos | N |
# | Basic Translation | label | wall | guide word | wall |
# 
# :::
# 
# 
# The `label` attribute gives a general indication of the meaning of the Sumerian word but is not context-sensitive. That is, the `label` of "lugal" is always "king", even if in context the word means "owner". The `pos` attribute gives the Part of Speech, but again the attribute is not context-sensitive. Where a verb (such as sag₉, to be good) is used as an adjective the `pos` is still "V" (for verb). Together `lemma`, `label`, and `pos` define a Sumerian lemma (dictionary entry).
# 
# In parsing the [ETCSL](http://etcsl.orinst.ox.ac.uk) files we will be looking for the `<w>` and `</w>` tags to isolate words and their attributes. Higher level tags identify lines (`<l>` and `</l>`), versions, secondary text (found only in a minority of sources), etcetera. The XML data structure is hierarchical and may be represented as a tree with a trunk, main branches, and ever smaller branches that all, eventually, connect to the same tree.
# 
# The [ETCSL](http://etcsl.orinst.ox.ac.uk) file set includes the file [etcslmanual.html](http://etcsl.orinst.ox.ac.uk/edition2/etcslmanual.php) with explanations of the tags, their attributes, and their proper usage.
# 
# Goal of the parsing process is to get as much information as possible out of the XML tree in a format that is as close as possible to the output of the [ORACC](http://oracc.org/) parser. The output of the parser is a word-by-word (or rather lemma-by-lemma) representation of the entire [ETCSL](http://etcsl.orinst.ox.ac.uk) corpus. For most computational projects it will be necessary to group words into lines or compositions, or to separate out a particular group of compositions. The data is structured in such a way that that can be achieved with a standard set of Python functions of the `pandas` library.
# 
# ### 2.2.1.2 Parsing XML: Xpath, and lxml
# 
# :::{margin}
# For proper introductions to `Xpath` and `lxml` see the [Wikipedia](https://en.wikipedia.org/wiki/XPath) article on `Xpath` and the homepage of the [lxml](https://lxml.de/) library, respectively.
# :::
# 
# There are several Python libraries specifically for parsing XML, among them the popular `ElementTree` and its twin `cElementTree`. The library `lxml` is largely compatible with `ElementTree` and `cElementTree` but differs from those in its full support of `Xpath`. `Xpath` is a language for finding and retrieving elements and attributes in XML trees. `Xpath` is not a program or a library, but a set of specifications that is implemented in a variety of software packages in different programming languages. 
# 
# `Xpath` uses the forward slash to describe a path through the hierarchy of the XML tree. The expression `"/body/l/w"` refers to all the `w` (word) elements that are children of `l` (line) elements that are children of the `body` element in the top level of XML hierarchy.
# 
# The expression `'//w'`means: all the `w` nodes, wherever in the hierarchy of the XML tree. The expression may be used to create a list of all the `w` nodes with all of their associated attributes. The attributes of a node are addressed  with the `@` sign, so that `//w/@label` refers to the `label` attributes of all the `w` nodes at any level in the hierarchy. 
# 
# ```python
# words = tree.xpath('//w')
# labels = tree.xpath('//w/@label')
# ```
# 
# Predicates are put between square brackets and describe conditions for filtering a node set. The expression  `//w[@emesal]` will return all the `w` elements that have an attribute `emesal`. 
# 
# `Xpath` also defines hundreds of functions. An important function is `'string()'` which will return the string value of a node or an attribute.  Once all `w` nodes are listed in the list `words` (with the code above) one may extract the transliteration and Guide Word (`label` in [ETCSL](http://etcsl.orinst.ox.ac.uk)) of each word as follows:
# 
# ```python
# form_l = []
# gw_l = []
# for node in words:
#     form = node.xpath('string(.)') 
#     form_l.append(form)
#     gw = node.xpath('string(@label)')
#     gw_l.append(gw)
# ```
# 
# The dot, the argument to the `string()` function in `node.xpath('string(.)')`, refers to the current node.

# ### 2.2.1.3 Parsing the XML Tree
# 
# The module `etree` from the `lxml` library is used to parse the XML files. The code basically works from the highest level of the hierarchy of the XML tree to the lowest, in the following way:
# 
# ```
# corpus									main process
# 	text								parsetext()
# 		version							getversion()
# 			segment						getsegment()
# 				line					getline()
# 					word				getword()
# 						format			etcsl_to_oracc()
# ```
# 
# Each of these functions divides the XML tree into smaller parts (versions, segments, lines, words) and sends one such smaller part of the tree to the next function. The functions do not return anything. Instead, they modify the dictionary `meta_d` by adding or changing keys that hold meta-data such as version name, line number, etc. Once arrived at the word level (the most basic level of this tree) the dictionary `meta_d` will hold accurate information about the composition name, the version name, the line number, etc. for this particular word. The function `getword()` will gather lemmatization information (form, citation form, part of speech, etc.) from the attributes of the `w` node, and meta-data from `meta_d`.
# 
# The function `etcsl_to_oracc()`, the last one in the hierarchy, transforms the [ETCSL](https://etcsl.orinst.ox.ac.uk/) style lemma into a [ORACC](http://oracc.org/) style lemma and appends the resulting dictionary data to a list (a list of dictionaries). In the end, each word in the entire [ETCSL](https://etcsl.orinst.ox.ac.uk/) corpus will have its own entry in this list.
# 
# The word `šeŋ₆-ŋa₂` in the file `c.1.2.2.xml` ([Enlil and Sud](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.2.2&display=Crit&charenc=gcirc#)), in Version A, segment A line 115, looks as follows in the original XML file: 
# 
# ```xml
# <w form="cej6-ja2" lemma="cej6" pos="V" label="to be hot">cej6-ja2</w>
# ```
# 
# The dictionary that is the result of the parsing process represents that same word as follows:
# 
# ```python
# {'id_text': 'c.1.2.2', 
#  'text_name': 'Enlil and Sud',
#  'version': 'A', 
#  'lang': 'sux',
#  'cf': 'šeŋ',
#  'gw': 'cook',
#  'pos': 'V/t',
#  'form': 'šeŋ₆-ŋa₂',
#  'label' : 'A115',
#  'id_line': 109,
#  'extent': ''}
# ```
# 
# :::{note}
# 
# In the process the transliteration and lemmatization data have been replaced by [ePSD2](http://oracc.org/epsd2) style data and terminology: ('gw' :  'cook' instead of 'label= "to be hot"' and 'cf' : 'šeŋ' instead of 'lemma="cej6"').  
# 
# :::
# 
# The sections below will discuss in some detail the various functions, starting with the pre-processing functions and going up the hierarchy from `etcsl_to_oracc()` to  `parsetext()`. 
# 
# :::{note}
# 
# The logic of the entire process goes from `parsetext()` via `getversion()` etc. down to `etcsl_to _oracc()`. Each of these functions calls the next one and since a function cannot be called before it is defined, we have to define the last function first and deal with them in the opposite order.
# 
# :::

# ## 2.2.2 Setting Up
# ### 2.2.2.1 Import Packages
# 
# :::{margin}
# For proper installation of packages for a Jupyter Notebook see [1.4.3 install_packages](1.4.3).
# :::
# 
# Before running this cell you may need to install the package `lxml` (for parsing XML) by running 
# ```python
# %conda install lxml
# ```
# 
# :::{important}
# 
# This notebook expects the following files and directories:
# 
# 1. Directory `etcsl/transliterations/`  
#    This directory should contain the [ETCSL](http://etcsl.orinst.ox.ac.uk) `TEI XML` transliteration files. The files may be downloaded from the [Oxford Text Archive](http://hdl.handle.net/20.500.12024/2518). The files are found in the directory `transliterations` in the file `etcsl.zip`, .
# 2. Directory `Equivalencies`  
#    `equivalencies.json`: a set of equivalency dictionaries used at various places in the parser. The directory and the file are included in the [COMPASS](https://github.com/niekveldhuis/compass) file set (see section [1.4.1](1.4.1).
# 3. Directory `output`.
# The output is saved in the `output` directory as a single `.csv` file. If the directory does not exist, it is created in the next cell.
# 
# :::

# * re: regular expressions
# * lxml: tools for parsing an XML tree
# * os: for basic Operating System operations (such as creating a directory)
# * json: for reading the equivalency dictionaries in JSON format
# * pandas: data analysis and manipulation; dataframes
# * tqdm: progress bar

# In[1]:


import re
from lxml import etree
import os
import json
import pandas as pd
from tqdm.auto import tqdm
os.makedirs('output', exist_ok = True)


# (2.2.2.2)=
# ### 2.2.2.2 Load Equivalencies 
# The file `equivalencies.json` contains a number of dictionaries that will be used to search and replace at various places in this notebook. The dictionaries are:
# - `suxwords`: Sumerian words (Citation Form, GuideWord, and Part of Speech) in [ETCSL](http://etcsl.orinst.ox.ac.uk) format and their [ORACC](http://oracc.org) counterparts.
# - `emesalwords`: idem for Emesal words
# - `propernouns`: idem for proper nouns
# - `ampersands`: HTML entities (such as `&aacute;`) and their Unicode counterparts (`á`; see section [2.2.3](2.2.3)).
# - `versions`: [ETCSL](http://etcsl.orinst.ox.ac.uk) version names and (abbreviated) equivalents
# 
# The `equivalencies.json` file is loaded with the `json` library (for JSON and the `json` library, see section [2.1.1](2.1.1)). The dictionaries `suxwords`, `emesalwords` and `propernouns` (which, together, contain the entire [ETCSL](http://etcsl.orinst.ox.ac.uk) vocabulary) are concatenated into a single dictionary.

# In[2]:


with open("equivalencies/equivalencies.json", encoding="utf-8") as f:
    eq = json.load(f)
equiv = eq["suxwords"]
equiv.update(eq["emesalwords"])
equiv.update(eq["propernouns"])


# (2.2.3)=
# ## 2.2.3 Pre-processing: HTML-entities
# Before the XML files can be parsed, it is necessary to remove character sequences that are not allowed in XML proper (so-called HTML entities). 
# 
# In non-transliteration contexts (bibliographies, composition titles, etc.) [ETCSL](https://etcsl.orinst.ox.ac.uk/) uses so-called HTML entities to represent non-ASCII characters such as,  á, ü, or š. These entities are encoded with an opening ampersand (`&`) and a closing semicolon (`;`). For instance, `&C;` represents the character `Š`. The HTML entities are for the most part project-specific and are declared in the file `etcsl-sux.ent` which is part of the file package and is used by the [ETCSL](https://etcsl.orinst.ox.ac.uk/) project in the process of validating and parsing the XML for on-line publication.
# 
# For purposes of data acquisition these entities need to be resolved, because XML parsers will not recognize these sequences as valid XML. 
# 
# The key `ampersands` in the file `equivalencies.json` has as its value a dictionary, listing all the HTML entities that appear in the [ETCSL](https://etcsl.orinst.ox.ac.uk/) files with their Unicode counterparts:
# 
# ```json
# { 
#  "&C;": "Š",
#  "&Ccedil;": "Ç",
#  "&Eacute;": "É",
#  "&G;": "Ŋ",
#  "&H;": "H",
#  "&Imacr;": "Î",
#  "&X;" : "X",
#  "&aacute;": "á"
# }
# ```
# 
# etc.
# 
# This dictionary is used to replace each HTML entity with its unicode (UTF-8) counterpart in the entire corpus.
# 
# :::{margin}
# The regular expression `[^;]+` means: a sequence of one or more (`+`) characters, except the semicolon. The symbol `^` is the negation symbol in regular expressions. The expression `&[^;]+;` therefore captures a sequence of any length that begins with an ampersand and ends with a semicolon. There are many introductions for regular expressions on the web, for instance [regular-expressions.info](https://www.regular-expressions.info/), or [An Introduction to Regular Expressions](https://www.oreilly.com/content/an-introduction-to-regular-expressions/) by Thomas Nield.
# :::
# 
# The function `ampersands()` is called in `parsetext()` (see section [2.2.11](2.2.11) before the `etree` is built. The function uses the `sub()` function from the `re` (Regular Expressions) module. The arguments of this function are `sub(find_what, replace_with, text)`. In this case, the `find_what` is the compiled regular expression `amp`, matching all character sequences that begin with & and end with a semicolon (;). This regular expression is defined in the main process (see section [2.2.12](2.2.12) as follows:
# 
# ```python
# amp = re.compile(r'&[^;]+;')
# ```
# 
# The `replace_with` argument is a temporary `lambda` function that uses the `ampersands` dictionary to find the utf-8 counterpart of the HTML entity. The dictionary is queried with the `get()` function (m.group(0) represents the match of the regular expression `amp`). The `get()` function allows a fall-back argument, to be returned in case the dictionary does not have the key that was requested. This second argument is the actual regular expression match, so that in those cases where the dictionary does not contain the match it is replaced by itself.

# In[3]:


def ampersands(string):    
    string = re.sub(amp, lambda m: 
               eq["ampersands"].get(m.group(0), m.group(0)), string)
    return string


# (2.2.4)=
# ## 2.2.4 Pre-Processing: Additional Text and Secondary Text
# 
# In order to be able to preserve the [ETCSL](http://etcsl.orinst.ox.ac.uk) distinctions between main text (the default), secondary text, and additional text, such information needs to be added as an attribute to each `w` node (word node). This must take place in pre-processing, before the XML file is parsed.
# 
# [ETCSL](http://etcsl.orinst.ox.ac.uk) transliterations represent composite texts, put together (in most cases) from multiple exemplars. The editions include substantive variants, which are marked either as "additional" or as "secondary". Additional text consists of words or lines that are *added* to the text in a minority of sources. In the opening passage of [Inana's Descent to the Netherworld](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&amp;amp;amp;display=Crit&amp;amp;amp;charenc=gcirc#), for instance, there is a list of temples that Inana leaves behind. One exemplar extends this list with eight more temples; in the composite text these lines are marked as "additional" and numbered lines 13A-13H. Secondary text, on the other hand, is variant text (words or lines) that are found in a minority of sources *instead of* the primary text. An example in [Inana's Descent to the Netherworld](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&amp;amp;amp;display=Crit&amp;amp;amp;charenc=gcirc#) is lines 30-31, which are replaced by 30A-31A in one manuscript (text and translation from [ETCSL](http://etcsl.orinst.ox.ac.uk)):
# 
# | line | text                                       | translation                                                  |
# | ---- | ------------------------------------------ | ------------------------------------------------------------ |
# | 30   | sukkal e-ne-eĝ₃ sag₉-sag₉-ga-ĝu₁₀          | my minister who speaks fair words,                           |
# | 31   | ra-gaba e-ne-eĝ₃ ge-en-gen₆-na-ĝu₁₀        | my escort who speaks trustworthy words                       |
# | 30A  | \[na\] ga-e-de₅ na de₅-ĝu₁₀ ḫe₂-\[dab₅\]    | I am going to give you instructions: my instructions must be followed; |
# | 31A  | \[inim\] ga-ra-ab-dug₄ ĝizzal \[ḫe₂-em-ši-ak\] | I am going to say something to you: it must be observed      |
# 
# "Secondary text" and "additional text" can also consist of a single word and there are even cases of "additional text" within "additional text" (an additional word within an additional line).
# 
# In [ETCSL](http://etcsl.orinst.ox.ac.uk) TEI XML secondary/additional text is introduced by a tag of the type:
# 
# ```xml
# <addSpan to="c141.v11" type="secondary"/>
# ```
# 
# or
# 
# ```xml
# <addSpan to="c141.v11" type="additional"/>
# ```
# 
# The number c141 represents the text number in [ETCSL](http://etcsl.orinst.ox.ac.uk) (in this case [Inana's Descent to the Netherworld](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&amp;amp;amp;display=Crit&amp;amp;amp;charenc=gcirc#), text c.1.4.1). The return to the primary text is indicated by a tag of the type:
# 
# ```xml
# <anchor id="c141.v11"/>
# ```
# 
# Note that the `id` attribute in the `anchor` tag is identical to the `to` attribute in the `addSpan` tag.
# 
# We can collect all the `w` tags (words) between `addSpan` and its corresponding `anchor` tag with the following `xpath` expression:
# 
# ```python
# secondary = tree.xpath('//w[preceding::addSpan[@type="secondary"]/@to = following::anchor/@id]')
# ```
# 
# In the expression `preceding` and `following` are so-called `axes` (plural of `axis`) which describe the relationship of an element to another element in the tree. The expression means: get all `w` tags that are preceded by an `addSpan` tag and followed by an `anchor` tag. The `addSpan` tag has to have an attribute `type` with value `secondary` , and the value of the `to` attribute of this `addSpan` tag is to be equal to the `id` attribute of the following `anchor` tag.
# 
# Once we have collected all the "secondary" `w` tags this way, we can add a new attribute to each of these words in the following way:
# 
# ```python
# for word in secondary:
#     word.attrib["status"] = "secondary"
# ```
# 
# In the process of parsing we can retrieve this new `status` attribute to mark all of these words as `secondary`.
# 
# Since we can do exactly the same for "additional text" we can slightly adapt the above expression for use in the function `mark_extra()`
# 
# The function `mark_extra()` is called twice by the function `parsetext()` (see below, section [2.2.11](2.2.11)), once for "additional" and once for "secondary" text, indicated by the `which` argument. 

# In[4]:


def mark_extra(tree, which):
    extra = tree.xpath(f'//w[preceding::addSpan[@type="{which}"]/@to = following::anchor/@id]')
    for word in extra:
        word.attrib["status"] = which
    return tree


# (2.2.5)=
# ## 2.2.5 Transliteration Conventions
# 
# The function `tounicode()` is called in the function `getword()` to format Citation Forms and Forms (transliteration). It changes 'c' into  'š', 'j' into 'ŋ', 'e2' into 'e₂', etc. This is done in two steps. First sign index numbers are changed from regular numbers into Unicode index numbers (du3 > du₃). The replacement of sign index numbers is complicated by the fact that Citation Form and Form may include real numbers, as in 7-ta-am3 ("seven each") where the 7 should remain unchanged, while am3 should become am₃. The replacement routine for numbers uses a regular expression to search for a letter immediately followed by one or two digits. The regular expression and the accompanying translation table `transind` are defined in the main process (see [2.2.12](2.2.12)), as follows:
# 
# ```python
# ind = re.compile(r'[a-zŋḫṣšṭA-ZŊḪṢŠṬ][0-9x]{1,2}')
# ascind, uniind = '0123456789x', '₀₁₂₃₄₅₆₇₈₉ₓ'
# transind = str.maketrans(ascind, uniind)
# ```
# 
# :::{margin}
# 
# In this case it is not necessary to define a so-called look-behind in the regular expression `ind`. The match of `ind` includes the letter that precedes the index number, but since the translation table only has digits, this letter is returned unchanged.
# 
# :::
# 
# The replacement code uses the `re.sub()` function with a temporary lambda function to translate the regular digits into their Unicode subscript counterparts. Using a function in `re.sub()` was discussed above in section [2.2.3](2.2.3):
# 
# Finally,  `tounicode()` uses another `translate()` call to replace 'c' by 'š', 'j' by 'ŋ', etc, using the table `transcj` which is also created in the main process.
# 
# ```python
# asccj, unicj = 'cjCJ', 'šŋŠŊ'
# transcj = str.maketrans(asccj, unicj)
# 
# ```

# In[5]:


def tounicode(string):
    string = re.sub(ind, lambda m: m.group().translate(transind), string)
    string = string.translate(transcj)
    return string


# (2.2.6)=
# ## 2.2.6 Replace ETCSL-style by ORACC-style Lemmatization
# 
# The function `etcsl_to_oracc()` is called in the function `getword()` with a single argument: the dictionary `word`. This dictionary contains, besides meta data, the citation form, basic meaning ('label') and Part of Speech of a single word in ETCSL-style. The function will look up each lemma (a combination of Citation Form, Guide Word, and Part of Speech) in the dictionary `equiv`. This dictionary is a combination of three dictionaries in the file `equivalencies.json`, namely `suxwords`, `emesalwords` and `propernouns` (see [2.2.2.2](2.2.2.2)). If the lemma is found in `equiv`, the [ETCSL](https://etcsl.orinst.ox.ac.uk/) 'cf', 'gw', and 'pos' are replaced by their [ORACC](http://oracc.org/) counterparts.
# In the `equiv` dictionary the lemmas are stored in the following format:
# ```json
# {"taka₄[to leave behind]V": {
#             "gw": "abandon",
#             "pos": "V/t",
#             "cf": "taka"
#         },
#  "me-te-ŋal₂[seemly]AJ": {
#             "gw": "seemly",
#             "pos": "AJ",
#             "cf": "meteŋal"
#         }
# }
# ```
# The keys in this dictionary are combinations of 'cf', 'gw', and 'pos' ([ETCSL](https://etcsl.orinst.ox.ac.uk/)-style) in a single string. The `etcsl_to_oracc()` function, therefore first has to create the `lemma` from the fields `cf`, `gw`, and `pos` before it can look the word up in `equiv`. 
# 
# In a few cases a single word in [ETCSL](https://etcsl.orinst.ox.ac.uk/) is represented by a sequence of two words in [ePSD2](http://oracc.org/epsd2) style. This is represented as follows in the `equiv` dictionary:
# 
# ```json
#  {"maš₂-sa-la₂[bug-ridden goat]N": {
#      		"cf": "maš",
#      		"pos": "N",
#      		"gw": "goat",
#      		"cf2": "sala",
#      		"pos2": "AJ",
#      		"gw2": "bug-ridden" 
#         },}
# ```
# 
# The code checks for the existence of a `cf2` key. If present, a new dictionary is created (`word2`) and both dictionaries (`word` and `word2`) are appended to the list `alltexts`.
# 
# If the lemma is not found in the `equiv` list the `word` dictionary is left unchanged and appended to the list `alltexts`.

# In[6]:


def etcsl_to_oracc(word):
    lemma = f"{word['cf']}[{word['gw']}]{word['pos']}"
    if lemma in equiv:
        word['cf'] = equiv[lemma]["cf"]
        word["gw"] = equiv[lemma]["gw"]
        word["pos"] = equiv[lemma]["pos"]
        alltexts.append(word)
        if "cf2" in equiv[lemma]: # if an ETCSL word is replaced by two ORACC words
            word2 = word.copy()
            word2["cf"] = equiv[lemma]["cf2"]
            word2["gw"] = equiv[lemma]["gw2"]
            word2["pos"] = equiv[lemma]["pos2"]
            alltexts.append(word2)
    else: # word not found in equiv
        alltexts.append(word)
    return


# ## 2.2.7 Formatting Words
# 
# The function `getword()`, which is called by the function `getline()`,  is the most complex of the series of functions that parses the [ETCSL](http://etcsl.orinst.ox.ac.uk) data. This is the case because different types of words (regular Sumerian words, proper nouns, Emesal words, Akkadian glosses) are processed in different ways.
# 
# As a first step `getword()` will copy all the meta-data from the dictionary `meta_d` into the dictionary `word`. This dictionary will hold all the data for one individual word token.
# 
# :::{margin}
# 
# For Akkadian glosses in Sumerian literary texts, see Szilvia Sövegjártó, [*Sumerische Glossenhandschriften als Quellen des altbabylonischen hermeneutischen Denkens*](https://www.zaphon.de/sumerische-glossenhandschriften/en) (2020).
# 
# :::
# 
# If `getword()` receives a `gloss` node, this node represents either an Akkadian word, or an entire Akkadian phrase or sentence, that is inserted in a Sumerian text as a translation gloss. Akkadian words are not lemmatized in [ETCSL](https://etcsl.orinst.ox.ac.uk/), so all we can collect is the `form` (the transliteration) and the language. These fields are added to the `word` dictionary, `word` is appended to the list `alltexts` and control is returned to the previous function (`getline()`), which will send the next word.
# 
# If `getword()` receives a `w` node (a word) it will assign different attributes of that node to different fields in the `word` dictionary. The Citation Form ('cf') is found in the attribute `lemma`; the Guide Word ('gw') is found in the attribute `label`; and the Part of Speech ('pos') in the attribute `pos`.
# 
# :::{admonition} Sumerian word in ETCSL XML
# :class: tip, dropdown
# Sumerian [ŋen](http://oracc.org/epsd2/o0029256) "to go," in the form i-im-ŋen: 
# ```XML
# <w form="i-im-jen" lemma="jen" pos="V" label="to go">i-im-jen</w>
# ```
# 
# :::
# 
# The rest of the code takes care of some special situations:
# 
# * **Unlemmatized**: If there is no attribute `pos`, this indicates that the word was not lemmatized (because it is broken or unknown). In such cases `pos` and `gw` are both assigned 'NA'. Note that 'NA' is a string, not Missing Value.
# 
# * **Emesal words** in [ETCSL](http://etcsl.orinst.ox.ac.uk) use their Sumerian equivalents as `citation form` (attribute `lemma`), adding a separate attribute (`emesal`) for the Emesal form proper. This Emesal form is the one that is used as `citation form` in the output.
# 
# :::{admonition} Emesal word in ETCSL XML
# :class: tip, dropdown
# Sumerian [inim](http://oracc.org/epsd2/o0031116) ("word") in the Emesal form e-ne-eŋ₃:
# 
# ```xml
# <w form="e-ne-ej3" lemma="inim" pos="N" label="word" emesal="e-ne-ej3">e-ne-ej3</w> 
# ```
# 
# ::: 
# 
# * **Proper Nouns**: in [ETCSL](https://etcsl.orinst.ox.ac.uk/) proper nouns are nouns (`pos` = "N"), which are qualified by an additional attribute `type` (Divine Name, Personal Name, Geographical Name, etc.; abbreviated as DN, PN, GN, etc.). In [ORACC](http://oracc.org/) a word has a single `pos`; for proper nouns this is DN, PN, GN, etc. - so what is `type` in [ETCSL](https://etcsl.orinst.ox.ac.uk/) becomes `pos` in [ORACC](http://oracc.org/). [ORACC](http://oracc.org/) proper nouns usually do not have a guide word (only a number to enable disambiguation of namesakes). The [ETCSL](https://etcsl.orinst.ox.ac.uk/) guide words (`label`) for names come pretty close to [ORACC](http://oracc.org/) citation forms. Proper nouns are therefore formatted differently from other nouns.
# 
# :::{admonition} Proper Noun in ETCSL XML
# :class: tip, dropdown
# The temple name Eana:
# 
# ```xml
# <w form="e2-an-na-ju10" lemma="e2-an-na" pos="N" type="TN" label="E-ana">e2-an-na-ju10</w>
# ```
# 
# :::
# 
# * **Additional/Secondary**: finally, in pre-processing we added to some `w` nodes an attribute `status`, which is either 'additional' or 'secondary' ([2.2.4](2.2.4)). If the attribute exists, it is added to the `word` dictionary.
# 
# The dictionary `word` now has all the information it needs, but Citation Form, Guide Word, and Part of Speech are still mostly in [ETCSL](https://etcsl.orinst.ox.ac.uk/) format. The function `getword()` calls `tounicode()` to change (Sumerian) text from ASCII to Unicode representation (see section [2.2.5](2.2.5)). The argument of `tounicode()` is a string, the `form` or the `cf` (Citation Form) of the word that is being processed. The function returns the same string in Unicode representation.
# 
# The function `getword()`, finally sends the `word` dictionary to `etcsl_to_oracc()` (section [2.2.6](2.2.6)) for final formatting of these data elements and to add the the data to the list `alltexts`.

# In[7]:


def getword(node, meta_d):
    word = {key:meta_d[key] for key in meta_d} # copy all meta data from meta_d into the word dictionary
    
    if node.tag == 'gloss': # these are Akkadian glosses which are not lemmatized
        form = node.xpath('string(.)')
        form = form.replace('\n', ' ').strip() # occasionally an Akkadian gloss may consist of multiple lines
        word["form"] = tounicode(form)
        word["lang"] = node.xpath("string(@lang)")
        alltexts.append(word)
        return
    
    word["cf"] = node.xpath('string(@lemma)') # xpath('@lemma') returns a list. The string
    word["cf"] = word["cf"].replace('Xbr', '(X)')  # function turns it into a single string
    word["gw"] = node.xpath('string(@label)')

    if node.xpath('@pos'):
        word["pos"] = node.xpath('string(@pos)')
    else:         # if a word is not lemmatized (because it is broken or unknown) add pos = NA and gw = NA
        word["pos"] = 'NA'
        word["gw"] = 'NA'

    form = node.xpath('string(@form)')
    word["form"] = form.replace('Xbr', '(X)')
    
    if node.xpath('@emesal'):
        word["cf"] = node.xpath('string(@emesal)')
        word["lang"] = "sux-x-emesal"
    else:
        word["lang"] = "sux"

    exception = ["unclear", "Mountain-of-cedar-felling", "Six-headed Wild Ram", 
                     "The-enemy-cannot-escape", "Field constellation", 
                     "White Substance", "Chariot constellation", 
                 "Crushes-a-myriad", "Copper"]
    
    if node.xpath('@type') and word["pos"] == 'N': # special case: Proper Nouns
        if node.xpath('string(@type)') != 'ideophone':  # special case in the special case: skip ideophones
            word["pos"] = node.xpath('string(@type)')
            word["gw"] = '1'
            if node.xpath('string(@label)') not in exception:
                word["cf"] = node.xpath('string(@label)')
                
    if node.xpath('@status'):
        word['status'] = node.xpath('string(@status)')
    
    word["cf"] = tounicode(word["cf"])
    word["form"] = tounicode(word["form"])
    etcsl_to_oracc(word)

    return


# ## 2.2.8 Formatting Lines
# 
# The function `getline()` is called by `getsegment()`. It first updates the field `id_line` in `meta_d`, increasing it by 1. The data type of `id_line` is integer - it is used to keep lines and gaps in correct order.
# 
# A line may either be an actual line (in Sumerian and/or Akkadian) or a gap (a portion of text lost). Both receive a line reference (`id_line`).
# 
# If `getline()` receives an `l` node (a line) it will collect `w` nodes (words) and `gloss` nodes with the language attribute `akk`. The `Xpath` expression looks as follows: './/w|.//gloss\[@lang="akk"\]'. The "pipe" symbol (|) is a logical "or" - the condition looks for either a `w` tag or a `gloss` tag with a `lang` attribute that equals "akk". This will find Sumerian words and Akkadian glosses.
# 
# The function iterates over the list of words, sending each word to `getword()`.
# 
# A gap of one or more lines in the composite text, due to damage to the original cuneiform tablet, is encoded as follows:
# 
# ```xml
# <gap extent="8 lines missing"/>
# ```
# If getline() receives a gap node it copies all the meta data in the dictionary `meta_d` into the dictionary `line` and adds a field `extent` (the length of the gap). This data is found in the attribute `extent` of the gap node. This dictionary is then appended to the list `alltexts` and control is returned to the function `getsegment()`. A row in `alltexts`, therefore, usually represents a word, but may also represent a textual gap.
# 
# :::{admonition} Dealing with gaps: ORACC vs ETCSL
# :class: tip, dropdown
# 
# In [ORACC](http://oracc.org), gaps are described with the fields `extent` (a number, or 'n' for unknown),  and `scope` (line, column, obverse, etc.). [ORACC](http://oracc.org) uses a restricted vocabulary for these fields, but [ETCSL](https://etcsl.orinst.ox.ac.uk/) does not. The code currently does not try to make the [ETCSL](https://etcsl.orinst.ox.ac.uk/) encoding of gaps compatible with the [ORACC](http://oracc.org) encoding.
# 
# :::

# In[8]:


def getline(lnode, meta_d):
    meta_d["id_line"] += 1
    if lnode.tag == 'gap':
        line = {key:meta_d[key] for key in ["id_text", "text_name", "version", "id_line"]}
        line["extent"] = lnode.xpath("string(@extent)")
        alltexts.append(line)
        return
    
    for node in lnode.xpath('.//w|.//gloss[@lang="akk"]'):
                        # get <w> nodes and <gloss> nodes, but only Akkadian glosses
        getword(node, meta_d)
    return


# ## 2.2.9 Segments
# 
# Some compositions in [ETCSL](http://etcsl.orinst.ox.ac.uk) are divided into segments. That is the case, in particular, when a composition has gaps of unknown length. Segment B supposedly follows segment A, but how much text is missing between them cannot be reconstructed. This is the case, for instance, in [The Death of Gilgameš](https://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.8.1.3&display=Crit&charenc=gcirc#), which is rather fragmentarily preserved.
# 
# ```{figure} ../images/P264388.jpg
# :scale: 25%
# [UM 29-16-086](http://cdli.ucla.edu/P264388): fragments of the [Death of Gilgameš: Nippur version](https://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.8.1.3&display=Crit&charenc=gcirc#).
# ```
# 
# The function `getsegment()` is called by `getversion()` and receives the arguments `tree` (the `etree` object representing one version of the composition) and `meta_d` (the dictionary of meta data). The function `getsegment()` first checks to see whether a sub-division into segments is present. 
# 
# Segments are indicated in the XML with a node `div1` with the attribute `type="segment"`. Segment names (usually a capital letter) are found in an attribute of `div1` called `n`.  
# 
# :::{admonition} ETCSL XML: version, segment, gap
# :class: tip, dropdown
# 
# From the beginning of [The Death of Gilgameš](https://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.8.1.3&display=Crit&charenc=gcirc#). The text is known in multiple versions (from Nippur, from Meturan), and the versions themselves are subdivided into segments, with unknown numbers of lines missing in between.
# 
# ```xml
# <body>
# <head lang="eng">A version from Nibru</head>
# <div1 type="segment" n="A">
# <gap extent="unknown no. of lines missing"/>
# ```
# 
# :::
# 
# The function will collect all `l` (line) *and* `gap` nodes that belong to a single segment. The Xpath expression that is used for that is `.//l|.//gap` (where "|" is the "or" operator). In some regards gaps are treated as lines - they need to be placed after the last extant line and before the first line after the break. Iterating over this list, if the node is an `l` node the `meta_d` dictionary is updated with a (human-legible) line number (or segment + line number, if the text is divided into segments). This line number, which is a string, is stored in the key "label" in order to achieve consistency with [ORACC](http://oracc.org/) naming conventions. The function then calls `getline()`. The first argument of `getline()` is the part of the XML tree that belongs to a single line or gap; the second argument is `meta_d`.
# 
# :::{admonition} Terminology: ORACC label vs ETCSL label
# :class: tip, dropdown
# 
# In ETCSL 'label' is used for the general translation of a lemma (Guide Word in ORACC). In ORACC 'label' is reserved for human-legible references to lines, columns, obverse, reverse, etc. such as o ii 15 (obverse column 2 line 15).
# 
# :::

# In[9]:


def getsegment(tree, meta_d):
    segments = tree.xpath('.//div1[@type="segment"]')
    
    if segments: # if the text is not divided into segments - skip to else:
        for snode in segments:
            segment = snode.xpath('string(@n)')
            for lnode in snode.xpath('.//l|.//gap'):
                if lnode.tag == 'l':
                    line = segment + lnode.xpath('string(@n)')
                    meta_d["label"] = line   # "label" is the human-legible line number
                getline(lnode, meta_d)

    else:
        for lnode in tree.xpath('.//l|.//gap'):
            if lnode.tag == 'l':
                line_no = lnode.xpath('string(@n)')
                meta_d["label"] = line_no
            getline(lnode, meta_d)
    return


# ## 2.2.10 Versions
# 
# In some cases an [ETCSL](http://etcsl.orinst.ox.ac.uk) file contains different versions of the same composition. The versions may be distinguished as 'Version A' vs. 'Version B' or may indicate the provenance of the version ('A version from Urim' vs. 'A version from Nibru'). In the edition of the proverbs the same mechanism is used to identify tablets (often lentils) that contain just one proverb, or a few, and are collected in the files "Proverbs from Urim," "Proverbs from Nibru," etc. ([ETCSL](http://etcsl.orinst.ox.ac.uk) c.6.2.1 - c.6.2.5).
# 
# :::{margin}
# This lentil is edited in the collection [Proverbs from Urim](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.6.2.3&display=Crit&charenc=gcirc) "If bread is left over, the mongoose eats it. If I have bread left over, a stranger consumes it." (translation [ETCSL](http://etcsl.orinst.ox.ac.uk)).
# :::
# 
# ```{figure} ../images/P346317.jpg
# :scale: 25%
# [UET 6/2 239](http://oracc.org/epsd2/P346317): lentil from Ur with a [proverb](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.6.2.3&display=Crit&charenc=gcirc).
# ```
# 
# The function `getversion()` is called by the function `parsetext()` and receives two arguments: `tree` (the `etree` object) and `meta_d` (the dictionary of meta data). In the XML tree versions are marked by a node `body` with a child `head`. The node `head` contains the name of the version. Iterating through the versions, the function updates the key "version" in `meta_d` with the name of that version and then calls the `getsegment()` function. The first argument is the portion of the tree that represents the version that is being parsed, the second argument is `meta_d`. If a composition is not divided into versions the entire tree is passed to `getsegment()` and the version name in `meta_d` is the empty string.
# 
# In some cases version names are very long and somewhat unwieldy. For instance, [The Cursing of Agade](https://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.2.1.5&display=Crit&charenc=gcirc#) has a version that is called "Fragments of an earlier version from Nibru, dating to the Ur III period." This version name is abbreviated to "Ur III". The equivalency list `versions` (in `equivalencies/equivalencies.json`; see [2.2.2.2](2.2.2.2)) is used to adjust version names.

# In[10]:


def getversion(tree, meta_d):
    versions = tree.xpath('.//body[child::head]')

    if versions: # if the text is not divided into versions - skip 'getversion()':
        for vnode in versions:
            version = vnode.xpath('string(head)')
            version = eq["versions"].get(version, version)
            meta_d["version"] = version
            getsegment(vnode, meta_d)

    else:
        meta_d["version"] = ''
        getsegment(tree, meta_d)
    return


# (2.2.11)=
# ## 2.2.11 Parse a Text
# 
# The main process iterates through the list of XML files (one for each composition in [ETCSL](https://etcsl.orinst.ox.ac.uk/)) and calls for each of them the function `parsetext()`. After opening the XML file `parsetext()` first calls the function `ampersands()` in order to replace HTML entities by their unicode counterparts ([2.2.3](2.2.3)). The module `etree` from the `lxml` library is used to read the XML tree. Since `etree` does not read the XML directly from file, but rather reads the output of the `ampersands()` function, we need the function `fromstring()`:
# 
# After creating the tree, the function `mark_extra()` ([2.2.4](2.2.4)) is called in order to explicitly mark "additional" and "secondary" words.  The composition name is found in the node `title`. This name is slightly adjusted in two ways. First, all [ETCSL](https://etcsl.orinst.ox.ac.uk/) text names include the phrase " -- a composite transliteration". This is useful for online presentation, but not for computational text analysis. Second, some titles include commas, which may create problems when data are saved in `cvs` format. These two elements are removed from the title.
# 
# The dictionary `meta_d`, which was created as an empty dictionary in the main process, is now filled with meta data on the composition level: the text ID (the [ETCSL](https://etcsl.orinst.ox.ac.uk/) text number, for instance c.1.4.1 for Inana's Descent) and the text name. Finally, the line reference count is set to 0. This line reference is updated every time the function `getline()` is called.
# 
# The XML tree is now forwarded to the function `getversion()` together with the dictionary `meta_d`.

# In[11]:


def parsetext(file, meta_d):
    with open(f'etcsl/transliterations/{file}') as f:
        xmltext = f.read()
    xmltext = ampersands(xmltext)          #replace HTML entities by Unicode equivalents
    
    tree = etree.fromstring(xmltext)
    
    tree = mark_extra(tree, "additional") # mark additional words with attribute status = 'additional'
    tree = mark_extra(tree, "secondary")  # mark secondary words with attribute status = 'secondary'
    name = tree.xpath('string(//title)')
    name = name.replace(' -- a composite transliteration', '')
    name = name.replace(',', '')
    meta_d["id_text"] =  file[:-4]
    meta_d["text_name"] = name
    meta_d["id_line"] = 0
    getversion(tree, meta_d)

    return


# (2.2.12)=
# ## 2.2.12 Main Process
# 
# The list `alltexts` is created as an empty list. It will be filled with dictionaries, each dictionary representing one word form.
# 
# The variable `textlist` is a list of all the XML files with [ETCSL](http://etcsl.orinst.ox.ac.uk) compositions in the directory `etcsl/transliterations`. Iterating through this list, each file  is sent as an argument to the function `parsetext()`. 
# 
# The dictionary `meta_d` is created as an empty dictionary. On each level of analysis the dictionary is updated with meta-data, such as text ID, version name, line number, etc.
# 
# The main process also defines a number of variables (compiled regular expressions and translation tables) that are used later on in the process for adjusting transliteration conventions in the function `tounicode()` (see [2.2.5](2.2.5))
# 
# After the loop has gone through all the file names (this may take a few minutes) the list `alltexts` is transformed into a `pandas` DataFrame. The progress bar should indicate that 394 files have been processed and the resulting dataframe should have 12 columns and 170,856 rows, each row representing a single word or a gap. All missing values (`NaN`) are replaced by empty strings. 

# In[12]:


textlist = os.listdir('etcsl/transliterations')
textlist = [file for file in textlist if file[-4:] == '.xml']
textlist.sort()

amp = re.compile(r'&[^;]+;') #regex for HTML entities, used in ampersands()

asccj, unicj = 'cjCJ', 'šŋŠŊ'
transcj = str.maketrans(asccj, unicj) # translation table for c > š and j > ŋ

ind = re.compile(r'[a-zŋḫṣšṭA-ZŊḪṢŠṬ][0-9x]{1,2}') #regex for sign index nos preceded by a letter
ascind, uniind = '0123456789x', '₀₁₂₃₄₅₆₇₈₉ₓ'
transind = str.maketrans(ascind, uniind) # translation table for index numbers
# regex ind and the translation tables transind and transcj are used in tounicode()

alltexts = []
files = tqdm(textlist)
for file in files:
    files.set_description(f'ETCSL {file[2:-4]}')
    meta_d = {}
    parsetext(file, meta_d)

df = pd.DataFrame(alltexts).fillna('')


# In[13]:


df


# ## 2.2.13 Save as CSV
# 
# The DataFrame that is the result of the notebook is saved as a `csv` file named `alltexts.csv`, where each word form occupies a single row. In many cases, however, we may want to represent the data in a line-by-line or composition-by-composition format and/or filter out certain words (for instance: use only lemmatized words, remove Akkadian words, remove "additional" and/or "secondary" text - etc.). Such transformations can be done most easily in a `pandas` dataframe. 
# 
# :::{margin}
# 
# For manipulating a dataframe in `pandas`, see Chapter 2.1: Data Acquisition ORACC (for instance the sections [2.1.2.6](2.1.2.6) and [2.1.3.8](2.1.3.8)).
# 
# :::

# In[14]:


with open('output/alltexts.csv', 'w', encoding="utf-8") as w:
    df.to_csv(w, index=False)


# In[ ]:




