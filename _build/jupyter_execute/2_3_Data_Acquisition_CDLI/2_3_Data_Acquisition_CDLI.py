#!/usr/bin/env python
# coding: utf-8

# # 2.3 Data Acquisition from CDLI
# ## 2.3.1 Introduction: CDLI data
# 
# ```{figure} ../images/Robert+Englund.jpg
# :figclass: margin
# :scale: 25%
# 
# [Bob Englund](https://cdli.ucla.edu/?q=news/obituary-robert-k-englund) 1952-2020
# ```
# 
# The [Cuneiform Digital Library Initiative](http://cdli.ucla.edu), created by [Bob Englund](https://cdli.ucla.edu/?q=robert-k-englund) (UCLA) in the early two thousands, is a central repository for meta-data, images, and transliterations of cuneiform objects (translations are offered only for a small minority of texts). Today more than 335,000 objects are listed in the [CDLI](http://cdli.ucla.edu) catalog, with tens of thousands of photographs and line drawings. Each object in [CDLI](http://cdli.ucla.edu) receives a unique ID number (the so-called P-number), and these numbers are widely used today in print and in on-line projects. Initially, [CDLI](http://cdli.ucla.edu) focused primarily on administrative texts from the third millennium, and this is still the area of its greatest strength. Currently, approximately 121,000 texts are available in transliteration in [CDLI](http://cdli.ucla.edu). Part of this corpus was produced by the [CDLI](http://cdli.ucla.edu) team at UCLA, others were contributed by partners or were imported from other projects such as [ETCSL](https://etcsl.orinst.ox.ac.uk/) (for Sumerian literary texts), [DCCLT](http://oracc.org/dcclt) (for lexical texts), or [BDTNS](http://bdtns.filol.csic.es/) (for Ur III administrative texts). The photographs on [CDLI](http://cdli.ucla.edu) were largely produced in cooperative projects with museums all over the world, where [CDLI](http://cdli.ucla.edu) staff or partners would go to scan an entire collection or major parts of a collection. These images are copyright of the museum where the object is held and there is no wholesale downloading of the entire image set.
# 
# ```{figure} ../images/cdli_logo.gif
# :figclass: margin
# :scale: 50%
# ```
# 
# The [CDLI](http://cdli.ucla.edu) project transformed the practice of Assyriology in multiple ways. The availability of large numbers of photographs made it possible to collate problematic passages in texts only published in transliteration and/or hand drawing. Issuing ID numbers made it easier to refer to a particular tablet unambiguously, while avoiding the confusion of obscure publication abbreviations and museum numbers. The spread of all this information on the web made it available to everyone with an internet connection.
# 
# For each cuneiform object the [CDLI](http://cdli.ucla.edu) catalog provides information about where it was published (and by whom), in which collection it is kept, where it was excavated, to which period it belongs, what textual genre it represents, etc. In addition, an object may be represented by one or more images (photographs and/or hand drawings) and by a transliteration. Several of the fields in the [CDLI](http://cdli.ucla.edu) catalog either use a restricted vocabulary (period, genre) or have been standardized (provenance, author's name, owner, museum number), greatly facilitating search. 
# 
# The issue of standardization is much more difficult for linguistic data in transliteration. Here, Sumerian and Akkadian pose rather different challenges. For Sumerian, there are two main issues. First, Sumerologists tend to use different sets of conventions for representing Sumerian words in the Latin alphabet. The word for "to give" is read [**šum₂**](http://oracc.org/epsd2/o0039914) by some, but **sum** by others. Similarly, the word for "ox" is read either [**gud**](http://oracc.org/epsd2/o0028670) or **gu₄**. These readings (**šum₂** vs **sum** or **gud** vs. **gu₄**) represent the same word and render the same cuneiform sign - they simply differ in modern transliteration conventions. Variation in such conventions has grown recently by the introduction of a new set of readings by P. Attinger (Bern), which has received wide following, in particular in Germany. Such variation in sign readings is based on the one hand on differing interpretations of the data from [ancient sign lists](http://oracc.org/dcclt/signlists) (which provide transcriptions of Sumerian words in Akkadian) and on the other hand on the definition of what an ideal transliteration should achieve (whether it should represent the abstract lexeme, or rather its concrete pronunciation, or something in between). For the [CDLI](http://cdli.ucla.edu) search engine, which is based on a FileMaker database, such variation presents a problem when searching for (Sumerian) words. The solution has been to strictly impose a set of [preferred sign readings](https://cdli.ucla.edu/methods/sign_reading.html), a policy that has been carried out with admirable consistency. 
# 
# :::{admonition} Attinger readings
# :class: tip, dropdown
# For the readings introduced by P. Attinger, see the introduction to his [Glossaire sumérien–français](https://www.harrassowitz-verlag.de/isbn_9783447116169.ahtml) (2021).
# :::
# 
# Second, Sumerologists today have no good standard for word segmentation. In the [CDLI](http://cdli.ucla.edu) data set one may find the word [**ninda-i₃-de₂-a**](http://oracc.org/epsd2/o0036259) (a pastry) transliterated as **ninda-i₃-de₂-a**, **ninda i₃-de₂-a**, **ninda i₃ de₂-a**, **nig₂-i₃-de₂-a**, **nig₂ i₃ de₂-a**, etcetera (**nig₂** and **ninda** are two different words, written by the same sign and there is no full agreement which of these is to be used in this particular expression). None of these various renderings is necessarily "wrong," because we know fairly little about the formation and segmentation of Sumerian nouns. For computational approaches this variation poses an important challenge.
# 
# For Akkadian the variation in reading conventions plays a much smaller role; for most dialects of Akkadian (with the exception of Old Akkadian) scholars generally agree on transliteration conventions; word segmentation is hardly ever a problem. For search engines, however, Akkadian transliteration is much more difficult to deal with because the same word may be spelled in many different ways. Without lemmatization, there is no way a machine can tell that ***ša-ar-ru-um***, ***ša-ar-ri-im***, ***ša-ar-ra-am***, ***šar-ru***, ***šar-ri***, ***šar-ra***, **LUGAL**, and **MAN** all represent forms of the same word for "king" in syllabic and logographic writing. The rich morphology of Akkadian, with prefixes, suffixes, and infixes and various vowel patterns to be applied to different forms of a single verb further complicates this issue.
# 
# Since [CDLI](http://cdli.ucla.edu) does not offer lemmatization, searching for words on this site is much more popular (and more useful) for Sumerian than it is for Akkadian. Sumerian words usually include the root of the word (written logographically) with prefixes and/or suffixes attached. Although spelling variations exist (e.g. **dag-si**, **da-ag-si**, **da-ag-ši-um**, and **da-ag-zi-um**, all representing variants of the word [dagsi](http://oracc.org/epsd2/o0025593) for saddle hook or saddle bag), such variation plays a much smaller role in Sumerian than in Akkadian.

# ## 2.3.2 Downloading CDLI data
# 
# There are various ways in which one can acquire [CDLI](http://cdli.ucla.edu) data. The website includes a [Downloads](https://cdli.ucla.edu/?q=downloads) page where one can get access to a daily clone of the catalog and the entire set of transliterations. Alternatively, one can perform a search on the [CDLI](http://cdli.ucla.edu) search page and request a download of the data (transliteration only or catalog and transliteration data) by pushing a button. This works well for a few or several dozens of texts, but not for very large data sets. The present notebook will download the [CDLI](http://cdli.ucla.edu) files from the daily clone on [Github](https://github.com/cdli-gh/data).
# 
# Currently, the set of transliterations is offered in one big file, named `cdliatf_unblocked.atf `. The catalog is split into two files because of file-size limitations at [Github](http://github.com); they are named `cdli_catalogue_1of2.csv` and `cdli_catalogue_2of2.csv`, respectively. The files need to be concatenated before they can be used.
# 
# ### 2.3.2.0 Import Packages
# * requests: for communicating with a server over the internet
# * tqdm: for creating progress bars
# * pandas: data analysis and manipulation; dataframes
# * BeautifulSoup: web scraping
# * os: for basic Operating System operations (such as creating a directory)
# * shutil: file operations (such as concatenating files)

# In[1]:


import requests
from tqdm.auto import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import os
import shutil


# ### 2.3.2.1 Create Download Directory
# Create a directory called `cdlidata`. If the directory already exists, do nothing. 

# In[2]:


os.makedirs('cdlidata', exist_ok = True)


# ### 2.3.2.2 Retrieve File Names
# 
# ```{margin}
# For BeautifulSoup, see chapter 4 [Data Collection](https://melaniewalsh.github.io/Intro-Cultural-Analytics/Data-Collection/Web-Scraping-Part1.html#beautifulsoup) in Melanie Walsh's [Introduction to Cultural Analytics and Python](https://melaniewalsh.github.io/Intro-Cultural-Analytics/welcome.html).
# ```
# 
# The code first retrieves the names of the files that are offered for download on the CDLI [download](https://github.com/cdli-gh/data) page on GitHub. The script requests the HTML of the download page and uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (a package for web scraping) to retrieve all the links from the page. This includes the file names, but also all kinds of other links.
# 
# Scraping the file names (rather than simply listing them) is useful, because in the future the data may have to be split in more than two files.

# In[3]:


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


# ### 2.3.2.3 Download
# The download code in this cell is essentially identical with the code in section [2.1.0](2.1.0): Download ORACC JSON. Because of the size of the files, and depending on the speed of your computer and internet connection the downloading process can take some time.

# In[4]:


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


# ### 2.3.2.4. Concatenate the Catalogue Files
# The catalogue files are concatenated, using a utility from the `shutil` package. The new, concatenated, file is called `catalogue.csv`.

# In[5]:


filenames = [f for f in files if "cdli_catalogue" in f]
filenames.sort()  # to make sure we read cdli_catalogue_1of2.csv first.
with open('cdlidata/catalogue.csv','wb') as concatenated_file:
    for file in filenames:
        with open(f'cdlidata/{file}','rb') as one_file:
            shutil.copyfileobj(one_file, concatenated_file)


# ### 2.3.2.4 Load in a Pandas data frame
# 
# The field `id_text` holds the text ID number as a string, without the preceding "P" and without padding zeroes to the left. The text ID "P001023" is thus represented as 1023. When reading the data into `pandas`, chances are that the data type of `id_text` is interpreted as integer. The function `zfill()` adds the padding zeros to create a six-digit number as a string. 

# In[6]:


cat = pd.read_csv('cdlidata/catalogue.csv', engine='python', error_bad_lines=False).fillna('')
cat['id_text'] = ["P" + str(no).zfill(6) for no in cat['id_text']]
cat


# ## 2.3.3 Use the Catalog to Select Transliterations
# In the example code in the following cell the catalog is used to select from the transliteration file all texts from the Early Dynastic IIIa period. The field "period" is used to select those catalog entries that have "ED IIIa" in that field. 
# 
# In the transliteration file, a new text is introduced by a line that begins with an ampersand (&) followed by a P number, followed by a publication reference (journal or book) using a commonly used set of abbreviations, as in:
# 
# > 	&P212416 = AAICAB 1/1, pl. 008, 19282-439
# 
# The set of transliterations in the file `cdliatf_unblocked.atf` is read into a list, one line at a time, with the `readlines()` method. The code iterates through that list of lines. The flag `keep` (which initially is set to `False`) is set to `True` if the code encounters a P number that is present in the list `pnos`. As long as `keep = True` subsequent lines are added to the list `ed3a_atf`. When the script encounters a P-number that is not in `pnos`, the flag `keep` is set to `False`.
# 
# The result is a of list lines with all the transliteration data of the Early Dynastic IIIa texts in [CDLI](http://cdli.ucla.edu).

# In[7]:


ed3a = cat.loc[cat["period"].str[:7] == "ED IIIa"]
pnos = list(ed3a["id_text"])
#pnos = ["P" + str(no).zfill(6) for no in pnos]
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


# ## 2.3.4 Create a Data Frame with the Selected Texts
# The following code will transform the list `ed3a_atf` into a format where each text is a row in a `pandas` data frame, with the text ID in column 1, and the transliteration in column 2 (as a single string, without line numbers or line demarcations). This is, of course, just one example of how the data may be selected and formatted - we can use all the power of the `pandas` library to slice and manipulated the data.
# 
# ```{figure} ../images/P212416.jpg
# :scale: 25%
# [P212416](http://cdli.ucla.edu/P212416), an ED IIIa administrative document from Kish
# ```
# 
# The lines are read in reverse order, so that when the script encounters an '&P' line (as in '&P212416 = AAICAB 1/1, pl. 008, 19282-439'), this signals that all the lines of a text have been read and that the document can be added to the list `docs`. (When reading the lines in regular order - taking the '&P' line as signaling the end of the previous document - one needs to separately save the last document, because there is no '&P' line anymore to indicate that the text is complete).

# In[8]:


docs = []
document = ''
id_text = ''
ed3a_atf = [line for line in ed3a_atf if line.strip()]  # remove empty lines, which cause trouble
for line in tqdm(reversed(ed3a_atf)):
    if line[0] == "&":  # line beginning with & marks the beginning of a document
        id_text = line[1:8] # retrieve the P number
        docs.append([id_text, document])
        document = ''   # after appending the data to docs, reset the variable `document`.
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


# In[9]:


ed3a_df


# In[ ]:




