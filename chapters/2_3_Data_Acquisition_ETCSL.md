## 2.3 Data Acquisition: ETCSL

The Electronic Text Corpus of Sumerian Literature ([ETCSL][] contains editions and translations of almost 400 Sumerian literary texts, mostly from the Old Babylonian period (around 1800 BCE). The project was led by Jeremy Black (Oxford University) and was active until 2006, when it was archived. Information about the project, its stages, products and collaborators may be found in the project's [About](http://etcsl.orinst.ox.ac.uk/edition2/general.php) page. By the time of its inception [ETCSL][] was a pioneering effort - the first larger digital project in Assyriology, using well-structured data according to the standards and best practices of the time. [ETCSL][] allows for various kinds of searches in Sumerian and in English translation and provides lemmatization for each individual word. Numerous scholars contributed data set to the [ETCSL][] project (see [Acknowledgements](http://etcsl.orinst.ox.ac.uk/edition2/credits.php#ack)). The availability of [ETCSL][] has fundamentally altered the study of Sumerian literature and has made this literature available for undergraduate teaching.

The original [ETCSL][] files in TEI XML are stored in the [Oxford Text Archive][] from where they can be downloaded as a ZIP file under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License ([by-nc-sa 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/)). The copyright holders are Jeremy Black, Graham Cunningham, Jarle Ebeling, Esther Flückiger-Hawker, Eleanor Robson, Jon Taylor, and Gábor Zólyomi.

The [Oxford Text Archive][] page offers the following description:

> The Electronic Text Corpus of Sumerian Literature (ETCSL) comprises transliterations and English translations of 394 compositions attested on sources dating to the period from approximately 2100 to 1700 BCE. The compositions are divided into seven categories: ancient literary catalogues; narrative compositions; royal praise poetry and hymns to deities on behalf of rulers; literary letters and letter-prayers; divine and temple hymns; proverbs and proverb collections; and a more general category including compositions such as debates, dialogues and riddles. The numbering of the compositions within the corpus follows Miguel Civil's unpublished catalogue of Sumerian literature (etcslfullcat.html).Files with an initial c are composite transliterations (a reconstructed text editorially assembled from the extant exemplars but including substantive variants) in which the cuneiform signs are represented in the Roman alphabet. Files with an initial t are translations. The composite files include full references for the cuneiform sources and author-date references for the secondary sources (detailed in bibliography.xml). The composite and translation files are in XML and have been annotated according to the TEI guidelines. In terms of linguistic information, each word form in the composite transliterations has been assigned to a lexeme which is specified by a citation form, word class information and basic English translation.

Since [ETCSL][] is an archival site the editions are not updated to reflect new text finds or new insights in the Sumerian language. Many of the [ETCSL][] editions were based on standard print editions that itself may have been 10 or 20 years old by the time they were digitized. Any computational analysis of the [ETCSL][] corpus will have to deal with the fact that: 

- the text may not represent the latest standard
- the [ETCSL][] corpus is extensive - but does not cover all of Sumerian literature known today

In terms of data acquisition, the way to deal with these limitations is to make the [ETCSL][] data as much as possible compatible with the data standards of the Open Richly Annotated Cuneiform Corpus ([ORACC][]). [ORACC][] is an active project where new or updated editions can be produced. If compatible, if [ETCSL][] and [ORACC][] data may be freely mixed and matched, then the [ETCSL][] data set can effectively be updated and expanded.

Compatability between [ETCSL][] and [ORACC][] is achievable because part of the crew that was involved in [ETCSL][] also laid the foundations of [ORACC][], in particular Steve Tinney and Eleanor Robson.

In order to achieve compatability the code uses a number of equivalence dictionaries, that enable replacement of characters, words, or names. These equivalence dictionaries are stored in JSON format (for JSON see section 2.4) in the file `equivalancies.json`  in the directory `etcsl/equivalencies` in the `Computational-Assyriology` repo.

### 2.3.1 TEI XML format

The [ETCSL][] files as distributed by the [Oxford Text Archive][] are encoded in a dialect of XML (Extensible Markup Language) that is referred to as TEI (Text Encoding Initiative). In this encoding each word (in transliteration) is an *element* that is surrounded by `<w>` and `</w>` tags. Inside the start-tag the word may receive several attributes, encoded as name/value pairs:

```xml
<w form="mah-bi" lemma="mah" pos="V" label="to be majestic">mah-bi</w>
```

In parsing the [ETCSL][] files we will be looking for these `<w>` and `</w>` tags to isolate words and their attributes. Higher level tags identify lines (`<l>` and `</l>`) , versions, secondary text (found only in a minority of sources), etcetera.

The [ETCSL][] file set includes the [etcslmanual.html](http://etcsl.orinst.ox.ac.uk/edition2/etcslmanual.php) with explanations of the tags, their attributes, and their proper usage.

Goal of the parsing process is to get as much information as possible out of the `XML` tree in a format that is useful for computational text analysis. What "useful" means depends, of course, on the particular project. I hope that the parsing discussed below is extensive and flexible enough that it will prove useful for a variety of purposes.

### 2.3.2 `lxml` and `Xpath

There are several Python libraries specifically for parsing `XML`, among them the popular `ElementTree` and its twin `cElementTree`. The library `lxml` is largely compatible with `ElemntTree` and `cElementTree` but differs from those in its full support of `Xpath`. `Xpath` is a language for finding and retrieving elements and attributes in XML trees.

[Explain some essentials of Xpath]

### 2.3.3 Pre-processing: HTML entities

Before the XML files can be parsed, it is necessary to remove character sequences that are not allowed in XML proper (so-called HTML entities). 

In non-transliteration contexts (bibliographies, text titles, etc.) [ETCSL][] uses so-called HTML entities to represent non-ASCII chracaters such as,  á, ü, or š. These entities are encoded with an opening ampersand (`&`) and a closing semicolon (`;`). For instance, `&C;` represents the character `Š`. The HTML entities are for the most part project-specific and are declared in the file `etcsl-sux.ent` which is part of the file package and is used by the [ETCSL][] project in the process of validating and parsing the XML for online publication.

For purposes of data acquisition these entities need to be resolved, because XML parsers will not recognize these sequences as valid XML. 

The key `ampersands`in the file `equivalences.json` includes a dictionary, listing all the HTML entities that appear in the [ETCSL][] files with their Unicode counterparts:

```json
{'&C;': 'Š',
 '&Ccedil;': 'Ç',
 '&Eacute;': 'É',
 '&G;': 'Ŋ',
 '&H;': 'H',
 '&Imacr;': 'Î',
 '&X;': 'X',
 '&aacute;': 'á',
 etc.  
```

This dictionary may be used to replace each HTML entity with its unicode (UTF-8) counterpart in each of the data files (note that the original files are left untouched). The function `ampersands()` is called in the main process. 

```python
import json
with open("equivalencies/equivalencies.json") as f:
    eq = json.load(f)
def ampersands(x):
    for amp in eq["ampersands"]:
        x = x.replace(amp, eq["ampersands"][amp])
    return x
```



### 2.3.4 Additional Text and Secondary Text

[ETCSL][] transliterations represent composite texts, put together (in most cases) from multiple exemplars. The text includes substantive variants, which are marked either as "additional" or as "secondary". Additional text consists of words or lines that are added to the text in a minority of sources. In the opening passage of [Inana's Descent to the Netherworld][], for instance, there is a list of temples that Inana leaves behind. One exemplar extends this list with eight more temples; in the composite text these lines are marked as "additional" and numbered lines 13A-13H. Secondary text, on the other hand, is variant text (words or lines) that are found in a minority of sources instead of the primary text. An example in [Inana's Descent to the Netherworld][] is lines 30-31, which are replaced by 30A-31A in one manuscript:

| line | text                                     | translation |
| ---- | ---------------------------------------- | ----------- |
| 30   | sukkal e-ne-eĝ₃ sag₉-sag₉-ga-ĝu₁₀        |             |
| 31   | ra-gaba e-ne-eĝ₃ ge-en-gen₆-na-ĝu₁₀      |             |
| 30A  | [na] ga-e-de₅ na de₅-ĝu₁₀ /ḫe₂\\-[dab₅]  |             |
| 31A  | [inim] ga-ra-ab-dug₄ ĝizzal [ḫe₂-em-ši-ak] |             |

"Secondary text" and "additional text" can also consist of a single word and there are even cases of "additional text" within "additional text" (an additional word within an additional line).

In [ETCSL][] TEI XML secondary/additional text is introduced by a tag of the type:

```xml
<addSpan to="c141.v11" type="secondary"/>
```

or

```xml
<addSpan to="c141.v11" type="additional"/>
```

The number c141 represents the text number in [ETCSL][] (in this case [Inana's Descent to the Netherworld][], text c.1.4.1). The return to the primary text is indicated by a tag of the type:

```xml
<anchor id="c141.v11"/>
```

Note that the `id` attribute in the `anchor` tag is identical to the `to` attribute in the `addSpan` tag.

We can collect all the `w` tags (words) between `addSpan` and its corresponding `anchor` tag wih the following `xpath` expression:

```python
secondary = tree.xpath('//w[preceding::addSpan[@type="secondary"]/@to = following::anchor/@id]')
```

In the expression `preceding` and `following` are so-called `axes` (plural of `axis`) which describe the relationship of an element to another element in the tree. The expression means: get all `w` tags that are preceded by an `addSpan` tag and followed by an `anchor` tag. The `addSpan` tag has to have an attribute `type` with value `secondary` , and the value of the `to` attribute of this `addSpan` tag is to be equal to the `id` attribute of the following `anchor` tag.

Once we have collected all the "secondary" `w` tags this way, we can add an attribute to each of these words in the following way:

```python
for word in secondary:
    word.attrib["status"] = "secondary"
```

In the process of parsing we can retrieve this new `status` attribute to mark all of these words as `secondary`.

Since we can do exactly the same for "additional text" we can slightly adapt the above expression for use in a function:

```python
def mark_extra(tree, which):
    extra = tree.xpath('//w[preceding::addSpan[@type="' + which + '"]/@to = following::anchor/@id]')
    for word in extra:
        word.attrib["status"] = which
	return tree
```

In the main process we can call this function with the second argument "additional" and "secondary".

### 2.3.6 Gaps

Gaps of one or more lines in the composite text, due to damage to the original cuneiform tablet, is encoded as follows:

```xml
<gap extent="8 lines missing"/>
```

In order to be able to process this information and keep it at the right place in the data we will parse the `gap` tags together with the `l` (line) tags and process the gap as a line.



### 2.3.3 Parsing the XML Tree

The Python library `xml.etree.ElementTree`, abbreviated as `ET` is specialized in parsing XML element trees. One can search for specific types of nodes, retrieve elements and attributes, etc. The code basically works from the highest level of the hierarchy  to the lowest, in the following way:

```
	version						getversion()
		section					getsection()
			line				getline()
				word			getword()
```

The main process calls the function `parsetext()` which calls the pre-processing functions discussed in section 2.3.2. It then calls `getversion()`, which calls `getsection()`, which calls `getline()`, which, finally, calls `getword()`. Along the way a dictionary, `meta_d` collects information about text IDs, text names, version names, and line numbers. The function `getline()` adds a line reference number (`line_ref`), an integer, in order to be able to put the lines in their correct sequence (`line_no` is a string and will put line "11" before line "3"). The function `getword()` at the lowest level of this hierarchy, will create a dictionary for each word. This dictionary contains all the information about line number, section, version name, text name, etc. plus the lemmatization data of the single word.

Thus the word `šeŋ₆-ŋa₂` in the file `c.1.2.2.xml` ([Enlil and Sud](http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.2.2&display=Crit&charenc=gcirc#)), in Version A, section A line 115, looks as follows in XML: 

```xml
<w form="cej6-ja2" lemma="cej6" pos="V" label="to be hot">cej6-ja2</w>
```

The dictionary that is created in `getword()` represents that same word as follows:

```python
{'id_text': 'c.1.2.2', 
 'text_name': 'Enlil and Sud',
 'version': 'A', 
 'lang': 'sux',
 'cf': 'šeŋ',
 'gw': 'cook',
 'pos': 'V/t',
 'form': 'šeŋ₆-ŋa₂',
 'line_no' : 'A115',
 'line_ref': 109,
 'extent': ''}
```

Note that in the process the transliteration and lemmatization data have been replaced by [epsd2][] style data. The function `tounicode()` replaces `j` by `ŋ` , `c` by `š`, etc. and substitutes Unicode subscript numbers for the regular numbers in sign indexes. The function `etcsl_to_oracc()` replaces [ETCSL][] style lemmatization with [epsd2][] style. Both replacements use dictionaries in the `equivalences.json` file.  

[ETCSL]:                               http://etcsl.orinst.ox.ac.uk
[ORACC]:                             http://oracc.org
[epsd2]:                               http://oracc.org/epsd2/sux
[Inana's Descent to the Netherworld]: http://etcsl.orinst.ox.ac.uk/cgi-bin/etcsl.cgi?text=c.1.4.1&amp;amp;amp;display=Crit&amp;amp;amp;charenc=gcirc#
[Oxford Text Archive]:       http://ota.ox.ac.uk/desc/2518
