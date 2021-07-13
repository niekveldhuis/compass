## 2.4.1 Data Acquisition BDTNS

The Database of Neo-Sumerian Texts ([BDTNS][]) was created by Manuel Molina (Consejo Superior de Investigaciones Científicas). The site provides a detailed catalog of the administrative, legal, and epistolary documents from the so-called Ur III period (21st century BCE). Molina estimates that museums and private collections all over the world may hold at least 120,000 such documents, not including the holdings of the Iraq Museum, Baghdad. Currently, almost 65% of those documents are available through [BDTNS][] in transliteration, and/or in photograph and line drawing. 

There is a considerable overlap in the data sets offered by [CDLI][] and [BDTNS][]. All photographs and line drawings of Ur III tablets that are available in [CDLI][] have been imported into [BDTNS][]; in addition, [BDTNS][] offers its own collection of thousands of photographs, in particular of tablets now in the British Museum, London. The initial core of the [BDTNS][] transliterations was provided by Remco de Maaijer and Bram Jagersma (Leiden University), who prepared tens of thousands of Ur III texts and distributed those data freely. This same set of transliterations was also one of the initial data sets of [CDLI][]. Close cooperation between the two projects has led to further exchange of data. Not infrequently, therefore, misreadings or simple typos appear in the same way in both projects.

Still, [BDTNS][] is not simply a duplicate of the Ur III data in [CDLI][]. Most Ur III scholars today prefer [BDTNS][] over [CDLI][] because the smaller focus of the Spanish project implies that there is more attention to detail and that more effort is made to update the record. One example is the book *Der König und sein Kreis* (2012)[^1] in which Paola Paoletti studied in detail several hundred documents from the so-called treasure archive at Puzriš-Dagan. This archive reports on the manufacturing of luxury goods made of precious metals and leather and includes many rare words. Since the archive (like almost all Ur III archives) is scattered over museums all over the world, most of these texts were published as single documents or in small groups. Studying the entire group frequently allowed Paoletti to arrive at a more satisfying reading and understanding than the original editor's. The [BDTNS][] editions of these texts reflect Paoletti's improvements, but the [CDLI][] editions not (yet).

The [BDTNS][] data can be downloaded by hand through the [Search](http://bdtns.filol.csic.es/index.php?p=formulario_urIII) option in the Catalogue & Transliterations drop-down menu. One can search by a variety of criteria (including word and grapheme strings) and then download the search results by clicking on the Export button. The export page provides options for the types of information to include (various types of meta-data and/or transliterations). By searching for a blank string one may export the entire data set. The export yields two files: one for the meta-data and one for the  transliterations, both in raw text (`.txt`) format.

### 2.4.1.1 Vertical TABs

The [BDTNS][] transliteration files use "vertical TABs", represented by ^K, \v, or \x0b (depending on which editor is used for reading the file). These "vertical TABS" are inserted between lines that belong to the same document; the regular newline character is used to separate one document from the next. Because of those vertical tabs, the following code will lead to somewhat problematic results:

```python
with open("query_text_19_03_1-210747.txt", encoding="utf8") as b: 
    bdtns = b.readlines()
```

The `readlines()` function does not recognize the vertical tab as a newline character. The code, therefore, will result in a list that has one entry for every document, with ^K separating the lines within a document. The issue can be circumvented by reading the entire document as a single string with the `read()` function, and then split the string with the `splitlines()` function, as follows:

```python
with open("query_text_19_03_1-210747.txt", encoding="utf8") as b: 
    bdtns = b.read().splitlines()
```

The `splitlines()` function does recognize the vertical tabs as newline characters, and this code results in a list with each line in the original `.txt` file as a separate element of that list.

### 2.4.1.2 Format as DataFrame

In order to format this data in a DataFrame we first need to look for lines that indicate a new document. In the [BDTNS][] export file such lines begin with a six-digit number, for instance:

> 	038576	AAICAB 1/1, Ashm. 1911-146 = CDLI P142659

We can isolate the [BDTNS][] number (which can also be used to create a URL of the format http://bdtns.filol.csic.es/038576) by selecting the first six characters of the line:

```python
if line[:6].isdigit(): 
	bdtns_no = line[:6]
```

All other lines are transliteration lines that may have one or more of the following:

- line number in the format 'o.ii 5' (obverse column ii line 5)
- transliteration
- editorial remarks

Line numbers are separated from transliteration by five spaces. Editorial remarks (which may indicate the presence of a seal impression, an erased line, or provide an alternative reading) are introduced by the hash mark and are placed at the end of the line. A specific type of editorial remark is the sign name, which explains an x-value (see below section 2.4.1.3), a rare sign form, or a rare sign reading. These particular editorial remarks have the form (=SIGN NAME).

The script replaces the five spaces with a hash mark and '(=' with '#(=', so that we can use the hash mark to split the line in (potentially) three elements: line number, transliteration, and editorial comment. Both types of editorial comments (sign names and true comments) end up in the third column. We then prefix each line with the [BDTNS][] number that was isolated previously, and with a counter (`id_line`) that is set to zero for each new document. The field `id_line` is an integer that can be used to keep or to restore the proper order of the lines within a document. The full code looks as follows:

```python
l = []
id_text = ""
id_line = 0
for line in tqdm.tqdm(bdtns): 
    if line[:6].isdigit(): 
        id_text = line[:6]
        id_line = 0
        continue
    else: 
        id_line += 1
        li = line.strip()
        li = li.replace("(=", "#(=", 1).replace('     ', '#', 1)
        li_l = li.split('#', 2)
        li_l = [bdtns_no, id_line] + li_l
        l.append(li_l)
```

This results in a list of lists called `l` that contains the same data as the original `bdtns` list, but in a more explicit format, seperating between text and non-text. This list of lists is transformed into a five-column DataFrame with column names `id_text` (the [BDTNS][] number), `id_line` (an integer, starting at 0 for each document), `label` (the traditional line number), `text` (transliteration), and `comments` (holding comments as well as sign explications).

### 2.4.1.3 X-values

A peculiarity of the [BDTNS][] data set is the way so-called x-values are represented. In Assyriology, x-values are sign readings that have not (yet) received a conventional index number. For instance, the (very common) word  for "to cut (reeds)" is written either with the sign **zi** or with the sign **SIG₇**. Based on the distribution of those spellings (**SIG₇** only in Umma, **zi** elsewhere), M. Molina and M. Such-Guttiérez (2004)[^2] concluded that both spellings write the same word /**zi**/. On that basis the new reading **/zi/** for the sign **SIG₇** was introduced (and is now commonly accepted among Sumerologists). In such cases one may transliterate **ziₓ(SIG₇)** where the SIG₇ between brackets is the name of the sign transliterated as **ziₓ** (and thus the principle of a one-to-one mapping of a transliterated token to a cuneiform sign is maintained). In the [BDTNS][] export file this is represented as follows: 

> 	o. 2     gi ziX-a 12 sar-⌈ta⌉ (=SIG7)		cut reed per 12 *sar* of field

The index ₓ is represented by a capital X (as in ziX), and the sign name is added at the end of the line, between parens and preceded by the equal sign. 

In order to use this data for computational purposes (for instance computing sign frequencies) it is necessary to move the sign specification and to transform this into

> 	o. 2     gi ziₓ(SIG7)-a 12 sar-⌈ta⌉ 

It is possible to do so with a script or regular expression, and to move the sign name to the position immediately after the capital X. Before we do so, it is useful to inspect some exceptions to the pattern. In some cases sign names are provided for rare readings, for instance:

> 	18 gin2 nagga mu-kuX gibil (=AN.NA) (=DU)

If we naively move the first sign name to the first X, we will get:

> 	18 gin2 nagga mu-kuX(AN.NA) gibil  (=DU)

(=AN.NA), in this case, explains the rare reading **nagga** (tin, or some similar substance), whereas (=DU) explains **kuX** - but there is no obvious way for a regular expression or script to recognize that. Another type of exception is reduplicated "gurₓ-gurₓ" (to reap) which is represented thus:

> 6.0.0 še ur5-ra še gurX-gurX-ta su-ga (=ŠE.KIN.ŠE.KIN)

which, if we naively moved the sign name, would result in:

> 	6.0.0 še ur5-ra še gurₓ(ŠE.KIN.ŠE.KIN)-gurₓ-ta su-ga

The issue is solved by approaching the x-values in two separate ways. First, unambiguous x-values (those that are always resolved in the same way) are replaced with the help of a dictionary that lists the x-values with their resolutions. This dictionary includes the most common x-values encountered in [BDTNS][]. Second, for ambiguous x-values the sign explication in [BDTNS][] is used. Both search-and-replace actions are performed in the function `ogsl_v()`, which is applied to each row  of the DataFrame. In addition to resolving x-values, the function `ogsl_v()` also replaces regular numbers (as in **du3**) by unicode index numbers (**du₃**), while leaving alone regular numbers that express quantities (**7 sila4** becomes **7 sila₄**).

For `ogsl_v()` to run properly and efficiently, a number of translation tables, dictionaries, and compiled [regular expressions](https://www.regular-expressions.info/) are defined before the function is called. A detailed explanation of how `ogsl_v()` works is found in the notebook itself.

Since `ogsl_v` is applied to more than a million rows in a dataframe, it is necessary to keep track of progress. This is done using the `tqdm` library which is imported as follows:

```python
from tqdm.auto import tqdm
tqdm.pandas()
```

Importing `tqdm` from the `tqdm.auto` submodule allows `tqdm` to run either in notebook mode (with colored progress bars) or in regular mode. The expression `tqdm.pandas()` initiates the `pandas` integration and allows the use of `progress_apply()` and `progress_map()` instead of the regular `pandas` functions `apply()` and `map()`.

The resulting DataFrame distinguishes between text data (the column `text`) and other data (line numbers, comments, text ID numbers) and follows as much as possible the specifications of the ORACC Global Sign List ([OGSL](http://oracc.org/ogsl)).

### 2.4.1.4 Save

Finally, the newly created DataFrame with [BDTNS][] data is saved in two ways. The `to_pickle()` function of the `pandas` library is used to created a pickle, a file that can be opened in a future session to recreate the DataFrame. Second, the DataFrame is saved in JSON format, a format that is more suitable for sharing with other researchers. Both files are saved in the `output` directory.

## 2.4.2 Building Sign Search

Combining the data from [BDTNS][], as prepared in the previous section, with data from the ORACC Global Sign List ([OGSL][]) we can build a search engine for [BDTNS][] that finds a sequence of signs, independent of the particular reading employed in the transliteration. The sign search is built here primarily as an example of the kinds of things one can do with data as produced in 2.4.1 (standardized and with proper separation between text data and non-text data).

The code downloads and parses the JSON zip file that contains all the [OGSL][] data. The result is a dictionary that provides for each sign reading (key) the corresponding sign name (value). This dictionary is used to add a new column (`sign_name`) to the [BDTNS][] DataFrame that was created above. This new column represents the same line of text, now as a sequence of sign names, ignoring flags (such as question marks, square brackets, etc.).

Thus the line 
> \[lu\]kur-ki-ag₂ lugal 

is represented in the column `sign_name` as 

> SAL ME KI |NINDA₂×NE| LUGAL

The [OGSL][] dictionary returns |SAL.ME| for lukur and |NINDA₂×NE| for ag₂. Since |SAL.ME| represents a sign sequence that, at least in theory, could also be read as a sequence of any of the values of SAL and ME, it is represented in the `sign_name` column as the sequence SAL ME and therefore a search for lukur will also find, for instance, munus-me. Such re-analysis is not possible for |NINDA₂×NE| (the sign NE inscribed in the sign NINDA₂), and thus such compounds are not split.

The same function that is used to transform a line of transliteration into a sequence of sign names is also used by the search engine for transforming the user input. User input is thus also transformed into a sequence of sign names, using the same [OGSL][] dictionary, and compound signs such as **lukur** are separated into their constituent signs (SAL ME). As a result, search for **lukur**, **sal-me**, or **munus išib** will all yield the same results.

When searching for **sar-ki**, however, we should not find **sar kin**, in other words, the search should identify only full sign names. Sign names are separated from each other by spaces. By adding a space before and after each line (in the `sign_name` column) each individual sign is preceded and followed by a space, even when it appears at the beginning or the end of the line. The (transformed) search input is also put between spaces.

> A more common approach to the "whole sign" issue would be to add the regular expression \\b ("word boundary") before and after the input. However, this fails on sign names that begin and end with pipes (as in |NINDA₂×NE|), because the pipe is not considered a word character in regular expressions. It is possible to add look-behind and look-ahead regular expressions to take care of this issue. The expression would look like this: '(?:(?<=\s)|(?<=^))'+signs+'(?=\s|$') where `signs` represents the (transformed) search input. As it turns out, this works, but since look-behind and look-ahead expressions are relatively slow, it was decided to circumvent the problem with the extra spaces.

In the output the columns `id_text`, `label` (line number), and `text` are shown (not `sign_name`). By default, the search displays only the first 25 hits and the `id_text` (the [BDTNS][] number) is used to create a link to the text in question. The Max hits box and the checkbox may be used to increase the number of displayed hits and/or to switch off the links. For larger number of hits, styling the `pandas` output to create these links may be rather slow and so by default with Max hits larger than 250 the links are switched off.

The search engine uses "widgets" (pieces of software to create a user interface) to call the search function and display the results. It creates a text box (for the search term), a numerical text box (for the maximum number of hits), a checkbox and a button, to be clicked to run the search. A drop-down menu provides the possibility to order search results in a variety of ways (note that ordering by date is done alphabetically - Amar-Sîn dates will thus come before Shulgi dates). On a fast machine one may do away with the button and have the software react immediately to user input (see Alternative Interface in the notebook).

Detailed search instructions are found in the Notebook.

## 2.4.3 Search BDTNS
The final notebook in section 2.4 is called `2_4_3_Search_BDTNS.ipynb`. It offers the same search functionality as the search built in section 2.4.2, but it mostly hides the code and does not create the files necessary for the search - assuming they are already there. In other words, before using this notebook for the first time, first run `2_4_1_Data_Acquisition_BDTNS.ipynb` and `2_4_2_Build_Sign_Search.ipynb`(in that order) to create the files `bdtns_tokenized.p`and `ogsl_dict.p` that are used by the code in `2_4_3_Search_BDTNS.ipynb`. Afterwards, you can continue to use the same files and run the search again, or you can rebuild them and capture the latest data from [BDTNS][] and [OGSL][].

The code that is used by the Search is essentially the same as in `2_4_2_Build_Sign_Search.ipynb` but it calls the file `Search_BDTNS.py` in the `py` directory, so that the code itself does not clutter the page.

[^1]: Paola Paoletti, *Der König und sein Kreis: das staatliche Schatzarchiv der III. Dynastie von Ur*, Biblioteca del próximo oriente antiguo 10. Madrid: 2012.

[^2]: Molina, Manuel and Such-Gutiérrez, Marcos, On Terms for Cutting Plants and Noses in Ancient Sumer: *Journal of Near Eastern Studies* 63 (2004) 1-16

[BDTNS]: http://bdtns.filol.csic.es
[CDLI]: http://cdli.ucla.edu
[OGSL]: http://oracc.org/ogsl
