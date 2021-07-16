#!/usr/bin/env python
# coding: utf-8

# # Build Sign Search for BDTNS
# Goal of this notebook is to search the [BDTNS](http://bdtns.filol.csic.es) data by signs, irrespective of their reading. For instance, the sign NE may be read bi₂, ne, izi, šeŋ₆, kum₂, lam₂, zah₂, etc. It is easy to search for transliteration (and/or metadata) in the [BDTNS](http://bdtns.filol.csic.es) search page, but there is currently no way to search for a sequence of signs. This is useful, in particular, in two situations. 
# 
# 1. Sumerological transliteration conventions may differ quite substantially between different schools. Thus, lu₂ kin-gi₄-a, {lu₂}kin-gi₄-a, lu₂ kiŋ₂-gi₄-a and {lu₂}kiŋ₂-gi₄-a all represent the same sequence of signs and the same word (meaning 'messenger'), but without knowledge of the particular set of conventions used it may be difficult to guess which search will yield the desired results. In the sign search one may enter sign readings according to any convention recognized by the ORACC Global Sign List ([OGSL](http://oracc.org/ogsl)).
# 
# 2. In some cases the correct reading and interpretation of a sign sequence may be unclear and this ambiguiuty may have been resolved in different ways throughout the database. The names lugal-mudra₅, lugal-zuluhu₂ and lugal-siki-su₁₃ all represent the same sign sequence. Which of these is correct is not entirely clear (although the third seems unlikely) and, depending on the research question, may even be unimportant (for instance for an SNA analysis). In the sign search one may enter any of these forms and the results will include all of them.

# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # this suppresses a warning about pandas from tqdm
import pandas as pd
pd.set_option('display.max_rows', None)
from tqdm.auto import tqdm  # tqdm.auto will activate the notebook version when called from a notebook
tqdm.pandas() # initiate progress bars for pandas
import os
import sys
import re
import pickle
import zipfile
import json
from ipywidgets import interact # User Interface for search
import ipywidgets as widgets
from IPython.display import display, clear_output
util_dir = os.path.abspath('../utils') # make Compass utilities available
sys.path.append(util_dir)
import utils


# ## 0 Create Directories, if Necessary
# The two directories needed for this script are `jsonzip` and `output`.

# In[ ]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# ## 1 Download the OGSL ZIP file
# The sign search uses the ORACC Global Sign List [OGSL](http://oracc.org/ogsl), available in JSON format at http://build-oracc.museum.upenn.edu/json/ogsl.zip. The function `oracc_download()` from the `utils` module downloads the JSON file in ZIP format. The function expects a list as its sole argument.

# In[ ]:


project = ["ogsl"] # oracc_download() expects a list
p = utils.oracc_download(project)


# # 2 The `parse_ogsl_json()` function
# The function iterates through the JSON object. The output is a dictionary where each possible reading, listed in [OGSL](http://oracc.org/ogsl) is a key, the value is the sign name of that reading. For instance
# ```python
# {'u₄' : 'UD', 'ud' : 'UD', 'babbar' : 'UD'}
# ```
# etc.
# 
# In the process of parsing the JSON the sign list is adapted to reflect Ur III writing. Some signs that are distinguished in [OGSL](http://oracc.org/ogsl) coincided in the Ur III period. For instance, the signs NI₂ and IM, which are different in the Fara period, are the same in Ur III. Such signs are listed in the dictionary `equiv`, which is used in the `parse_ogsl_json()` function. When adding more signs to the dictionary, make sure to use the canonical sign names as defined in [OGSL](http://oracc.org/ogsl).

# In[ ]:


equiv = {'ANŠE' : 'GIR₃', 
        'DUR₂' : 'KU', 
        'NAM₂' : 'TUG₂', 
        'TIL' : 'BAD', 
        'NI₂' : 'IM',
        'ŠAR₂' : 'HI', 
        'ZI₃'  : 'EŠ₂'
        }


# In[ ]:


def parse_ogsl_json(data_json):
    value2signname = {}
    word = re.compile(r'\w+') # replace whole words only - do not replace TILLA with BADLA.
                           # but do replace |SAL.ANŠE| with |SAL.GIR₃|
    for sign_name, sign_data in data_json["signs"].items():
        sign_name = re.sub(word, lambda m: equiv.get(m.group(), m.group()), sign_name)
        if "values" in sign_data:
            for reading in sign_data["values"]:
                value2signname[reading] = sign_name
    return value2signname


# # 3 Process the JSON
# In the main process the file `ogsl-sl.json` is extracted from the zip and made into a JSON object (with the `json.loads()` function). This object is sent to the `parsejson()` function defined above.

# In[ ]:


file = "jsonzip/ogsl.zip"
zip_file = zipfile.ZipFile(file) 
filename = "ogsl/ogsl-sl.json"
signlist = zip_file.read(filename).decode('utf-8')
data_json = json.loads(signlist)                # make it into a json object (essentially a dictionary)
value2signname = parse_ogsl_json(data_json)  
with open('output/ogsl_dict.p', 'wb') as p:
    pickle.dump(value2signname, p)  


# # 4 Inspect the Results in Dataframe
# This DataFrame is only for inspection - it is not otherwise used in the code below.

# In[ ]:


ogsl = pd.DataFrame.from_dict(value2signname, orient='index', columns = ["Name"]).sort_values(by = 'Name')
ogsl[1000:1025]


# # 5 Open BDTNS Data
# We can now open the dataframe with the [BDTNS](http://bdtns.filol.csic.es) transliterations. This dataframe was pickled in notebook [2_4_1_Data_Acquisition_BDTNS.ipynb](./2_4_1_Data_Acquisition_BDTNS.ipynb). The dataframe has five fields: `id_text` (the [BDTNS](http://bdtns.filol.csic.es) number of a document), `id_line` (a continuous line numbering that starts at 1 for each new document; integer), `label` (the regular, human legible [BDTNS](http://bdtns.filol.csic.es) line number), `text` (the transliteration of the line) and `comments` (any comments added to the line in [BDTNS](http://bdtns.filol.csic.es)).

# In[ ]:


file = 'output/bdtns.p'
bdtns = pd.read_pickle(file)
bdtns.head()


# # 6 Tokenizing Signs
# In order to search by sign, we need to tokenize signs in the transliteration column (`text`) while ignoring elements such as question marks or (half-) brackets. First step is to define different types of separators, and flags that may be present in the text or in the sign name. The most common separators are space and hyphen. Curly brackets are placed around determinatives (semantic classifiers), as in {d}En-lil₂ ("the god Enlil"). Curly brackets and hyphens will be replaced by spaces. The separators in `separators2` are used in compound signs, as in |SI.A|, or |ŠU+NIGIN|. Operators, finally, are also used in compound signs and indicate how the signs are written in relation to each other (on top of each other, one inside the other, etc.). Compound signs that represent a sequence of simple signs (|SI.A| for **dirig** or |A.TU.GAB.LIŠ| for **asal₂**) will be decomposed in their component signs. Compound signs of the type |KA×GAR| (for **gu₇**) are not analyzed, but their component parts are aligned with [OGSL](http://oracc.org/ogsl) practices (that is |KA×NINDA| will be re-written as |KA×GAR|, because in [OGSL](http://oracc.org/ogsl) GAR is the name of the sign that can be read **ninda** or **gar**).
# 
# Finally the flags include various characters that may appear in the transliteration but will be ignored in the search. A search for `ninda`, therefore, will find `ninda`, `[nin]da`, `ninda?`, etc., as well as `gar`, `⸢gar⸣`, `gar!(SIG)`, etc. (but not `nagar`, see below).
# 
# The variable `flags2none` represents a table in which each character in `flags` corresponds to `None`. This is used by the `translate()` method; see below.

# In[ ]:


separators = ['{', '}', '-']
separators2 = ['.', '+', '|']  # used in compound signs
#operators = ['&', '%', '@', '×']
flags = "][?<>⸢⸣⌈⌉*/" # note that ! is omitted from flags, because it is dealt with separately
flags2none = str.maketrans(dict.fromkeys(flags))


# In[ ]:


def translit_to_signnames(translit):  
    """This function takes a string of transliterated cuneiform text (in any transliteration style) and translates that string into a string of
    sign names, separated by spaces. In order to work it needs the variables separators, separators2, and flags2none defined above. The variable flags2none
    is used by the translate() method to translate all flags (except for !) to None. The function also needs a dictionary, called value2signname, that has as
    keys sign readings and sign names as corresponding values. In case a key is not found, the sign reading is replaced by itself."""
    signnames_l = []
    translit = translit.translate(flags2none).lower()  # remove flags, half brackets, square brackets.
    translit = translit.replace('...', 'x')
    for separator in separators: # split transliteration line into signs   
        translit = translit.replace(separator, ' ').strip()
    signs_cleaned = translit.split() # s_l is a list that contains the sequence of transliterated signs without separators or flags
    signs_cleaned = [value2signname.get(sign, sign) for sign in signs_cleaned] # replace each transliterated sign with its sign name.
    # Now take care of some special situations: signs with qualifiers, compound signs.
    for sign in signs_cleaned:
        if '!' in sign: # corrected sign, as in ka!(SAG), get only the corrected reading.
            sign = sign.split('!(')[0]
            sign = sign.replace('!', '') # remove remaining exclamation marks
        elif sign[-1] == ')' and '(' in sign: # qualified sign, as in ziₓ(SIG₇) - get only the qualifier
            sign = sign.split('(')[1][:-1]
        if '×' in sign: #compound. Compound like |KA×NINDA| to be replaced by |KA×GAR|
            sign_l = sign.replace('|', '').split('×')
            #replace individual signs of the compound by OGSL names
            sign_l = [value2signname.get(sign, sign) for sign in sign_l] 
            # if user enters |KA*EŠ| this is transformed to ['KA', '|U.U.U|']. The pipes around U.U.U must be replaced by brackets
            sign_l = [f'({sign[1:-1]})' if len(sign) > 1 and sign[0] == '|' else sign for sign in sign_l]
            sign = f"|{'×'.join(sign_l)}|"  #put the sign together again with enclosing pipes.
        elif '.' in sign or '+' in sign: # using elif, so that compounds like |UD×(U.U.U)| are not further analyzed.
            for separator in separators2:
                sign = sign.replace(separator, ' ').strip() 
            sign_l = sign.split()  # compound sign split into multiple signs
            sign_l = [value2signname.get(sign, sign) for sign in sign_l]
            signnames_l.extend(sign_l)
            continue
        sign = value2signname.get(sign, sign)
        signnames_l.append(sign)
    # add space before and after each line so that each sign representation is enclosed in spaces
    signnames = f" {' '.join(signnames_l).upper()} " 
    return signnames


# The function `translit_to_signnames()` is called for every row in the `bdtns` dataframe with the `map()` function. The output is stored in a new column of that same dataframe called `sign_names`. The function `progress_map()` adds a progress bar to the regular `map()` function; `progress_map()` is activated by `tqdm.pandas()` in the first cell of this notebook.
# 
# After running this cell the `bdtns` dataframe will have a column `sign_names` that represents a single line of text as a sequence of sign names as in " KI UR AN EN KID TA " (for ki ur-{d}en-lil₂-ta).

# In[ ]:


bdtns["sign_names"] = bdtns["text"].progress_map(translit_to_signnames)


# # 7 Adding Metadata
# Open the [BDTNS](http://bdtns.filol.csic.es) catalog DataFrame (pickled in section 2.4.1) and add provenance, date, and publication to each row. Note that in the [BDTNS](http://bdtns.filol.csic.es) transliteration file the [BDTNS](http://bdtns.filol.csic.es) numbers are strings, whereas in the catalog file they are integers.

# In[ ]:


p = 'output/bdtns_cat.p'
cat_df = pd.read_pickle(p)
date_d = dict(zip(cat_df['id_text'], cat_df['date']))
prov_d = dict(zip(cat_df['id_text'], cat_df['provenance']))
publ_d = dict(zip(cat_df['id_text'], cat_df['publication']))
bdtns['provenance'] = [prov_d.get(int(idt), '') for idt in bdtns['id_text']]
bdtns['date'] = [date_d.get(int(idt), '') for idt in bdtns['id_text']]
bdtns['publication'] = [publ_d.get(int(idt), '') for idt in bdtns['id_text']]


# In[ ]:


bdtns.to_pickle('output/bdtns_tokenized.p')


# # 8 The Search Function
# The search function takes as input any style of transliteration recognized in [OGSL](http://orac.org/ogsl) in upper or lower case (see the search instructions below).  
# 
# The search engine will find any matching sequence of signs, independent of the transliteration, thus 'nig2 sig' will also find 'ninda sig' or 'nig2-sig' or 'gar-sig' etc.
# 
# The search results are listed in a DataFrame with links to the [BDTNS](http://bdtns.filol.csic.es) pages of the matching texts.

# In[ ]:


digits = '0123456789x'
indexes = '₀₁₂₃₄₅₆₇₈₉ₓ'
input_char = '{}-cjĝ*'
translate_to = '   šŋŋ×'
index = str.maketrans(digits, indexes)
char = str.maketrans(input_char, translate_to)
ind = re.compile(r'[a-zŋḫṣšṭA-ZŊḪṢŠṬ][0-9x]{1,2}') # regular expression for a letter
                                                   # followed immediately by one or two digits or x
anchor = '<a href="http://bdtns.filol.csic.es/{}", target="_blank">{}</a>'


# In[ ]:


def search(Search, Max_hits, Links, Sortby = 'id_text'): 
    search_term = Search.lower().replace('sz', 'š').translate(char).strip() # replace sz by š; translate c, j, ĝ, and * to š, ŋ, ŋ, and ×, respectively.
    search_term = re.sub(ind, lambda m: m.group().translate(index), search_term) #translate regular numbers (and x) to index numbers
    search_term = translit_to_signnames(search_term)  # replace a sequence of transliterated signs by a sequence of sign names
    search_term_esc = re.escape(search_term) # use escapes for characters that have special meaning in regular expressions
    search_term_esc = search_term_esc.replace('\ X\ ', '(?:\ [^ ]+)*\ ') # use X (preceded and followed by space) as wild card for any sequence of signs
    show = ['id_text', 'label', 'text', 'provenance', 'date', 'publication']
    results = bdtns.loc[bdtns['sign_names'].str.contains(search_term_esc, regex=True), show].copy() # this is the actual search command
    hits = len(results)
    if Max_hits > hits: 
        Max_hits = hits 
    if hits == 1:
        pl = ''
    else:
        pl = 's'
    print(search_term), print(f"{str(hits)} hit{pl}; {str(Max_hits)} displayed.")
    results = results.sort_values(by = Sortby)[:Max_hits]
    if Links:
        results['id_text'] = [anchor.format(val,val) for val in results['id_text']]
        results = results.style.hide_index().set_properties(subset=['publication'], **{'width': '200px'})
    return results


# # 9. Creating a User Interface
# The user interface is created with widgets from the package `ipywidgets`. Widgets are pieces of software that allow a user to interact with functions through text boxes, sliders, buttons, drop-down menus, check boxes, etc. These widgets contain code in javascript and are treated differently in Jupyter Notebook and Jupyter Lab. Jupyter Notebook allows the embedding of any kind of javascript code. For safety reasons, this is not the case in Jupyter Lab. The Jupyter widgets need to be installed as a Jupyter Lab extension before they can be run; enabling Jupyter Lab extensions, in turn, requires `node.js`. For more information about installing and enabling the extension (including node.js) see [install_packages.ipynb](../1_Preliminaries/install_packages.ipynb). For detailed information about widgets, see [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/).
# 
# The widgets used here are
# - Button - when clicked, the search function is called
# - Text - a text box in which the user may enter a sequence of signs; after hitting ENTER (or clicking the Search button) the search function is called
# - BoundIntText - a text box that indicates the maximum number of hits (default is 25)
# - Checkbox - when checked (default) the search results display active links to BDTNS pages. When maximum hits is set to larger than 250 the default becomes unchecked.
# - Dropdown - a drop-down menu for arranging the search results by different columns.
# 
# In addition, a number of special widgets are used, namely 
# - Vbox, for displaying widgets vertically
# - Hbox, for displaying widgets horizontally
# - Output, an area where the search output is displayed
# 
# The code for each widget consists of several parts. First, the widget is called with various parameters, such as its default value, or the text that is to appear on a button. Second is a function that defines what happens when the button is clicked, or when the user hits the ENTER button. Third, a method for each of the widgets defines what event will trigger the function. For the button it is the event `on_click`, for the text box it is `on_submit` (that is, when the user hits ENTER); the other three widgets listen for a change in value with the `observe` method. Finally, the VBox and HBox widgets define the layout. 

# In[ ]:


# Creating a User Interface
button = widgets.Button(description='Search')
text = widgets.Text(
       value='',
       description='', )
maxhits = widgets.BoundedIntText(
        value=25,
        min=0,
        max=len(bdtns),
        step=1,
        description='Max hits:',
        continuous_update = True)
links = widgets.Checkbox(
    value=True,
    indent = False,
    description='Display Links')
sortby = widgets.Dropdown(
    options = ['id_text', 'text', 'date', 'provenance', 'publication'],
    value = 'id_text',
    description = 'Sort By: ')
out = widgets.Output()
def submit_search(change):
      # "linking function with output"
        with out:
          # what happens when we press the button
            clear_output()
            display(search(text.value, maxhits.value, links.value, sortby.value))
# when maxhits is set larger than 250, default becomes no links
def update_maxhits(change):
    links.value = maxhits.value < 250
    submit_search(change)
# linking button to search function the button's method
button.on_click(submit_search)
# linking text box to search function - called when user hits ENTER.
text.on_submit(submit_search)
# linking drop-down menu and search function - called when the value of the drop-down menu changes
sortby.observe(submit_search, 'value')
# linking the maximum hits box and search function - called when the value changes
maxhits.observe(update_maxhits, 'value')
# linking the links checkbox and search function - called when its value changes
#links.observe(submit_search, 'value')
# displaying the widgets and output together
col1 = widgets.VBox([text, links, button]) # first column: text box, checkbox, and button
col2 = widgets.VBox([maxhits, sortby]) # second column: Maximum Hits and drop-down menu.
box = widgets.HBox([col1, col2]) # put first and second column next to each other in a row
widgets.VBox([box,out]) # add ouput below the widgets.


# # 10 Alternative Interface
# The following alterative interface is much simpler in its coding (essentially letting the `interact` function do all the work). To be useful, this interface requires a fairly fast machine because the search will update live while you type. The interface uses the same search function as above, so search instructions and results are the same.

# In[ ]:


interact(search, Search = '',
        Max_hits = widgets.BoundedIntText(
        value=25,
        min=0,
        max=len(bdtns),
        step=1,
        description='Max hits:',
        continuous_update = True), 
        Links = True, 
        Sortby = ['id_text', 'text', 'date', 'provenance', 'publication'] );


# # 11 Search Instructions
# 
# Search for a sequence of sign values in any transliteration system recognized by [OGSL](http://oracc.org/ogsl). Thus, sugal₇, sukkal, or luh, in upper or lower case will all return the same results.
# 
# - Determinatives (semantic classifiers) may be entered between curly brackets or as regular signs. Thus, gesz taskarin, gesz-taskarin, {gesz}taskarin, and {ŋeš}tug₂ will all yield the same results. 
# 
# - Signs may be connected with spaces or hyphens.
# 
# - The Shin may be represented by š, c, or sz in upper or lower case; nasal g may be represented as j, ŋ, or ĝ.
# 
# - Sign index numbers may be represented by regular numbers or by index numbers (e₂ or e2, but not é).
# 
# - Compound signs (such as diri) are resolved in their component signs if the compound represents a simple sequence of signs. Thus diri is resolved as SI A, but gu₇ is resolved as |KA×GAR|.
# 
# - To search for a compound sign by sign name, enter it between pipes (|). The "times" sign may be represented by \* (enter |UR₂×A| or |UR₂\*A|, but not |URxA|).
# 
# - Wildcard: x or X, represents any number of signs in between (e.g. ku6-x-muszen will find all lines where HA is followed by HU with zero or more signs in between).
# 
# - For large numbers of hits, the clickable links to [BDTNS](http://bdtns.filol.csic.es/) editions will make display very slow. Unclick the check box to display [BDTNS](http://bdtns.filol.csic.es/) numbers only, without links. Setting the number of hits higher than 250 will change the default to no links.

# In[ ]:




