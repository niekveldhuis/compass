#!/usr/bin/env python
# coding: utf-8

# # Data Acquisition from CDLI
# The downloadable [CDLI](http://cdli.ucla.edu) files are found on the download page http://cdli.ucla.edu/bulk_data. The data available are a set of transliterations and a catalog file with meta-data. Because of its size the catalog file is currently split in two, it is possible that in the future there will be either more or fewer such files. The script identifies the file names and downloads those to a directory `cdlidata`. Once downloaded the catalog is reconstituted as a single file and is loaded into a `pandas` DataFrame. The DataFrame is used, by way of example, to select the transliterations from the Early Dynastic IIIa period.
# 

# # 0 Import Packages

# In[ ]:


import requests
from tqdm.auto import tqdm
import pandas as pd
import csv
from bs4 import BeautifulSoup
import os
import sys
import shutil


# # 1. Create Download Directory
# Create a directory called `cdlidata`. If the directory already exists, do nothing. 

# In[ ]:


os.makedirs('cdlidata', exist_ok = True)


# # 2. Retrieve File Names
# We first need to retrieve the names of the files that are offered for download on the CDLI [download](https://github.com/cdli-gh/data) page on GitHub. The script requests the HTML of the download page and uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (a package for web scraping) to retrieve all the links from the page. This includes the file names, but also all kinds of other links.

# In[ ]:


download_page = "https://github.com/cdli-gh/data"
r = requests.get(download_page)
html = r.text
soup = BeautifulSoup(html)
links = soup.find_all('a')       # retrieve all html anchors, which define links
files = set()
for link in links:
    f = link.get('href')        # from the anchors, retrieve the URLs
    files.add(f)
files = {f for f in files if 'master/cdli' in f}  # filter out the relevant URLs
files = {f.split('/')[-1] for f in files} # only keep the file names (without the path)
files


# # 3. Download
# The download code in this cell is essentially identical with the code in notebook 2_1_0_download_ORACC-JSON.ipynb. Depending on the speed of your computer and internet connection the downloading process can take some time because of the size of the files.

# In[ ]:


CHUNK = 1024
for file in files:
    url = f"https://raw.github.com/cdli-gh/data/master/{file}"
    target = f'cdlidata/{file}'
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            total_size = int(r.headers.get('content-length', 0))
            tqdm.write(f'Saving {url} as cdlidata/{file}')
            t=tqdm(total=total_size, unit='B', unit_scale=True, desc = file)
            with open(target, 'wb') as f:
                for c in r.iter_content(chunk_size=CHUNK):
                    t.update(len(c))
                    f.write(c)
        else:
            print(f"{url} does not exist.")


# # 4. Concatenate the Catalogue Files
# The catalogue files are concatenated, using a utility from the `shutil` package. The new, concatenated, file is called `catalogue.csv`.

# In[ ]:


filenames = [f for f in files if "cdli_catalogue" in f]
filenames.sort()  # to make sure we read cdli_catalogue_1of2.csv first.
with open('cdlidata/catalogue.csv','wb') as concatenated_file:
    for file in filenames:
        with open(f'cdlidata/{file}','rb') as one_file:
            shutil.copyfileobj(one_file, concatenated_file)


# # 5 Load in Pandas DataFrame

# In[ ]:


cat = pd.read_csv('cdlidata/catalogue.csv', engine='python', error_bad_lines=False).fillna('')
cat


# # 6 Use Catalog to Select Transliterations
# In the example code in the following cell the catalog is used to select from the transliteration file all texts from the Early Dynastic IIIa period. The field "period" is used to select those catalog entries that have "ED IIIa" in that field. P numbers are stored in the catalog as integers without the initial 'P' and without leading zeros (that is '1183' corresponds to 'P001183'). The function `zfill()` is used to created a 6-digit number with leading zeros, if necessary. The P-numbers of our catalog selection are stored in the variable `pnos` (but note that the numbers do not have the initial 'P'!).
# 
# The code then iterates through the list of lines. The flag `keep` (which initially is set to `FALSE`) is set to `TRUE` if the code encounters a P number that is present in the list `pnos`. As long as `keep = TRUE` subsequent lines are added to the list `ed3a_atf`. When the script encounters a P-number that is not in `pnos`, the flag `keep` is set to `FALSE`.
# 
# The result is a list lines with all the transliteration data of the Early Dynastic IIIa texts in [CDLI](http://cdli.ucla.edu).

# In[ ]:


ed3a = cat.loc[cat["period"].str[:7] == "ED IIIa"]
pnos = list(ed3a["id_text"])
pnos = ["P" + str(no).zfill(6) for no in pnos]
with open("cdlidata/cdliatf_unblocked.atf", encoding="utf8") as c: 
    lines = c.readlines()
keep = False
ed3a_atf = []
for line in tqdm(lines):
    if line[0] == "&": 
        if line[1:8] in pnos: 
            keep = True
        else: 
            keep = False
    if keep: 
        ed3a_atf.append(line)


# # 7 Place in DataFrame
# Place the ED IIIa texts in a DataFrame, where each row represents one document (line numbers are omitted). This is, of course, just one example of how the data may be selected and formatted.
# 
# The lines are read in reverse order, so that when the script encounters an '&P' line (as in '&P212416 = AAICAB 1/1, pl. 008, 19282-439'), this signals that all the lines of a text have been read and that the document can be added to the list `docs`. (When reading the lines in regular order - taking the '&P' line as signaling the end of the previous document - one needs to separately save the last document, because there is no '&P' line anymore to indicate that the text is complete).

# In[ ]:


docs = []
document = ''
id_text = ''
ed3a_atf = [line for line in ed3a_atf if line.strip()]  # remove empty lines, which cause trouble
for line in tqdm(reversed(ed3a_atf)):
    if line[0] == "&":  # line beginning with & marks the beginning of a document
        id_text = line[1:8] # retrieve the P number
        docs.append([id_text, document])
        document = ''   # after appending the data to docs, reset d for a new document.
        continue
    elif line [0] in ["#", "$", "<", ">", "@"]:  # skip all non-transliteration lines
        continue
    else:
        try:
            line = line.split(' ', 1)[1].strip() # split line at first space (after the line number)
            document = f'{line} {document}' # add the new line in front
        except:
            continue   # malformed lines (no proper separation between line number and text) are skipped
ed3a_df = pd.DataFrame(docs)
ed3a_df.columns = ["id_text", "transliteration"]


# In[ ]:


ed3a_df


# In[ ]:




