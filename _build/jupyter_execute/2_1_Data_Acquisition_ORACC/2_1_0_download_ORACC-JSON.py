#!/usr/bin/env python
# coding: utf-8

# (2.1.0)=
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
# One may also use the function `oracc_download()` in the `utils` module. See below ([2.1.0.5](2.1.0.5)) for instructions on how to use the `utils` module.
# :::
# 
# ```{figure} ../images/mocci_banner.jpg
# :scale: 50%
# :figclass: margin
# ```
# 
# Some [ORACC](http://oracc.org) projects are maintained by the Munich Open-access Cuneiform Corpus Initiative ([MOCCI](https://www.en.ag.geschichte.uni-muenchen.de/research/mocci/index.html)). This includes, for example, Official Inscriptions of the Middle East in Antiquity ([OIMEA](http://oracc.org/oimea)) and, Archival Texts of the Middle East in Antiquity ([ATMEA](http://oracc.org/atmea)) and various other projects and sub-projects. In theory, project data are copied from the Munich server to the Philadelphia ORACC server (and v.v.), but in order to get the most recent data set it is sometimes advisable to request the `zip` files directly from the Munich server. The address is `http://oracc.ub.uni-muenchen.de/[PROJECT]/[SUBPROJECT]/json/[PROJECT]-[SUBPROJECT].zip`. 
# 
# :::{note}
# The function `oracc_download()` in the `utils` module will try the various servers to find the project(s) of your choice.
# :::
# 
# After downloading the JSON `zip` file you may unzip it to inspect its contents but there is no necessity to do so. For larger projects unzipping may result in hundreds or even thousands of files; the scripts will always read the data directly from the `zip` file.

# ## 2.1.0.0. Import Packages
# 
# * requests: for communicating with a server over the internet
# * tqdm: for creating progress bars
# * os: for basic Operating System operations (such as creating a directory)
# * ipywidgets: for user interface (input project names to be downloaded)

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

# In[3]:


projects = widgets.Textarea(
    placeholder='Type project names, separated by commas',
    description='Projects:',
)
projects


# 
# ## 2.1.0.3 Split the List of Projects
# Lower case the list of projects and split it to create a list of project names.

# In[4]:


project_list = projects.value.lower().split(',')   # split at each comma and make a list called `project_list`
project_list = [project.strip() for project in project_list]  # strip spaces left and right of each entry


# ## 2.1.0.4 Download the ZIP files
# 
# For larger projects (such as [DCCLT](http://oracc.org/dcclt)) the `zip` file may be 25Mb or more. Downloading may take some time and it may be necessary to chunk the downloading process. The `iter_content()` function in the `requests` library takes care of that.
# 
# In order to show a progress bar (with `tqdm`) we need to know how large the file to be downloaded is (this value is is then fed to the `total` parameter). The http protocol provides a key `content-length` in the headers (a dictionary) that indicates file length. Not all servers provide this field - if `content-length` is not avalaible it is set to 0. With the `total` value of 0 `tqdm` will show a bar and will count the number of chunks received, but it will not indicate the degree of progress.

# In[5]:


CHUNK = 1024
for project in project_list:
    proj = project.replace('/', '-')
    url = f"http://oracc.museum.upenn.edu/json/{proj}.zip"
    file = f'jsonzip/{proj}.zip'
    with requests.get(url, stream=True) as request:
        if request.status_code == 200:   # meaning that the file exists
            total_size = int(request.headers.get('content-length', 0))
            tqdm.write(f'Saving {url} as {file}')
            t=tqdm(total=total_size, unit='B', unit_scale=True, desc = project)
            with open(file, 'wb') as f:
                for c in request.iter_content(chunk_size=CHUNK):
                    t.update(len(c))
                    f.write(c)
        else:
            tqdm.write(f"WARNING: {url} does not exist.")


# (2.1.0.5)=
# ## 2.1.0.5 Downloading with the utils Module
# In the chapters 3-6, downloading of [ORACC](http://oracc.org) data will be done with the `oracc_download()` function in the module `utils` that can be found in the `utils` directory. The following code illustrates how to use that function. 
# 
# The function `oracc_download()` takes a list of project names as its first argument. Replace the line
# ```python
# projects = ["dcclt", "saao/saa01"]
# ```
# with the list of projects (and sub-projects) of your choice. 
# 
# The second (optional) argument is `server`; possible values are "penn" (default; try the Penn server first) and "lmu" (try the Munich server first). The `oracc_download()` function returns a cleaned list of projects with duplicates and non-existing projects removed.

# In[6]:


import os
import sys
util_dir = os.path.abspath('../utils') # When necessary, adapt the path to the utils directory.
sys.path.append(util_dir)
import utils
directories = ["jsonzip"]
os.makedirs("jsonzip", exist_ok = True)
projects = ["dcclt", "saao/saa01"] # or any list of ORACC projects
utils.oracc_download(projects, server="penn")


# In[ ]:





# In[ ]:




