#!/usr/bin/env python
# coding: utf-8

# # Download ORACC JSON Files
# This script downloads open data from the Open Richly Annotated Cuneiform Corpus ([ORACC](http://oracc.org)) in `json` format. The JSON files are made available in a ZIP file. For a description of the various JSON files included in the ZIP see the [open data](http://oracc.org/doc/opendata) page on [ORACC](http://oracc.org). 
# 
# The code in this notebook is also available in the module `utils` in the directory `utils` and can be called as follows: 
# ```python
# import os
# import sys
# util_dir = os.path.abspath('../utils') # When necessary, adapt the path to the utils directory.
# sys.path.append(util_dir)
# import utils
# directories = ["jsonzip"]
# os.makedirs("jsonzip", exist_ok = True)
# projects = ["dcclt", "saao/saa01"] # or any list of ORACC projects
# utils.oracc_download(projects)
# ```

# # 0. Import Packages

# In[5]:


import requests
from tqdm.notebook import tqdm
import os


# # 1. Create Download Directory
# Create a directory called `jsonzip`. If the directory already exists, do nothing.

# In[6]:


os.makedirs("jsonzip", exist_ok = True)


# # 2.1 Input a List of Project Abbreviations
# Enter one or more project abbreviations to download their JSON zip files. The project names are separated by commas. Note that the subprojects must be given explicitly, they are not automatically included in the main project. For instance: 
# * saao/saa01, aemw/alalakh/idrimi, rimanum

# In[7]:


projects = input('Project(s): ').lower().strip() # lowercase user input and strip accidental spaces


# # 2.2 Split the List of Projects
# Split the list of projects and create a list of project names.

# In[8]:


project_list = projects.split(',')   # split at each comma and make a list called `p`
project_list = [project.strip() for project in project_list]        # strip spaces left and right of each entry


# ## Download the ZIP files
# For each project from which files are to be processed download the entire project (all the json files) from `http://oracc.museum.upenn.edu/PROJECT/json/`. The file is called `PROJECT.zip` (for instance: `dcclt.zip`). For subprojects the file is called `PROJECT-SUBPROJECT.zip` (for instance `cams-gkab.zip`). 
# 
# For larger projects (such as [DCCLT](http://oracc.org/dcclt)) the `zip` file may be 25Mb or more. Downloading may take some time and it may be necessary to chunk the downloading process. The `iter_content()` function in the `requests` library takes care of that.
# 
# This code is also available as the function `oracc_download()` in the module `utils/utils.py`, which is used by some of the other scripts in Compass. The function `oracc_download()` takes a list of projects as its only argument (e.g. `['dcclt', 'hbtin', 'saao/saa01']` and will download those, omitting duplicates and invalid project names.
# 
# [ORACC](http://oracc.org) JSON files may be downloaded from three different servers: the build server at Penn, the public [ORACC](http://oracc.org) server and the server at [LMU](http://oracc.ub.uni-muenchen.de/) (Munich). The current code will only check the build server and may therefore not work with projects maintained at [LMU](http://oracc.ub.uni-muenchen.de/). The `oracc_download()` function in `utils` will check all three servers, in the order build, penn, lmu.
# 
# In order to show a progress bar (with `tqdm`) we need to know how large the file to be downloaded is (this value is is then fed to the `total` parameter). The http protocol provides a key `content-length` in the headers (a dictionary). Not all servers provide this field, therefore it is accessed with the `get()` function, which allows for a fall-back value in case a key is not found. This fall-back value is 0. With the `total` value of 0 `tqdm` will show a bar and will count the number of chunks received, but it will not indicate the degree of progress.

# In[9]:


CHUNK = 1024
for project in project_list:
    proj = project.replace('/', '-')
    url = f"http://build-oracc.museum.upenn.edu/json/{proj}.zip"
    file = f'jsonzip/{proj}.zip'
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            total_size = int(r.headers.get('content-length', 0))
            tqdm.write(f'Saving {url} as {file}')
            t=tqdm(total=total_size, unit='B', unit_scale=True, desc = project)
            with open(file, 'wb') as f:
                for c in r.iter_content(chunk_size=CHUNK):
                    t.update(len(c))
                    f.write(c)
        else:
            tqdm.write(f"WARNING: {url} does not exist.")


# In[ ]:




