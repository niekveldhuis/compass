#!/usr/bin/env python
# coding: utf-8

# # 2.4 Data Acquision BDTNS
# 
# Goal of this notebook is to transform [BDTNS](http://bdtns.filol.csic.es/) data into a structured format that clearly distinguishes between text and non-text (such as line numbers) and that, for the text part, follows as much as possible the standards of the Oracc Global Sign List ([OGSL](http://oracc.org/ogsl)). We will use this structured data to build a search engine that is independent of sign readings (that is, searching for **sukkal**, **sugal₇** or **luh** will all yield the same results). The search engine will serve as an example of the potential power of mashing two independent projects.
# 
# ```{margin}
# A similar search engine was developed by Marc Endesfelder for his [Writing Sumerian](https://corpus.writing-sumerian.assyriologie.uni-muenchen.de/) project.
# ```
# 
# ## 2.4.1 BDTNS
# 
# ```{margin}
# For the numbers, see the BDTNS [about](http://bdtns.filol.csic.es/index.php?p=about) page. The [map](http://bdtns.filol.csic.es/mapa.php?modo=colecciones) gives an impression of the distribution of this corpus in libraries and collections in Europe, the Middle East, North America, China, Japan, and Australia.
# ```
# 
# The Database of Neo-Sumerian Texts ([BDTNS](http://bdtns.filol.csic.es)) was created by Manuel Molina (Consejo Superior de Investigaciones Científicas). The site provides a detailed catalog of the administrative, legal, and epistolary documents from the so-called Ur III period (21st century BCE). Molina estimates that museums and private collections all over the world may hold at least 120,000 such documents, not including the holdings of the Iraq Museum, Baghdad. Currently, almost 65% of those documents are available through [BDTNS](http://bdtns.filol.csic.es) in transliteration, and/or in photograph and line drawing. 
# 
# ```{figure} ../images/logo_BDTNS.gif
# :figclass: margin
# [BDTNS](http://bdtns.filol.csic.es) logo.
# ``` 
# 
# There is a considerable overlap in the data sets offered by [CDLI](http://cdli.ucla.edu) and [BDTNS](http://bdtns.filol.csic.es). All photographs and line drawings of Ur III tablets that are available in [CDLI](http://cdli.ucla.edu) have been imported into [BDTNS](http://bdtns.filol.csic.es); in addition, [BDTNS](http://bdtns.filol.csic.es) offers its own collection of thousands of photographs, in particular of tablets now in the British Museum, London. The initial core of the [BDTNS](http://bdtns.filol.csic.es) transliterations was provided by Remco de Maaijer and Bram Jagersma (Leiden University), who prepared tens of thousands of Ur III texts and distributed those data freely. This same set of transliterations was also one of the initial data sets of [CDLI](http://cdli.ucla.edu). Close cooperation between the two projects has led to further exchange of data. Not infrequently, therefore, misreadings or simple typos appear in the same way in both projects.
# 
# ```{margin}
# Paola Paoletti, *Der König und sein Kreis: das staatliche Schatzarchiv der III. Dynastie von Ur*, Biblioteca del próximo oriente antiguo 10. Madrid: 2012.
# ```
# 
# Still, [BDTNS](http://bdtns.filol.csic.es) is not simply a duplicate of the Ur III data in [CDLI](http://cdli.ucla.edu). Most Ur III scholars today prefer [BDTNS](http://bdtns.filol.csic.es) over [CDLI](http://cdli.ucla.edu) because the smaller focus of the Spanish project implies that there is more attention to detail and that more effort is made to update the record. One example is the book *Der König und sein Kreis* (2012) in which Paola Paoletti studied in detail several hundreds of documents from the so-called treasure archive at Puzriš-Dagan (see also Chapter 4). This archive reports on the manufacturing of luxury goods made of precious metals and leather and includes many rare words. Since the archive (like almost all Ur III archives) is scattered over museums all over the world, most of these texts were published as single documents or in small groups. Studying the entire group frequently allowed Paoletti to arrive at a more satisfying reading and understanding than the original editor's. The [BDTNS](http://bdtns.filol.csic.es) editions of these texts reflect Paoletti's improvements, but the [CDLI](http://cdli.ucla.edu) editions not (yet).
# 
# The [BDTNS](http://bdtns.filol.csic.es) data can be downloaded by hand through the [Search](http://bdtns.filol.csic.es/index.php?p=formulario_urIII) option in the Catalogue & Transliterations drop-down menu. One can search by a variety of criteria (including word and grapheme strings) and then download the search results by clicking on the Export button. The export page provides options for the types of information to include (various types of meta-data and/or transliterations). By searching for a blank string one may export the entire data set. The export yields two files: one for the meta-data and one for the  transliterations, both in raw text (`.txt`) format.
# 
# ```{admonition} BDTNS Download function Broken
# :class: dropdown, warning
# Currently, the export option in [BDTNS](http://bdtns.filol.csic.es) does not work. The code below will grap a version of the data set, made available by Manuel Molina, from the Compass project site at Github. There is no guarantee that this is the most recent version.
# ```

# ## 2.4.2 BDTNS Data
# ### 2.4.2.0 Import Packages and create directory
# * requests: for communicating with a server over the internet
# * pandas: data analysis and manipulation; dataframes
# * re: Regular Expressions
# * tqdm: progress bar
# * os: basic Operating System tasks (such as creating a directory)
# * sys: change system parameters
# * utils: compass-specific utilities (download files from ORACC, etc.)
# * pickle: save data for future use
# * zipfile: read data from a zipped file

# In[1]:


import requests
import pandas as pd
import re
from tqdm.auto import tqdm
tqdm.pandas() # initiate pandas support in tqdm, allowing progress_apply() and progress_map()
import os
import sys
import pickle
import zipfile
from io import StringIO
os.makedirs('output', exist_ok = True)


# ### 2.4.2.1 Get BDTNS Data Files
# For the time being, the data are downloaded in Zipped format from the [Compass](https://github.com/niekveldhuis/compass) repository.

# In[2]:


url = "https://raw.github.com/niekveldhuis/compass/master/BDTNS_data/BDTNS.zip"
file = "../BDTNS_data/BDTNS.zip"
CHUNK = 1024
r = requests.get(url)
with requests.get(url, stream=True) as request:
    if request.status_code == 200:   # meaning that the file exists
        total_size = int(request.headers.get('content-length', 0))
        tqdm.write(f'Saving {url} as {file}')
        t=tqdm(total=total_size, unit='B', unit_scale=True, desc = "BDTNS")
        with open(file, 'wb') as f:
            for c in request.iter_content(chunk_size=CHUNK):
                t.update(len(c))
                f.write(c)
    else:
        tqdm.write(f"WARNING: {url} does not exist.")


# ## 2.4.3 BDTNS Catalog
# ### 2.4.3.1 Extract BDTNS files
# Extract the files from the ZIP and transform the catalog file into a Pandas data frame.
# 
# ```{tip}
# Inspect the catalog to see if the column names correspond to the actual contents. Different versions of the [BDTNS](http://bdtns.filol.csic.es) catalog may have different selections of fields and/or may present those fields in a different order. Adjust the variable `cols`, if necessary.
# ```

# In[3]:


file_name = "../BDTNS_data/BDTNS.zip"
with zipfile.ZipFile(file_name, 'r') as zip_file:
    zip_file.extractall("../BDTNS_data")
cat = "../BDTNS_data/QUERY_catalogue.txt"
cols = ['id_text', 'cdli', 'publication', 'mus_no',
        'date', 'provenance']
cat_df = pd.read_csv(cat, sep = '\t', names= cols, dtype='string', header=None, encoding='utf-8').fillna('')
cat_df


# ### 2.4.3.2 Pickle Catalog DataFrame
# The catalog DataFrame is not used further in this notebook, but will be used in the search engine, to be built in 2.4.2. For now it is saved as a file with the `pickle` package.

# In[4]:


pickled = "output/bdtns_cat.p"
cat_df.to_pickle(pickled)


# ## 2.4.4 BDTNS Transliterations
# ### 2.4.4.1 Read the Transliteration File as a List
# The transliteration file is already extracted from the file BDTNS.zip and is located in the directory `../BDTNS_data/`.
# 
# :::{admonition} utf-8, utf-8-sig, vertical tabs
# :class: dropdown, tip
# 
# If the first line of the output begins with "\ufeff" (the Byte Order Mark, or BOM), check that the encoding is set to "utf-8-sig" (not "utf-8"). In some of its output files [BDTNS](http://bdtns.filol.csic.es/) uses so-called "vertical tabs" (represented by `^K`, `\v`, or `\x0b`, depending on your editor).  These "vertical TABS" are inserted between lines that belong to the same document; the regular newline character is used to separate one document from the next. If that is the case adjust the line
# 
# ```python
# bdtns = f.readlines()
# ```
# to
# ```python
# bdtns = f.read().splitlines()
# ```
# 
# The `.splitlines()` method takes both the vertical tab and the regular newline character as a line separator. The `.read()` method puts the entire file in memory and is therefore less efficient - if possible, use the `.readlines()` method.
# 
# :::
# 
# Empty lines and lines filled with spaces or tabs only will cause trouble downstream and are removed. Also removed are lines that consist of sequences of '=' signs (those are used to demarcate one text from the next.

# In[5]:


file = '../BDTNS_data/QUERY_transliterations.txt'
with open(file, mode = 'r', encoding = 'utf-8-sig') as f:
    bdtns = f.readlines()
bdtns = [line for line in bdtns if line.replace('=', '').strip()] # remove empty lines and lines consisting of '=' signs only
bdtns[:25] # inspect the results


# ### 2.4.4.2 Split Data into Fields
# Each data type (text ID, line number, comments, etc.) is made into a separate column of a data frame. Each row of that data frame represents one line in an Ur III document.
# 
# First, the code looks for lines that begin with 6 digits, for instance:
# 
# > 	038576	AAICAB 1/1, Ashm. 1911-146 = CDLI P142659
# 
# Those numbers are the [BDTNS](http://bdtns.filol.csic.es/) text ID numbers and mark the beginning of a new document. The numbers correspond to the `id_text` numbers in the catalog above. If such a line is found, the number is stored in the variable `bdtns_no`. Other data available in such lines (such as publication and [CDLI](http://cdli.ucla.edu) P-number) are omitted, because they are better derived from the catalog file.
# 
# Other lines are transliteration lines that may have one or more of the following:
# 
# - line number in the format 'o.ii 5' (obverse column ii line 5)
# - transliteration
# - editorial remarks
# 
# For instance:
# 
# > o. 4     --- Lu2-Ib-gal dumu Ur-⌈x⌉-[...] # (1 nu-dib erased)
# 
# Line numbers are separated from transliteration by five spaces. Editorial remarks (which may indicate the presence of a seal impression, an erased line, or provide an alternative reading) are introduced by the hash mark and are placed at the end of the line. A specific type of editorial remark is the sign name, which explains an x-value (see below section [2.4.4.4.1](2.4.4.4.1)), a rare sign form, or a rare sign reading. These particular editorial remarks have the form (=SIGN NAME), for instance:
# 
# > o. 2     gi ziX-a 12 sar-⌈ta⌉ (=SIG7)
# 
# The script replaces the five spaces with a hash mark and '(=' with '#(=', so that we can use the hash mark to split the line in (potentially) three elements: line number, transliteration, and editorial comment. Both types of editorial comments (sign names and true comments) end up in the third column. We then prefix each line with the [BDTNS](http://bdtns.filol.csic.es) number that was isolated previously, and with a counter (`id_line`) that is set to zero for each new document. The field `id_line` is an integer that can be used to keep or to restore the proper order of the lines within a document.

# In[6]:


lines = []
id_line = 0
id_text = ''
for line in tqdm(bdtns): 
    if line[:6].isdigit(): 
        id_text = line[:6]
        id_line = 0
        continue
    else: 
        id_line += 1
        li = line.strip()
        li = li.replace("(=", "#(=", 1).replace('     ', '#', 1)
        li_l = li.split('#', 2)  # split line into a list with length 3.
        li_l = [id_text, id_line] + li_l
        lines.append(li_l)


# ### 2.4.4.3 Create DataFrame
# The list `lines` is now a list of lists which can be transformed into a `pandas` DataFrame. The DataFrame will have `NaN` (for 'Not a Number') in all cases where a field is empty. `NaN`s are treated by Python as a numerical data type and will throw errors when trying to apply a string function. Therefore, all `NaN`s are replaced by the empty string with the `fillna()` method.

# In[7]:


columns = ["id_text", "id_line", "label", "text", "comments"]
df = pd.DataFrame(lines, columns=columns).fillna("")
df  # inspect the results


# ### 2.4.4.4 Make OGSL compliant
# [OGSL](http://oracc.org/ogsl) is the ORACC Global Sign List, which lists for each sign its possible readings. [OGSL](http://oracc.org/ogsl) compliance opens the possibility to search or compare by sign *name* rather than sign value. For instance, one may search for the sequence "aga₃ kug-sig₁₇" (golden tiara) and find a line reading "gin₂ ku₃-GI".
# 
# The main steps towards [OGSL](http://oracc.org/ogsl) compliance are: 
# 
# - add sign names to x-values
# - replace regular numbers by index numbers in sign values

# (2.4.4.4.1)=
# #### 2.4.4.4.1 Dealing with x-values
# 
# ```{margin}
# Molina, Manuel and Such-Gutiérrez, Marcos, On Terms for Cutting Plants and Noses in Ancient Sumer: *Journal of Near Eastern Studies* 63 (2004) 1-16
# ```
# 
# A peculiarity of the [BDTNS](http://bdtns.filol.csic.es) data set is the way so-called x-values are represented. In Assyriology, x-values are sign readings that have not (yet) received a conventional index number. For instance, the (very common) word  for "to cut (reeds)" is written either with the sign **zi** or with the sign **SIG₇**. Based on the distribution of those spellings (**SIG₇** only in Umma, **zi** elsewhere), M. Molina and M. Such-Guttiérez (2004)[^2] concluded that both spellings write the same word /**zi**/. On that basis the new reading **/zi/** for the sign **SIG₇** was introduced (and is now commonly accepted among Sumerologists). In such cases one may transliterate **ziₓ(SIG₇)** where the SIG₇ between brackets is the name of the sign transliterated as **ziₓ** (and thus the principle of a one-to-one mapping of a transliterated token to a cuneiform sign is maintained). In the [BDTNS](http://bdtns.filol.csic.es) export file this is represented as follows: 
# 
# > 	o. 2     gi ziX-a 12 sar-⌈ta⌉ (=SIG7)		cut reed per 12 *sar* of field
# 
# The index ₓ is represented by a capital X (as in ziX), and the sign name is added at the end of the line, between parens and preceded by the equal sign. 
# 
# In order to use this data for computational purposes (for instance computing sign frequencies) it is necessary to move the sign specification and to transform this into
# 
# > 	o. 2     gi ziₓ(SIG7)-a 12 sar-⌈ta⌉ 
# 
# It is possible to do so with a script or regular expression, and to move the sign name to the position immediately after the capital X. Before we do so, it is useful to inspect some exceptions to the pattern. In some cases sign names are provided for rare readings, for instance:
# 
# > 	18 gin2 nagga mu-kuX gibil (=AN.NA) (=DU)
# 
# If we naively move the first sign name to the first X, we will get:
# 
# > 	18 gin2 nagga mu-kuX(AN.NA) gibil  (=DU)
# 
# (=AN.NA), in this case, explains the rare reading **nagga** (tin, or some similar substance), whereas (=DU) explains **kuX** - but there is no obvious way for a regular expression or script to recognize that. Another type of exception is reduplicated "gurₓ-gurₓ" (to reap) which is represented thus:
# 
# > 6.0.0 še ur5-ra še gurX-gurX-ta su-ga (=ŠE.KIN.ŠE.KIN)
# 
# which, if we naively moved the sign name, would result in:
# 
# > 	6.0.0 še ur5-ra še gurₓ(ŠE.KIN.ŠE.KIN)-gurₓ-ta su-ga
# 
# - x-values that are unambiguous are resolved with a search and replace, using a dictionary - replacing, e.g. ziX with ziₓ(IGI@g). This process does not pay attention to the [BDTNS](http://bdtns.filol.csic.es) sign explication in the `comments` column (=SIG7). A special case in this category is mu-kuX ("delivery"), which is very frequent and should be resolved as mu-kuₓ(DU). However, kuX by itself may also be resolved as kuₓ(LIL) or kuₓ(KWU147) (both for the verb "to enter").
# - x-values that do not resolve unambiguously (muruₓ, ušurₓ, ummuₓ, and several others) are resolved by moving the [BDTNS](http://bdtns.filol.csic.es) sign name (in the `comments` column) after the X sign between brackets, as discussed above.
# 
# Both of these steps are included in the function `ogsl_v()`, that is applied to every row of the DataFrame. In addition, this function will replace index numbers (such as the 7 in sig7) with Unicode index numbers (sig₇), leaving alone numbers that represent quantities (**7 sila3** becomes **7 sila3**, not **₇ sila₃**).
# 
# For `ogsl_v()` to run properly and efficiently, a number of translation tables, dictionaries, and compiled [regular expressions](https://www.regular-expressions.info/) are defined before the function is called.

# #### 2.4.4.4.2 Step 1: Unambiguous x-values
# 
# Some x-values are always resolved in the same way. Thus, ziX is always ziₓ(IGI@g), hirinX is always hirinₓ(KWU318), and gurX is always gurₓ(|ŠE.KIN|). In some cases, x-values have been assigned an index number in [OGSL](http://oracc.org/ogsl). In those cases (nigarₓ = nigar; nemurₓ(PIRIG.TUR) = nemur₂; nagₓ(GAZ) = nag₃; and pešₓ(ŠU.PEŠ5) = peš₁₄) the appropriate index number should be added and the sign name ignored.
# 
# A dictionary of such unambiguous x-values (`xvalues`) has as its key the x-value as represented in [BDTNS](http://bdtns.filol.csic.es) in lower case ('zix') and as its value the index ₓ plus the appropriate sign name ('ₓ(IGI@g)') in [OGSL](http://oracc.org/ogsl) format.
# 
# ```{admonition} OGSL Sign Names
# :class: dropdown, tip
# [OGSL](http://oracc.org/ogsl) uses a set of standard sign names. What is represented as SIG7 in [BDTNS](http://bdtns.filol.csic.es) has the name IGI@g in [OGSL](http://oracc.org/ogsl). In IGI@g the element @g is an abbreviation for the (Akkadian) word *gunû*, which was used by ancient scribal scholars to describe a sign with extra hatching. IGI: 𒅆; IGI@g: 𒅊. Other such markers are @t (*tenû*) for a slanted sign and @š (*šeššig*) for a sign with additional wedges inscribed. The 'times' sign (×) is used to describe a sign that consists of a container sign, inscribed with another sign (as in |KA×GAR| 𒅥). In [OGSL](http://oracc.org/ogsl) such compound signs are demarcated by pipes.
# ```
# 
# The substitution is done with a somewhat complex [regular expression](https://www.regular-expressions.info/), that looks as follows: 
# 
# ```python
# row['text'] = re.sub(xv, lambda m: m.group()[:-1] + xvalues.get(m.group().translate(table).lower(), 'X'), row['text'])
# ```
# The `sub()` function of the `re` library has the general form `re.sub(search_pattern, replace, string)`. Instead of a replace string, one may also give a function (in this case a temporary `lambda` function) that returns the `replace` string. The `lambda` function queries the dictionary `xvalues` to see if the match that was found in the search pattern is present among the keys. The basic format of that command is `xvalues.get(m.group())`, where `m.group()` represents the current match of the search pattern. The search pattern, `xv` (to be explained in more detail below) may match `zahX`, `NigarX`, or `[bu]lugX` - in other words, the match may include capitals (as in `NigarX`) or brackets and flags (as in `[bu]lugX`). In order to find that match in the dictionary it is lowercased and "translated". The function `translate()` translates individual characters into other characters - according to a translation pattern in a table. In this case, the characters representing flags and brackets are all translated to `None` which means, in practice, that they are removed. The matches `zahX`, `NigarX`, and `[bu]lugX`, therefore, will be looked up in the dictionary as `zahx`, `nigarx`, and `bulugx` - and each of those are indeed keys in `xvalues`. In the `get()` function one may optionally add a fall-back value in case the key is not found - in this case the fall-back is 'X'. 
# 
# If a match is found, say `[bu]lugX`, the key `bulugx` is found in the dictionary `xvalues`, returning `ₓ(|ŠIM×KUŠU₂|)`. The return value of the lambda function is the search match (`[bu]lugX`) minus the last character (`[bu]lug`) plus the value that was returned from the dictionary (`ₓ(|ŠIM×KUŠU₂|)`), resulting in `[bu]lugₓ(|ŠIM×KUŠU₂|)`. If the search pattern returns a match that is not found in the dictionary (for instance `ušurX`), the return value of the lambda function is, again, the search match (`ušurX`), minus the last character (`ušur`) plus `X`, the fallback return of the `get()` function, resulting in `ušurX`. In other words - in those cases the search match is replaced by itself and nothing changes.
# 
# The search pattern is a compiled regex (compiled expressions are faster than expressions that need to be interpreted on the fly), `xv`, which is defined as
# ```python
# xv = re.compile(r'[\w' + re.escape(flags) + ']+X')
# ```
# This matches any sequence of one or more (`+`) word-characters (`\w`; this includes letters from the English alphabet as well as special characters such as š, ṣ, and ṭ, the digits 0-9, and the underscore) and/or flags (such as square brackets etc.; see below: Flags), followed by a capital X. This regex will match `ziX`, `zahX`, or `ušurX`, but also `[za]hX`, etc. It does not match 'KA×X', ' X', or 'x-X', because the characters × (for 'times') the hyphen and the space are neither word characters nor flags.
# 
# Special case: **mu-kuX**. There are multiple possible solutions for **kuX**, including kuₓ(LIL) or kuₓ(KWU147), but the very frequent form **mu-kuX** is always to be resolved **mu-kuₓ(DU)**. The regular expression `xv` in the preceding does not match hyphens and thus it will never find the key `mu-kuX` in the dictionary `xvalues`. However, this expression (meaning 'delivery') is so frequent that it makes sense to deal with it separately, rather than depend on the sign names in the `comments` column. The expression **mu-kuX** therefore, has its own line in the function.

# #### 2.4.4.4.3 Step 2: Remaining x-values
# For the remaining x-values (many of them ambiguous) we will copy the [BDTNS](http://bdtns.filol.csic.es) sign name, found in the `comments` column, to the x-value. For instance, **ummu₃** is |A.EDIN.LAL|, but the sign complex has many variants, all rendered **ummuX**: EDIN.A.SU, A.EDIN, A.EDIN.A.LAL, EDIN, etc. The code will result in ummuₓ(|A.EDIN.SU|), ummuₓ(|A.EDIN|), ummuₓ(|A.EDIN.LAL|), ummuₓ(EDIN), etc. Compound signs are put between pipes (|A.EDIN.SU|), according to [OGSL](http://oracc.org/ogsl) conventions.
# 
# In this step the code will naively replace the capital X by the index ₓ, followed by the first word in the `comments` column. This will result in errors if there are more such x-values in a single line - but because we have already dealt with many such values in the preceding, that risk is not very high. The code will test that the capital X does in fact follow a sign reading (as in ziX), and is not an illegible sign (as in KA×X, or simply X). This is done with a [regular expression](https://www.regular-expressions.info/) using a so-called "positive lookbehind" (?<=), to see if the preceding character is a letter. The regular expression for a capital 'X' preceded by any letter valid in Sumerian or Akkadian, is compiled in the variable `lettersX` in order to speed up the process (see below: Letters).

# #### 2.4.4.4.4 Step 3: Index Numbers
# In a third step all sign reading index numbers (as in 'du11') are replaced by Unicode index numbers ('du₁₁'). Regular numbers that express quantities should not be affected. This is done with a regular expression that finds a character, valid in Sumerian or Akkadian transcription, immediately followed by one or more digits. If such a match is found, the string is translated, replacing any digit by its corresponding index number.

# #### 2.4.4.4.5 Errors
# Inevitably, each of the steps in dealing with x-values may introduce its own errors. It is likely, moreover, that there are more x-values not treated here, or that there will be more x-values in a future version of the [BDTNS](http://bdtns.filol.csic.es) data. The dictionary of x-values below can be adjusted to deal with those situations. 

# #### 2.4.4.4.6 Helpful Variables, Lists, and Dictionaries
# A number of lists, dictionaries, and variables (including compiled regular expressions) are defined before the main function is called.
# 
# The list `flags` enumerates characters like square brackets, half-brackets and exclamation marks that may appear in a sign reading in  in [BDTNS](http://bdtns.filol.csic.es). The list is used in two ways. First, it is used in compiling the regular expression `xv` that will match any sign reading that ends in a capital X (see below). Second, it is used to create a table in which each flag corresponds to `None`. The `maketrans()` function is a specialized function that prepares a table that is understood by the `translate()` command. The command `translate(table)` is used in the function `ogsl_v()` (see below) to ignore any flag.
# 
# The [regular expression](https://www.regular-expressions.info/) `xv` matches a sequence of one or more characters, immediately followed by a capital `X`. The characters allowed in the sequence are "word" characters (represented by `\w`), as well as the flags. Word characters are implemented slightly differently in different programs that use regular expressions. In Python it includes the English letters of the alphabet, as well as special characters such as ṭ, ṣ, and š, but also digits (0-9) and the underscore. The `escape()` function from the `re` library supplies the proper escape character for characters in the `flags` variable that otherwise have a special function in regular expressions. For instance, the question mark, which is included in the flags, means 'zero or one time' in a regular expression. In order to match the literal question mark it should be represented as `\?` - the `escape()` funcion takes care of that.
# 
# The variable `letters` is a string that includes all letters that are valid in Sumerian or Akkadian, to be used in regular expressions. The variable `lettersX` is a compiled regular expression that represents a capital `X` preceded by any character in `letters`. The variable `lettersX`is a so-called look-behind expression so that the match consists only of the capital X. Similarly, the variable `lettersNo` is a compiled regular expression that represents a sequence of one or more digits (represented by `\d+`) or capital `X` preceded by any character in `letters`. The variable `lettersno`, however, does not use the lookbehind function (which is relatively slow) because the translation affects only the digits, other characters are left unchanged.
# 
# The dictionary `xvalues` provides the unambiguous x-values in [BDTNS](http://bdtns.filol.csic.es) as keys with their resolution according to [OGSL](http://oracc.org/ogsl) standards.

# In[8]:


flags = "][!?<>⸢⸣⌈⌉*/"
table = str.maketrans(dict.fromkeys(flags))
xv = re.compile(fr'[\w{re.escape(flags)}]+X') #this matches a sequence of word signs (letters) and/or flags, followed by capital X

letters = r'a-zḫĝŋṣšṭA-ZḪĜŊṢŠṬ'
lettersX = re.compile(fr'(?<=[{letters}])X') # capital X preceded by a letter
lettersNo = re.compile(fr'[{letters}](\d+|X)') # any sequence of digits, or X, preceded by a letter

ascind, uniind = '0123456789x', '₀₁₂₃₄₅₆₇₈₉ₓ'
transind = str.maketrans(ascind, uniind) # translation table for index numbers

xvalues = {'nagx' : '₃', 'nigarx' : '', 'nemurx' : '₂', 'pešx' : '₁₄', 'urubx' : '', 
        'tubax' : '₄', 'niginx' : '₈', 'šux' : '₁₄', 
        'alx' : 'ₓ(|NUN.LAGAR|)' , 'bulugx' : 'ₓ(|ŠIM×KUŠU₂|)', 'dagx' : 'ₓ(KWU844)', 
        'durux' : 'ₓ(|IGI.DIB|)', 'durunx' : 'ₓ(|KU.KU)', 
        'gigirx' : 'ₓ(|LAGAB×MU|)', 'giparx' : 'ₓ(KISAL)', 'girx' : 'ₓ(GI)', 
        'gišbunx' : 'ₓ(|KI.BI|)', 'gurx' : 'ₓ(|ŠE.KIN|)', 
        'hirinx' : 'ₓ(KWU318)', 'kurunx' : 'ₓ(|DIN.BI|)',
        'mu-kux' : 'ₓ(DU)', 'munsubx' : 'ₓ(|PA.GU₂×NUN|)',  
        'sagx' : 'ₓ(|ŠE.KIN|)', 'subx' : 'ₓ(|DU.DU|)', 
        'sullimx' : 'ₓ(EN)', 'šaganx' : 'ₓ(|GA×AN.GAN|)', 
        'ulušinx' : 'ₓ(|BI.ZIZ₂|)', 'zabalamx' : 'ₓ(|MUŠ₃.TE.AB@g|)', 
        'zahx' : 'ₓ(ŠEŠ)', 'zahdax' : 'ₓ(|DUN.NE.TUR|)',  
        'zix' : 'ₓ(IGI@g)'}


# #### 2.4.4.4.7 The Main Function
# The function `ogsl_v()` takes one row of the DataFrame at the time and goes through three separate steps, as discussed above (unambiguous x-values, other x-values, sign index numbers).
# 
# In each of these steps the function uses one or more of the tables, dictionaries, and compiled regular expressions created above.

# In[9]:


def ogsl_v(row):
    # 1. deal with unambiguous x-values, listed in the dictionary xvalues.
    row['text'] = re.sub(xv, lambda m: m.group()[:-1] + xvalues.get(m.group().translate(table).lower(), 'X'), row['text'])
    if 'mu-kuX' in row['text'].translate(table): 
        row['text'] = row['text'].replace('X', xvalues['mu-kux'])
    # 2. deal with remaining x-values
    if row["comments"][:2] == "(=": 
        sign_name = row["comments"][2:]  # remove (=  from (=SIG7)
        sign_name = sign_name.split(')')[0] #remove ) and anything following
        if re.findall(r'\.|×|\+', sign_name): # if sign_name contains either . or × or +
            sign_name = f'ₓ(|{sign_name}|)'  # add pipes
        else: 
            sign_name = f'ₓ({sign_name})'
        ogsl_valid = re.sub(lettersX, sign_name, row['text']) # find sequence of letters followed by X; 
                                                              #replace X by ₓ followed by sign name between brackets.
    else:
        ogsl_valid = row["text"]    
    # 3 deal with index numbers
    ogsl_valid = re.sub(lettersNo, lambda m: m.group().translate(transind), ogsl_valid)
    return ogsl_valid


# #### 2.4.4.4.8 Apply the Function
# The `ogsl_v` function is now applied to each row (`axis = 1`) in the DataFrame. Since the DataFrame currently has more than 1.1 million rows (lines) the function may take a few minutes and a progress bar from the `tqdm` library is added.
# 
# In the first cell of this notebook we initiated the use of tqdm with pandas with the line `tqdm.pandas()`. Instead of the regular `apply()` method from the `pandas` library we may now use `progress_apply()` to do the same thing as `apply()`, but with a progress bar.

# In[10]:


df["text"] = df.progress_apply(ogsl_v, axis = 1) 


# #### 2.4.4.4.9 Check for Remaining X-signs
# Any remaining capital X should indicate an illegible sign - or else the script has run into an inconsistency. Such errors may be caused by
# - square brackets occuring immediately before X (as in gari[g]X).
# - X-values that are not explained in the `comments` column.
# - other irregularities in transcription and/or comments.

# In[11]:


df[df.text.str.contains('X')]


# ### 2.4.4.5 Save
# Finally, the newly created DataFrame with [BDTNS](http://bdtns.filol.csic.es) data is saved in two ways. The `to_pickle()` function of the `pandas` library is used to created a pickle, a file that can be opened in a future session to recreate the DataFrame. Second, the DataFrame is saved in JSON format, a format that is more suitable for sharing with other researchers. Both files are saved in the `output` directory.
# #### 2.4.4.5.1 Pickle for Future Use
# Pickle the DataFrame for future use.

# In[12]:


pickled = "output/bdtns.p"
df.to_pickle(pickled)


# #### 2.4.4.5.2 Dump in JSON Format for Distribution
# And/or dump the DataFrame in [JSON](https://www.json.org/) format to share the data with others.

# In[13]:


json = 'bdtns.json'
with open(f'output/{json}', 'w', encoding='utf-8') as w: 
    df.to_json(w, orient='records', force_ascii=False)


# In[ ]:




