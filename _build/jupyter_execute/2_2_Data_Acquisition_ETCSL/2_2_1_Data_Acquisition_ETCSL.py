#!/usr/bin/env python
# coding: utf-8

# # 2.2 Parsing ETCSL
# ## 2.2.1. Introduction
# 
# The Electronic Text Corpus of Sumerian Literature ([ETCSL](http://etcsl.orinst.ox.ac.uk); 1998-2006) provides editions and translations of 394 Sumerian literary compositions. Goal of this Notebook is to format the [ETCSL] data in such a way that the (lemmatized) texts are made available for computational text analysis. The [ETCSL](http://etcsl.orinst.ox.ac.uk) lemmatizations are made compatible with [ORACC] standards (see [ePSD2](http://oracc.org/epsd2/sux)), so that [ETCSL](http://etcsl.orinst.ox.ac.uk) and [ORACC](http://oracc.org) data can be mixed and matched for text analysis purposes.
# 
# The output of this notebook is a `csv` file of lemmatized words (one record is one word) with information about composition, line number, etc.
# 
# The original [ETCSL](http://etcsl.orinst.ox.ac.uk) files in `TEI XML` may be downloaded from the [Oxford Text Archive](http://ota.ox.ac.uk/desc/2518) under a Creative Commons Attribution non-Commercial Share-Alike ([BY-NC-SA 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/)) license.
# 
# The editors and copyright holders of [ETCSL](http://etcsl.orinst.ox.ac.uk) are: Jeremy Black, Graham Cunningham, Jarle Ebeling, Esther Flückiger-Hawker, Eleanor Robson, Jon Taylor, and Gábor Zólyomi.
# 
# The [manual](http://etcsl.orinst.ox.ac.uk/edition2/etcslmanual.php) of the [ETCSL](http://etcsl.orinst.ox.ac.uk) project explains in full detail the editorial principles and technical details. 

# ### 2.2.1.1 XML, Xpath, and lxml
# The [ETCSL](http://etcsl.orinst.ox.ac.uk) files as distributed by the [Oxford Text Archive](http://ota.ox.ac.uk/desc/2518) are encoded in the `TEI` (Text Encoding Initiative) dialect of `XML` (Extensible Markup Language). 
# 
# The `XML`tree is parsed in `Xpath`, a language that defines ways in which one can move through an `XML` file and identify particular nodes, sub-nodes, attributes, and elements. The module `etree`of the library [`lxml`](https://lxml.de/) provides a full implementation of `Xpath 1.0` and is largely compatible with more widely-used libraries such as `ElementTree` and its counterpart `cElementTree`.

# ### 2.2.1.2 Input and Output
# 
# This scraper expects the following files and directories:
# 
# 1. Directory `etcsl/transliterations/`  
#    This directory should contain the [ETCSL](http://etcsl.orinst.ox.ac.uk) `TEI XML` transliteration files.  
# 2. Directory `Equivalencies`  
#    `equivalencies.json`: a set of equivalence dictionaries used at various places in the parser.  
# 
# The output is saved in the `output` directory as a single `.csv` file.

# ## 2.2.2 Setting Up
# ### 2.2.2.1 Load Libraries
# Before running this cell you may need to install the packages `lxml` (for parsing `XML`) and  `tqdm` (for displaying a progress bar). For proper installation of libraries for a Jupyter Notebook see [install_packages.ipynb](../1_Preliminaries/install_packages.ipynb).

# In[ ]:


import re
from lxml import etree
import os
import json
import pandas as pd
from tqdm.auto import tqdm
os.makedirs('output', exist_ok = True)


# ### 2.2.2.2 Load Equivalencies 
# The file `equivalencies.json` contains a number of dictionaries that will be used to search and replace at various places in this notebook. The dictionaries are:
# - `suxwords`: Sumerian words (Citation Form, GuideWord, and Part of Speech) in [ETCSL](http://etcsl.orinst.ox.ac.uk) format and their [ORACC](http://oracc.org) counterparts.
# - `emesalwords`: idem for Emesal words
# - `propernouns`: idem for proper nouns
# - `ampersands`: HTML entities (such as `&aacute;`) and their Unicode counterparts (`á`; see section 3).
# - `versions`: [ETCSL](http://etcsl.orinst.ox.ac.uk) version names and (abbreviated) equivalents
# 
# The `equivalencies.json` file is loaded with the `json` library. The dictionaries `suxwords`, `emesalwords` and `propernouns` (which, together, contain the entire [ETCSL](http://etcsl.orinst.ox.ac.uk) vocabulary) are concatenated into a single dictionary.

# In[ ]:


with open("equivalencies/equivalencies.json", encoding="utf-8") as f:
    eq = json.load(f)
equiv = eq["suxwords"]
equiv.update(eq["emesalwords"])
equiv.update(eq["propernouns"])


# ## 2.2.3 Preprocessing: HTML-entities
# The [ETCSL](http://etcsl.orinst.ox.ac.uk) `TEI XML` files are written in ASCII and represent special characters (such as š or ī) by a sequence of characters that begins with & and ends with ; (e.g. `&c;` represents `š`). The `lxml` library cannot deal with these entities and thus we have to replace them with the actual (Unicode) character that they represent before feeding the data to `etree` module.
# 
# The function `ampersands()` uses the dictionary `ampersands` for a search-replace action. The dictionary `ampersands` is included in the file `equivalencies.json`, which was loaded above (section 2).
# 
# The function `ampersands()` is called in `parsetext()` (see section 11) before the `etree` is built. The regular expression `amp` captures all so-called HTML entities (beginning with a '&' and ending with a ';'). The regex is compiled in the main process.

# In[ ]:


def ampersands(string):    
    string = re.sub(amp, lambda m: 
               eq["ampersands"].get(m.group(0), m.group(0)), string)
    return string


# ## 2.2.4 Marking 'Secondary Text' and/or 'Additional Text'
# 
# The [ETCSL](http://etcsl.orinst.ox.ac.uk) web pages include variants, indicated as '(1 ms. has instead: )', with the variant text enclosed in curly brackets. Two types of variants are distinguished: 'additional text' and 'secondary text'. 'Additional text' refers to a line that appears in a minority of sources (often in only one) in addition to the majority text. 'Secondary text' refers to variant words or variant lines that are found in a minority of sources, replacing the text of the majority sources. The function `mark_extra()` marks each word of 'secondary text' or 'additional text' by adding the attribute `status` with the value "additional" or "secondary". 
# 
# The function `mark_extra()` is called twice by the function `parsetext()` (see below, section 11), once for "additional" and once for "secondary" text, indicated by the `which` argument. 

# In[ ]:


def mark_extra(tree, which):
    extra = tree.xpath(f'//w[preceding::addSpan[@type="{which}"]/@to = following::anchor/@id]')
    for word in extra:
        word.attrib["status"] = which
    return tree


# ## 2.2.5 Transliteration Conventions
# 
# Transliteration of Sumerian text in [ETCSL](http://etcsl.orinst.ox.ac.uk) `TEI XML` files uses **c** for **š**, **j** for **ŋ** and regular numbers for index numbers. The function `tounicode()` replaces each of those. For example **cag4** is replaced by **šag₄**. This function is called in the function `getword()` to format `Citation Forms` and `Forms` (transliteration). The function `tounicode()` uses the translation tables `transind` (for index numbers) and `transcj` (for c and j), defined in the main process. The `translate()` function replaces individual characters from a string, according to the table.
# 
# In order to replace regular numbers with index numbers the function uses a [regular expression](https://www.regular-expressions.info/) to select only those single or double digit numbers that are preceded by a letter (leaving alone the "7" in 7-ta-am3). The regex `ind` is compiled in the main process.

# In[ ]:


def tounicode(string):
    string = re.sub(ind, lambda m: m.group().translate(transind), string)
    string = string.translate(transcj)
    return string


# ## 2.2.6 Replace [ETCSL](http://etcsl.orinst.ox.ac.uk) by [ORACC](http://oracc.org) Lemmatization
# For every word, once `cf` (Citation Form), `gw` (Guide Word), and `pos` (Part of Speech) have been pulled out of the [ETCSL](http://etcsl.orinst.ox.ac.uk) `XML` file, they are combined into a lemma and run through the etcsl/oracc equivalence lists to match it with the [ORACC](http://oracc.org)/[ePSD2](http://oracc.org/epsd2) standards. The equivalence lists are stored in the file `equivalencies.json`, which was loaded above (section 2).
# 
# The function `etcsl_to_oracc()` is called by the function `getword()`.

# In[ ]:


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
# A word in the [ETCSL](http://etcsl.orinst.ox.ac.uk) files is represented by a `<w>` node in the `XML` tree with a number of attributes that identify the `form` (transliteration), `citation form`, `guide word`, `part of speech`, etc. The function `getword()` formats the word as closely as possible to the [ORACC](http://oracc.org) conventions. Three different types of words are treated in three different ways: Proper Nouns, Sumerian words and Emesal words.
# 
# In [ETCSL](http://etcsl.orinst.ox.ac.uk) **proper nouns** are nouns (`pos` = "N"), which are qualified by an additional attribute `type` (Divine Name, Personal Name, Geographical Name, etc.; abbreviated as DN, PN, GN, etc.). In [ORACC](http://oracc.org) a word has a single `pos`; for proper nouns this is DN, PN, GN, etc. - so what is `type` in [ETCSL](http://etcsl.orinst.ox.ac.uk) becomes `pos` in [ORACC](http://oracc.org). [ORACC](http://oracc.org) proper nouns usually do not have a guide word (only a number to enable disambiguation of namesakes). The [ETCSL](http://etcsl.orinst.ox.ac.uk) guide words (`label`) for names come pretty close to [ORACC](http://oracc.org) citation forms. Proper nouns are therefore formatted differently from other nouns.
# 
# **Sumerian words** are essentially treated in the same way in [ETCSL](http://etcsl.orinst.ox.ac.uk) and [ORACC](http://oracc.org), but the `citation forms` and `guide words` are often different. Transformation of citation forms and guide words to [ORACC](http://oracc.org)/[epsd2](http://oracc.org/epsd2/sux) standards takes place in the function `etcsl_to_oracc()` (see above, section 6).
# 
# **Emesal words** in [ETCSL](http://etcsl.orinst.ox.ac.uk) use their Sumerian equivalents as `citation form` (attribute `lemma`), adding a separate attribute (`emesal`) for the Emesal form proper. This Emesal form is the one that is used as `citation form` in the output.
# 
# The function `getword()` uses the dictionary `meta_d` which has collected all the meta-data (text ID, composition name, version, line number, etc.) of this particular word It produces the dictionary `word` which is sent to the function `etcsl_to_oracc()`

# In[ ]:


def getword(node):
    word = {key:meta_d[key] for key in meta_d} # copy all meta data from metad_d into the word dictionary
    if node.tag == 'gloss': # these are Akkadian glosses which are not lemmatized
        form = node.xpath('string(.)')
        form = form.replace('\n', ' ').strip() # occasionally an Akkadian gloss may consist of multiple lines
        word["form"] = tounicode(form) # check - is this needed?
        word["lang"] = node.xpath("string(@lang)")
        alltexts.append(word)
        return
    
    word["cf"] = node.xpath('string(@lemma)') # xpath('@lemma') returns a list. The string
    word["cf"] = word["cf"].replace('Xbr', '(X)')  # function turns it into a single string
    word["gw"] = node.xpath('string(@label)')

    if len(node.xpath('@pos')) > 0:
        word["pos"] = node.xpath('string(@pos)')
    else:         # if a word is not lemmatized (because it is broken or unknown) add pos = NA and gw = NA
        word["pos"] = 'NA'
        word["gw"] = 'NA'

    form = node.xpath('string(@form)')
    word["form"] = form.replace('Xbr', '(X)')
    
    if len(node.xpath('@emesal')) > 0:
        word["cf"] = node.xpath('string(@emesal)')
        word["lang"] = "sux-x-emesal"
    else:
        word["lang"] = "sux"

    exception = ["unclear", "Mountain-of-cedar-felling", "Six-headed Wild Ram", 
                     "The-enemy-cannot-escape", "Field constellation", 
                     "White Substance", "Chariot constellation", 
                 "Crushes-a-myriad", "Copper"]
    
    if len(node.xpath('@type')) > 0 and word["pos"] == 'N': # special case: Proper Nouns
        if node.xpath('string(@type)') != 'ideophone':  # special case in the special case: skip ideophones
            word["pos"] = node.xpath('string(@type)')
            word["gw"] = '1'
            if node.xpath('string(@label)') not in exception:
                word["cf"] = node.xpath('string(@label)')
    if len(node.xpath('@status')) > 0:
        word['status'] = node.xpath('string(@status)')
    
    word["cf"] = tounicode(word["cf"])
    word["form"] = tounicode(word["form"])
    etcsl_to_oracc(word)

    return


# ## 2.2.8 Formatting Lines
# 
# A line may either be an actual line (in Sumerian and/or Akkadian) or a gap (a portion of text lost). Both receive a line reference. A line reference is an integer that is used to keep lines (and gaps) in their proper order.
# 
# The function `getline()` is called by `getsection()`. If the argument of `getline()` is an actual line (not a gap) it calls `getword()` for every individual word in that line.

# In[ ]:


def getline(lnode):
    meta_d["id_line"] += 1
    if lnode.tag == 'gap':
        line = {key:meta_d[key] for key in ["id_text", "text_name", "version", "id_line"]}
        line["extent"] = lnode.xpath("string(@extent)")
        alltexts.append(line)
        return
    
    for node in lnode.xpath('.//w|.//gloss[@lang="akk"]'):
                        # get <w> nodes and <gloss> nodes, but only Akkadian glosses
        getword(node)
    return


# ## 2.2.9 Sections
# 
# Some [ETCSL](http://etcsl.orinst.ox.ac.uk) compositions are divided into **sections**. That is the case, in particular, when a composition has gaps of unknown length. 
# 
# The function `getsection()` is called by `getversion()` and receives one argument: `tree` (the `etree` object representing one version of the composition). The function updates `meta_d`, a dictionary of meta data. The function `getsection()` checks to see whether a sub-division into sections is present. If so, it iterates over these sections. Each section (or, if there are no sections, the composition/version as a whole) consists of series of lines and/or gaps. The function `getline()` is called to process each line or gap. 

# In[ ]:


def getsection(tree):
    sections = tree.xpath('.//div1')
    
    if len(sections) > 0: # if the text is not divided into sections - skip to else:
        for snode in sections:
            section = snode.xpath('string(@n)')
            for lnode in snode.xpath('.//l|.//gap'):
                if lnode.tag == 'l':
                    line = section + lnode.xpath('string(@n)')
                    meta_d["label"] = line   # "label" is the human-legible 
                getline(lnode)

    else:
        for lnode in tree.xpath('.//l|.//gap'):
            if lnode.tag == 'l':
                line_no = lnode.xpath('string(@n)')
                meta_d["label"] = line_no
            getline(lnode)
    return


# ## 2.2.10 Versions
# 
# In some cases an [ETCSL](http://etcsl.orinst.ox.ac.uk) file contains different versions of the same composition. The versions may be distinguished as 'Version A' vs. 'Version B' or may indicate the provenance of the version ('A version from Urim' vs. 'A version from Nibru'). In the edition of the proverbs the same mechanism is used to distinguish between numerous tablets (often lentils) that contain just one proverb, or a few, and are collected in the files "Proverbs from Susa," "Proverbs from Nibru," etc. ([ETCSL](http://etcsl.orinst.ox.ac.uk) c.6.2.1 - c.6.2.5).
# 
# The function `getversion()` is called by the function `parsetext()` and receives one argument: `tree` (the `etree` object). The function updates`meta_d`, a dictionary of meta-data. The function checks to see if versions are available in the file that is being parsed. If so, the function iterates over these versions while adding the version name to the `meta_d` dictionary. If there are no versions, the version name is left empty. The parsing process is continued by calling `getsection()` to see if the composition/version is further divided into sections.

# In[ ]:


def getversion(tree):
    versions = tree.xpath('.//body[child::head]')

    if len(versions) > 0: # if the text is not divided into versions - skip 'getversion()':
        for vnode in versions:
            version = vnode.xpath('string(head)')
            version = eq["versions"][version]
            meta_d["version"] = version
            getsection(vnode)

    else:
        meta_d["version"] = ''
        getsection(tree)
    return


# ## 2.2.11 Parse a Text
# 
# The function `parsetext()` takes one xml file (a composition in [ETCSL](http://etcsl.orinst.ox.ac.uk)) and parses it, calling a variety of functions defined above. 
# 
# The parsing is done by the `etree` package in the `lxml` library. Before the file can be parsed properly the so-called HTML entities need to be replaced by their Unicode equivalents. This is done by calling the `ampersands()` function (see above, section 3: Preprocessing).

# In[ ]:


def parsetext(file):
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
    getversion(tree)

    return


# ## 2.2.12 Main Process
# 
# The list `alltexts` is created as an empty list. It will be filled with dictionaries, each dictionary representing one word form.
# 
# The variable `textlist` is a list of all the `XML` files with [ETCSL](http://etcsl.orinst.ox.ac.uk) compositions in the directory `etcsl/transliterations`. Each file  is sent as an argument to the function `parsetext()`. 
# 
# The dictionary `meta_d` is created as an empty dictionary. On each level of analysis the dictionary is updated with meta-data, such as text ID, version name, line number, etc.
# 
# The list is transformed into a `pandas` DataFrame. All missing values (`NaN`) are replaced by empty strings. 

# In[ ]:


textlist = os.listdir('etcsl/transliterations')
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
    parsetext(file)

df = pd.DataFrame(alltexts).fillna('')


# In[ ]:


df


# ## 2.2.13 Save as CSV
# The DataFrame is saved as a `CSV` file named `alltexts.csv` in the directory `output`.

# In[ ]:


with open('output/alltexts.csv', 'w', encoding="utf-8") as w:
    df.to_csv(w, index=False)


# In[ ]:




