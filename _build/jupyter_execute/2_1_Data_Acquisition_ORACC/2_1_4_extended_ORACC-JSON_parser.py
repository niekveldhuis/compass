#!/usr/bin/env python
# coding: utf-8

# # 2.1.4 ORACC JSON: Extended Parser
# 
# The basic `parse_text_json()` discussed in 2.1.3 captures only lemmatization data, it ignores line numbers, text breaks, and other types of information that are included in the JSON files. The basic `parse_text_json()` is good enough for a "Bag of Words" approach, which looks only at vocabulary frequency, ignoring word order. For many other types of analysis we do need to capture line numbers and text breaks. Such information is stored in "d" nodes in a level above the "l" node in the `cdl` hierarchy. Similarly, sentence identifiers (and other discourse units) are stored in "c" nodes. The `parse_text_json()` function can easily be enhanced to capture various types of such meta-data storing them in a dictionary called `meta_d`. This dictionary is updated whenever the `parse_text_json()` function encounters a relevant node. Each lemma that the function returns receives the current meta-data from `meta_d`. 
# 
# :::{note}
# For an explanation of the `cdl` hierarchy see section 2.1.3 and the [opendata/JSON](http://oracc.org/doc/opendata/json/index.html) page on [ORACC](http://oracc.org).
# :::
# 
# The output of the Extended Parser contains text IDs, line IDs, lemmas, and (potentially) other data. 
# 
# The code in this notebook (sections 0 to #: downloading, parsing, and formatting in DataFrame) is also available in the `get_data()` function in the `utils` module. The function `utils.get_Data()` takes a single argument: a string with a sequence of [ORACC](http://oracc.org) projects and sub-projects, separated by commas. It returns a dataframe that includes lemmatization data, line numbers, information on breakage and horizontal ruilings, etc. The function may be called as follows: 
# 
# ```python
# import os
# import sys
# util_dir = os.path.abspath('../utils')
# sys.path.append(util_dir)
# import utils
# projects = "dcclt, saao/saa01" # (or any other sequence of ORACC projects, separated by commas)
# words_df = utils.get_data(projects)  
# ```
# 
# The code for creating directories (`jsonzip` and `output`), and selecting and downloading the relevant [ORACC](http://oracc.org) projects is the same as in previous notebooks and is not commented upon.

# ## 2.1.4.0 Import Packages
# * pandas: data analysis and manipulation; dataframes
# * ipywidgets: user interface (enter project names)
# * zipfile: read data from a zipped file
# * json: read a json object
# * tqdm: progress bar
# * os: basic Operating System tasks (such as creating a directory)
# * sys: change system parameters
# * utils: compass-specific utilities (download files from ORACC, etc.)

# In[1]:


import pandas as pd
import ipywidgets as widgets
import zipfile
import json
from tqdm.auto import tqdm
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils


# ## 2.1.4.1 Preliminary: Create Directories, Download Projects

# In[2]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# Input Project Names
# 
# :::{margin}
# Subprojects must be listed separately, they are not included in the main project. A subproject is named `[PROJECT]/[SUBPROJECT]`, for instance `saao/saa01`.
# :::

# In[3]:


projects = widgets.Textarea(
    value="saao/saa01",
    placeholder='Type project names, separated by commas',
    description='Projects:',
)
projects


# In[4]:


project_list = utils.format_project_list(projects.value)
project_list = utils.oracc_download(project_list)


# ## 2.1.4.2 The extended `parse_text_json()` function
# The `parse_text_json()` function is identical in structure with the function of that same name in section 2.1.3, but it fetches more data. 
# 
# :::{margin}
# In the `id_word` string `Q000039.76.2` the number `76` is not a line number strictly speaking but an object reference within the text object. Things like horizontal rulings, columns, and breaks also get object references - which allows us to keep all those elements in their correct order.
# :::
# 
# First, we need to capture data elements that are potentially relevant for more than one lemma, for instance line numbers. Those are stored in the dictionary `meta_d`, and subsequently retrieved for each lemma. Human legible line numbers are found in the field `label`. The field `field` is used primarily in lexical texts. For the field abbreviations and their meanings, see the [documentation](http://oracc.museum.upenn.edu/doc/help/editinginatf/lexicaltexts/index.html). The field label looks like `wp` (word or phrase), or `sg` (Sign) and is found under the JSON key `subtype` after a `field-start` entry. The field label is copied to the `meta_d` dictionary (under the key `field`), but this key is removed from `meta_d` as soon as the parser encounters a `field-end` value (with the `pop()` method). The great majority of lemmas have no field attribute - the key is "popped" so that it does not inadvertently get copied to all subsequent lemmas. Administrative text may have a `field` indicating that a word belongs to a year name (`yn`). This may be used, for instance, to remove yearnames in analyzing the vocabulary of the Ur III corpus.
# 
# When the parser encounters an `f` key, the contents of that key (the lemmatization of a word) are copied to `lemma` (a dictionary). To this dictionary several fileds are added: `id_word` (stored in the node `ref`), `label` (form `meta_d`) and `id_text` (also from `meta_d`).
# 
# Instead of an `f` key (which signals a word) the parser may also encounter a key `strict`. If `strict` has the value '1' (a string), this signals some kind of interruption in the text. That can be a break, a blank line, or a horizontal ruling. This is indicated in a restricted vocabulary (hence the node `strict`) in the nodes `extent`, `scope` and `state`, giving metatextual data about the condition of the object; they capture the number of broken lines or columns and similar information. This data is captured as if it were a lemma, and `id_word` and `id_text` are added.
# 
# The `parse_text_json()` returns a list of lemmas, but this list includes entries for broken passages, horizontal rulings, etc. Such information may be used to make sure that we do not create false neighbors - lemmas that seem to be adjacent, but that in fact are separated by a break or a ruling.
# 
# We can capture all these data elements with slight adjustments to the `json_text_parser()` and the code that calls that function. In the main process we create a dictionary `meta_d,` which will hold all the relevant meta data. Initially, it only contains the text ID. When the `parse_text_json()` function finds a dictionary that has the key `label` the key `label` in `meta_d` gets updated. When the process gets to the lemmatization data the `key` "label" in `meta_d` will hold the proper line label. The word ID is found in the key `ref` in the `l` node, and is added to the `lemma` dictionary. This same technique is used for all the other data elements that we sih to capture.
# 
# This version of the `parse_text_json()` function is also available in the module `utils`.
# 

# In[5]:


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


# ## 2.1.4.3 Call the `parsejson()` function for every `JSON` file
# The code in this cell will go through two nested loops - essentially the same as the code discussed in 2.1.3 (the basic parser). The main difference is the creation of a dictionary `meta_d` that is given as a second argument to `parse_text_json()`. Initially, this dictionary is empty. The value of the key `id_text` is updated in the main process every time a new JSON file is opened and sent to the `parse_text_json()` function. The `parse_text_json()` function itself will change values or add new keys, depending on the information found while iterating through the JSON file. When a new lemma row is created, `parse_text_json()` will supply data such as `id_text`, `label` and (potentially) other information from `meta_d`.

# In[6]:


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


# ## 2.1.4.4 Data Structuring: Pandas Dataframe
# The code in this section is essentially the same as the code for data structuring in 2.1.3 (basic parser).

# In[7]:


words_df = pd.DataFrame(lemm_l)
words_df = words_df.fillna('')   # replace NaN (Not a Number) with empty string
words_df


# Remove Spaces and Commas from Guide Word and Sense.

# In[8]:


findreplace = {' ' : '-', ',' : ''}
words_df = words_df.replace({'gw' : findreplace, 'sense' : findreplace}, regex=True)


# Create a lemma column. Compared to the code in 2.1.3, we now have rows that represent text breaks and the like. Those rows have no `form` and the `lemma` column should be empty.

# In[9]:


words_df["lemma"] = words_df["cf"] + '[' + words_df["gw"] + ']' + words_df["pos"]
words_df.loc[words_df["cf"] == "" , 'lemma'] = words_df['form'] + '[NA]NA'
words_df.loc[words_df["form"] == "", 'lemma'] = ""
words_df.loc[words_df["pos"] == "n", 'lemma'] = words_df['form'] + '[]NU'
words_df[['id_text', 'lemma', 'id_word', 'label']]


# ## 2.1.4.5 Create Line ID
# 
# In order to arrange the data in line-by-line format we need to create a line ID that will be added as a new field to each word in the DataFrame. The `id_word` captured by the extended parser has the format `ID_TEXT.ID_LINE.ID_WORD`, for instance `P338628.4.3`:  the third word of line 4 of [P338628](http://oracc.org/cams/gkab/P338628.4.3) (an astronomical fragment edited in [GKAB](http://oracc.org/cams/gkab)). Note that "4" in this case refers to the very first line of the fragment. The number "4" is not a traditional line number, but rather a reference number that is used to keep lines, breaks, rulings, etc. in their proper place. We can split the ID and keep only the middle part, using the `split()` function:
# 
# ```python
# ids = id_line.split(".")
# ```
# 
# The variable `ids` is now a list that holds the three elements; in our example above:
# 
# ```python
# ['P338628', '4', '1']
# ```
# 
# :::{margin}
# Python indexes start at 0, so that `ids[1]` refers to the second element of the list `ids`.
# 
# The second element (`ids[1]`) is the one we need (`'4'`). Note that this `'4'`is a string (between quotation marks), not a number. We need to change the data type into integer in order to arrange the lines properly (as string `'4'` comes between `'39'` and `'40'`). Putting all of this together we can create the proper `id_line` field with a list comprehension as follows:
# 
# ```python
# words['id_line'] = [int(wordid.split('.')[1]) for wordid in words['id_word']]
# ```
# 
# Rows that represent gaps in the text or horizontal drawings have an `id_word` in the format `ID_TEXT.ID_LINE` (consisting of only two elements), but are treated in exactly the same way. The `split()` function will result in a list of two elements, of which we need the second - and that is exactly what the code does.
# 
# :::{note}
# It would be more straightforward to derive `id_line` from the key `ref` in a `d` node in the `parse_text_json()`function:
# 
# ```json
# {
#                   "node": "d",
#                   "type": "line-start",
#                   "ref": "Q000376.26",
#                   "n": "26",
#                   "label": "26"
# }
# ```
# ```python
# 	if JSONobject.get("type") == "line-start":
# 		meta_d["id_line"] = JSONobject["ref"]
# 		meta_d["label"] = JSONobject["label"]
# ```
# 
# Although this works for most of the JSON files, not all `d` nodes of type `line-start` include the key `ref` and therefore the route through `id_word` is safer.

# In[10]:


words_df['id_line'] = [int(wordid.split('.')[1]) for wordid in words_df['id_word']]


# ## 2.1.4.6 Group by Line
# In the `words_df` dataframe each word has a separate row. In order to change this into a line-by-line representation we use the `pandas` `groupby()` function, using `id_text`, `id_line` and `label` fields as the sorting arguments. 
# 
# The fields that are aggregated are `lemma`, `extent`, `scope`, and `state`. The fields `extent`, `scope`, and `state` represent data on the number of broken lines. For instance, the notation `4 lines missing` in the [ORACC](http://oracc.org) edition will result in `extent = "4"`, `scope = "line"`, `state = "missing"` (note that the value of `extent` is a string and will be `"n"` if the number of missing lines or columns is unknown).
# 
# If your data does not have the fields `extent`, `scope`, and `state` the code below will fail - simply delete the lines that reference those fields.

# In[11]:


lines = words_df.groupby([words_df['id_text'], words_df['id_line'], words_df['label']]).agg({
        'lemma': ' '.join,
        'extent': ''.join, 
        'scope': ''.join,
        'state': ''.join
    }).reset_index()
lines


# ## 2.1.4.7 Alternative: Texts in Normalized Transcription
# This code (which is useful mostly for Akkadian texts) will produce a text in normalized transcription, essentially following the pattern of the preceding. Before grouping words into documents, we need to take care of words that have not been normalized (for instance because of breakage), using the field `form`. The new field `norm1` now has the normalized form of the word if it is available; if not it has the raw transliteration (without flags or breakage information).
# 
# :::{note}
# For Sumerian texts this method will reproduce the transliteration of the text, without the flags that indicate breakage or questionable readings.
# :::
# 
# :::{note}
# The data formattings demonstrated here are just examples of what one can do with the data extracted from the [ORACC](http://oracc.org) JSON files. The `parse_text_json()`function may be adapted to capture still other data types (such as sentence boundaries, or information on the sign level) and the `pandas` dataframe can be manipulated in innumerable ways.
# :::

# In[12]:


words_df["norm1"] = words_df["norm"]
words_df.loc[words_df["norm1"] == "" , 'norm1'] = words_df['form']


# In[13]:


texts_norm = words_df.groupby([words_df['id_text']]).agg({
        'norm1': ' '.join,
    }).reset_index()
texts_norm


# ## 2.1.4.8 Save Normalized Transcriptions
# The `texts_norm` DataFrame has one complete document in normalized transcription in each row. The code below saves each row as a separate `.txt` file, named after the document's ID.

# In[14]:


for idx, Q in enumerate(texts_norm["id_text"]):
    savefile =  f'{Q[-7:]}.txt'
    with open(f'output/{savefile}', 'w', encoding="utf-8") as w:
        texts_norm.iloc[idx].to_csv(w, index = False, header=False)


# ## 2.1.4.9 Other ORACC JSON files
# 
# The [Open Data/JSON](http://oracc.org/doc/opendata/json/index.html) page in [ORACC](http://oracc.org) explains in some detail the various other types of JSON files that are available. This section will briefly point out a few files that may be of use and that can be parsed with the techniques discussed above.
# 
# ### 2.1.4.9.1 metadata.json
# 
# The file `metadata.json` provides information about composite texts (which witnesses belong to which composite text) and about formats: `atf` (available in transliteration), `lem` (files with lemmatization) and `tr-en` (files with English translation). In projects that work with other translation languages one may find `tr-de` (for German), `tr-hun` (for Hungarian), etc. The file `metadata.json` may be useful, for instance, if you intent to parse all the files of a project that have lemmatization, but ignore those that do not. One may pull out the list `formats["lem"]` to get all the relevant text IDs.
# 
# ### 2.1.4.9.2 Indexes and Glossary
# 
# The Index and Glossary JSON files reproduce the indexes used by [ORACC Search](http://oracc.org/doc/search/searchingcorpora/index.html) and the project glossaries in JSON format. Indexes and glossaries may be used, among other things, to create searches beyond the scope of a line (for instance: search for `lugal` and `dalla` in the same text), a feature that is not currently available in standard [ORACC](http://oracc.org) search. How to build such a search engine is a topic not discussed in this study.

# In[ ]:




