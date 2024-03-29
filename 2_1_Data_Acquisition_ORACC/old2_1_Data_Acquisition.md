## 2.1.5 Enhancing parsejson()

The basic `parsejson()` captures only lemmatization data, it ignores line numbers, text breaks, and other types of information that are included in the JSON files. The basic `parsejson()` is good enough for a "Bag of Words" approach, which looks only at vocabulary frequency, ignoring word order. For many other types of analysis we do need to capture line numbers and text breaks. Such information is stored in "d" nodes in a level above the "l" node in the `cdl` hierarchy. Similarly, sentence identifiers (and other discourse units) are stored in "c" nodes. The `parsejson()` function can easily be enhanced to capture various types of such meta-data storing them in a dictionary called `meta_d`. This dictionary is updated whenever the `parsejson()` function encounters a relevant node. Each row (each word) in the list `lemm_l` receives the current meta-data from `meta_d`. 

### 2.1.5.1 Line Labels and Line IDs

For many types of explorations one may wish to keep together words in a line and order these lines in their proper sequence. In order to do so we need to capture the  `label` of the line and the word ID of each word. The `label` is human-legible and has the traditional format to indicate obverse, reverse, column and line number or side of a prism (e.g. "o ii 7" or "a i 19'"). The field `id_word` is machine -legible and has the format TEXT_ID.LINE_ID.WORD_ID, for instance "P273880.22.1", (the first word of the twenty-second line of [P273880](http://oracc.org/dcclt/P273880.22.1)). In the data formatting stage we will use the word ID to extract the line ID (section [2.1.7.2](#2.1.7.2-Create-Line-IDs)).

We can capture `label` and `id_word` with slight adjustments to the `jsonparser()` and the code that calls that function. In the main process we create a dictionary `meta_d,` which will hold all the relevant meta data. Initially, it only contains the text ID. When the `parsejson()` function finds a dictionary that has the `key` "label" the `key` "label" in `meta_d` gets updated. When the process gets to the lemmatization data the `key` "label" in `meta_d` will hold the proper line label. The word ID is found in the field "ref" in the `l` node, and is added to the `lemma` dictionary. 

```python
def parsejson(text, meta_d):  # this version captures line labels and line IDs
    l = []
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            l.extend(parsejson(JSONobject, meta_d))
        if "label" in JSONobject:
            meta_d["label"] = JSONobject.get("label")
        if "f" in JSONobject:
            lemma = JSONobject["f"]
            lemma["id_text"] = meta_d["textid"]
            lemma["label"] = meta_d["label"]
            lemma["id_word"] = JSONobject["ref"]
            l.append(lemma)
    return l
```
Before the new `parsejson()` function can be called we need to create the empty `lemm_l` list as well as the `meta_d` dictionary. Both wil be changed by the `parsejson()` function. We call `parsejson()` with the arguments `text` (as above) and `meta_d`. The variable `text` holds the JSON of text [P230754](http://oracc.org/obmc/P230754) from the [OBMC](http://oracc.org/obmc) project.

```python
lemm_l = []
meta_d = {"label" : None, "textid": "obmc/P230754"}
lemm_l.extend(parsejson(text, meta_d))
```
When using this version of `parsejson()` in a loop (to acquire data from multiple documents), the loop must update the value of the key `textid` in the meta_d dictionary before calling `parsejson()`.

#### 2.1.5.2 Select a Section

Using this same structure to select a section of a tablet for parsing, the code may be adapted as follows:

```python
def parsejson(text, meta_d):  # this version captures the lemmatization of a partial text
    l = []
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            l.extend(parsejson(JSONobject, meta_d))
        if "label" in JSONobject:
            meta_d["label"] = JSONobject["label"]
        if meta_d["label"] == meta_d["startlabel"]:
            meta_d["keep"] = True
        if meta_d["keep"] == True: 
             if "f" in JSONobject:
                lemma = JSONobject["f"]
                lemma["id_text"] = meta_d["id_text"]
                lemma["label"] = meta_d["label"]
                lemma["id_word"] = JSONobject["ref"]
                l.append(lemma)
        if meta_d["label"] == meta_d["endlabel"]:
            meta_d["keep"] = False
    return l
```
In this case we will use a different example, the text [P273244](http://oracc.org/dcclt/P273244) from [DCCLT](http://oracc.org/dcclt). In order to run this code the file `dcclt.zip` must be downloaded and put in the `jsonzip` folder (see above, section [2.1.2](#2.1.2-Acquiring-ORACC-JSON)).
```python
lemm_l = []
meta_d = {"label" : None, "startlabel": "r 1", "endlabel": "r 5", "keep": False,
             "id_text": "dcclt/P273244"}
file = "jsonzip/dcclt.zip"    
z = zipfile.ZipFile(file)
st = z.read("dcclt/corpusjson/P273244.json").decode("utf-8") 
text = json.loads(st)
if meta_d["startlabel"] == "":
    meta_d["keep"] = True
lemm_l.extend(parsejson(text, meta_d))
```

The text [P273244](http://oracc.org/dcclt/P273244) is a small Middle Babylonian exercise from Nippur with an extract from Gilgameš on the obverse, and a list of wooden objects (doors) on the reverse. The code will constantly refresh the value of the key `label` in the dictionary `meta_d`, while comparing `label` with the value of `startlabel` and `endlabel` to decide where to start and where to stop capturing the lemmatization. In this case only the lexical lines on the reverse are captured, skipping the Gilgameš extract on the obverse.

### 2.1.5.3 Sentences

One type of `c` nodes defines a sentence - a sequence of words that belong together in a self-contained syntactical unit. Such a JSON node may look like this (from [etcsri/Q000376](http://oracc.org/etcsri/Q000376)):

```json
 {
              "node": "c",
              "type": "sentence",
              "implicit": "yes",
              "tag": ".",
              "id": "Q000376.U8",
              "label": "26 - 26",
              "cdl": [
                {
                  "node": "d",
                  "type": "line-start",
                  "ref": "Q000376.26",
                  "n": "26",
                  "label": "26"
                },
                {
                  "node": "c",
                  "type": "phrase",
                  "tag": "phr",
                  "id": "Q000376.U105",
                  "ref": "Q000376.ls00000",
                  "cdl": [
                    {
                      "node": "l",
                      "id": "Q000376.l02092",
                      "ref": "Q000376.26.1",
                      "inst": "szud[prayer]\\abs",
                      "sig": "@etcsri%sux:šud₃\\abs=šud[prayer//prayer, dedication, blessing]N'N$šud.ø/šud₃#N1=šud.N5=ø##N1=STEM.N5=ABS",
                      "f": {
                        "lang": "sux",
                        "form": "šud₃",
                        "delim": "",
                        "gdl": [
                          {
                            "v": "šud₃",
                            "id": "Q000376.26.1.0"
                          }
                        ],
                        "cf": "šud",
                        "gw": "prayer",
                        "sense": "prayer, dedication, blessing",
                        "norm": "šud.ø",
                        "pos": "N",
                        "epos": "N",
                        "base": "šud₃",
                        "morph": "N1=šud.N5=ø",
                        "morph2": "N1=STEM.N5=ABS"
                      }
                    }
```

A subdivision of the sentence is the phrase. Phrases and sentences have their own ID. Obviously, such demarcations are only present in the JSON if the editor of the project (in this case Gábor Zólyomi of [ETCSRI](http://oracc.org/etcsri)) has marked such units (sentences and phrases) in the source files. In order to enable the `parsejson()` function to keep track of sentences, one may simply add another `if` statement to the code, store the sentence ID in the `meta_d` dictionary and add that ID to each word in the list of lemmas:

```python
def parsejson(text, meta_d):  # this version captures sentence IDs
    l = []
    for JSONobject in text["cdl"]:
        if JSONobject.get("type") == "sentence":
            meta_d["sentence"] = JSONobject["id"]
        if "cdl" in JSONobject: 
            parsejson(JSONobject, meta_d)
        if "f" in JSONobject:
            lemma = JSONobject["f"]
            lemma["sentence_id"] = meta_d["sentence"]
            lemma["id_text"] = meta_d["textid"]
            l.append(lemma)
    return l 
```
In the example we will use [Q000376](http://oracc.org/etcsri/Q000376) (The Victory of Utu-hegal) from the [ETCSRI](http://oracc.org/etcsri) project. In order for the code to work, place the file `etcsri.zip` in the `jsonzip` folder (see section [2.1.2](#2.1.2-Acquiring-ORACC-JSON)).
```python
lemm_l = []
meta_d = {"sentence" : None, "textid": "etcsri/Q000376"}
file = "jsonzip/etcsri.zip"    
z = zipfile.ZipFile(file)
st = z.read("etcsri/corpusjson/Q000376.json").decode("utf-8") 
text = json.loads(st)
lemm_l.extend(parsejson(text, meta_d))
```

The initial value of the key `sentence` in the `meta_d` dictionary is `None`, but when the `parsejson()` function encounters a key `type` with value `sentence` it changes the value of `meta_d["sentence"]` to hold the `id` of the sentence. The value of that parameter will stay the same, and is copied into the field `sentence_id` of every row (representing a word) in `l` until the `parsejson()` function encounters a new `"type" : "sentence"` pair. 

Each row (word) in the list `lemm_l` will now have a field `sentence_id` that can be used to identify words that belong together in a sentence - a feature that is particularly important for syntactic parsing in Natural Language Processing and building [treebanks](https://en.wikipedia.org/wiki/Treebank).



### 2.1.5.4 Using parsejson()

In practice, one will rarely wish to parse a single text - as in the examples above. The various `parsejson()` functions discussed above (or any that may be derived) may be embedded in code that uses a list of projects or text ID numbers (optionally provided with `startlabel` and `endlabel`) in order to parse a collection of documents or entire [ORACC](http://oracc.org) projects. Example code for doing so is available in the [Computational Assyriology](https://github.com/niekveldhuis/compass)  repo. The point of discussing some variants of the `parsejson()` function is to demonstrate its flexibility and the possibility of extracting various types of data.

The output of `parsejson()` is a list of words, where each word is represented by a dictionary that includes a number of data elements, including Citation Form, Guide Word, Part of Speech, GDL (grapheme information), Form (transliteration), etc. Some data elements are always present, others are specific for Sumerian or Akkadian, or are only present if the word in question has been lemmatized. For most projects it will be necessary to select and/or manipulate the data (section [2.1.7](#2.1.7-Data-Structuring)).

## 2.1.6 Other Data Types in Text Edition JSON Files

The JSON files for individual text editions include other data types that may be captured by still other permutations of the `parsejson()` function. These data types will be discussed here briefly. 

### 2.1.6.1 Phrasal Semantic Units (Compound Verbs, etc.)

In addition to words, [ORACC](http://oracc.org) recognizes Phrasal Semantic Units ([PSU](http://oracc.museum.upenn.edu/doc/help/lemmatising/psus/index.html)s), including idiomatic expressions, (Sumerian) Compound Verbs, multi-word proper nouns, etc. A PSU consists of multiple words, which are each lemmatized independently but are also indexed as a compound (and listed in the glossary).

In the JSON text edition files the PSUs are listed at the end under the node `linkbase` with references to where the expression appears in the text. The node `linkbase` has as its value a list of dictionaries, each dictionary represents one occurrence of a PSU. The following snippet represents **gu₃ de₂-a-za** ('of your speaking') in [Bau A](http://oracc.org/epsd2/literary/Q000616) Segment C line 9 ([ETCSL 4.02.1](<http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.4.02.1&display=Crit&charenc=gcirc&lineid=c4021.C.5#c4021.C.9>)): 

```json
{"linkbase": [{
          "type": "linkset",
          "xlink_title": "gu de[say//to say (addressing someone),]V/t'V/t",
          "id": "Q000616.ls00009",
          "xlink_type": "extended",
          "xlink_role": "psu",
          "sig": "{gu₃ de₂-a-za = gu[voice]N de[pour]V/t += gu de[say//to say (addressing someone),]V/t'V/t}::@epsd2%sux:gu₃=gu[voice//voice, cry, noise]N'N$gu/gu₃#~++@epsd2%sux:de₂-a-za=de[pour//to pour]V/t'V/t$de;a,zu.ak/de₂#~;a,zu.ak",
          "links": [
            {
              "type": "link",
              "xlink_title": "gu",
              "xlink_type": "locator",
              "xlink_href": "#Q000616.l19760",
              "xlink_role": "elt"
            },
            {
              "type": "link",
              "xlink_title": "de",
              "xlink_type": "locator",
              "xlink_href": "#Q000616.l19761",
              "xlink_role": "elt"
            }
          ]
        }]}
```

The node `linkbase` is an element in the highest level `cdl` list, and can thus be addressed as follows

```python
file = "jsonzip/epsd2-literary.zip"    
z = zipfile.ZipFile(file)
st = z.read("epsd2/literary/corpusjson/Q000616.json").decode("utf-8") 
text = json.loads(st)
cdl = text['cdl']
for n in cdl: 
    if 'linkbase' in n: 
		linkbase = n['linkbase']

```

### 2.1.6.2 Broken Lines

[ORACC](http://oracc.org) editions include information such as "10 lines broken", or "rest of column missing". There is a restricted vocabulary for such annotations, preserved in `d` (Discontinuity) nodes of the type `nonx` (non-textual). The information is found in four fields, named `strict`, `extent`, `scope` and `state`. The field `strict` has the value `"1"` (a string) if the annotation follows the restricted vocabulary (if `"0"`, it may contain all kinds of unstructured information, for instance about joins). A typical node looks like this:

```JSON
{
                  "node": "d",
                  "type": "nonx",
                  "ref": "Q000039.732",
                  "strict": "1",
                  "extent": "3",
                  "scope": "line",
                  "state": "missing"
                },
```

This tells us that at this position in [Q000039](http://oracc.org/dcclt/Q000039) three lines are missing. The reference number belongs to the same number sequence as the line ID numbers (see above section [2.1.5.1](#2.1.5.1-Line-Labels-and-Line-IDs)) and may thus be used to keep the three missing lines in their proper position. The same mechanism is used to record single or double horizontal rulings, as in: 

```json
{
                  "node": "d",
                  "type": "nonx",
                  "ref": "P273880.718",
                  "strict": "1",
                  "extent": "2",
                  "scope": "line",
                  "state": "ruling"
                },
```

This represents a double ruling at the end of the lexical prism [CUSAS 12, 3.1.01](http://oracc.org/dcclt/P273880.718). 

Such information may be captured by looking for nodes that include the key `type` with value `nonx` and add the relevant fields to the list `l` in `parsejson()`. The code for doing so is not discussed in the present chapter, but the [Extended JSON parser](https://github.com/niekveldhuis/compass/blob/master/2_1_Data_Acquisition_ORACC/2_1_3_extended_ORACC-JSON_parser.ipynb) in the [Compass](https://github.com/niekveldhuis/compass) repo does include that functionality.

## 2.1.7 Data Structuring

The output of `jsonparser()` is the list `lemm_l`, a list of dictionaries, where each dictionary represents a single word. This list can be read into a `pandas` DataFrame. DataFrames can be manipulated and sliced in any number of ways and give a visual impression of the structure of the data.

```python
import pandas as pd
words = pd.DataFrame(lemm_l).fillna("")
words
```
For a brief discussion of the `pandas` `fillna()` function see the end of section [2.1.4](#2.1.4-Parsing-an-ORACC-JSON-Text-Edition-File).
### 2.1.7.1 Remove Spaces and Commas from Guide Word

The column "gw" (Guide Word) in the `pandas` DataFrame just created includes bare-bones translations of individual words, such as "king" (for Sumerian lugal) or "(a kind of clamp)" for Akkadian *abāru*. Strictly speaking, Guide Words are not translations but disambiguators - disambiguating between potential homonyms. Akkadian Guide Words are derived from the first meaning in the *Concise Dictionary of Akkadian* (eds. Jeremy Black, Andrew George, and Nicholas Postgate; Harrasowitz Verlag 2000), as discussed in the manual for [ORACC lemmatization](http://oracc.org/doc/help/languages/akkadian/index.html). 

The presence of spaces in Guide Words may cause trouble in a variety of Natural Language Processing methods, because such methods will interpret the space as a word divider. Similarly, commas may cause trouble when saving data in a `.csv` (Comma Separated Values) file, because a comma will be interpreted as the beginning of a new field. 

For text analysis purposes, therefore it is useful to remove all commas and spaces from Guide Word and Sense. The `pandas` `replace()` function takes as its argument a nested dictionary, in which the top-level keys specify in which column the replacements should take place. Each value is a dictionary with find (key) and replace (value) pairs.  By default, `replace()` finds and replaces a full string; we need to set `regex = True` to replace a partial string.

```python
findreplace = {' ' : '-', ',' : ''}
words = words.replace({'gw' : findreplace, 'sense' : findreplace}, regex=True)
```

Now the Guide Word for *abāru* has become `(a-kind-of-clamp)`.

### 2.1.7.2 Create Line IDs

In order to arrange the data in line-by-line format we need to create a line ID that will be added as a new field to each word in the DataFrame. The `id_word` captured by the extended parser (see [2.1.5.1](#2.1.5.1-Line-Labels-and-Line-IDs)) has the format `ID_TEXT.ID_LINE.ID_WORD`, for instance `P338628.4.3`:  the third word of line 4 of [P338628](http://oracc.org/cams/gkab/P338628.4.3) (an astronomical fragment edited in [GKAB](http://oracc.org/cams/gkab)). Note that "4" in this case refers to the very first line of the fragment. The number "4" is not a traditional line number, but rather a reference number that is used to keep lines, breaks, rulings, etc. in their proper place. We can split the ID and keep only the middle part, using the `split()` function:

```python
ids = id_line.split(".")
```

The variable `ids` is now a list that holds the three elements; in our example above:

```python
['P338628', '4', '1']
```

The second element (`ids[1]`) is the one we need (`'4'`). Note that this `'4'`is a string (between quotation marks), not a number. We need to change the data type into integer in order to arrange the lines properly (as string `'4'` comes between `'39'` and `'40'`). Putting all of this together we can create the proper `id_line` field with a list comprehension as follows:

```python
words['id_line'] = [int(wordid.split('.')[1]) for wordid in words['id_word']]
```

The field `id_line` will be used in section [2.1.7.4](#2.1.7.4-Arrange-by-Line-or-by-Document) to arrange the data in line-by-line format.

The [Extended JSON parser](https://github.com/niekveldhuis/compass/blob/master/2_1_Data_Acquisition_ORACC/2_1_3_extended_ORACC-JSON_parser.ipynb) in the [Compass](https://github.com/niekveldhuis/compass) repo captures information about broken lines and horizontal rulings (see section [2.1.6.2](#2.1.6.2-Broken-Lines). Such features have a reference in the format `ID_TEXT.ID_LINE`; that reference is copied to the field 'id_word'.

Note that it would be more straightforward to derive `id_line` from the key "ref" in a `d` node in the `parsejson()`function:

```json
{
                  "node": "d",
                  "type": "line-start",
                  "ref": "Q000376.26",
                  "n": "26",
                  "label": "26"
}
```
```python
	if "type" in JSONobject and JSONobject["type"] == "line-start":
		meta_d["id_line"] = JSONobject["ref"]
		meta_d["label"] = JSONobject["label"]
```

Although this works for most of the JSON files, not all `d` nodes of type "line-start" include the key "ref" and therefore the route through `id_word` is safer.

### 2.1.7.3 Create Lemmas

The DataFrame `words` includes all the fields that were present in the `f` keys of the JSON files we parsed, plus the extra fields (such as `id_line` or `label`) that we have added. It is not likely that we want to keep the DataFrame in this raw format. For many types of analysis one may need the lemma. A lemma, [ORACC](http://oracc.org) style, combines Citation Form, Guide Word and Part of Speech into a unique reference to one particular entry in a standard dictionary, as in `lugal[king]N` (Sumerian) or `nadānu[give]V` (Akkadian). Usually, not all words in a text are lemmatized, because a word may be (partly) broken and/or unknown. The code below will create a new field `lemma` that has the following form:

| status       | lemma      | example       |
| :----------- | :--------- | :------------ |
| lemmatized   | CF[GW]POS  | lugal[king]N  |
| unlemmatized | Form[NA]NA | i-ze₂-x[NA]NA |

```python
words['lemma'] = words["cf"] + '[' + words["gw"] + ']' + words["pos"]
words.loc[words["cf"] == "" , 'lemma'] = words['form'] + '[NA]NA'
words.loc[words["form"] == "", 'lemma'] = ""
words
```

The first line creates the new "lemma" column by concatenating Citation Form, Guide Word and POS. The second and third line take care of two special situations. If there is no Citation Form the word is not lemmatized and the `lemma` column will contain the "form" (the transliterated form of the word) followed by "[NA]NA" (Guide Word and POS unknown). Finally, depending on the version of `parsejson()` that is used, the `words` dataframe may include rows that represent horizontal drawings or broken lines (see section [2.1.6.2](#2.1.6.2-Broken-Lines)). For those entries the "form" is an empty string and the "lemma" should be empty as well.



### 2.1.7.4 Arrange by Line or by Document

The word-by-word representation in the DataFrame `words` may be useful for a "Bag of Words" approach, but for most projects we may want the data either line-by-line, or document-by-document. In `pandas` the `groupby()` and `agg()`(aggregate) functions are used for that purpose. The `groupby()` function takes as its argument the field or fields by which to group the data. If multiple fields are used, they are given in a list. The `agg()` function takes a dictionary as its argument, in which one may indicate for each field how it is to be aggregated. The example below has only one such function: `' '.join` will join all entries that belong to the same line in the column `lemma` with a space in between. Arranging the data by document:

```python
docs = words.groupby("id_text").agg({"lemma": ' '.join})
```

Arranging line-by-line:

```python
lines = words.groupby(["id_text", "id_line", "label"]).agg({"lemma": ' '.join})
```

If necessary, one may specify multiple aggregate functions for multiple columns, for instance:

```python
lines = words.groupby(["id_text", "id_line", "label"]).agg({"lemma": ' '.join, "base": ' '.join})
```

## 2.1.8 Other ORACC JSON files

The [Open Data](http://oracc.org/doc/opendata/index.html) page in [ORACC](http://oracc.org) explains in some detail the various other types of JSON files that are available. This section will briefly point out a few files that may be of use and that can be parsed with the techniques discussed above.

### 2.1.8.1 metadata.json

The file `metadata.json` provides information about composite texts (which witnesses belong to which composite text) and about formats: `atf` (available in transliteration), `lem` (files with lemmatization) and `tr-en` (files with English translation). In projects that work with other translation languages one may find `tr-de` (for German), `tr-hun` (for Hungarian), etc. The file `metadata.json` may be useful, for instance, if you intent to parse all the files of a project that have lemmatization, but ignore those that do not. One may pull out the list `formats["lem"]` to get all the relevant text IDs.

### 2.1.8.2 Indexes and Glossary

The Index and Glossary JSON files reproduce the indexes used by [ORACC Search](http://oracc.org/doc/search/searchingcorpora/index.html) and the project glossaries in JSON format. Indexes and glossaries may be used, among other things, to create searches beyond the scope of a line (for instance: search for `lugal` and `dalla` in the same text), a feature that is not currently available in standard [ORACC](http://oracc.org) search. How to build such a search engine is a topic not discussed in this study.



