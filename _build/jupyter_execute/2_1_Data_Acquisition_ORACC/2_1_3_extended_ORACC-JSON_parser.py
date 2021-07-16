#!/usr/bin/env python
# coding: utf-8

# # Extract Lemmatization from JSON: Extended Parser
# The code in this notebook will parse [ORACC](http://oracc.org) `JSON` files to extract lemmatization data for one or more projects. The code shows how the word-by-word data structure can be reformatted to a line-by-line or document-by-document structure and discusses various other options.
# 
# The output of the Extended Parser contains text IDs, line IDs, lemmas, and (potentially) other data. The first few code blocks are identical with the Basic Parser.
# 
# The code in this notebook (sections 0 to 3: downloading, parsing, and formatting in DataFrame) is also available in the module `utils` in the directory `utils` and can be called as follows: 
# ```python
# import os
# import sys
# util_dir = os.path.abspath('../utils')
# sys.path.append(util_dir)
# import utils
# projects = "dcclt, saao/saa01" # (or any other sequence of ORACC projects, separated by commas)
# words_df = utils.get_data(projects)  
# ```

# In[ ]:


import pandas as pd
import zipfile
import json
from tqdm.auto import tqdm
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils


# ## 0 Create Directories, if Necessary
# The two directories needed for this script are `jsonzip` and `output`. The directories are created with the function `make_dirs()` from the `utils` module. 

# In[ ]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# ## 1.1 Input Project Names
# Provide a list of one or more project names, separated by commas. Note that subprojects must be listed separately, they are not included in the main project. For instance:
# 
# `saao/saa01,saao/saa02,blms`
# 
# The input is split into a proper list that python can iterate over using the `format_project_list()` function in the `utils` module. The code of this function is discussed in more detail in 2.1.0. Download ORACC JSON Files.

# In[ ]:


projects = input('Project(s): ').lower().strip()
project_list = utils.format_project_list(projects)


# ## Download the ZIP files.
# Download the zipped JSON files using the `oracc_download()` function in the `utils` module. The code of this function is discussed in 2.1.0. Download ORACC JSON Files.

# In[ ]:


project_list = utils.oracc_download(project_list)


# ## <a name="head21"></a>2.1 The `parsejson()` function
# The `parsejson()` function is identical in structure with the function of that same name in `2_1_2_basic_ORACC-JSON_parser.ipynb`, but it fetches more data. The field `id_word` consists of three parts, namely a text ID, line ID, and word ID, in the format `Q000039.76.2` meaning: the second word in line 76 of text object `Q000039`. Note that `76` is not a line number strictly speaking but an object reference within the text object. Things like horizontal rulings, columns, and breaks also get object references. The `id_word` field allows us to put lines, breaks, and horizontal rulings together in the proper order.
# 
# The field `label` is a human-legible label that refers to a line or another part of the text; it may look like `o i 23` (obverse column 1 line 23) or `r v 23'` (reverse column 5 line 23 prime). The `label` field is used in online [ORACC](http://oracc.org) editions to indicate line numbers.
# 
# The fields `extent`, `scope`, and `state` give metatextual data about the condition of the object; they capture the number of broken lines or columns and similar information. 
# 
# The field `field` is used primarily in lexical texts. For the field abbreviations and their meanings, see the [documentation](http://oracc.museum.upenn.edu/doc/help/editinginatf/lexicaltexts/index.html). The field label looks like `wp` (word or phrase), or `sg` (Sign) and is found under the JSON key `subtype` after a `field-start` entry. The field label is copied to the `meta_d` dictionary (under the key `field`), but this key is removed from `meta_d` as soon as the parser encounters a `field-end` value (with the `pop()` method). The great majority of lemmas have no field attribute - the key is "popped" so that it does not inadvertently get copied to all subsequent lemmas. Administrative text may have a `field` indicating that a word belongs to a year name (`yn`). This may be used, for instance, to remove yearnames in analyzing the vocabulary of the Ur III corpus.
# 
# This version of the `parsejson()` function is also available in the module `utils`.
# 

# In[ ]:


def parsejson(text, meta_d):
    lemmas = []
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            lemmas.extend(parsejson(JSONobject, meta_d))
        if "label" in JSONobject: 
            meta_d["label"] = JSONobject['label']   # `label` is the line number; it stays constant until
                                                    # the process move to a new line
        
        if JSONobject.get("type") == "field-start": # this is for sign lists, identifying fields such as
            meta_d["field"] = JSONobject["subtype"]  # sign, pronunciation, translation.
        elif JSONobject.get("type") == "field-end":
            meta_d.pop("field", None)                           # remove the key "field" to prevent it from being copied 
                                                              # to all subsequent lemmas (which may not have fields)
        if "f" in JSONobject:
            lemma = JSONobject["f"]
            lemma["id_word"] = JSONobject["ref"]
            lemma['label'] = meta_d["label"]
            lemma["id_text"] = meta_d["id_text"]
            if "field" in meta_d:
                lemma["field"] = meta_d["field"]
            lemmas.append(lemma)
        elif JSONobject.get("strict") == "1":      # horizontal ruling on tablet; or breakage
            lemma = {}
            lemma['extent'] = JSONobject['extent']
            lemma['scope'] = JSONobject['scope']
            lemma['state'] = JSONobject['state']
            lemma["id_word"] = JSONobject["ref"]
            lemma["id_text"] = meta_d["id_text"]
            lemmas.append(lemma)
    return lemmas


# ## 2.2 Call the `parsejson()` function for every `JSON` file
# The code in this cell will iterate through the list of projects entered above (1.1). For each project the `JSON` zip file is located in the directory `jsonzip`, named PROJECT.zip. The `zip` file contains a directory that is called `corpusjson` that contains a JSON file for every text that is available in that corpus. The files are called after their text IDs in the pattern `P######.json` (or `Q######.json` or `X######.json`).
# 
# The function `namelist()` of the `zipfile` package is used to create a list of the names of all the files in the ZIP. From this list we select all the file names in the `corpusjson` directory with extension `.json` (this way we exclude the name of the directory itself). 
# 
# Each of these files is read from the `zip` file and loaded with the command `json.loads()`, which transforms the string into a proper JSON object. 
# 
# This JSON object (essentially a Python dictionary), which is called `data_json` is now sent to the `parsejson()` function. The function returms a list of lemmata, each lemma represented by a dictionary. This list is added to the `lemm_l` list. In the end, `lemm_l` will contain as many list elements as there are words in all the texts in the projects requested.
# 
# The dictionary `meta_d` is created to hold temporary information. The value of the key `id_text` is updated in the main process every time a new JSON file is opened and send to the `parsejson()` function. The `parsejson()` function itself will change values or add new keys, depending on the information found while iterating through the JSON file. When a new lemma row is created, `parsejon()` will supply data such as `id_text`, `label` and (potentially) other information from `meta_d`.

# In[ ]:


lemm_l = []
meta_d = {"label": None, "id_text": None}
for project in project_list:
    file = f'jsonzip/{project.replace("/", "-")}.zip'
    try:
        zip_file = zipfile.ZipFile(file)       # create a Zipfile object
    except:
        errors = sys.exc_info() # get error information
        print(file), print(errors[0]), print(errors[1]) # and print it
        continue
    files = zip_file.namelist()     # list of all the files in the ZIP
    files = [name for name in files if "corpusjson" in name and name[-5:] == '.json']                                                                                                  #that holds all the P, Q, and X numbers.
    for filename in tqdm(files, desc = project):       #iterate over the file names
        id_text = project + filename[-13:-5] # id_text is, for instance, blms/P414332
        meta_d["id_text"] = id_text
        try:
            text_json_string = zip_file.read(filename).decode('utf-8')         #read and decode the json file of one particular text
            data_json = json.loads(text_json_string)                # make it into a json object (essentially a dictionary)
            lemm_l.extend(parsejson(data_json, meta_d))     # and send to the parsejson() function
        except:
            e = sys.exc_info() # get error information
            print(filename), print(e[0]), print(e[1]) # and print it
    zip_file.close()


# ## 3 Data Structuring
# ### 3.1 Transform the Data into a DataFrame
# The list `lemm_l` is transformed into a `pandas` dataframe for further manipulation.
# 
# For various reasons not all JSON files will have all data types that potentially exist in an [ORACC](http://oracc.org) signature. Only Sumerian words have a `base`, so if your data set has no Sumerian, this column will not exist in the DataFrame.  If a text has no breakage information in the form of `1 line broken` (etc.) the fields `extent`, `scope`, and `state` do not exist. Where such fields are referenced below, the code may fail and you may need to adjust some lines.

# In[ ]:


words_df = pd.DataFrame(lemm_l)
words_df = words_df.fillna('')   # replace NaN (Not a Number) with empty string
words_df


# ## 3.2 Remove Spaces and Commas from Guide Word and Sense
# Spaces and commas in Guide Word and Sense may cause trouble in computational methods in tokenization, or when saved in Comma Separated Values format. All spaces and commas are replaced by hyphens and nothing (empty string), respectively. By default the `replace()` function in `pandas` will match the entire string (that is, "lugal" matches "lugal" but there is no match between "l" and "lugal"). In order to match partial strings the parameter `regex` must be set to `True`.
# 
# The `replace()` function takes a nested dictionary as argument. The top-level keys identify the columns on which the `replace()` function should operate (in this case 'gw' and 'sense'). The value of each key is another dictionary with the search string as key and the replace string as value.

# In[ ]:


findreplace = {' ' : '-', ',' : ''}
words_df = words_df.replace({'gw' : findreplace, 'sense' : findreplace}, regex=True)


# The columns in the resulting DataFrame correspond to the elements of a full [ORACC](http://oracc.org) signature, plus information about text, line, and word ids:
# * base (Sumerian only)
# * cf (Citation Form)
# * cont (continuation of the base; Sumerian only)
# * epos (Effective Part of Speech)
# * form (transliteration, omitting all flags such as indication of breakage)
# * frag (transliteration; including flags)
# * gdl_utf8 (cuneiform)
# * gw (Guide Word: main or first translation in standard dictionary)
# * id_text (six-digit P, Q, or X number)
# * id_word (word ID in the format Text_ID.Line_ID.Word_ID)
# * label (traditional line number in the form o ii 2' (obverse column 2 line 2'), etc.)
# * lang (language code, including sux, sux-x-emegir, sux-x-emesal, akk, akk-x-stdbab, etc)
# * morph (Morphology; Sumerian only)
# * norm (Normalization: Akkadian)
# * norm0 (Normalization: Sumerian)
# * pos (Part of Speech)
# * sense (contextual meaning)
# * sig (full ORACC signature)
# 
# Not all data elements (columns) are available for all words. Sumerian words never have a `norm`, Akkadian words do not have `norm0`, `base`, `cont`, or `morph`. Most data elements are only present when the word is lemmatized; only `lang`, `form`, `id_word`, and `id_text` should always be there.

# ## Create Line ID
# The DataFrame currently has a word-by-word data representation. We will add to each word a field `id_line` that will make it possible to reconstruct lines. This newly created field `id_line` is different from a traditional line number (found in the field "label") in two ways. First, id_line is an integer, so that lines are sorted correctly. Second, `id_line` is assigned to words, but also to gaps and horizontal drawings on the tablet. The field `id_line` will allow us to keep all these elements in their proper order.
# 
# The field "id_line" is created by splitting the field "id_word" into (two or) three elements. The format of "id_word" is IDtext.line.word. The middle part, id_line, is selected and its data type is changed from string to integer. Rows that represent gaps in the text or horizontal drawings have an "id_word" in the format IDtext.line (consisting of only two elements), but are treated in exactly the same way.

# In[ ]:


words_df['id_line'] = [int(wordid.split('.')[1]) for wordid in words_df['id_word']]


# ## 4 Save Results in CSV file or in Pickle
# The output file is called `parsed.csv` and is placed in the directory `output`. In most computers, `csv` files open automatically in Excel. This program does not deal well with `utf-8` encoding (files in `utf-8` need to be imported; see the instructions [here](https://www.itg.ias.edu/content/how-import-csv-file-uses-utf-8-character-encoding-0). If you intend to use the file in Excel, change `encoding ='utf-8'` to `encoding='utf-16'`. For usage in computational text analysis applications `utf-8` is usually preferred. 
# 
# The Pandas function `to_pickle()` writes a binary file that can be opened in a later phase of the project with the `read_pickle()` command and will reproduce exactly the same DataFrame with the same data structure. The resulting file cannot be used in other programs.

# In[ ]:


savefile =  'parsed.csv'
with open(f'output/{savefile}', 'w', encoding="utf-8") as w:
    words_df.to_csv(w, index=False)
pickled = "output/parsed.p"
words_df.to_pickle(pickled)


# # 5 Post Processing
# # 5.1 Manipulate for Analysis on Line level
# For analyses that use a line as unit of analysis (e.g. lines in lexical texts as used in Chapter 3) one may need to create lemmas and combine these into lines by using the `id_line` variable.

# ## 5.1.1 Create Lemma Column
# A lemma, [ORACC](http://oracc.org) style, combines Citation Form, GuideWord and POS into a unique reference to one particular lemma in a standard dictionary, as in `lugal[king]N` (Sumerian) or `šarru[king]N`. Usually, not all words in a text are lemmatized, because a word may be (partly) broken and/or unknown. Unlemmatized and unlemmatizable words will receive a place-holder lemmatization that consists of the transliteration of the word (instead of the Citation Form), with `NA` as GuideWord and `NA` as POS, as in `i-bu-x[NA]NA`. Note that `NA` is a string. Finally, rows representing horizontal rulings or broken lines have the empty string in both Citation Form and Form. In those cases Lemma should have the empty string, too.

# In[ ]:


words_df['lemma'] = words_df["cf"] + "[" + words_df["gw"] + "]" + words_df["pos"]
words_df.loc[words_df["cf"] == "" , 'lemma'] = words_df['form'] + "[NA]NA"
words_df.loc[words_df["form"] == "", 'lemma'] = ""
words_df


# ## 5.1.2 Group by Line
# In the `words_df` dataframe each word has a separate row. In order to change this into a line-by-line representation we use the `pandas` `groupby()` function, using `id_text`, `id_line` and `label` fields as the sorting arguments. 
# 
# The fields that are aggregated are `lemma`, `extent`, `scope`, and `state`. The fields `extent`, `scope`, and `state` represent data on the number of broken lines. For instance, the notation `4 lines missing` in the [ORACC](http://oracc.org) edition will result in `extent = "4"`, `scope = "line"`, `state = "missing"` (note that the value of `extent` is a string and will be `"n"` if the number of missing lines or columns is unknown).
# 
# If your data does not have the fields `extent`, `scope`, and `state` the code below will fail - simply delete the lines that reference those fields.

# In[ ]:


lines = words_df.groupby([words_df['id_text'], words_df['id_line'], words_df['label']]).agg({
        'lemma': ' '.join,
        'extent': ''.join, 
        'scope': ''.join,
        'state': ''.join
    }).reset_index()
lines


# ## 5.2 Alternative: Texts in Normalized Transcription
# This code (which is useful mostly for Akkadian texts) will produce a text in normalized transcription, essentially following the pattern of the preceding. Before grouping words into documents, we need to take care of words that have not been normalized (for instance because of breakage), using the field `form`. The field `norm1` now has the normalized form of the word if it is available; if not it has the raw transliteration (without flags or breakage information).

# In[ ]:


words_df["norm1"] = words_df["norm"]
words_df.loc[words_df["norm1"] == "" , 'norm1'] = words_df['form']


# In[ ]:


texts_norm = words_df.groupby([words_df['id_text']]).agg({
        'norm1': ' '.join,
    }).reset_index()
texts_norm


# ### 5.2.1 Save Normalized Transcriptions
# The `texts_norm` DataFrame has one complete document in normalized transcription in each row. The code below saves each row as a separate `.txt` file, named after the document's ID.

# In[ ]:


for idx, Q in enumerate(texts_norm["id_text"]):
    savefile =  f'{Q[-7:]}.txt'
    with open(f'output/{savefile}', 'w', encoding="utf-8") as w:
        texts_norm.iloc[idx].to_csv(w, index = False, header=False)


# In[ ]:




