#!/usr/bin/env python
# coding: utf-8

# # 2.4 Data Acquision BDTNS
# 
# Goal of this notebook is to transform [BDTNS](http://bdtns.filol.csic.es/) data into a structured format that clearly distinguishes between text and non-text (such as line numbers) and that, for the text part, follows as much as possible the standards of the Oracc Global Sign List ([OGSL](http://oracc.org/ogsl)). Adherence to the [OGSL](http://oracc.org/ogsl) standard makes it possible to transform a line of text into a sequence of sign names or Unicode codepoints. This can be used to track transliteration inconsistencies, for instance in the rendering of names (U₂-da-mi-ša-ru-um vs. U₂-ta₂-mi-ša-ru-um), to build a search engine that finds a sign sequence regardless of the actual transliteration, or to compare editions of the same text in [BDTNS](http://bdtns.filol.csic.es/), [CDLI](http://cdli.ucla.edu), and [ePSD2](http://oracc.org/epsd2/admin/u3adm).
# 
# The search engine will be built in a separate notebook - primarily as a case study of the potential of this approach.
# 
# On the [BDTNS](http://bdtns.filol.csic.es/) website, search results can be downloaded with the "Export" button in the left pane. Searching for the empty string will select all texts currently available. The export creates two files: one with transliterations and one with meta-data. The transliteration file is discussed here most extensively. The file name is "query\_text\_" followed by a date and an additional number. Move the file to the `data` directory of this chapter.
# 
# This notebook uses the `pandas` integration of the `tqdm` package, for showing a progress bar. This is important, because the transformation of (currently) more than 1.1 million lines of text in [BDTNS](http://bdtns.filol.csic.es) takes some time. The pandas/tqdm integration is initialized with `tqdm.pandas()`, immediately after importing `tqdm`. This allows the usage of the functions `progress_apply()` and `progress_map()` instead of the standard `apply()` and `map()` functions in `pandas`.

# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import re
from tqdm.auto import tqdm
tqdm.pandas() # initiate pandas support in tqdm, allowing progress_apply() and progress_map()
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils
import pickle


# # Create Directories

# In[ ]:


os.makedirs('output', exist_ok = True)


# # Read Catalog Data
# Make sure to put the BDTNS data files (catalog and text files) in the `data` directory of `compass/2_4_Data_Acquisition_BDTNS` or adjust the code in the cell below to reflect the location of your downloaded [BDTNS](http://bdtns.filol.csic.es/) files. The code will identify the most recently downloaded catalog file and open that. Check that your file has all the fields (you can select the fields you want in the download process) and/or adjust the list `cols` to reflect the fields in your file.

# In[ ]:


datafiles = os.listdir('data')
catfiles = [filename for filename in datafiles if filename.startswith('query_cat')] # select the BDTNS catalogue files
catfiles.sort(reverse = True)
file = f'data/{catfiles[0]}' #select the file with the most recent date in the filename
cols = ['id_text', 'cdli', 'publication', 'mus_no',
        'collection', 'date', 'provenance', 'seal', 'object']
cat_df = pd.read_csv(file, sep = '\t', names= cols, header=None).fillna('')
cat_df.head()


# # Pickle Catalog DataFrame
# The catalog DataFrame is not used further in this notebook, but will be used in the search engine, to be built in 2.4.2. For now it is saved as a file with the `pickle` package.

# In[ ]:


pickled = "output/bdtns_cat.p"
cat_df.to_pickle(pickled)


# # Read the Transliteration File as a List
# Your downloaded [BDTNS](http://bdtns.filol.csic.es/) text file (named `query_text` followed by a date and an additional number) should be located in the `data` directory; the code will identify the most recent file and open that.
# 
# [BDTNS](http://bdtns.filol.csic.es/) uses so-called "vertical tabs" (represented by `^K`, `\v`, or `\x0b`, depending on your editor) as a new line within a single document, whereas the standard newline (`\n`) character is used to separate one document from the next. The Python `readlines()` function (which reads a file line-by-line, producing a list) is memory efficient, but keeps the vertical tabs and will result in a format where each document is represented as a single line. Instead, therefore, we read the entire file into memory with the `read()` function and then split the document into lines with `splitlines()`. The function `splitlines()` takes the vertical tab (as well as the regular newline character) as a line separator; this will result in a line-by-line representation of the document in the form of a list (called `bdtns`).
# 
# Empty lines (or lines filled with spaces or tabs only) will cause trouble downstream and are removed.

# In[ ]:


txtfiles = [filename for filename in datafiles if filename.startswith('query_text')]
txtfiles.sort(reverse = True)
file = f'data/{txtfiles[0]}'
with open(file, mode = 'r', encoding = 'utf8') as f:
    bdtns = f.read().splitlines()
bdtns = [line for line in bdtns if len(line.strip()) > 0] # remove empty lines
bdtns[:25] # inspect the results


# # Split Data into Fields
# The code looks for lines that begin with 6 digits (as in '145342'). Those numbers are the [BDTNS](http://bdtns.filol.csic.es/) text ID numbers and mark the beginning of a new document. If such a line is found, the number is stored in the variable `bdtns_no`. Other data available in such lines (such as publication and [CDLI](http://cdli.ucla.edu) P-number) are omitted, because they are better derived from the meta-data file (with the [BDTNS](http://bdtns.filol.csic.es) number as key).
# 
# If the line does not start with 6 digits, it is a transliteration line. The `split()` function is used to separate the line into three fields: line number, transliteration text, and comments. The variables `id_text` (the [BDTNS](http://bdtns.filol.csic.es) number) and `id_line` are added to each line as separate fields. The field `id_line` is a running number (an integer) that starts at 1 for each document. In the current notebook the variable is not used, but it can be used to keep or restore the proper order of the lines of a document. The variable `label` is the human-readable line number in the format 'r ii 7' (for reverse column 2 line 7).
# 
# In the [BDTNS](http://bdtns.filol.csic.es/) output line numbers are separated from transliteration text by 5 spaces. Editorial remarks are introduced by the hash-mark (#). Finally, sign names (qualifying x-values, rare signs, and, occasionally, readings with exclamation mark) are marked by '(=', as in '(=SIG7)'. In the script, the five spaces are replaced by '#' and '(=' is replaced by '#(=' so that we can split each line on the hash mark. The `replace()` function is done only once and `split()` is done twice, so that we end up with three columns, representing label, text, and comments (to which the `id_text` and `id_line` are added). The column `comments` will include both editorial comments and sign explications of x-values.

# In[ ]:


lines = []
id_line = 0
id_text = ''
for line in tqdm(bdtns): 
    if line[:6].isdigit(): 
        id_text = line[:6]
        id_line = 0
        continue
    else: 
        id_line += 1
        li = line.strip()
        li = li.replace("(=", "#(=", 1).replace('     ', '#', 1)
        li_l = li.split('#', 2)  # split line into a list with length 3.
        li_l = [id_text, id_line] + li_l
        lines.append(li_l)


# # Create DataFrame
# The list `lines` is now a list of lists which can be transformed into a `pandas` DataFrame. The DataFrame will have `NaN` (for 'Not a Number') in all cases where a field is empty. `NaN`s are treated by Python as a numerical data type and will throw errors when trying to apply a string function. Therefore, all `NaN`s are replaced by the empty string with the `fillna()` function from the `pandas` library.

# In[ ]:


columns = ["id_text", "id_line", "label", "text", "comments"]
df = pd.DataFrame(lines, columns=columns).fillna("")
df  # inspect the results


# # Make OGSL compliant
# [OGSL](http://oracc.org/ogsl) is the ORACC Global Sign List, which lists for each sign its possible readings. [OGSL](http://oracc.org/ogsl) compliance opens the possibility to search or compare by sign *name* rather than sign value. For instance, one may search for the sequence "aga₃ kug-sig₁₇" (golden tiara) and find a line reading "gin₂ ku₃-GI".
# 
# The main steps towards [OGSL](http://oracc.org/ogsl) compliance are: 
# 
# - add sign names to x-values
# - replace regular numbers by index numbers in sign values

# # Dealing with x-values
# In [OGSL](http://oracc.org/ogsl), a sign reading that does not (yet) have a commonly accepted index number receives the ₓ index, followed by the sign name, as in ziₓ(IGI@g). In the [BDTNS](http://bdtns.filol.csic.es) export file the subscripted ₓ is represented by a capital X and the sign name is given at the end of the line, as in
# 
# > o. 2     gi ziX-a 12 sar-⌈ta⌉ (=SIG7)
# 
# Note that IGI@g (the *gunû* form of the IGI sign, that is: IGI with extra wedges) is the standard [OGSL](http://oracc.org/ogsl) name of the same sign that is called SIG₇ in [BDTNS](http://bdtns.filol.csic.es).
# 
# In the DataFrame, the sign names are now found in the column `comments`. The most straightforward solution is to replace every capital X with an ₓ plus what is found in the comments column (minus the equal sign).
# 
# In our example, this would result in: 
# > o. 2     gi ziₓ(SIG₇)-a 12 sar-⌈ta⌉
# 
# In practice, however, there are quite a few exceptions to the pattern illustrated above. Examples include: 
# 
# > 18 gin2 nagga mu-kuX gibil (=AN.NA) (=DU)
# 
# Here (=AN.NA) explains the infrequent sign "nagga". However, since "nagga" is not followed by X the naive replacement would return
# 
# > 18 gin₂ nagga mu-kuₓ(AN.NA) gibil (=DU)
# 
# Another exception is reduplicated **gurₓ-gurₓ** which is represented thus: 
# > 6.0.0 še ur5-ra še gurX-gurX-ta su-ga (=ŠE.KIN.ŠE.KIN)
# 
# Naive replacement would result in: 
# > 6.0.0 še ur₅-ra še gurₓ(ŠE.KIN.ŠE.KIN)-gurₓ-ta su-ga
# 
# Finally, a few x-values are usually not resolved this way, for instance: 
# > 1 sila4 Ur-nigarX{gar}
# 
# with no sign name for nigarX - presumably because it can be unambiguously resolved as U.UD.KID.
# 
# For these reasons we will approach the x-values in two different ways
# 
# - x-values that are unambiguous are resolved with a search and replace, using a dictionary - replacing, e.g. ziX with ziₓ(IGI@g). This process does not pay attention to the [BDTNS](http://bdtns.filol.csic.es) sign explication in the `comments` column (=SIG7). A special case in this category is mu-kuX ("delivery"), which is very frequent and should be resolved as mu-kuₓ(DU). However, kuX by itself may also be resolved as kuₓ(LIL) or kuₓ(KWU147) (both for the verb "to enter").
# - x-values that do not resolve unambiguously (muruₓ, ušurₓ, ummuₓ, and several others) are resolved by moving the [BDTNS](http://bdtns.filol.csic.es) sign name (in the `comments` column) after the X sign between brackets, as discussed above.
# 
# Both of these steps are included in the function `ogsl_v()`, that is applied to every row of the DataFrame. In addition, this function will replace index numbers (such as the 7 in sig7) with Unicode index numbers (sig₇), leaving alone numbers that represent quantities.

# # Step 1: Unambiguous x-values
# 
# Some x-values are always resolved in the same way. Thus, ziX is always ziₓ(IGI@g), hirinX is always hirinₓ(KWU318), and gurX is always gurₓ(|ŠE.KIN|). In some cases, x-values have been assigned an index number in [OGSL](http://oracc.org/ogsl). In those cases (nigarₓ = nigar; nemurₓ(PIRIG.TUR) = nemur₂; nagₓ(GAZ) = nag₃; and pešₓ(ŠU.PEŠ5) = peš₁₄) the appropriate index number should be added and the sign name ignored.
# 
# A dictionary of such unambiguous x-values (`xvalues`) has as its key the x-value as represented in [BDTNS](http://bdtns.filol.csic.es) in lower case ('zix') and as its value the index ₓ plus the appropriate sign name ('ₓ(IGI@g)') in [OGSL](http://oracc.org/ogsl) format.
# 
# The substitution is done with a somewhat complex [regular expression](https://www.regular-expressions.info/), that looks as follows: 
# 
# ```python
# row['text'] = re.sub(xv, lambda m: m.group()[:-1] + xvalues.get(m.group().translate(table).lower(), 'X'), row['text'])
# ```
# The `sub()` function of the `re` library has the general form `re.sub(search_pattern, replace, string)`. Instead of a replace string, one may also give a function (in this case a temporary `lambda` function) that returns the `replace` string. In this case the `lambda` function accesses the dictionary `xvalues` to see if the match that was found in the search pattern is present among the keys. The basic format of that command is `xvalues.get(m.group())`, where `m.group()` represents the current match of the search pattern. The search pattern, `xv` (to be explained in more detail below) may match `zahX`, `NigarX`, or `[bu]lugX` - in other words, the match may include capitals (as in `NigarX`) or brackets and flags (as in `[bu]lugX`). In order to find that match in the dictionary it is lowercased and "translated". The function `translate()` translates individual characters into other characters - according to a translation pattern in a table. In this case, the characters representing flags and brackets are all translated to `None` which means, in practice, that they are removed. The matches `zahX`, `NigarX`, and `[bu]lugX`, therefore, will be looked up in the dictionary as `zahx`, `nigarx`, and `bulugx` - and each of those are indeed keys in `xvalues`. In the `get()` function one may optionally add a fall-back value in case the key is not found - in this case the fall-back is 'X'. 
# 
# If a match is found, say `[bu]lugX`, the key `bulugx` is found in the dictionary `xvalues`, returning `ₓ(|ŠIM×KUŠU₂|)`. The return value of the lambda function is the search match (`[bu]lugX`) minus the last character (`[bu]lug`) plus the value that was returned from the dictionary (`ₓ(|ŠIM×KUŠU₂|)`), resulting in `[bu]lugₓ(|ŠIM×KUŠU₂|)`. If the search pattern returns a match that is not found in the dictionary (for instance `ušurX`), the return value of the lambda function is, again, the search match (`ušurX`), minus the last character (`ušur`) plus `X`, the fallback return of the `get()` function, resulting in `ušurX`. In other words - in those cases the search match is replaced by itself and nothing changes.
# 
# The search pattern is a compiled regex (compiled expressions are faster than expressions that need to be interpreted on the fly), `xv`, which is defined as
# ```python
# xv = re.compile(r'[\w' + re.escape(flags) + ']+X')
# ```
# This matches any sequence of one or more (`+`) word-characters (`\w`; this includes letters from the English alphabet as well as special characters such as š, ṣ, and ṭ, the digits 0-9, and the underscore) and/or flags (such as square brackets etc.; see below: Flags), followed by a capital X. This regex will match `ziX`, `zahX`, or `ušurX`, but also `[za]hX`, etc. It does not match 'KA×X', ' X', or 'x-X', because the characters × (for 'times') the hyphen and the space are neither word characters nor flags.
# 
# Special case: **mu-kuX**. There are multiple possible solutions for **kuX**, including kuₓ(LIL) or kuₓ(KWU147), but the very frequent form **mu-kuX** is always to be resolved **mu-kuₓ(DU)**. The regular expression `xv` in the preceding does not match hyphens and thus it will never find the key `mu-kuX` in the dictionary `xvalues`. However, this expression (meaning 'delivery') is so frequent that it makes sense to deal with it separately, rather than depend on the sign names in the `comments` column. The expression **mu-kuX** therefore, has its own line in the function.

# # Step 2: Remaining x-values
# For the remaining x-values (many of them ambiguous) we will copy the [BDTNS](http://bdtns.filol.csic.es) sign name, found in the `comments` column, to the x-value. For instance, **ummu₃** is |A.EDIN.LAL|, but the sign complex has many variants, all rendered **ummuX**: EDIN.A.SU, A.EDIN, A.EDIN.A.LAL, EDIN, etc. The code will result in ummuₓ(|A.EDIN.SU|), ummuₓ(|A.EDIN|), ummuₓ(|A.EDIN.LAL|), ummuₓ(EDIN), etc. Compound signs are put between pipes (|A.EDIN.SU|), according to [OGSL](http://oracc.org/ogsl) conventions.
# 
# In this step the code will naively replace the capital X by the index ₓ, followed by the first word in the `comments` column. This will result in errors if there are more such x-values in a single line - but because we have already dealt with many such values in the preceding, that risk is not very high. The code will test that the capital X does in fact follow a sign reading (as in ziX), and is not an illegible sign (as in KA×X, or simply X). This is done with a [regular expression](https://www.regular-expressions.info/) using a so-called "positive lookbehind" (?<=), to see if the preceding character is a letter. The regular expression for a capital 'X' preceded by any letter valid in Sumerian or Akkadian, is compiled in the variable `lettersX` in order to speed up the process (see below: Letters).

# # Step 3: Index Numbers
# In a third step all sign reading index numbers (as in 'du11') are replaced by Unicode index numbers ('du₁₁'). Regular numbers that express quantities should not be affected. This is done with a regular expression that finds a character, valid in Sumerian or Akkadian transcription, immediately followed by one or more digits. If such a match is found, the string is translated, replacing any digit by its corresponding index number.

# # Errors
# Inevitably, each of the steps in dealing with x-values may introduce its own errors. It is likely, moreover, that there are more x-values not treated here, or that there will be more x-values in a future version of the [BDTNS](http://bdtns.filol.csic.es) data. The dictionary of x-values below can be adjusted to deal with those situations. 

# # Helpful Variables, Lists, and Dictionaries
# A number of lists, dictionaries, and variables (including compiled regular expressions) are defined before the main function is called.
# 
# The list `flags` enumerates characters like square brackets, half-brackets and exclamation marks that may appear in a sign reading in  in [BDTNS](http://bdtns.filol.csic.es). The list is used in two ways. First, it is used in compiling the regular expression `xv` that will match any sign reading that ends in a capital X (see below). Second, it is used to create a table in which each flag corresponds to `None`. The `maketrans()` function is a specialized function that prepares a table that is understood by the `translate()` command. The command `translate(table)` is used in the function `ogsl_v()` (see below) to ignore any flag.
# 
# The [regular expression](https://www.regular-expressions.info/) `xv` matches a sequence of one or more characters, immediately followed by a capital `X`. The characters allowed in the sequence are "word" characters (represented by `\w`), as well as the flags. Word characters are implemented slightly differently in different programs that use regular expressions. In Python it includes the English letters of the alphabet, as well as special characters such as ṭ, ṣ, and š, but also digits (0-9) and the underscore. The `escape()` function from the `re` library supplies the proper escape character for characters in the `flags` variable that otherwise have a special function in regular expressions. For instance, the question mark, which is included in the flags, means 'zero or one time' in a regular expression. In order to match the literal question mark it should be represented as `\?` - the `escape()` funcion takes care of that.
# 
# The variable `letters` is a string that includes all letters that are valid in Sumerian or Akkadian, to be used in regular expressions. The variable `lettersX` is a compiled regular expression that represents a capital `X` preceded by any character in `letters`. The variable `lettersX`is a so-called look-behind expression so that the match consists only of the capital X. Similarly, the variable `lettersNo` is a compiled regular expression that represents a sequence of one or more digits (represented by `\d+`) or capital `X` preceded by any character in `letters`. The variable `lettersno`, however, does not use the lookbehind function (which is relatively slow) because the translation affects only the digits, other characters are left unchanged.
# 
# The dictionary `xvalues` provides the unambiguous x-values in [BDTNS](http://bdtns.filol.csic.es) as keys with their resolution according to [OGSL](http://oracc.org/ogsl) standards.

# In[ ]:


flags = "][!?<>⸢⸣⌈⌉*/"
table = str.maketrans(dict.fromkeys(flags))
xv = re.compile(fr'[\w{re.escape(flags)}]+X') #this matches a sequence of word signs (letters) and/or flags, followed by capital X

letters = r'a-zḫĝŋṣšṭA-ZḪĜŊṢŠṬ'
lettersX = re.compile(fr'(?<=[{letters}])X') # capital X preceded by a letter
lettersNo = re.compile(fr'[{letters}](\d+|X)') # any sequence of digits, or X, preceded by a letter

ascind, uniind = '0123456789x', '₀₁₂₃₄₅₆₇₈₉ₓ'
transind = str.maketrans(ascind, uniind) # translation table for index numbers

xvalues = {'nagx' : '₃', 'nigarx' : '', 'nemurx' : '₂', 'pešx' : '₁₄', 'urubx' : '', 
        'tubax' : '₄', 'niginx' : '₈', 'šux' : '₁₄', 
        'alx' : 'ₓ(|NUN.LAGAR|)' , 'bulugx' : 'ₓ(|ŠIM×KUŠU₂|)', 'dagx' : 'ₓ(KWU844)', 
        'durux' : 'ₓ(|IGI.DIB|)', 'durunx' : 'ₓ(|KU.KU)', 
        'gigirx' : 'ₓ(|LAGAB×MU|)', 'giparx' : 'ₓ(KISAL)', 'girx' : 'ₓ(GI)', 
        'gišbunx' : 'ₓ(|KI.BI|)', 'gurx' : 'ₓ(|ŠE.KIN|)', 
        'hirinx' : 'ₓ(KWU318)', 'kurunx' : 'ₓ(|DIN.BI|)',
        'mu-kux' : 'ₓ(DU)', 'munsubx' : 'ₓ(|PA.GU₂×NUN|)',  
        'sagx' : 'ₓ(|ŠE.KIN|)', 'subx' : 'ₓ(|DU.DU|)', 
        'sullimx' : 'ₓ(EN)', 'šaganx' : 'ₓ(|GA×AN.GAN|)', 
        'ulušinx' : 'ₓ(|BI.ZIZ₂|)', 'zabalamx' : 'ₓ(|MUŠ₃.TE.AB@g|)', 
        'zahx' : 'ₓ(ŠEŠ)', 'zahdax' : 'ₓ(|DUN.NE.TUR|)',  
        'zix' : 'ₓ(IGI@g)'}


# # The Main Function
# The function `ogsl_v()` takes one row of the DataFrame at the time and goes through three separate steps. First, it treats the unambiguous x-values by adding the signs name, found in the dictionary `xvalues`. 
# 
# Second, if the line still contains x-values, it will try to find the sign name in the `comments` column. If the sign name as found is a compound sign (contains the characters `.`, `ₓ`, or `+`) the sign name is surrounded by pipes accoridng to [OGSL](http://oracc.org/ogsl) conventions.
# 
# Third, the function will replace all sign index numbers by their Unicode equivalents.
# 
# In each of these steps the function uses one or more of the tables, dictionaries, and compiled regular expressions created above.

# In[ ]:


def ogsl_v(row):
    # 1. deal with unambiguous x-values, listed in the dictionary xvalues.
    row['text'] = re.sub(xv, lambda m: m.group()[:-1] + xvalues.get(m.group().translate(table).lower(), 'X'), row['text'])
    if 'mu-kuX' in row['text'].translate(table): 
        row['text'] = row['text'].replace('X', xvalues['mu-kux'])
    # 2. deal with remaining x-values
    if row["comments"][:2] == "(=": 
        sign_name = row["comments"][2:]  # remove (=  from (=SIG7)
        sign_name = sign_name.split(')')[0] #remove ) and anything following
        if re.findall(r'\.|×|\+', sign_name): # if sign_name contains either . or × or +
            sign_name = f'ₓ(|{sign_name}|)'  # add pipes
        else: 
            sign_name = f'ₓ({sign_name})'
        ogsl_valid = re.sub(lettersX, sign_name, row['text']) # find sequence of letters followed by X; 
                                                              #replace X by ₓ followed by sign name between brackets.
    else:
        ogsl_valid = row["text"]    
    # 3 deal with index numbers
    ogsl_valid = re.sub(lettersNo, lambda m: m.group().translate(transind), ogsl_valid)
    return ogsl_valid


# # Apply the Function
# The `ogsl_v` function is now applied to each row (`axis = 1`) in the DataFrame. The DataFrame currently has more than 1.1 million rows (lines) and the function may take a few minutes. For that reason a progress bar has been added. The progress bar is part of the `tqdm` library.
# 
# In the first cell of this notebook we initiated the use of tqdm with pandas with the line `tqdm.pandas()`. Instead of the regular `apply()` function from the `pandas` library we may now use `progress_apply()` to do the same thing as `apply()`, but with a progress bar.

# In[ ]:


df["text"] = df.progress_apply(ogsl_v, axis = 1) 


# # Check for Remaining X-signs
# Any remaining capital X should indicate an illegible sign - or else the script has run into an inconsistency. Such errors may be caused by
# - square brackets occuring immediately before X (as in gari[g]X).
# - X-values that are not explained in the `comments` column.
# - other irregularities in transcription and/or comments.

# In[ ]:


df[df.text.str.contains('X')]


# # Pickle for Future Use
# Pickle the DataFrame for future use.

# In[ ]:


pickled = "output/bdtns.p"
df.to_pickle(pickled)


# # Dump in JSON Format for Distribution
# And/or dump the DataFrame in [JSON](https://www.json.org/) format to share the data with others.

# In[ ]:


json = 'bdtns.json'
with open(f'output/{json}', 'w', encoding='utf-8') as w: 
    df.to_json(w, orient='records', force_ascii=False)


# In[ ]:




