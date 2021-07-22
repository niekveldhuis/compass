#!/usr/bin/env python
# coding: utf-8

# # 2.1.2 Retrieve ORACC Catalog Data
# 
# Each [ORACC](http://oracc.org) JSON `zip` file includes a file named `catalogue.json`. Since the structure of `catalogue.json` is simple and there is relatively little depth in its hierarchy, it can be parsed in just a few lines.
# 
# :::{margin}
# For general information, see the [Oracc Open Data](http://oracc.org/doc/opendata) page.
# :::
# 
# The file `catalogue.json` contains all the catalog data for an [ORACC](http://oracc.org) project. We will transform the JSON into a `pandas` dataframe.

# ## 2.1.2.0 Load Packages
# * pandas: data analysis and manipulation; dataframes
# * ipywidgets: user interface (enter project names)
# * zipfile: read data from a ziped file
# * json: read a json object
# * os: basic Operating System tasks (such as creating a dictionary)
# * sys: change system parameters
# * utils: compass-specific utilities (download files from ORACC, etc.)

# In[1]:


import pandas as pd
import ipywidgets as widgets
import zipfile
import json
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils


# ## 2.1.2.1 Create Directories, if Necessary
# The two directories needed for this script are `jsonzip` and `output`. 

# In[2]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# ## 2.1.2.2 Input Project Names
# We can download and manipulate multiple [ORACC](http://oracc.org) `zip` files at the same time. Note, however that different [ORACC](http://oracc.org) projects use different fields in their catalogs; not all catalogs are mutually compatible.
# 
# Provide project abbreviations, separated by a comma. Note that subprojects must be processed separately, they are not included in the main project. A subproject is named `[PROJECT]/[SUBPROJECT]`, for instance `saao/saa01`.

# In[3]:


projects = widgets.Textarea(
    value="obmc",
    placeholder='Type project names, separated by commas',
    description='Projects:',
)
projects


# ## 2.1.2.3 Split the List of Projects and Download the ZIP files.
# Use the `format_project_list()` and `oracc_download()` functions from the `utils` module to download the requested projects. The code of these function is discussed in more detail in 2.1.0. Download ORACC JSON Files. The function returns a new version of the project list, with duplicates and non-existing projects removed.

# In[4]:


project_list = utils.format_project_list(projects.value)
project_list = utils.oracc_download(project_list)


# ## 2.1.2.4 Extract Catalogue Data from `JSON` files
# The process begins by turning a `zip` file (for instance `obmc.zip`) into a `zipfile` object that may be manipulated with the functions available in the `zipfile` library. This is done with the `zipfile.Zipfile()` function:
# 
# ```python
# import zipfile
# file = "jsonzip/obmc.zip"    
# # or: file = "jsonzip/dcclt-nineveh.zip"
# zipfile_object = zipfile.ZipFile(file)
# ```
# 
# The `read()` function from that same `zipfile` package reads one particular file from the `zip` and turns it into a string:
# 
# ```python
# string_object = zipfile_object.read("obmc/catalogue.json").decode("utf-8") 
# # or: string_object = zipfile_object.read("dcclt/nineveh/catalogue.json").decode("utf-8")
# ```
# 
# The `json` library provides functions for reading (loading) or producing (dumping) a JSON file. Reading is done with the function `load()`, which comes in two versions. Regular `json.load()` takes a filename as argument and will load a JSON file. In this case, however, the `read()` function from the `zipfile` library has produced a string (extracted from `obmc.zip`), and therefore we need the command `json.loads()`, which takes a string as its argument:  
# 
# ```python
# import json
# json_object = json.loads(string_object)
# ```
# 
# The variable `json_object` will now contain all the data in the `catalogue.json` file from the [OBMC](http://oracc.org/obmc) (Old Babylonian Model Contracts) project by Gabriella Spada. We may treat the variable `json_object` as a Python dictionary. The `catalogue.json` has various keys, including `type`, `project`, `source`, `license`, `license-url`, `more-info`, `UTC-timestamp`, `members`, and `summaries`. The key `members` is the only one that concerns us here, since it contains the actual catalog information. The value of the key `members` is itself a dictionary of dictionaries. Each of the keys in the top-level dictionary is a P, Q, or X-number (a text ID). The value of each of these keys is still another dictionary; each key in that dictionary is a field in the original catalog (`primary_publication`, `provenience`, `genre`, etc.). The dictionary of dictionaries under the key `members` may be transformed into a Pandas DataFrame for ease of viewing and manipulation.
# 
# ``` python
# import pandas as pd	
# cat = json_object["members"]
# df = pd.DataFrame.from_dict(cat)
# df
# ```
# 
# By default, the `DataFrame.from_dict()` function in the `pandas` library takes each key as a column - in this case the keys of `cat` are the P numbers (text IDs); the catalog fields will become rows. To address that issue, we need to tell the `DataFrame.from_dict()` function explicitly that each key should be a row (`orient="index"`) 
# 
# ```python
# df = pd.DataFrame.from_dict(cat, orient="index")
# df
# ```

# We can put the code discussed above in a loop that will iterate through the list of projects entered above (2.1.2.2). For each project the `JSON` zip file, named `[PROJECT].zip` has been downloaded in the directory `jsonzip`. 
# 
# In the last step of the loop, the individual dataframes (one for each project requested) are concatenated. Since individual [ORACC](http://oracc.org) project catalogs may have different fields, the dataframes may have different column names. By default `pandas` concatenation uses an `outer join` so that all column names of all the catalogs are preserved.

# In[5]:


df = pd.DataFrame() # create an empty dataframe
for project in project_list:
    file = f"jsonzip/{project.replace('/', '-')}.zip"
    try:
        zip_file = zipfile.ZipFile(file)       # create a Zipfile object
    except:
        errors = sys.exc_info() # get error information
        print(file), print(errors[0]), print(errors[1]) # and print it
        continue
    try:
        json_cat_string = zip_file.read(f"{project}/catalogue.json").decode('utf-8')  #read and decode the catalogue.json file of one project
                                                                # the result is a string object
    except:
        errors = sys.exc_info() # get error information
        print(project), print(errors[0]), print(errors[1]) # and print it
        continue
    zip_file.close()
    cat = json.loads(json_cat_string)
    cat = cat['members']  # select the 'members' node 
    cat_df = pd.DataFrame.from_dict(cat, orient="index")
    cat_df["project"] = project  # add project name as separate field
    df = pd.concat([df, cat_df], sort=True)  # sort=True is necessary in case catalogs have a different set of fields
df


# ## 2.1.2.5 Clean the Dataframe
# The function `fillna('')` will put a blank (instead of `NaN`) in all fields that have no entry.

# In[6]:


df = df.fillna('')
df


# ## 2.1.2.6 Select Relevant Fields
# :::{margin}
# Various introductions to Pandas may be found on the web or in [VanderPlas 2016](https://github.com/jakevdp/PythonDataScienceHandbook) and similar overviews.
# :::
# 
# The Pandas library allows one to manipulate and slice a dataframe in many different ways. For instance, one may select the relevant fields by creating a new dataframe. [ORACC](http://oracc.org) catalogs may have custom fields, the only fields that are obligatory are `id_text` (the P, Q, or X number that identifies the text, for instance "P243546") and `designation` (the human-readable reference, for instance "VS 17, 012"). The example code below works with field names that are available in (almost) every catalog. Adjust the code to your data and your needs.

# In[7]:


df1 = df[['designation', 'period', 'provenience',
        'museum_no', 'project', 'id_text']]
df1


# ## 2.1.2.7 Save as CSV
# Save the resulting data set as a `csv` file. `UTF-8` encoding is the encoding with the widest support in text analysis and the standard encoding in Python. It is also  the encoding used by [ORACC](http://oracc.org)). 
# 
# :::{note}
# If you intend to use the catalog file in Excel, it is better to use `utf-16` encoding.
# :::

# In[8]:


filename = 'output/catalog.csv'
df1.to_csv(filename, index=False, encoding='utf-8')


# ## 2.1.2.7 Save with Pickle
# One may pickle a file either with the `pickle` library or directly from within `pandas` library with the `to_pickle()` function. A pickled file preserves the data structure of the dataframe, which is an advantage over saving as `csv`. The pickle file is a binary file, so we must open the file with the `wb` (write binary) option and we cannot give an encoding. 
# 
# :::{note}
# To open the pickled file again:
# ```python
# import pandas as pd
# df = pd.read_pickle(o)
# ```
# :::

# In[9]:


filename = "output/catalog.p"
df1.to_pickle(filename)


# In[ ]:




