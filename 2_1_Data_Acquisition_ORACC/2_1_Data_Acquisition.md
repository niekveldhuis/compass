## 2.1 Data Acquisition: [ORACC][oracc]
[ORACC][ORACC] (the Open Richly Annotated Cuneiform Corpus) is an umbrella project for the online publication of cuneiform texts. [ORACC][oracc] counts several dozens of independent projects, some with one or more sub-projects. Corpus-based projects include editions and translations of cuneiform texts with linked local glossaries. [ORACC][oracc] was created by Steve Tinney (University of Pennsylvania) in 2006.

[ORACC][oracc] data are made available as open data in JSON format under the [CC0](https://creativecommons.org/publicdomain/zero/1.0/) license (public domain). JSON (JavaScript Object Notation) is a file format that is used widely for exchanging data between programs or between web sites. The file format is simple and straightforward, but allows for complex representations of data in a hierarchical format (not unlike XML). The structure of JSON files is very easy to read and parse in Python and in many other programming languages.

The sections that follow explain how the [ORACC][oracc] JSON is parsed and how the data can be reformatted in various ways. This is rather technical in nature and perhaps not a very interesting place to start (there are no research results to be reported or to be evaluated at the end). Proper data acquisition is foundational for all computational research. *What* data are collected (transliteration, transcription, or a series of lemmas) and in what *format* they are collected (word-by-word, line-by-line, or text-by text) depends on the research question and therefore the acquisition techniques discussed below are flexible and allow the user to adjust the code to her or his needs. The analytical chapters (Chapter 3-6) will provide the data in the required format and thus the present section is not necessary to follow along. The reader who wishes to devise her own research project - and format the data accordingly - will require a deeper understanding of the JSON format and the techniques for parsing the data.

### 2.1.1 The JSON Data Format

JavaScript Object Notation, or [JSON](http://www.json.org) is recognized as a lightweight but very versatile data structure. Databases (and `.csv` files) need a fixed number of fields; key/value combinations in JSON can be extended at will. Representation of hierarchical structures is very natural in JSON, but is complex in (relational) databases. We will see that [ORACC][oracc] JSON makes extensive use of hierarchies. The two characteristics mentioned here (extensibility and hierarchical structure) are shared with XML, which is in many ways similar to JSON. Generally, JSON is considered to be lighter (smaller files) and more efficient, because the data structure is very closely aligned to data structures in common programming languages such as Python, and R. 

The contents of a valid JSON file are always wrapped in curly brackets, very similar to a Python dictionary. Dictionaries consist entirely of `"key" : "value"` pairs, as in:

```json
{"id_text": "P334930", "designation": "SAA 03, 001"}
```

In a `"key" : "value"` pair, keys are always strings. Values may be string, number, list, boolean (true or false), or another dictionary. A list is wrapped in square brackets and may look like this:

```json
["ABRT 1 32", "SAA 03, 001"]
```

A dictionary is wrapped in curly brackets and consists, again, of `key`: `value` pairs.

The following is an (abbreviated) example of a JSON file (the catalog of an imaginary [ORACC][oracc] project) that illustrates the format:

```json
{"members": {
		"P334930": {
			"id_text": "P334930",
			"designation": "SAA 03, 001",
			"publications": ["ABRT 1 32", "SAA 03, 001"]
		},
		"P334929": {
			"id_text": "P334929",
			"designation": "SAA 03, 002",
			"publications": ["ABRT 1 29", "SAA03, 002"]
		}
	}
}
```

The value of the key `members` is a dictionary (surrounded by curly brackets) with length of 2. Each element in the dictionary is again a dictionary (surrounded by curly brackets and consisting of `key` : `value` pairs). The key `publications` has a list as its value. A list is a way to give multiple values to the same key. In `publications`  the values inside the list are strings (surrounded by quotation marks), but they may be of any data type, including lists or dictionaries. This allows for very complex trees with a minimal arsenal of data structures.

For all practical purposes, a JSON object is identical in structure to a Python dictionary, but the naming conventions are slightly different. To avoid confusion, we use the Python vocabulary here (key, list, dictionary), even when talking about the JSON  structure.

| JSON   | Python     | Surrounded by | Defined as                                               |
| ------ | ---------- | ------------- | -------------------------------------------------------- |
| object | dictionary | {}            | unordered sequence of name/value pairs                   |
| array  | list       | []            | ordered sequence of values                               |
| value  | value      |               | string, number, list (= array), or dictionary (= object) |
| name   | key        |               | string                                                   |

 For a more formal and exhaustive description of the JSON data structure see [http://www.json.org/](http://www.json.org). 

### 2.1.2 Acquiring ORACC JSON

Each [ORACC][oracc] project has a `zip` file that contains a collection of JSON files, which provide data on lemmatizations, transliterations, catalog data, indexes, etc. The `zip` file can be found at `http://build-oracc.museum.upenn.edu/json/[PROJECT].zip`, where `[PROJECT]` is to be replaced with the project abbreviation (e.g. http://build-oracc.museum.upenn.edu/json/etcsri.zip). For sub-projects the address is `http://build-oracc.museum.upenn.edu/json/[PROJECT]-[SUBPROJECT].zip`(e.g. http://build-oracc.museum.upenn.edu/json/cams-gkab.zip). One may download these files by hand (simply type the address in your browser), or use the notebook [2_3_0_download_ORACC-JSON.ipynb](https://github.com/niekveldhuis/compass/blob/master/2_3_Data_Acquisition_ORACC/2_3_0_download_ORACC-JSON.ipynb). The notebook will create a directory `jsonzip` and copy the file to that directory - all further scripts will expect the `zip` files to reside in `jsonzip`.

After downloading the JSON `zip` file you may unzip it to inspect its contents. Note, however, that the scripts will always read the data directly from the `zip` file.

### 2.1.3 Parsing JSON: catalogue.json

Each [ORACC][oracc] JSON `zip` file includes a file named `catalogue.json`. Since the structure of `catalogue.json` is simple and there is relatively little depth in its hierarchy, it can be parsed in just a few lines. The example code assumes that the file `obmc.zip` is available in the directory `jsonzip`. You may download it at http://build-oracc.museum.upenn.edu/json/obmc.zip or use the notebook referenced above. The comment lines (beginning with #) show the proper naming conventions for a sub-project.

```python
import zipfile
import json
file = "jsonzip/obmc.zip"    
# or: file = "jsonzip/dcclt-nineveh.zip"
z = zipfile.ZipFile(file)
st = z.read("obmc/catalogue.json").decode("utf-8") 
# or: st = z.read("dcclt/nineveh/catalogue.json").decode("utf-8")
cat = json.loads(st)
```

The command `ZipFile` from the `zipfile` library turns the `zip` file into a `zipfile` object that may be manipulated with the functions available in the `zipfile` library. The `read()` command from that same package reads one particular file from the `zip`.  The `json` library provides functions for reading (loading) or producing (dumping) a JSON file. Reading is done with the function `load()`, which comes in two versions. Regular `json.load()` takes a filename as argument and will load a JSON file. In this case, however, the `read()` function from the `zipfile` library has produced a string (extracted from `obmc.zip`), and therefore we need the command `json.loads()`, which takes a string as its argument (here represented by the variable `st`).  

The variable `cat` will now contain the entire `catalogue.json` object from the [OBMC][obmc] (Old Babylonian Model Contracts) project by Gabriella Spada. We can treat the variable `cat` as a Python dictionary. The value of the key `members` is itself a dictionary of dictionaries which may be transformed into a Pandas Dataframe for ease of viewing and manipulation.

``` python
import pandas as pd	
cat = cat["members"]
df = pd.DataFrame(cat)
df
```

The `DataFrame()` function in the `pandas` library takes each key as a column - in this case the keys of `cat["members"]` are the P numbers (text IDs); the catalog fields have become rows. In other words we need to transpose the DataFrame, which we can do in the same go:

```python
df = pd.DataFrame(cat).T
df
```

The table in `df` now contains all the catalog data available in [OBMC][obmc]. The Pandas library allows one to manipulate and slice the DataFrame in many different ways. For instance, one may select the relevant fields by creating a new DataFrame as follows:

```python
df1 = df[["provenience", "period", "id_text"]]
```

Pandas is a powerful Python library – we will see some of its functionality in later sections. Various introductions to Pandas may be found on the web or in [VanderPlas 2016](https://github.com/jakevdp/PythonDataScienceHandbook) and similar overviews.

The notebook [2-3-1_parse-json-cat.ipynb](https://github.com/niekveldhuis/compass/blob/master/2_3_Data_Acquisition_ORACC/2_3_1_parse-json-cat.ipynb) allows one to enter one or more project abbreviations, download the JSON `zip` file, extract the catalog information and store that information in a `csv` file and/ or a `pickle` file.

### 2.1.4 Parsing an ORACC JSON Text Edition File

[ORACC][oracc] JSON text edition files include transliteration and lemmatization, as well as information on the sign level. Translation is not included. The files are found in the `corpusjson` directory of each project's `zip` file and are named after their text ID, for instance `dcclt/corpusjson/P251867.json`, or `saao/saa01/corpusjson/P224485.json`.

Reading in the data works in exactly the same way as above:

```python
import zipfile
import json
file = "jsonzip/obmc.zip"    
# or: file = "jsonzip/saao-saa01.zip"
z = zipfile.ZipFile(file)
st = z.read("obmc/corpusjson/P230754.json").decode("utf-8") 
# or: st = z.read("dcclt/saao/saa01/corpusjson/P251867.json").decode("utf-8")
text = json.loads(st)
```

The structure of the JSON files for text editions, however, is much more complex, because of the hierarchical structure of textual data. A text may have one or more surfaces (obverse, reverse), each surface may have one or more columns; each column has lines; each line has words; and each word has signs.

	text object
		surface
			column
				line
					word
						sign

How many of those layers are present in a particular text is impossible to predict. Some tablets have columns, others do not; most surfaces have text, but not all surfaces do. Moreover, [ORACC][oracc] JSON potentially also has information about sentences or other discourse units, which may or may not align with the division of the object in columns and lines.	

The JSON tree for a text edition consists of a hierarchy of `cdl` keys. The name `cdl` is based on the three main components of the nested tree: Chunks, Discontinuities, and Lemmas. A Chunk is a chunk of text of any length: the entire text, a discourse unit (such as a sentence), a column, a line, a word, etc. A discontinuity is the beginning of a column, a break in the text, or the beginning of a line. A Lemma is the lemmatization of a single word in the text, including the information on the sign level. The value of a `cdl` key is a list of one or more dictionaries. Each of these dictionaries contains the key "node" which may have the values "c" (for Chunk), "d" (for Discontinuity), or "l" (for Lemma). Any "c" dictionary may contain a further `cdl` key, which again has as its value a list of dictionaries of the "c", "d", or "l" type. An "l" (Lemma) dictionary, is always at the bottom of the `cdl` hierarchy. The "l" dictionary itself contains an "f" key which has as its value a dictionary that contains all the lemmatization data. The "f" dictionary includes a "gdl" key (for Grapheme Description Language), which identifies the graphemes (cuneiform signs) of which the word is composed, with information on the  reading and the function (syllabogram, logogram, determinative, etc.) of those graphemes (in some [ORACC][oracc] projects the `gdl` node will include the cuneiform sign itself as well).

The structure may be illustrated with the beginning of [P251867](http://oracc.org/dcclt/P251867), an Old Babylonian 3-line lentil (beginning of the file omitted): 

```json
{"cdl": [
{
  "node": "c",
  "type": "text",
  "id": "P251867.U0",
  "cdl": [
    {
      "node": "d",
      "type": "object",
      "ref": ""
    },
    {
      "node": "d",
      "subtype": "obverse",
      "type": "obverse",
      "ref": "P251867.o.1",
      "label": "o"
    },
    {
      "node": "c",
      "type": "discourse",
      "subtype": "body",
      "id": "P251867.U1",
      "cdl": [
        {
          "node": "c",
          "type": "sentence",
          "id": "P251867.U2",
          "label": "o 1 - o 3",
          "cdl": [
            {
              "node": "d",
              "type": "line-start",
              "ref": "P251867.2",
              "n": "1",
              "label": "o 1"
            },
            {
              "node": "l",
              "frag": "{ŋeš}ma₂-durah-abzu",
              "id": "P251867.l1ac01",
              "ref": "P251867.2.1",
              "inst": "Madurahabzu[1]ON",
              "sig": "@dcclt%sux:{ŋeš}ma₂-durah-abzu=Madurahabzu[1//1]ON'ON$Madurahabzu/{ŋeš}ma₂-durah-abzu#~",
              "f": {
                "lang": "sux",
                "form": "{ŋeš}ma₂-durah-abzu",
                "gdl": [
                  {
                    "det": "semantic",
                    "pos": "pre",
                    "seq": [
                      {
                        "v": "ŋeš",
                        "id": "P251867.2.1.0"
                      }
                    ]
                  },
```

The first `cdl` key contains a list that has a single element, a dictionary (the ending square bracket of this list is not included in the snippet). This dictionary is a `c` node (Chunk) representing the entire text. The `c` node contains a new `cdl` key which has a list of dictionaries as its value including two `d` (Discontinuity) nodes (`object` and `obverse`) and another `c` node that represents a discourse unit, namely the body of the text (note that Chunk `text` and Chunk `body` are identical here - but that need not be the case). Eventually, there is a node `l` that contains the transliteration and lemmatization data for the first word of this text.

This hierarchy implies that a word (an "l" node) may belong to multiple Chunks ("c" nodes) that do not necessarily align. For instance, a word may belong to a sentence that continues from the obverse to the reverse of a tablet. The JSON structure allows to express (and to retrieve) those facts simultaneously.

In order to pull out the lemmatization data we need to iterate through the hierarchy of `cdl` keys until we encounter an `l` node, containing an `f` key. The value of the `f` key is the data we want.

A straightforward way of doing this is by defining a recursive function, that is, a function that calls itself to recursively inspect the value of successive layers of `cdl` keys until one encounters an `f` key. The contents of the `f` key are then added to a list. In its most basic form that function looks like this:

```python
def parsejson(text):
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            parsejson(JSONobject)
        if "f" in JSONobject:
            lemm_l.append(JSONobject["f"])
    return 
```

For the `parsejson()` function to run properly we need to define `lemm_l` as an empty list before the function is called. Then the function is called with the argument `text`, which contains the contents of the entire JSON file, as retrieved above. The function modifies the list `lemm_l`, adding a new row of lemmatization data (one word at a time) each time it encounters an `f` key.

```python
lemm_l = []
parsejson(text)
```

The list `lemm_l` now contains all the lemmatization data of [P230754](http://oracc.org/obmc/P230754) as edited in [OBMC][obmc]. We can inspect the data by reading it into a `pandas` DataFrame

```python
import pandas as pd
words = pd.DataFrame(lemm_l).fillna("")
words
```
The function `fillna()` from the `pandas` library fills holes in the DataFrame where no data are available. For instance, a word that has not been lemmatized has no data in the fields "cf" (Citation Form), "gw" (Guide Word), and "pos" (Part of Speech). Without this function empty slots in the DataFrame will have the value NaN (or: "Not a Number"), which can be problematic in further data manipulation. The argument of the function is the value to be placed in empty cells - in this case the empty string. Note that NaN and "" are of different data types. NaN belongs to a numeric data type; the empty string is a string.

One may write the list (or the DataFrame) directly to a `csv` (or some similar file format), but it is often more useful to structure the data a bit more (section [2.1.7](#2.1.7-Data-Structuring)). Before we get to that we will first discuss several enhancements of the`parsejson()` function.

![P251867](http://cdli.ucla.edu/dl/tn_photo/P251867.jpg)



### 2.1.5 Enhancing parsejson()

The basic `parsejson()` captures only lemmatization data, it ignores line numbers, text breaks, and other types of information that are included in the JSON files. The basic `parsejson()` is good enough for a "Bag of Words" approach, which looks only at vocabulary frequency, ignoring word order. For many other types of analysis we do need to capture line numbers and text breaks. Such information is stored in "d" nodes in a level above the "l" node in the `cdl` hierarchy. Similarly, sentence identifiers (and other discourse units) are stored in "c" nodes. The `parsejson()` function can easily be enhanced to capture various types of such meta-data storing them (temporarily) in a dictionary called `meta_d`. This dictionary is created in the main process and is updated whenever the `parsejson()` function encounters a relevant node. Each row (each word) in the list `lemm_l` receives the current meta-data from `meta_d`. 

#### 2.1.5.1 Line Labels and Line IDs

For many types of explorations one may wish to keep together words in a line and order these lines in their proper sequence. In order to do so we need to capture the  `label` of the line and the word ID of each word. The `label` is human-legible and has the traditional format to indicate obverse, reverse,  column and line number or side of a prism (e.g. "o ii 7" or "a i 19'"). The field `id_word`, has the format TEXT_ID.LINE_ID.WORD_ID, for instance "P273880.22.1", (the first word of the twenty-second line of [P273880](http://oracc.org/dcclt/P273880.22.1)). In the data formatting stage we will use the word ID to extract the line ID (section [2.1.7.2](#2.1.7.2-Create-Line-IDs)).

We can capture `label` and `id_word` with slight adjustments to the `jsonparser()` and the code that calls that function. In the main process we create a dictionary `meta_d,` which will hold all the relevant meta data. Initially, it only contains the text ID. When the `parsejson()` function finds a dictionary that has the `key`  "label" the `key` "label" in`meta_d` gets updated. When the process gets to the lemmatization data the `key` "label" in `meta_d` will hold the proper line label. The word ID is found in the field "ref" in the `l` node, and is added to the `lemma` dictionary. 

```python
def parsejson(text):  # this version captures line labels and line IDs
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            parsejson(JSONobject)
        if "label" in JSONobject:
            meta_d["label"] = JSONobject["label"]
        if "f" in JSONobject:
            lemma = JSONobject["f"]
            lemma["id_text"] = meta_d["textid"]
            lemma["label"] = meta_d["label"]
            lemma["id_word"] = JSONobject["ref"]
            lemm_l.append(lemma)
    return  
```
Before the new `parsejson()` function can be called we need to create the empty `lemm_l` list as well as the `meta_d` dictionary. Both wil be changed by the `parsejson()` function. We call `parsejson()` with the same variable `text` that was created above, holding the JSON of text [P230754](http://oracc.org/obmc/P230754) from the [OBMC][obmc] project.

```python
lemm_l = []
meta_d = {"label" : None, "textid": "obmc/P230754"}
parsejson(text)
```

#### 2.1.5.2 Select a Section

Using this same structure to select a section of a tablet for parsing, the code may be adapted as follows:

```python
def parsejson(text):  # this version captures the lemmatization of a partial text
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            parsejson(JSONobject)
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
                lemm_l.append(lemma)
        if meta_d["label"] == meta_d["endlabel"]:
            meta_d["keep"] = False
    return 
```
In this case we will use a different example, the text [P273244](http://oracc.org/dcclt/P273244) from [DCCLT][dcclt]. In order to run this code the file `dcclt.zip` must be downloaded and put in the `jsonzip` folder (see above, section [2.1.2](#2.1.2-Acquiring-ORACC-JSON)).
```python
lemm_l = []
meta_d = {"label" : None, "startlabel": "r 1", "endlabel": "r 5", "keep": False,
             "id_text": "dcclt/P273244"}
file = "jsonzip/dcclt.zip"    
z = zipfile.ZipFile(file)
st = z.read("dcclt/corpusjson/P273244.json").decode("utf-8") 
data_json = json.loads(st)
if meta_d["startlabel"] == "":
    meta_d["keep"] = True
parsejson(data_json)

```

The text [P273244](http://oracc.org/dcclt/P273244) is a small Middle Babylonian exercise from Nippur with an extract from Gilgameš on the obverse, and a list of wooden objects (doors) on the reverse. The code will constantly refresh the value of the key `label` in the dictionary `meta_d`, while comparing `label` with the value of `startlabel` and `endlabel` to decide where to start and where to stop capturing the lemmatization. In this case only the lexical lines on the reverse are captured, skipping the Gilgameš extract on the obverse.

#### 2.1.5.3 Sentences

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

A subdivision of the sentence is the phrase. Phrases and sentences have their own ID. Obviously, such demarcations are only present in the JSON if the editor of the project (in this case Gábor Zólyomi of [ETCSRI][etcsri]) has marked such units (sentences and phrases) in the source files. In order to enable the `parsejson()`function to keep track of sentences, one may simply add another `if` statement to the code, store the sentence ID in the `meta_d` dictionary and add that ID to each word in the list of lemmas:

```python
def parsejson(text):  # this version captures and sentence IDs
    for JSONobject in text["cdl"]:
        if "type" in JSONobject and JSONobject["type"] == "sentence":
            meta_d["sentence"] = JSONobject["id"]
        if "cdl" in JSONobject: 
            parsejson(JSONobject)
        if "f" in JSONobject:
            lemma = JSONobject["f"]
            lemma["sentence_id"] = meta_d["sentence"]
            lemma["id_text"] = meta_d["textid"]
            lemm_l.append(lemma)
    return 
```
In the example we will use [Q000376](http://oracc.org/etcsri/Q000376) (The Victory of Utu-hegal) from the [ETCSRI][etcsri] project. In order for the code to work, place the file `etcsri.zip` in the `jsonzip`folder (see section [2.1.2](#2.1.2-Acquiring-ORACC-JSON)).
```python
lemm_l = []
meta_d = {"sentence" : None, "textid": "etcsri/Q000376"}
file = "jsonzip/etcsri.zip"    
z = zipfile.ZipFile(file)
st = z.read("etcsri/corpusjson/Q000376.json").decode("utf-8") 
text = json.loads(st)
parsejson(text)
```

The initial value of the key `sentence` in the `meta_d` dictionary is `None`, but when the `parsejson()` function encounters a key `type` with value `sentence` it changes the value of `meta_d["sentence"]` to hold the `id` of the sentence. The value of that parameter will stay the same, and is copied into the field `sentence_id` of every row (representing a word) in `lemma_l` until the `parsejson()` function encounters a new `"type" : "sentence"` pair. 

Each row (word) in the list `lemm_l` will now have a field `sentence_id`that can be used to identify words that belong together in a sentence - a feature that is particularly important for syntactic parsing in Natural Language Processing and building [treebanks](https://en.wikipedia.org/wiki/Treebank).



#### 2.1.5.4 Using parsejson()

In practice, one will rarely wish to parse a single text - as in the examples above. The various `parsejson()` functions discussed above (or any that may be derived) may be embedded in code that uses a list of projects or text ID numbers (optionally provided with `startlabel`and `endlabel`) in order to parse a collection of documents or entire [ORACC][oracc] projects. Example code for doing so is available in the [Computational Assyriology][compass]  repo. That part of code (iterating through a list of text IDs) is not specific to [ORACC][oracc] or to JSON and will not be discussed here (some code explanation is available in the notebooks).

The output of `parsejson()` is a list of words, where each word is represented by dictionary that includes a number of data elements, including Citation Form, Guide Word, Part of Speech, GDL (grapheme information), Form (transliteration), etc. Some data elements are always present, others are specific for Sumerian or Akkadian, or are only present if the word in question has been lemmatized. For most projects it will be necessary to select and/or manipulate the data (section [2.1.7](#2.1.7-Data-Structuring)).

### 2.1.6 Other Data Types in Text Edition JSON Files

The JSON files for individual text editions include other data types that may be captured by still other permutations of the `parsejson()` function. These data types will be discussed here briefly. 

#### 2.1.6.1 Phrasal Semantic Units (Compound Verbs, etc.)

In addition to words, [ORACC][oracc] recognizes Phrasal Semantic Units ([PSU](http://oracc.museum.upenn.edu/doc/help/lemmatising/psus/index.html)s), including idiomatic expressions, (Sumerian) Compound Verbs, multi-word proper nouns, etc. A PSU consists of multiple words, which are each lemmatized independently but are also indexed as a compound (and listed in the glossary).

In the JSON text edition files the PSUs are listed at the end under the node `linkbase` with references to where the expression appears in the text.

#### 2.1.6.2 Broken Lines

[ORACC][oracc] editions include information such as "10 lines broken", or "rest of column missing". There is a restricted vocabulary for such annotations, preserved in `d` (Discontinuity) nodes. The information is found in four fields, named `strict`, `extent`, `scope` and `state`. The field `strict` has the value `"1"` (a string) if the remark follows the restricted vocabulary (if `"0"`, it may contain all kinds of unstructured information, for instance about joins). A typical node looks like this:

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

This tells us that at this position in `Q000039` three lines are missing. The reference number belongs to the same number sequence as the line ID numbers (see above section [2.1.5.1](#2.1.5.1-Line-Labels-and-Line-IDs)) and may thus be used to keep the three missing lines in their proper position. The same mechanism is used to record single or double horizontal rulings, as in: 

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

This indicates a double ruling at the end of the lexical prism [CUSAS 12, 3.1.01](http://oracc.org/dcclt/P273880.718). 

Such information may be captured by looking for nodes that include the key `type` with value `nonx` and add the relevant fields to the list `lemm_l in `parsejson()`. The code for doing so is not discussed in the present chapter, but the [Extended JSON parser](https://github.com/niekveldhuis/compass/blob/master/2_1_Data_Acquisition_ORACC/2_1_3_extended_ORACC-JSON_parser.ipynb) in the [Compass][compass] repo does include that functionality.

### 2.1.7 Data Structuring

The output of `jsonparser()` is the list `lemm_l`, a list of dictionaries, where each dictionary represents a single word. This list can be read into a `pandas` DataFrame. DataFrames can be manipulated and sliced in any number of ways and give a visual impression of the structure of the data.

```python
import pandas as pd
words = pd.DataFrame(lemm_l).fillna("")
words
```
For a brief discussion of the `pandas` `fillna()` function see the end of section [2.1.4](#2.1.4-Parsing-an-ORACC-JSON-Text-Edition-File).
#### 2.1.7.1 Remove Spaces and Commas from Guide Word

The column "gw" (Guide Word) in the `pandas` DataFrame just created includes bare-bones translations of individual words, such as "king" (for Sumerian lugal) or "(a kind of clamp)" for Akkadian *abāru*. Strictly speaking, Guide Words are not translations but disambiguators - disambiguating between potential homonyms. Akkadian Guide Words are derived from the first meaning in the *Concise Dictionary of Akkadian* (eds. Jeremy Black, Andrew George, and Nicholas Postgate; Harrasowitz Verlag 2000), as discussed in the manual for [ORACC lemmatization](http://oracc.org/doc/help/languages/akkadian/index.html). 

The presence of spaces in Guide Words may cause trouble in a variety of computational methods, because such methods will interpret the space as a word divider. Similarly, commas may cause trouble when saving data in a `.csv` (Comma Separated Values) file, because a comma will be interpreted as the beginning of a new field. 

For text analysis purposes, therefore it is important to remove all commas and spaces from Guide Word and Sense. The `pandas` `replace()` function takes as its argument a nested dictionary, in which the top-level keys specify in which column the replacements should take place. Each value is a dictionary with find (key) and replace (value) pairs.  By default, `replace()` replaces a full string; we need to set `regex = True` to replace a partial string.

```python
findreplace = {' ' : '-', ',' : ''}
words = words.replace({'gw' : findreplace, 'sense' : findreplace}, regex=True)
```

Now the Guide Word for *abāru* has become `(a-kind-of-clamp)`.

#### 2.1.7.2 Create Line IDs

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

The field `id_line` will be used in section [2.1.7.4](#2.1.7.4-Arrange-by-Line-or-by-Document) to arrange the data in line-by-line fashion.

The [Extended JSON parser](https://github.com/niekveldhuis/compass/blob/master/2_1_Data_Acquisition_ORACC/2_1_3_extended_ORACC-JSON_parser.ipynb) in the [Compass][compass] repo captures information about broken lines and horizontal rulings (see section [2.1.6.2](#2.1.6.2-Broken-Lines). Such features have a reference in the format `ID_TEXT.ID_LINE`; that reference is copied to the field 'id_word' and extended with an extra '.0' to mimic the format of true word IDs.

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

#### 2.1.7.3 Create Lemmas

The DataFrame `words` includes all the fields that were present in the `f` keys of the JSON files we parsed, plus the extra fields (such as `id_line` or `label`) that we have added. It is not likely that we want to keep the DataFrame in this raw format. For many types of analysis one may need the lemma. A lemma, [ORACC][oracc] style, combines Citation Form, Guide Word and Part of Speech into a unique reference to one particular entry in a standard dictionary, as in `lugal[king]N` (Sumerian) or `nadānu[give]V` (Akkadian). Usually, not all words in a text are lemmatized, because a word may be (partly) broken and/or unknown. The code below will create a new field `lemma` that has the following form:

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

The first line creates the new "lemma" column by concatenating Citation Form, Guide Word and POS. The second and third line take care of two special situations. If there is no Citation Form the word is not lemmatized and the "lemma" column will contain the "form" followed by "[NA]NA" (Guide Word and POS unknown). Finally, depending on the version of `parsejson()`that is used, the `words`dataframe may include rows that represent horizontal drawings or broken lines (see section [2.1.6.2](#2.1.6.2-Broken-Lines)). For those entries the "form" is an empty string and the "lemma" should be empty as well.



#### 2.1.7.4 Arrange by Line or by Document

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

### 2.1.8 Other ORACC JSON files

The [Open Data](http://oracc.org/doc/opendata/index.html) page in [ORACC][oracc] explains in some detail the various other types of JSON files that are available. This section will briefly point out a few files that may be of use and that can be parsed with the techniques discussed above.

#### 2.1.8.1 metadata.json

The file `metadata.json` provides information about composite texts (which witnesses belong to which composite text) and about formats: `atf` (available in transliteration), `lem` (files with lemmatization) and `tr-en` (files with English translation). In projects that work with other translation languages one may find `tr-de` (for German), `tr-hun`(for Hungarian), etc. The file `metadata.json` may be useful, for instance, if you intent to parse all the files of a project that have lemmatization, but ignore those that do not. One may pull out the list `formats["lem"]` to get all the relevant text IDs.

#### 2.1.8.2 Indexes and Glossary

The Index and Glossary JSON files reproduce the indexes used by [ORACC Search](http://oracc.org/doc/search/searchingcorpora/index.html) and the project glossaries in JSON format. Indexes and glossaries may be used, among other things, to create searches beyond the scope of a line (for instance: search for `lugal` and `dalla` in the same text), a feature that is not currently available in standard [ORACC][oracc] search. How to build such a search engine is a topic not discussed in this book.


[oracc]: http://oracc.org
[obmc]: http://oracc.org/obmc
[dcclt]: http://oracc.org/dcclt
[etcsri]: http://oracc.org/etcsri
[compass]: https://github.com/niekveldhuis/compass

