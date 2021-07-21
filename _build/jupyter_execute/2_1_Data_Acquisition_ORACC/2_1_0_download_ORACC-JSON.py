#!/usr/bin/env python
# coding: utf-8

# # 2.1.0 Download ORACC JSON Files
# 
# Each public [ORACC](http://oracc.org) project has a `zip` file that contains a collection of JSON files, which provide data on lemmatizations, transliterations, catalog data, indexes, etc. The `zip` file can be found at `http://oracc.museum.upenn.edu/[PROJECT]/json/[PROJECT].zip`, where `[PROJECT]` is to be replaced with the project abbreviation. For sub-projects the address is `http://oracc.museum.upenn.edu/[PROECT]/[SUBPROJECT]/json/[PROJECT]-[SUBPROJECT].zip`
# 
# :::{note}
# For instance http://oracc.museum.upenn.edu/etcsri/json/etcsri.zip or, for a subproject http://oracc.museum.upenn.edu/cams/gkab/json/cams-gkab.zip.
# ::: 
# 
# One may download these files by hand (simply type the address in your browser), or use the code in the current notebook. The notebook will create a directory `jsonzip` and copy the file to that directory - all further scripts will expect the `zip` files to reside in `jsonzip`. 
# 
# :::{note}
# One may also use the function `oracc_download()` in the `utils` module. See below for instructions how to use the functions of the `utils` module.
# :::
# 
# ```{figure} ../images/mocci_banner.jpg
# :scale: 50%
# :figclass: margin
# ```
# 
# Some [ORACC](http://oracc.org) projects are maintained in Munich by the Munich Open-access Cuneiform Corpus Initiative ([MOCCI](https://www.en.ag.geschichte.uni-muenchen.de/research/mocci/index.html)). This includes, for example, State Archives of Assyria ([SAAO](http://oracc.org/saao)), the Royal Inscriptions of the Neo-Assyrian Period ([RINAP](http://oracc.org/rinap)) and various other projects and sub-projects. In theory, project data are copied from the Munich server to the Philadelphia ORACC server (and v.v.), but in order to acquire the most recent data set it is sometimes advisable to request the `zip` files directly from the Munich server. The address is `http://oracc.ub.uni-muenchen.de/[PROJECT]/[SUBPROJECT]/json/[PROJECT]-[SUBPROJECT].zip`. 
# 
# :::{note}
# The function `oracc_download()` in the `utils` module will try the various servers to find the project(s) of your choice.
# :::
# 
# After downloading the JSON `zip` file you may unzip it to inspect its contents. Note, however, that for larger projects this may result in hundreds or even thousands of files and that the scripts will always read the data directly from the `zip` file.

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

# ## 2.1.0.0. Import Packages

# In[1]:


import requests
from tqdm.auto import tqdm
import os
import ipywidgets as widgets


# ## 2.1.0.1. Create Download Directory
# Create a directory called `jsonzip`. If the directory already exists, do nothing.

# In[2]:


os.makedirs("jsonzip", exist_ok = True)


# ## 2.1.0.2 Input a List of Project Abbreviations
# Enter one or more project abbreviations to download their JSON zip files. The project names are separated by commas. Note that subprojects must be given explicitly, they are not automatically included in the main project. For instance: 
# * saao/saa01, aemw/alalakh/idrimi, rimanum

# In[6]:


projects = widgets.Textarea(
    placeholder='Type project names, separated by commas',
    description='Projects:',
)
projects


# 
# ## 2.1.0.3 Split the List of Projects
# Split the list of projects and create a list of project names.

# In[4]:


project_list = projects.value.lower().split(',')   # split at each comma and make a list called `project_list`
project_list = [project.strip() for project in project_list]  # strip spaces left and right of each entry


# ## 2.1.0.4 Download the ZIP files
# For each project from which files are to be processed download the entire project (all the json files) from `http://oracc.museum.upenn.edu/PROJECT/json/`. The file is called `PROJECT.zip` (for instance: `dcclt.zip`). For subprojects the file is called `PROJECT-SUBPROJECT.zip` (for instance `cams-gkab.zip`). 
# 
# For larger projects (such as [DCCLT](http://oracc.org/dcclt)) the `zip` file may be 25Mb or more. Downloading may take some time and it may be necessary to chunk the downloading process. The `iter_content()` function in the `requests` library takes care of that.
# 
# This code is also available as the function `oracc_download()` in the module `utils/utils.py`, which is used by some of the other scripts in Compass. The function `oracc_download()` takes a list of projects as its only argument (e.g. `['dcclt', 'hbtin', 'saao/saa01']` and will download those, omitting duplicates and invalid project names.
# 
# [ORACC](http://oracc.org) JSON files may be downloaded from three different servers: the build server at Penn, the public [ORACC](http://oracc.org) server and the server at [LMU](http://oracc.ub.uni-muenchen.de/) (Munich). The current code will only check the build server and may therefore not work with projects maintained at [LMU](http://oracc.ub.uni-muenchen.de/). The `oracc_download()` function in `utils` will check all three servers, in the order build, penn, lmu.
# 
# In order to show a progress bar (with `tqdm`) we need to know how large the file to be downloaded is (this value is is then fed to the `total` parameter). The http protocol provides a key `content-length` in the headers (a dictionary). Not all servers provide this field, therefore it is accessed with the `get()` function, which allows for a fall-back value in case a key is not found. This fall-back value is 0. With the `total` value of 0 `tqdm` will show a bar and will count the number of chunks received, but it will not indicate the degree of progress.

# In[5]:


CHUNK = 1024
for project in project_list:
    proj = project.replace('/', '-')
    url = f"http://oracc.museum.upenn.edu/json/{proj}.zip"
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




