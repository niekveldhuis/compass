# 1. Introduction

This book project attempts to bring together two recent trends: the digital turn in Assyriology, and the rise of Data Science. Although Assyriologists had actively used databases since the nineteen sixties, such data sets were available only to a small circle - important examples include Miguel Civil's Nippur Corpus (a group of Sumerian literary texts, now largely available on [ETCSL][ETCSL]) and Simo Parpola's database of Neo-Assyrian texts, subsequently published in  print in the State Archives of Assyria series and now available online in [SAAo](http://oracc.org/saao) . With the advent of the Internet, it became possible to give public access to data in the form of transliterations, translations, photographs, and glossaries. This development began in earnest in 1996 with the appearance of the Electronic Text Corpus of Sumerian Literature ([ETCSL][ETCSL]), and continues to the present day. Data Science is an interdisciplinary field that draws its techniques from Statistics and Computer Science and (essentially) involves a third field, a domain discipline. Although "Data Science" is a relatively recent coinage, its roots go back well into the twentieth century. In recent years many universities have created institutes or departments for Data Science and/or for Digital Humanities, and have developed undergraduate and graduate programs in such fields. The eco-system for applying Data Science methods to Assyriological data, therefore, is much better today than it was even five years ago. 

This Introduction will briefly discuss the history of the digital turn in Assyriology and some relevant aspects of developments in Data Science (1.1). Next we will discuss software and installing software (1.2), with a brief discussion of differences between Windows and Mac. Section 1.3 is devoted to principles of Data Science in Assyriology: open data, open source, and reproducibility.

## 1.1 Assyriology and Data Science

### 1.1.1 Digital Assyriology

The turn towards publicly available electronic data is due in no small part to the initiative by Jeremy Black (Oxford University) to develop the Electronic Text Corpus of Sumerian Literature ([ETCSL][ETCSL]), which started in 1996 and remained active until 2006, when it became archival. Initially [ETCSL][ETCSL] offered composite editions (transliterations) of Sumerian literary texts with translations. In version 2, using tools developed by Steve Tinney, the entire corpus was lemmatized, which allowed for the addition of glossaries and other tools for search and research.  

[ETCSL][ETCSL] was quickly followed by the Cuneiform Digital Library Inititative ([CDLI][CDLI]), created by Bob Englund, UCLA. This project provides access to metadata, photographs, line drawings, and transliterations (occasionally also translations) of cuneiform documents of all periods and genres. Importantly, [CDLI][CDLI] assigns unique ID numbers to cuneiform objects. Initially, [CDLI][CDLI] focused on administrative and legal documents from the fourth and third millennium BCE, but today one may find a broad variety of text genres from all periods of cuneiform. In 2006 (after several precursors) the Open Richly Annotated Cuneiform Corpus ([ORACC][ORACC]) was built by Steve Tinney (University of Pennsylvania), who had previously been involved in the development of both [ETCSL][ETCSL] and [CDLI][CDLI]. [ORACC][ORACC] works with semi-independent projects, where project directors have broad leeway in the definition of the scope of their project, but follow shared editorial principles in terms of transliteration and lemmatization.

These three projects together fundamentally changed research and teaching in Assyriology and many Assyriologists today depend in one way or another on these and other digital resources. Together, these three make available large amounts of searchable data and make those data freely accessible to other scholars. All three projects use explicit standards, and reuse data where possible, setting a fairly high standard for digital Assyriology. Many other larger and smaller projects were created in their wake, among the most important are the Database of Neo-Sumerian Texts ([BDTNS][BDTNS]; currently comprising almost 100,000 documents in transliteration); Sources of Early Akkadian Literature ([SEAL][SEAL]; several hundred literary texts in Akkadian from the third and second millennium BCE) and Archives Babyloniennes ([ARCHIBAB][ARCHIBAB]; a collection of thousands of Old Babylonian letters, and legal, and administrative documents)[Charpin2014].  The [BDTNS][BDTNS] data set is freely available (transliterations and metadata). [ARCHIBAB][ARCHIBAB] and [SEAL][SEAL] both make their data available in the form of PDFs and restrict usage to non derivatives, making the data of these projects unavailable for computational analysis.

Reflecting on this (very abbreviated) history one may note that scholars working in Sumerian have been the driving force behind almost all the major projects (exceptions are [ARCHIBAB][archibab] and [SEAL][seal]). The main reason for this situation is that the (traditional) tool set for reading Sumerian is far behind - there is no comprehensive (printed) Sumerian dictionary[^2] and no generally accepted Sumerian grammar. In other words: the need for creating such (digital) tools and the opportunities afforded by the development of the digital landscape were felt much more acutely by scholars working in Sumerian.

### 1.1.2 Data Science

Data Science developed in response to the quantitative explosion in data collected and produced by cell phones, personal computers, tablets, and web-connected utilities. Most relevant for the current project are  developments in Natural Language Processing (NLP), in software tools, and in institutional eco-systems. Natural Language Processing, which may be considered one branch of Data Science, has taken advantage of the huge amounts of textual data available on the web - either originally produced for the web, or in the form of scanned documents. Equally important were developments in computer language recognition (speech recognition and Optical Character Recognition). Search engines need efficient ways to determine which pages are likely to be relevant in response to a user's search entry. This led, for example, to concepts such as [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) (Text Frequency - Inverse Document Frequency), a family of statistical measures that indicate the importance of a word (or token) in a document in a particular corpus, expressed by a number between 0 and 1. A word that is frequent in a particular document, but relatively infrequent across all the documents in the corpus, will have a high TF-IDF value in that document. TF-IDF is now widely used not only in search engines, but in all kinds of research projects that deal with natural language. Similarly, research teams at Google ([GloVe](https://nlp.stanford.edu/projects/glove/)) and Facebook ([fastText](https://fasttext.cc/)) have contributed significantly to the development of so-called word-embeddings (word vectors), which allow one to express the semantic distance between two words as a vector or as a number between 0 and 1. Word embeddings, which are based on neural network architecture, are now routinely used in a wide variety of NLP tasks. Typically, such developments are initially driven by commercial interests, but yield tools that are useful for research purposes in a wide variety of disciplines.  

On the software side, the introduction of the [Jupyter Notebook][jupyter] (developed by Fernando Pérez, UC Berkeley) fundamentally changed research and teaching in Data Science. [Jupyter][jupyter] is an application that allows one to run Python (or one of many other programming languages) in a local page of a web browser. The [Jupyter Notebook][jupyter] mixes interactive code with narrative text, and shows the results of its computations (including visualizations) on that same page. [Jupyter Notebooks][jupyter] can easily be transformed into HTML for web publication (where they can be displayed for explanatory purposes, but cannot be run) and can be rendered by [Github][git] (a popular software development platform). All the coding for the present project is done in [Jupyter Notebooks][Jupyter] and made available on the Github pages of [Compass][compass]. 

In terms of institutional embedding, many universities now have an institute for Data Science, a Department of Digital Humanities, or some type of technical support or training for humanities scholars and social scientists. Although the specifics are very different from one university to the next, such initiatives may create exciting venues for interaction between disciplines, working on very different data with similar computational tools. Where such programs exist students (graduate and undergraduate) may need real-world research projects where they can display and apply their often very considerable data-analytic skills.

Taken together, the developments in (digital) Assyriology and in Data Science provide an exciting opportunity and form the background against which this project was made possible. Initially, Assyriological web projects were used almost exclusively as a cheap and convenient alternative to book publications, where search capabilities were perceived as the main added value. An early exception was *Analysing Literary Sumerian. Corpus Based Approaches* (edited by Jarle Ebeling and Graham Cunningham; 2007), which attempted to utilize the [ETCSL][etcsl] data set for a corpus-linguistic approach to Sumerian. The volume contains some excellent articles, but did not start a new trend. 

With input from Data Science, Assyriological data sets enable the search for patterns, not immediately visible to the naked eye (or latent variables, in Data Science speak). Few projects so far have attempted to do so. Saana Svärd and her team (Helsinki University) have worked on word embeddings, using Akkadian data derived from [ORACC][ORACC]. The Machine Translation and Automated Analysis of Cuneiform Languages ([MTAAC][MTAAC]) team (including Emilie Pagé-Peron, Toronto and Bob Englund, UCLA) has received a major grant (2017) to train a neural network in order to translate the 67,000 Ur III documents now available on [CDLI][CDLI]. Both projects presented initial results in V B Jouloux , A R Gansell & A di Ludovico (eds) , [*CyberResearch on the Ancient Near East and Neighboring Regions*](https://doi.org/10.1163/9789004375086) Brill , Leiden 2018.

### 1.1.3 Compass

The present project, [Computational Assyriology][compass],  is intended as an introduction to some of the things one can do computationally with cuneiform text data. Three projects of increasing complexity will be discussed.

Chapter 3 will ask: what is the overlap between the Sumerian vocabulary of Old Babylonian (ca. 1,800 BCE) lexical texts and the corpus of contemporary literary texts. Old Babylonian lexical texts (lists of words) were used to introduce scribal pupils to reading and writing Sumerian (a dead language by this time). In a more advanced stage of their education, pupils started to copy Sumerian literary texts. It stands to reason, therefore, to see the lexical corpus as a kind of dictionary or concordance, that might have helped pupils to master the literary material. It has long been known, however, that the relationship between literary and lexical vocabulary is not that straightforward - is it possible to express that intuition computationally? And once we are at it, can we dig deeper and see which lexical texts and which literary texts contribute particularly to the overlap - or to the lack of overlap?

Chapter 4 will focus on the Treasure Archive, a group of administrative texts in Sumerian from the so-called Ur III period (last century of the third millennium). This hroup of documents has been studied in great detail by Paola Paoletti in her book *Der König und sein Kreis*. Goal of the scripts in Chapter 4 will be to create a social network out of the text data and to create interactive visualizations of that network. We will identify various ways to identify the most central actors in that network.

Chapter 5 will discuss word embeddings for Sumerian. Various types of word embeddings and various ways of representing Sumerian text will be explored. We will use word embeddings to explore the semantics of words for animals.

Chapter 6, finally, by way of conclusion will reflect on the advantages and disadvantages of a computational approach to Assyriology.

Before any of this can be done, however, it is necessary to gain access to data. Chapter 2, therefore, deals with data acquisition, with separate discussions of the various online projects ([ORACC][ORACC], [ETCSL][ETCSL], [BDTNS][BDTNS], and [CDLI][CDLI]).

Each of the chapters will discuss and explain code. More detailed explanations of the code will be found in the [Jupyter Notebooks][Jupyter] that accompany each chapter and that are available on the [Compass][compass] github pages. Chapter 2 (Data Acquisition) is more technical than any of the other chapters. Data acquisition, data formatting, and data cleaning are fundamental to any computational project and often take considerably more time than the data analysis. The goal of Chapter 2 (and the accompanying notebooks) is not just to prepare the data for the chapters 3-5, but also to provide the reader with technical means for exploring her own research questions. For an initial exploration of this book one may well skip Chapter 2 and go along with the analyses in the Chapters 3-5. In order to devise your own project, it will be necessary to gain a deeper understanding of how data is acquired and formatted and the (many) options that you have.

This study, finally, is not an introduction to Python. The chapters and notebooks contain code explanation, but for the fundamentals one would need to consult one of the many excellent introductions to Python, to scripting languages in general, or to data science that are available on the Web or in paper[^3].

## 1.2 The Software

### 1.2.1 Compass

In order to download the scripts and other files go to http://github.com/niekveldhuis/compass and click the green "Clone or Download" button. Now click "Download Zip" to acquire all the files that belong to the [Compass][compass] project. Unzip the files in a convenient place.

**Recommended usage**: after installing [Anaconda][] (section 1.2.2) open Anaconda Prompt (Windows) or the Terminal (Mac OS X) and type `jupyter lab`. Navigate to the place where you unzipped the [compass][] files and open the Notebook file (extension `ipynb`) that you wish to run.

### 1.2.2 Anaconda, Python, and Jupyter

In order to run the scripts in [Compass][] it is necessary to first install Python and Jupyter/Jupyter Lab. The easiest way to do so is by installing the [Anaconda Distribution][anaconda], a data science platform that includes a host of useful tools. It is important to choose the [Anaconda][anaconda] version with Python 3.7 or higher (if you happen to have 3.6, that should work, too). [Anaconda][anaconda] is available for Windows, Mac OS X, and Linux.

By installing [Anaconda][anaconda] you will have access to a number of programs and tools, including:
- **Python 3.x**. This is the programming language used in [Compass][]. Note that the [Compass][] scripts will not work with Python 2.x and will run into errors with so-called formatted strings in Python 3.5 or lower.
- **Python Packages**. With [Anaconda][] you install a host of useful packages such `pandas` (for creating and manipulating tables or dataframes), `requests` (for communicating with a server over the internet), or `re` (for using [regular expressions](https://www.regular-expressions.info/)). A package is a collection of functions, expanding Python's core functionality. [Anaconda][] installs many such packages for you, but occasionally we will need to install additional ones (see 1.2.3).
- **Anaconda Navigator**. This is the environment in which you can open Jupyter Notebook, Jupyter Lab, and various other programs by clicking on their icon. Anaconda Navigator is quite slow to start and most of the tools available there are not used in [Compass][]. It is recommended to start Jupyter Notebook or Jupyter Lab through a terminal (see below).
- **Jupyter Notebook**. Jupter Notebook is an environment in which you can run Python (or any of a host of other programming languages), mixed with explanatory text (in Markdown) and rich output, including graphs. Jupyter Notebook runs on a local web page in your browser. You can start Jupyter Notebook from within Anaconda Navigator, or you can open Anaconda Prompt (Windows) or the Terminal (OS X) and type `jupyter notebook`. Either way, starting Jupyter Notebook will open a directory listing - navigate to the place where you saved the [Compass][] files and open any file with the `ipynb` extension. For more details see the instructions for [installing](http://jupyter.org/install) and [running](https://jupyter.readthedocs.io/en/latest/running.html) notebooks on the [Jupyter][jupyter] web site.
- **Jupyter Lab**. Jupyter Lab is an environment in which you can run Jupyter Notebooks and various other tools, including a Markdown reader and editor. Jupyter Lab is considered the successor to the classical Jupyter Notebook and it is therefore recommended to use Jupyter Lab instead of Jupyter Notebook. You can open Jupyter Lab from within Anaconda Navigator, or you can open Anaconda Prompt (Windows) or the Terminal (OS X) and type `jupyter lab`. Either way, starting Jupyter Lab will open a directory listing - navigate to the place where you saved the [Compass][] files and open any file with the `ipynb` extension to run a notebook. You may also right click on any file with a `md` extension, select `open with` and choose "Markdown Preview". This will open a text document like the present one. If you choose to use Jupyter Lab, it will be necessary to install a Jupyter Lab extension; see below 1.2.2.1. For more information about Jupyter Lab, see their [website](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html). Jupyter Lab version 3.0 and higher does not require installation of `nodejs` or the Jupyter widgets extension anymore (see 1.2.2.1). You can tell the Jupyter Lab version by opening Anaconda Navigator. The icon for Jupyter Lab includes a version number.
- **Anaconda Prompt** (Windows). Anaconda Prompt is the Windows command prompt, to which are added a number of PATHs, so that you have access to all the Anaconda and conda commands. For Windows users it is recommended to use Anaconda Prompt to start Jupyter Lab (or Jupyter Notebook) by typing `jupyter lab` or `jupyter notebook`. Mac OS X users can use the standard Terminal with the same commands.

#### 1.2.2.1 Installing the Jupyter Lab ipywidgets extension
If you are running Jupyter Lab 3.0 or higher you may skip this step. Check the version number by opening Anaconda Navigator and inspect the icon for Jupyter Lab.

Jupyter Lab is designed as an extensible environment; for [Compass][] to run under earlier versions of Jupyter Lab (<3.0) we will need at least one such [extension](https://jupyterlab.readthedocs.io/en/stable/user/extensions.html) in order to run a pretty progress bar with [tqdm](https://tqdm.github.io/), and use interactive tools. Before extensions can be installed we need to install `nodejs`.

Open the Anaconda Prompt (Windows) or Terminal (OS X) and copy the following commands:
``` bash
conda install nodejs
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
For more information about installing the jupyter widgets for Jupyter Lab see the instructions [here](https://ipywidgets.readthedocs.io/en/stable/user_install.html#installing-the-jupyterlab-extension).

### 1.2.3 Additional Python Packages

Python libraries or packages are extensions of the Python core that provide useful functionality. A package needs to be *installed* once (after which it may be updated occasionally) but must be *imported* each time a script that uses the package is run. Each script, therefore, starts with a number of import statements that look like: 

```python
import requests   # a library for communicating with servers over the internet
import pandas as pd # data analytics
from gensim.models.fasttext import FastText as FT_gensim # word embeddings
```
Installing packages can be challenging, in particular if your computer happens to have multiple instances of Python (which is not uncommon). Luckily, many important packages belong to the [Anaconda Distribution][anaconda] and are properly installed with [Anaconda][anaconda]. Installing additional packages can be done from within a [Jupyter][jupyter] notebook with the command

```python
%conda install [package name]
```
or from the Anaconda Prompt (Windows)/Terminal (Mac OS X) with the command
```bash
conda install [package name]
```
Installing from the terminal, however may not always work properly and when you try to `import` the package you may get an error. The notebook `install_packages.ipynb` in the directory `1_Preliminaries` of [Compass][compass]  provides a more robust way of installing packages, based on a [blog](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/) by Jake VanderPlas.

### 1.2.4 Windows vs. Mac OS X: Unicode and UTF-8

[Jupyter][jupyter] notebooks and Python are largely platform independent and the notebooks in this project are tested for both Windows and Mac OS X. There is one issue that one may encounter with some frequency and that is reading and writing files. Python 3 by default stores any string as Unicode, using the UTF-8 encoding (an encoding is a way to represent a Unicode code point as a set of bytes in memory). Internally, however, Windows uses another kind of encoding (usually CP-1252), which means that in reading and writing files the option `encoding = "utf-8"` needs to be added explicitly. The option is superfluous in Mac OS X (or in Unix) where `utf-8` is the default, but is added in the notebooks at every place appropriate to ensure interoperability, as in the following examples:  

```python
with open("equivalencies/equivalencies.json", 'r', encoding="utf-8") as f: # reading
    eq = json.load(f)
with open('output/alltexts.csv', 'w', encoding="utf-8") as w: # writing
    df.to_csv(w, index=False)
```

In developing your own code, it is advisable to do so (even if things work fine without the `encoding` option on your computer), to ensure that your code will run for others, too. 

To complicate matters further, the popular spreadsheet program Excel expects files to be encoded in `utf-16`. Many computers will open `.csv`  files automatically in Excel. Excel will scramble special characters (such as š) unless you tell it explicitly that your file is in `utf-8`. To get around this issue there are three options: 

- **Recommended**: instead of Excel use Google Sheets, which by default uses the `utf-8` encoding. Keep all files in `utf-8`.
- Import the file in Excel, following instructions [here](https://www.itg.ias.edu/content/how-import-csv-file-uses-utf-8-character-encoding-0) for Excel 2007. This option also allows you to keep all files in `utf-8`.
- In writing output files, meant to be read in Excel, use `encoding = 'utf-16'` and open the output file directly in Excel. This option is recommended only if Excel is your end station. If you ever wish to use the file in a Notebook again, you would need to remember its encoding.

Binary files (such as `ZIP` files, pickled files, or image files) have no encoding since they do not represent characters. They should be opened with the option `rb` (read binary) or `wb` (write binary), which does not allow an `encoding` parameter.

```python
with open("zipfiles/obmc.zip", "rb") as f:
    z = zipfile.ZipFile(f)
```

## 1.3 The Practice of Computational Assyriology

Computational Assyriology will have to develop a new set of values and practices, combining practices from Assyriology and from Data Science. Data Science commonly embraces three core principles: open data, open code, and reproducibility. How can the practice of Computational Assyriology incorporate these principles?

### 1.3.1 Reproducibility

The discipline of Assyriology evolved over more than 150 years, inheriting some of its practices from other ancient philologies such as Classics and Biblical studies. The common practice of Assyriology builds upon an infrastructure that is rarely questioned or discussed and that includes footnotes, standardized lists of abbreviations, and well-stocked research libraries. Thus, a footnote saying "CT 20 41 K 4432 i 6'" leads a researcher to the hand drawing of a particular cuneiform tablet from Nineveh with omens that is kept in the British Museum and was published by Wallis Budge in 1904 in the series *Cuneiform Texts from Babylonian Tablets in the British Museum* Vol. 20. Column 1 line 6'  presumably supports the author's statement and any Assyriologist can go ahead and see for herself. This, one might say, represents reproducibility in traditional Assyriology and the often very considerable number of footnotes in Assyriological articles and books shows how seriously this is taken (in a more ignominious perspective one might see the flood of footnotes and esoteric abbreviations as effective border markers that keep out the non-initiated). A bottleneck in this approach to reproducibility is the well-stocked library. Researchers who work at smaller institutions or in areas of the world with little tradition in the field of cuneiform studies are essentially left out of the conversation - a problem that is increasingly alleviated by making publications available online.

In Data Science reproducibility is a core value as well as a core problem[^4]. Ideally, reproducibility means that research is published in such a way that any researcher can access the data and run the same code to arrive at the same result. In practice, this ideal is rarely fully realized for a number of reasons. First, the original researcher may not own the data (copyright issues), or the data may be sensitive (for instance, privacy concerns). More relevant for Assyriology, the data may be constantly changing. Currently active projects such as [ORACC][oracc], [CDLI][cdli], and [BDTNS][bdtns] make their data available as time capsules, but do not give easy access to all the previous stages. In practice that means that an analysis based on, say, the [BDTNS][bdtns] transliterations of Drehem texts will yield different results when run at different times. This issue could be resolved by including the full data set, as used by the researcher, in the research publication, or in a repository created for that purpose. This may well be how this should be done in the (near) future, but for now, Assyriological journals do not offer such facilities and the data sets easily grow out of proportion for a site like [Github][git] to offer a real solution.

More problematic for the present project are the practical limitations in reproducing and rerunning code. Standard Python libraries (such as `Pandas` or `requests`) are usually unproblematic to install and use. Others, such as `fastText` may require some wrangling, the installation of separate software, or the use of more arcane options in a package management system. This, by itself, does not make it impossible to reproduce the analysis, but does put considerable obstacles in the way and may discourage many. Where possible, therefore, Compass will use widely used and robustly supported modules - in Chapter 6 we will not use the original `fasttext` package, but rather the implementation in `gensim`, exactly for that reason. More problematic even are issues of versioning and compatibility. Most Python libraries are under constant development, and so is Python itself. Some developers consistently try to make their software backwards compatible, so that earlier code will run smoothly on later versions - but this is not always the case. A particularly bad example is `folium`, a Python wrapper around `leaflet`, which is a Java Script package for creating interactive maps. Each version of `folium` seems to have its own set of function names, updating `leaflet` is likely to make earlier scripts invalid. It is important, therefore, to mention the version of each library used. In some cases it may be necessary to update or maintain the code (adapt it to new versions of the packages used) - but at the same time such updates will undermine the ideal of reproducibility in that the reader will see a version of the code that was not used in the original research.

Not all of these problems have a straightforward solution and we may thus conclude that Computational Assyriology should strive for maximal reproducibility, in the awareness that full reproducibility may not be achievable.

### 1.3.2 Open Data

Historically, Assyriologists have been rather protective of their data, guarding data until final publication. All Assyriologists know examples of projects that, in the end, never arrived at that final stage. The bar for print publication was high, and scholars needed time to put their data in the best shape possible.

This has changed, to some extent, with the arrival of digital publication. Digital publication is not as final as print is, one can publish provisional data sets, in the hope that it is useful to someone, even if it is not perfect. Digital cuneiform data, moreover, are usually a group effort, not as immediately related to a particular author as a print publication is. Digital data, therefore, tend to be perceived as of lesser quality than print data - even if that judgment may frequently be unfair. Most major digital cuneiform projects today have embraced the principle of open data (exceptions are [SEAL][seal] and [ArchiBab][archibab]) and make their data sets available for free.

Data, however, not only need to be free, they also need to be findable and re-usable. Data Science, fond of acronyms, has introduced the [FAIR](https://www.force11.org/group/fairgroup/fairprinciples) principle (or rather a set of FAIR principles): Findable, Accessible, Interoperable, Re-Usable. The *Findable* principle refers primarily to the availability of metadata and persistent identifiers. Cuneiform studies is in the lucky circumstance of having identifiers in the form of P and S numbers (for cuneiform object and seals, respectively; assigned by [CDLI][cdli]) and Q numbers (for composite texts; assigned by [ORACC][oracc]). As of January 2020, [epsd2][epsd2] is assigning object identifiers to Sumerian words. Ideally, we would also have persistent identifiers for places, persons, etc. Identifiers for places are currently assigned by [Pleiades](https://pleiades.stoa.org/), a gazetteer of ancient place names.  The project started with place names from the ancient Greek and Roman world, but is now also expanding into Ancient Near Eastern place names and is actively used by the [ARMEP](https://www.armep.gwi.uni-muenchen.de/) project for drawing digital maps, showing where cuneiform objects were found. Identifiers for persons and for Akkadian words currently do not exist.

The *Accessible* principle essentially says that data should be made available in a way that it can always be obtained by humans and machines, without requiring unusual software or techniques. In general, this is not an issue for the cuneiform projects under discussion here. Data can be downloaded over the web directly from the project server or from [Github][github] in a way that is straightforward and intuitive. Machine accessibility is available for [ORACC][oracc] and [CDLI][cdli], but currently not for [BDTNS][bdtns].

The *Interoperable* principle requires data and meta-data to be machine-actionable. Here, digital cuneiform does not fare so well, in particular because concepts used in meta-data are not always well-defined or linked to established ontologies.

Finally the *Re-usable* principle implies that (meta)-data are labeled and described explicitly, so that the data can be used not only by a close colleague, but by anyone who may develop an interest in that data. Here, again, digital Assyriology is not fully compliant.

The FAIR principles are designed to develop a metric, indicating whether a particular data set is more or less FAIR. Clearly, data sets available through [ORACC][oracc], [CDLI][cdli], or [BDTNS][bdtns] will not receive the maximum score in this metric. A large step forward will be the implementation of unique identifiers for Akkadian words and persons. On the whole, however, keeping in mind that FAIR principles were developed with, for instance, medical data in mind, Assyriology is not doing badly.

### 1.3.3 Open Source

Open Source generally refers to large projects such Python or Linux, which are carried by communities of volunteers who contribute code. Packages in Python and R are developed that way and Jupyter is another example of a successful open source project.

For [Compass][compass] open source simply means that the scripts for data acquisition, formatting, cleaning, and analysis are made available through [Github][github], at the address http://github.com/niekveldhuis/compass. Github was founded in 2008 and has grown to host the code of millions of users, including [ORACC](https://github.com/oracc/), and [CDLI](https://github.com/cdli-gh); the CDLI repository includes the code of the *Machine Translation and Automated Analysis of Cuneiform Languages* project [MTAAC][mtaac]. [Github][github] is thus part of the eco-system that makes Computational Assyriology possible.

## 1.4 Why Computational Assyriology?

### 1.4.1 Scalability

### 1.4.2 Accessibility


[^Charpin2014]: [D. Charpin, *Bibliotheca Orientalis* 71, 331-357](http://doi.org/10.2143/BIOR.71.3.3062115 ) (open access).

[^2]: For literary Sumerian we now have the excellent *Glossaire sumérien-français* by Pascal Attinger (2021).
[^3]: See, for instance, Melanie Walsh, *Introduction to Cultural Analytics & Python*, Version 1 (2021), https://doi.org/10.5281/zenodo.4411250.
[^4]: Justin Kitzes, Daniel Turek, Fatma Deniz (eds); *The Practice of Reproducible Research: Case Studies and Lessons from the Data-Intensive Sciences* 2017. [online version](https://www.practicereproducibleresearch.org/)



[Charpin2014]

[Anaconda]: http://www.anaconda.com
[ARCHIBAB]: http://www.archibab.fr
[Compass]: http://github.com/niekveldhuis/compass
[ETCSL]: http://etcsl.orinst.ox.ac.uk
[CDLI]: http://cdli.ucla.edu
[MTAAC]: https://cdli-gh.github.io/mtaac/
[ORACC]: http://oracc.org
[BDTNS]: http://bdtns.filol.csic.es/
[SEAL]: https://www.seal.uni-leipzig.de/
[epsd]: http://psd.museum.upenn.edu/epsd1/index.html
[epsd2]: http://oracc.org/epsd2
[Jupyter]: http://jupyter.org
[git]: http://github.com
[jupyterlab]: https://jupyterlab.readthedocs.io/en/stable/
[Markdown]: https://en.wikipedia.org/wiki/Markdown