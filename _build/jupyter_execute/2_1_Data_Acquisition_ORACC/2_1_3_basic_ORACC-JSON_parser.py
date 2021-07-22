#!/usr/bin/env python
# coding: utf-8

# # 2.1.3 Extract Lemmatization from ORACC JSON: Basic Parser
# The code in this notebook will parse [ORACC](http://oracc.org) `JSON` files to extract lemmatization data for one or more projects. The resulting `csv` (Comma Separated Values) file is named `parsed.csv` and has two fields: a Text ID (e.g. `dcclt/Q000039`) and a string of lemmas in the format `lugal[king]N` (or `šarru[king]N` for Akkadian texts).
# 
# The output of the Basic Parser contains *only* text IDs and lemmas. This format is useful for so-called [bag of words](https://en.wikipedia.org/wiki/Bag-of-words_model) techniques such as word clouds or [topic modeling](https://en.wikipedia.org/wiki/Topic_model). The `JSON` files, however, contain a wealth of other data, including language (Sumerian, Akkadian, Emesal, etc.), orthographic form, morphology (currently only for Sumerian and Emesal), line numbers, breakage, etc. The extended JSON parser notebook (2.1.4), building upon the techniques demonstrated here, will show how to extract any type of data.

# ## 2.1.3.0 Import Packages
# * pandas: data analysis and manipulation; dataframes
# * ipywidgets: user interface (enter project names)
# * panel: another set of widget tools (here used for displaying a JSON file)
# * zipfile: read data from a zipped file
# * json: read a json object
# * tqdm: progress bar
# * os: basic Operating System tasks (such as creating a directory)
# * sys: change system parameters
# * utils: compass-specific utilities (download files from ORACC, etc.)

# In[6]:


import pandas as pd
import ipywidgets as widgets
import zipfile
import panel as pn
import json
from tqdm.auto import tqdm
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils
pn.extension()


# ## 2.1.3.1 Create Directories, if Necessary
# The two directories needed for this script are `jsonzip` and `output`. 

# In[7]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# ## 2.1.3.2 Input Project Names
# We can download and manipulate multiple [ORACC](http://oracc.org) `zip` files at the same time. The `Textarea` widget provides a space for typing project abbreviations, separated by a comma. The widget is assigned to the variable `projects`. The text entered in the `Textarea` widget can be retrieved as `projects.value`.
# 
# :::{warning}
# Subprojects must be listed separately, they are not included in the main project. A subproject is named `[PROJECT]/[SUBPROJECT]`, for instance `saao/saa01`.
# :::

# In[8]:


projects = widgets.Textarea(
    value="obmc",
    placeholder='Type project names, separated by commas',
    description='Projects:',
)
projects


# ## 2.1.3.3 Split the List of Projects and Download the ZIP files.
# Use the `format_project_list()` and `oracc_download()` functions from the `utils` module to download the requested projects. The code of these function is discussed in more detail in 2.1.0. Download ORACC JSON Files. The function returns a new version of the project list, with duplicates and non-existing projects removed.

# In[10]:


project_list = utils.format_project_list(projects.value)
project_list = utils.oracc_download(project_list)


# ## 2.1.3.4 ORACC JSON: the CDL Structure
# [ORACC](http://oracc.org) `zip` files contain JSON files for each individual text (exemplar or composite) that is part of that project. These files are found in the directory `corpusjson` and are named after the text ID (for instance `P200931.json`). The `parse_text_json()` function (2.1.3.5) extracts basic lemmatization data from each of those files. In the next section (2.1.4) we will review techniques to extract other types of information from these same files.
# 
# The structure of the JSON files for text editions is fairly complex, because of the hierarchical structure of textual data. A text may have one or more surfaces (obverse, reverse), each surface may have one or more columns; each column has lines; each line has words; and each word has signs.
# 
# 	text object
# 		surface
# 			column
# 				line
# 					word
# 						sign
# 
# How many of those layers are present in a particular text is impossible to predict. Some tablets have columns, others do not; most surfaces have text, but not all surfaces do. In addition, a text consists of textual units, such as paragraphs, sentences, phrases and words, which form a separate hierarchy.
# 
# 	text
# 		paragraph
# 			sentence
# 				phrase
# 					word
# 
# These two hierarchies, which do not necessarily coincide, are simultaneously represented in the JSON tree. The object-oriented hierarchy is represented by d (Discontinuity) nodes, the discourse-oriented hierarchy is represented by c (Chunk) nodes.
# 
# The [ORACC](http://oracc.org) JSON tree for a text edition consists of a hierarchy of `cdl` keys. The name `cdl` is based on the three main components of the nested tree: Chunks (text units), Discontinuities (physical units), and Lemmas (words). A Chunk is a chunk of text of any length: the body of the text, a sentence, a phrase, a word, etc. A Discontinuity is the text object, the obverse or reverse, the beginning of a column, a break in the text, a horizontal ruling on the tablet, or the beginning of a new line. A Lemma is the lemmatization of a single word in the text, including the information on the sign level. 
# 
# The value of a `cdl` key is a list of one or more dictionaries. Each of these dictionaries contains the key "node" which may have the values "c" (for Chunk), "d" (for Discontinuity), or "l" (for Lemma). Any "c" dictionary may contain a further `cdl` key, which again has as its value a list of dictionaries of the "c", "d", or "l" type. The "c" and "d" dictionaries always have a key `type`, which may have values such as `text`, `discourse`, or `sentence` (for "c" nodes) or `object`, `obverse`, `column-start`, `line-start` (for "d" nodes). Discontinuities (or "d" nodes") may also have `type : nonx`, recording non-textual physical features such as rulings on the tablet, or missing lines. An "l" (Lemma) dictionary, is always at the bottom of the `cdl` hierarchy. The "l" dictionary itself contains an "f" key which has as its value a dictionary that contains all the lemmatization data of a single word (transliteration, citation form, guide word, part of speech, etc.). The "f" dictionary includes a "gdl" key (for Grapheme Description Language), which identifies the graphemes (cuneiform signs) of which the word is composed, with information on the reading and the function (syllabogram, logogram, determinative, etc.) of those graphemes. 
# 
# :::{note}
# In some [ORACC](http://oracc.org) projects the `gdl` node will also include the actual glyphs of the cuneiform signs.
# :::
# 
# :::{margin}
# Note that the JSON display in the cell below utilizes the JSON vocabulary for the various data structures: array (instead of list) and object (instead of dictionary). See section 2.1.1.
# :::
# 
# The structure may be illustrated with the beginning of [P251867](http://oracc.org/dcclt/P251867), an Old Babylonian 3-line lentil (school text), edited in [DCCLT](http://oracc.org/dcclt) (beginning of the file omitted): 

# ```json
# {"cdl": [
# {
#   "node": "c",
#   "type": "text",
#   "id": "P251867.U0",
#   "cdl": [
#     {
#       "node": "d",
#       "type": "object",
#       "ref": ""
#     },
#     {
#       "node": "d",
#       "subtype": "obverse",
#       "type": "obverse",
#       "ref": "P251867.o.1",
#       "label": "o"
#     },
#     {
#       "node": "c",
#       "type": "discourse",
#       "subtype": "body",
#       "id": "P251867.U1",
#       "cdl": [
#         {
#           "node": "c",
#           "type": "sentence",
#           "id": "P251867.U2",
#           "label": "o 1 - o 3",
#           "cdl": [
#             {
#               "node": "d",
#               "type": "line-start",
#               "ref": "P251867.2",
#               "n": "1",
#               "label": "o 1"
#             },
#             {
#               "node": "l",
#               "frag": "{ŋeš}ma₂-durah-abzu",
#               "id": "P251867.l1ac01",
#               "ref": "P251867.2.1",
#               "inst": "Madurahabzu[1]ON",
#               "sig": "@dcclt%sux:{ŋeš}ma₂-durah-abzu=Madurahabzu[1//1]ON'ON$Madurahabzu/{ŋeš}ma₂-durah-abzu#~",
#               "f": {
#                 "lang": "sux",
#                 "form": "{ŋeš}ma₂-durah-abzu",
#                 "gdl": [
#                   {
#                     "det": "semantic",
#                     "pos": "pre",
#                     "seq": [
#                       {
#                         "v": "ŋeš",
#                         "id": "P251867.2.1.0"
#                       }
#                     ]
#                   },
# ```
# 
# The first `cdl` key contains a list that has a single element, a dictionary (the ending square bracket of this list is not included in the snippet). This dictionary is a `c` node (Chunk) representing the entire text. The `c` node contains a new `cdl` key which has a list of dictionaries as its value including two `d` (Discontinuity) nodes (`object` and `obverse`) and another `c` node that represents a discourse unit, namely the body of the text (note that Chunk `text` and Chunk `body` are identical here - but that need not be the case). Eventually, there is a node `l` that contains the transliteration and lemmatization data for the first word of this text.
# 
# This hierarchy implies that a word (an "l" node) may belong to different hierarchies that do not necessarily align. For instance, a word may belong to a sentence (a Chunk) that continues from the obverse to the reverse (Discontinuities) of a tablet. The JSON structure allows to express (and to retrieve) those facts simultaneously.
# 
# In order to pull out the lemmatization data we need to iterate through the hierarchy of `cdl` keys until we encounter an `l` node, containing an `f` key. The value of the `f` key is the data we want.

# ## 2.1.3.5 The `parse_text_json()` function
# A straightforward way of extracting the lemmatization data out of an [ORACC](http://oracc.org) JSON file is by defining a recursive function, that is, a function that calls itself to recursively inspect the value of successive layers of `cdl` keys until one encounters an `f` key. The contents of the `f` key are then added to a list. In its most basic form that function looks like this:
# 
# ```python
# def parse_text_json(text):
#     lemmas = []
#     for JSONobject in text["cdl"]:
#         if "cdl" in JSONobject: 
#             lemmas.extend(parse_text_json(JSONobject))
#         if "f" in JSONobject:
#             lemmas.append(JSONobject["f"])
#     return lemmas
# ```
# 
# The function is called with the argument `text`, which contains the contents of the entire JSON file. The function adds a new dictionary of lemmatization data (one word at a time) each time it encounters an `f` key to the list `lemmas`. 
# 
# The `parse_text_json()` we will use here adds one thing to the basic function discussed above. It will add the project name and text ID in the format `cams/gkab/P338616` or `dcclt/Q000039` to the lemmatization data of each word. If we parse data from multiple projects this additional field will allow us to trace back to the original data.
# 
# The `parse_text_json()` function thus takes two arguments: the JSON object that is being parsed (and that contains the information of one text as edited in [ORACC](http://oracc.org)) and a text identifier. The function returns a list of dictionaries (`lemmas`) where each element in the list represents the lemmatization data of one word.

# In[19]:


def parse_text_json(text, id_text):
    lemmas = []
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            lemmas.extend(parse_text_json(JSONobject, id_text))
        if "f" in JSONobject:
            lemm = JSONobject["f"]
            lemm["id_text"] = id_text
            lemmas.append(lemm)
    return lemmas


# ## 2.1.3.6 Call the `parse_text_json()` function for every `JSON` file
# The code in this cell will iterate through the list of projects entered above (2.1.3.2). For each project the `JSON` zip file is located in the directory `jsonzip`, named PROJECT.zip. The `zip` file contains a directory that is called `corpusjson` that contains a JSON file for every text that is available in that corpus. The files are called after their text IDs in the pattern `P######.json` (or `Q######.json` or `X######.json`).
# 
# The function `namelist()` of the `zipfile` package is used to create a list of the names of all the files in the ZIP. From this list we select all the file names in the `corpusjson` directory with extension `.json` (this way we exclude the name of the directory itself). 
# 
# Each of these files is read from the `zip` file and loaded with the command `json.loads()`, which transforms the string into a proper JSON object. 
# 
# This JSON object (essentially a Python dictionary), which is called `data_json` is now sent to the `parse_text_json()` function. The function returns a list of lemmata (each lemma represented by a dictionary). The `extend()` method is used to add this list to the list `lemm_l`, one document at the time. In the end, `lemm_l` will contain as many list elements as there are words in all the texts in the projects requested.

# In[22]:


lemm_l = [] # initiate the list that will hold all the lemmatization data of all texts in all requested projects
for project in project_list:
    file = f"jsonzip/{project.replace('/', '-')}.zip"
    try:
        zip_file = zipfile.ZipFile(file)       # create a Zipfile object
    except:
        errors = sys.exc_info() # get error information
        print(file), print(errors[0]), print(errors[1]) # and print it
        continue
        
    files = zip_file.namelist()     # list of all the files in the ZIP
    files = [name for name in files if "corpusjson" in name and name[-5:] == '.json']                                                                                                  #that holds all the P, Q, and X numbers.

    for filename in tqdm(files, desc=project):  #iterate over the file names
        id_text = project + filename[-13:-5] # id_text is, for instance, blms/P414332
        try:
            text = zip_file.read(filename).decode('utf-8')         #read and decode the json file of one particular text
            data_json = json.loads(text)                # make it into a json object (essentially a dictionary)
            lemm_l.extend(parse_text_json(data_json, id_text))               # and send to the parsejson() function
        except:
            errors = sys.exc_info() # get error information
            print(filename), print(errors[0]), print(errors[1]) # and print it
    zip_file.close()


# ## 2.1.3.7 Data Structuring
# The list `lemm_l` is transformed into a `pandas` dataframe (`word_df`) for further manipulation. The `pandas` function `fillna('')` fills gaps in the dataframe. If a particular data field is not available for a particular row, `pandas` will fill that cell with NaN ("Not a Number"). The data type of NaN is numeric, which creates problems in string manipulation further down the road (for instance in creating a Lemma column, section 3.2). The function `fillna()` will fill all empty cells with the argument it is given - in this case the empty string.
# 
# For various reasons not all JSON files will have all data types that potentially exist in an [ORACC](http://oracc.org) lemmatization. For instance, only Sumerian words have a `base`, so if your data set has no Sumerian, this column will not exist in the DataFrame. Where such fields are referenced below, the code may fail and you may need to adjust some lines.

# In[23]:


word_df = pd.DataFrame(lemm_l).fillna('')
# replace NaN (Not a Number) with empty string
word_df


# ## 2.1.3.8 Remove Spaces and Commas from Guide Word and Sense
# Spaces and commas in Guide Word and Sense may cause trouble in computational methods in tokenization, or when saved in Comma Separated Values format. All spaces and commas are replaced by hyphens and nothing (empty string), respectively. By default the `replace()` function in `pandas` will match the entire string (that is, "lugal" matches "lugal" but there is no match between "l" and "lugal"). In order to match partial strings the parameter `regex` must be set to `True`.
# 
# The `replace()` function takes a nested dictionary as argument. The top-level keys identify the columns on which the `replace()` function should operate (in this case 'gw' and 'sense'). The value of each key is another dictionary with the search string as key and the replace string as value.

# In[24]:


findreplace = {' ' : '-', ',' : ''}
word_df = word_df.replace({'gw' : findreplace, 'sense' : findreplace}, regex = True)


# ## 2.1.3.9 Create a `lemma` column
# A lemma, [ORACC](http://oracc.org) style, combines Citation Form, GuideWord and POS into a unique reference to one particular lemma in a standard dictionary, as in `lugal[king]N` (Sumerian) or `šarru[king]N` (Akkadian). Usually, not all words in a text are lemmatized, because a word may be (partly) broken and/or unknown. Unlemmatized and unlemmatizable words will receive a place-holder lemmatization that consists of the transliteration of the word (instead of the Citation Form), with `NA` as GuideWord and `NA` as POS, as in `i-bu-x[NA]NA`. 
# 
# :::{note}
# Note that `NA` is a string and does not equal the missing value symbol NaN.
# :::

# In[25]:


word_df["lemma"] = word_df["cf"] + '[' + word_df["gw"] + ']' + word_df["pos"]
word_df.loc[word_df["cf"] == "" , 'lemma'] = word_df['form'] + '[NA]NA'
word_df[['id_text', 'lemma']]


# ## 2.1.3.10 Group by Textid
# Get all the lemmas that belong to a single text in one row (one row = one document). The `agg()` (aggregate) function, which works on the result of a `groupby()` process, aggregates data of the original dataframe. The aggregate function takes a dictionary in which the keys are column names and the values are functions to be used in the aggregation process. The example below has only one such function (`' '.join` will join all entries in the colum `lemma` with a space in between); one may specify (the same or different) functions for different columns, for instance:
# ```python
# word_df = word_df.groupby("textid").agg({"lemma": ' '.join, "base": ' '.join})
# ```
# The process will create a compound index. It is useful to flatten the index with a reset (`reset_index()`).
# 
# The result is a dataframe with two columns: `id_text` and `lemma`. The `lemma` column has a sequence of all the lemmas in that text (in the original order).
# 
# :::{note}
# This is just one example of how the output of the `parse_text_json()` may be structured in a `pandas` dataframe. How to structure the data depends on the research project.
# :::

# In[26]:


doc_df = word_df.groupby("id_text").agg({"lemma": ' '.join})
doc_df = doc_df.reset_index()
doc_df


# ## 2.1.3.11 Save the Results: CSV
# The output file is called `parsed.csv` and is placed in the directory `output`. In most cases, `csv` files open automatically in Excel. This program does not deal well with `utf-8` encoding. If you intend to use the file in Excel, change `encoding ='utf-8'` to `encoding='utf-16'`. For usage in computational text analysis applications `utf-8` is usually preferred. The option `index=False` excludes the (numerical) index from the saved `csv`.

# In[27]:


savefile =  'parsed.csv'
with open(f'output/{savefile}', 'w', encoding="utf-8") as w:
    doc_df.to_csv(w, index=False)


# ## 2.1.3.12 Save the Results: Pickle
# The Pandas function `to_pickle()` writes a binary file that can be opened in a later phase of the project with the `read_pickle()` command, reproducing exactly the same DataFrame. The resulting file cannot be used in other programs but preserves the data structure of the DataFrame.

# In[ ]:


pickled = "output/parsed.p"
doc_df.to_pickle(pickled)


# In[ ]:




