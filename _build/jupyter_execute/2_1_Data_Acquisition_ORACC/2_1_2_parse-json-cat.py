#!/usr/bin/env python
# coding: utf-8

# # Retrieve Catalog Data from `catalogue.json`
# 
# The file `catalogue.json` contains all the catalog data for an [ORACC](http://oracc.org) project (for general information, see the [Oracc Open Data](http://oracc.org/doc/opendata) page). The `zip` that contains all JSON files of a particular project can be found at `http://oracc.museum.upenn.edu/[PROJECT]/json/[PROJECT].zip`. In the URL replace [PROJECT] with your project name (e.g. `dcclt`). For sub-projects the URL pattern is `http://oracc.museum.upenn.edu/[PROJECT]/[SUBPROJECT]/json/[PROJECT]-[SUBPROJECT].zip`. 
# 
# The main key in a `catalogue.json` file is called `members`. The value of this key contains the information of all the fields and all the entries in the project catalog. This information is put in a `pandas` DataFrame.

# In[ ]:


import pandas as pd
import zipfile
import json
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils


# ## 0 Create Directories, if Necessary
# The two directories needed for this script are `jsonzip` and `output`. 

# In[ ]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# ## 1.1 Input Project Names
# We can download and manipulate multiple [ORACC](http://oracc.org) `zip` files at the same time. Note, however that different [ORACC](http://oracc.org) projects use different fields in their catalogs; not all catalogs are mutually compatible.
# 
# Provide project abbreviations, separated by a comma. Note that subprojects must be processed separately, they are not included in the main project. A subproject is named `[PROJECT]/[SUBPROJECT]`, for instance `saao/saa01`.
# 
# Split the list of projects and create a list of project names, using the `format_project_list()` function from the `utils` module.

# In[ ]:


projects = input('Project(s): ').lower().strip() # lowercase user input and strip accidental spaces
project_list = utils.format_project_list(projects)


# ## 1.2 Split the List of Projects and Download the ZIP files.
# Use the `oracc_download()` function from the `utils` module to download the requested projects. The code of this function is discussed in more detail in 2.1.0. Download ORACC JSON Files. The function returns a new version of the project list, with duplicates and non-existing projects removed.

# In[ ]:


project_list = utils.oracc_download(project_list)


# ## 2 Extract Catalogue Data from `JSON` files
# The code in this cell will iterate through the list of projects entered above (1.1). For each project the `JSON` zip file, named `[PROJECT].zip` has been downloaded in the directory `jsonzip` (1.2). Each of these `zip` files includes a file called `catalogue.json`. This file is read in and loaded with the command `json.loads()`, which transforms a string into a JSON object - a sequence of names and values.
# 
# The JSON object is transformed into a `pandas` Dataframe. By default, when reading in a dictionary, the `DataFrame()` function will take the top-level keys (in this case the text IDs) as columns. The dataframe needs to be transposed (`.T`), so that the P, Q, and X numbers become indexes or row names, and each column represents a field in the catalog.  The individual dataframes (one for each project requested) are concatenated. Since individual [ORACC](http://oracc.org) project catalogs may have different fields, the dataframes may have different column names. By default `pandas` concatenation uses an `outer join` so that all column names of all the catalogs are preserved.

# In[ ]:


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
    for item in cat.values():
        item["project"] = project # add project name as separate field
    cat_df = pd.DataFrame.from_dict(cat, orient="index")
    df = pd.concat([df, cat_df], sort=True)  # sort=True is necessary in case catalogs have a different set of fields
df


# ## 3. Clean the Dataframe
# The function `fillna('')` will put a blank (instead of `NaN`) in all fields that have no entry.

# In[ ]:


df = df.fillna('')
df


# ## 4 Select Relevant Fields
# [ORACC](http://oracc.org) catalogs may have custom fields, the only fields that are obligatory are `id_text` (the P, Q, or X number that identifies the text, for instance "P243546") and `designation` (the human-readable reference, for instance "VS 17, 012"). The example code below works with field names that are available in (almost) every catalog. Adjust the code to your data and your needs.

# In[ ]:


df1 = df[['designation', 'period', 'provenience',
        'museum_no', 'project', 'id_text']]
df1


# ## 5.1 Save as CSV
# Save the resulting data set as a `csv` file. `UTF-8` encoding is the encoding with the widest support in text analysis (and also the encoding used by [ORACC](http://oracc.org)). If you intend to use the catalog file in Excel, however, it is better to use `utf-16` encoding.

# In[ ]:


filename = 'output/catalog.csv'
df1.to_csv(filename, index=False, encoding='utf-8')


# ## 5.2 Save with Pickle
# One may pickle a file either with the `pickle` library or directly from within `pandas` with the `to_pickle()` function. A pickled file preserves the data structure of the dataframe, which is an advantage over saving as `csv`. The pickle file is a binary file, so we must open the file with the `wb` (write binary) option and we cannot give an encoding. To open the pickled file one may use the `read_pickle()` function from the `pandas` library, as in:
# 
# ```python
# import pandas as pd
# df = pd.read_pickle(o)
# ```

# In[ ]:


filename = "output/catalog.p"
df1.to_pickle(filename)


# In[ ]:




