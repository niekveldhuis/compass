## 2.3 Data Acquisition: CDLI

### 2.3.1 CDLI Data

The [Cuneiform Digital Library Initiative](http://cdli.ucla.edu), created by [Bob Englund](https://cdli.ucla.edu/?q=robert-k-englund) (UCLA) in the early two thousands, is a central repository for meta-data, images, and transliterations of cuneiform objects (translations are offered only for a small minority of texts). Today more than 335,000 objects are listed in the [CDLI](http://cdli.ucla.edu) catalog, with tens of thousands of photographs and line drawings. Each object in [CDLI](http://cdli.ucla.edu) receives a unique ID number, and these numbers are widely used today in print and in on-line projects. Initially, [CDLI](http://cdli.ucla.edu) focused primarily on administrative texts from the third millennium, and this is still the area of its greatest strength. Currently, approximately 121,000 texts are available in transliteration in [CDLI](http://cdli.ucla.edu). Part of this corpus was produced by the [CDLI](http://cdli.ucla.edu) team at UCLA, others were contributed by partners or were imported from other projects such as [ETCSL](https://etcsl.orinst.ox.ac.uk/) (for Sumerian literary texts), [DCCLT](http://oracc.org/dcclt) (for lexical texts), or [BDTNS](http://bdtns.filol.csic.es/) (for Ur III administrative texts). The photographs on [CDLI](http://cdli.ucla.edu) were largely produced in cooperative projects with museums all over the world, where [CDLI](http://cdli.ucla.edu) staff or partners would go to scan an entire collection or major parts of a collection. These images are copyright of the museum where the object is held and there is no wholesale downloading of the entire image set.

Many of the fields in the [CDLI](http://cdli.ucla.edu) catalog either use a restricted vocabulary (period, genre) or have been standardized to a great degree (provenance, author's name, owner, museum number), greatly facilitating search. 

The issue of standardization is much more difficult for linguistic data in transliteration. Here, Sumerian and Akkadian pose rather different challenges. For Sumerian, there are two main issues. First, Sumerologists tend to use different sets of conventions for representing Sumerian words in the Latin alphabet. The word for "to give" is read **šum₂** by some, but **sum** by others. Similarly, the word for "ox" is read either **gud** or **gu₄**. These readings (**šum₂** vs **sum** or **gud** vs. **gu₄**) represent the same word and render the same sign - they simply differ in modern transliteration conventions. Variation in such conventions has grown recently by the introduction of a new set of readings by P. Attinger (Bern), which has received wide following, in particular in Germany. Such variation in sign readings is based on the one hand on differing interpretations of the data from [ancient sign lists](http://oracc.org/dcclt/signlists) (which provide transcriptions of Sumerian words in Akkadian) and on the other hand on the definition of what an ideal transliteration should do (whether it should represent the abstract lexeme, or rather its concrete pronunciation, or something in between). For the [CDLI](http://cdli.ucla.edu) search engine, which is based on a FileMaker database, such variation presents a problem when searching for (Sumerian) words. The solution has been to strictly impose a set of [preferred sign readings](https://cdli.ucla.edu/methods/sign_reading.html) (available on the web site), a policy that has been carried out with great consistency. 

Second, Sumerian has no good standard for word segmentation. In the [CDLI](http://cdli.ucla.edu) data set one may find the word **ninda-i₃-de₂-a** (a pastry) transliterated as **ninda-i₃-de₂-a**, **ninda i₃-de₂-a**, **ninda i₃ de₂-a**, **nig₂-i₃-de₂-a**, **nig₂ i₃ de₂-a**, etcetera (**nig₂** and **ninda** are two different words, written by the same sign and there is no full agreement which of these readings is to be used in this particular word). None of these various renderings is necessarily "wrong", because we know fairly little about the formation and segmentation of Sumerian nouns. For computational approaches this variation poses an important challenge.

For Akkadian the variation in reading conventions plays a much smaller role; for most dialects of Akkadian (with the exception of Old Akkadian) scholars generally agree on transliteration conventions; word segmentation is hardly ever a problem. For search engines, however, Akkadian transliteration is much more difficult to deal with because the same word may be spelled in many different ways. Without lemmatization, there is no way a machine can tell that ***ša-ar-ru-um***, ***šar-ru*** and **LUGAL**, etc. all represent the same word for "king" in syllabic and logographic writing. The rich morphology of Akkadian, with prefixes, suffixes, and infixes and various vowel patterns to be applied to different forms of a single verb further complicates this issue.

Since [CDLI](http://cdli.ucla.edu) does not offer lemmatization, searching for words on this site is much more popular (and more useful) for Sumerian than it is for Akkadian. Sumerian words usually include the root of the word (written logographically) with prefixes and/or suffixes attached. Although spelling variations exist (e.g. **dag-si**, **da-ag-ši-um**, and **da-ag-zi-um**, all representing the same word for saddle hook or saddle bag), such variation plays a much smaller role in Sumerian than in Akkadian.

### 2.3.2 Downloading

There are various ways in which one can acquire [CDLI](http://cdli.ucla.edu) data. The website includes a [Downloads](https://cdli.ucla.edu/?q=downloads) page where one can get access to a daily clone of the catalog and the entire set of transliterations. Alternatively, one can perform a search on the [CDLI](http://cdli.ucla.edu) search page and request a download of the data (transliteration or catalog and transliteration data) by pushing a button. This works well for a few or several dozens of texts, but not for very large data sets.

Furthermore, the daily data dump is available from [Github](http://github.com) at https://github.com/cdli-gh/data. Currently, the set of transliterations is offered in one big file, named `cdliatf_unblocked.atf `. The catalog is split into two files because of file-size limitations at [Github](http://github.com); they are named `cdli_catalogue_1of2.csv` and `cdli_catalogue_2of2.csv`, respectively. The files need to be concatenated before they can be used.

The script for downloading these files (2_3_Data_Acquisition_CDLI.ipynb) essentially follows the same patterns as the script for downloading [ORACC](http://oracc.org) files, discussed in section 2.1. The script uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) from the `bs4` module to scrape the filenames from the [Github](https://github.com/cdli-gh/data/raw/master/) page.

### 2.3.3 Manipulating

After downloading and concatenating the catalog files, the data may be ingested in a `pandas` DataFrame for further manipulation. 

The catalog may be used to create a sub-set of the [CDLI](http://cdli.ucla.edu) transliteration file by finding the P numbers (text IDs) that belong to, for instance, texts from Ebla, or texts dating to the ED IIIa period (as in the example below).

The field `id_text` holds the text ID number as a string, without the preceding "P" and without padding zeroes to the left. The text ID "P001023" is thus represented as 1023. When reading the data into `pandas`, chances are that the data type of `id_text` is interpreted as integer, to be transformed into a string. The function `zfill()` adds the padding zeros to create a six-digit number as a string. In the transliteration file, a new text is introduced by a line that begins with an ampersand (&) followed by a P number, followed by a publication reference (journal or book) using a commonly used set of abbreviations, as in:

> 	&P212416 = AAICAB 1/1, pl. 008, 19282-439

The script uses this pattern to recognize the beginning of a document, and matches the P number with the catalog data to see if it belongs to the right time period. If so, the &-line and the following lines are added to a list.

```python
ed3a = cat.loc[cat["period"].str[:7] == "ED IIIa"] 
pnos = list(ed3a["id_text"])           # create a list of P numbers
pnos = ["P" + str(no).zfill(6) for no in pnos] # format the P numbers as strings with padding
with open("cdlidata/cdliatf_unblocked.atf", encoding="utf8") as c: 
    lines = c.readlines()
keep = False
ed3a_atf = []
for line in lines:
    if line[0] == "&": 
        if line[1:8] in pnos: 
            keep = True
        else: 
            keep = False
    if keep: 
        ed3a_atf.append(line)
```

This will represent the ED IIIa corpus as a list, where each line in the original ATF document is represented by one element in the list. The following code will transform this list into a format where each text is a row in a `pandas` DataFrame, with the text ID in column 1, and the transliteration in column 2 (as a single string, without line numbers or line demarcations). The lines are read in reverse order, so that when the script encounters an '&P' line (as in '&P212416 = AAICAB 1/1, pl. 008, 19282-439'), this signals that all the lines of a text have been read and that the document can be added to the list `docs`. (When reading the lines in regular order - taking the '&P' line as signaling the end of the previous document - one may accidentally omit the last document, because there is no '&P' line anymore to indicate that the text is complete).

```python
form tqdm.notebook import tqdm
docs = []
document = ''
id_text = ''
ed3a_atf = [line for line in ed3a_atf if line.strip()]  # remove empty lines, which cause trouble
for line in tqdm(reversed(ed3a_atf)):  # start at the end
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
            document = f'{line} {document}'
        except:
            continue   # malformed lines (no proper separation between line number and text) are skipped
ed3a_df = pd.DataFrame(docs)
ed3a_df.columns = ["id_text", "transliteration"]
```


