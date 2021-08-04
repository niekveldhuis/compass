#!/usr/bin/env python
# coding: utf-8

# # 1. Introduction
# 
# This book project attempts to bring together two recent trends: the digital turn in Assyriology, and the rise of Data Science. Although Assyriologists had actively used databases since the nineteen sixties, such data sets were available only to a small circle - important examples include Miguel Civil's Nippur Corpus (a group of Sumerian literary texts, now largely available on [ETCSL](https://etcsl.orinst.ox.ac.uk/) and Simo Parpola's database of Neo-Assyrian texts, subsequently published in  print in the State Archives of Assyria series and now available online in [SAAo](http://oracc.org/saao) . With the advent of the Internet, it became possible to give public access to data in the form of transliterations, translations, photographs, and glossaries. This development began in earnest in 1996 with the appearance of the Electronic Text Corpus of Sumerian Literature ([ETCSL](https://etcsl.orinst.ox.ac.uk/)), and continues to the present day. Data Science is an interdisciplinary field that draws its techniques from Statistics and Computer Science and (essentially) involves a third field, a domain discipline. Although "Data Science" is a relatively recent coinage, its roots go back well into the twentieth century. In recent years many universities have created institutes or departments for Data Science and/or for Digital Humanities, and have developed undergraduate and graduate programs in such fields. The eco-system for applying Data Science methods to Assyriological data, therefore, is much better today than it was even five years ago. 
# 
# This Introduction will briefly discuss the history of the digital turn in Assyriology and some relevant aspects of developments in Data Science (1.1).  Section 1.2 is devoted to principles of Data Science in Assyriology: open data, open source, and reproducibility. Section 1.3 will ask the "why" question, focussing on scalability and accessibility. Finally we will discuss software and installing software (1.4), with a brief discussion of differences between Windows and Mac.
# 
# ## 1.1 Assyriology and Data Science
# 
# ### 1.1.1 Digital Assyriology
# 
# The turn towards publicly available electronic data is due in no small part to the initiative by Jeremy Black (Oxford University) to develop the Electronic Text Corpus of Sumerian Literature ([ETCSL](https://etcsl.orinst.ox.ac.uk/)), which started in 1996 and remained active until 2006, when it became archival. Initially [ETCSL](https://etcsl.orinst.ox.ac.uk/) offered composite editions (transliterations) of Sumerian literary texts with translations. In version 2, using tools developed by Steve Tinney, the entire corpus was lemmatized, which allowed for the addition of glossaries and other tools for search and research.  
# 
# [ETCSL](https://etcsl.orinst.ox.ac.uk/) was quickly followed by the Cuneiform Digital Library Inititative ([CDLI](http://cdli.ucla.edu)), created by Bob Englund, UCLA. This project provides access to metadata, photographs, line drawings, and transliterations (occasionally also translations) of cuneiform documents of all periods and genres. Importantly, [CDLI](http://cdli.ucla.edu) assigns unique ID numbers to cuneiform objects. Initially, [CDLI](http://cdli.ucla.edu) focused on administrative and legal documents from the fourth and third millennium BCE, but today one may find a broad variety of text genres from all periods of cuneiform. In 2006 (after several precursors) the Open Richly Annotated Cuneiform Corpus ([ORACC](http://oracc.org)) was built by Steve Tinney (University of Pennsylvania), who had previously been involved in the development of both [ETCSL](https://etcsl.orinst.ox.ac.uk/) and [CDLI](http://cdli.ucla.edu). [ORACC](http://oracc.org) works with semi-independent projects, where project directors have broad leeway in the definition of the scope of their project, but follow shared editorial principles in terms of transliteration and lemmatization.
# 
# :::{margin}
# See D. Charpin, "Ressources assyriologiques sur internet" [*Bibliotheca Orientalis* 71 (2014), 331-357](http://doi.org/10.2143/BIOR.71.3.3062115) (open access).
# :::
# 
# These three projects together fundamentally changed research and teaching in Assyriology and many Assyriologists today depend in one way or another on these and other digital resources. Together, these three make available large amounts of searchable data and make those data freely accessible to other scholars. All three projects use explicit standards, and reuse data where possible, setting a fairly high standard for digital Assyriology. Many other larger and smaller projects were created in their wake, among the most important are the Database of Neo-Sumerian Texts ([BDTNS](http://bdtns.filol.csic.es/); currently comprising almost 100,000 documents in transliteration); Sources of Early Akkadian Literature ([SEAL](https://seal.huji.ac.il/); several hundred literary texts in Akkadian from the third and second millennium BCE) and Archives Babyloniennes ([ARCHIBAB](https://www.archibab.fr/); a collection of thousands of Old Babylonian letters, and legal, and administrative documents).  The [BDTNS](http://bdtns.filol.csic.es/) data set is freely available (transliterations and metadata). [ARCHIBAB](https://www.archibab.fr/) and [SEAL](https://seal.huji.ac.il/) both make their data available in the form of PDFs and restrict usage to non derivatives, making the data of these projects unavailable for computational analysis.
# 
# :::{margin}
# For literary Sumerian we now have the excellent [*Glossaire sumérien-français*](https://www.harrassowitz-verlag.de/isbn_9783447116169.ahtml) by Pascal Attinger (2021).
# :::
# 
# Reflecting on this (very abbreviated) history one may note that scholars working in Sumerian have been the driving force behind almost all the major projects (exceptions are [ARCHIBAB](https://www.archibab.fr/) and [SEAL](https://seal.huji.ac.il/)). The main reason for this situation is that the (traditional) tool set for reading Sumerian is far behind - there is no comprehensive (printed) Sumerian dictionary and no generally accepted Sumerian grammar. In other words: the need for creating such (digital) tools and the opportunities afforded by the development of the digital landscape were felt much more acutely by scholars working in Sumerian.
# 
# 
# ### 1.1.2 Data Science
# 
# Data Science developed in response to the quantitative explosion in data collected and produced by cell phones, personal computers, tablets, and web-connected utilities. Most relevant for the current project are  developments in Natural Language Processing (NLP), in software tools, and in institutional eco-systems. Natural Language Processing, which may be considered one branch of Data Science, has taken advantage of the huge amounts of textual data available on the web - either originally produced for the web, or in the form of scanned documents. Equally important were developments in computer language recognition (speech recognition and Optical Character Recognition). Search engines need efficient ways to determine which pages are likely to be relevant in response to a user's search entry. This led, for example, to concepts such as [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) (Text Frequency - Inverse Document Frequency), a family of statistical measures that indicate the importance of a word (or token) in a document in a particular corpus, expressed by a number between 0 and 1. A word that is frequent in a particular document, but relatively infrequent across all the documents in the corpus, will have a high TF-IDF value in that document. TF-IDF is now widely used not only in search engines, but in all kinds of research projects that deal with natural language. Similarly, research teams at Google ([GloVe](https://nlp.stanford.edu/projects/glove/)) and Facebook ([fastText](https://fasttext.cc/)) have contributed significantly to the development of so-called word-embeddings (word vectors), which allow one to express the semantic distance between two words as a vector or as a number between 0 and 1. Word embeddings, which are based on neural network architecture, are now routinely used in a wide variety of NLP tasks. Typically, such developments are initially driven by commercial interests, but yield tools that are useful for research purposes in a wide variety of disciplines.  
# 
# On the software side, the introduction of the [Jupyter Notebook](http://jupyter.org) (developed by Fernando Pérez, UC Berkeley) fundamentally changed research and teaching in Data Science. [Jupyter](http://jupyter.org) is an application that allows one to run Python (or one of many other programming languages) in a local page of a web browser. The [Jupyter Notebook](http://jupyter.org) mixes interactive code with narrative text, and shows the results of its computations (including visualizations) on that same page. [Jupyter Notebooks](http://jupyter.org) can easily be transformed into HTML for web publication (where they can be displayed for explanatory purposes, but cannot be run) and can be rendered by [Github](https://github.com) (a popular software development platform). All the coding for the present project is done in [Jupyter Notebooks](http://jupyter.org) and made available on the Github pages of [Compass](http://github.com/niekveldhuis/compass). 
# 
# In terms of institutional embedding, many universities now have an institute for Data Science, a Department of Digital Humanities, or some type of technical support or training for humanities scholars and social scientists. Although the specifics are very different from one university to the next, such initiatives may create exciting venues for interaction between disciplines, working on very different data with similar computational tools. Where such programs exist students (graduate and undergraduate) may need real-world research projects where they can display and apply their often very considerable data-analytic skills.
# 
# Taken together, the developments in (digital) Assyriology and in Data Science provide an exciting opportunity and form the background against which this project was made possible. Initially, Assyriological web projects were used almost exclusively as a cheap and convenient alternative to book publications, where search capabilities were perceived as the main added value. An early exception was *Analysing Literary Sumerian. Corpus Based Approaches* (edited by Jarle Ebeling and Graham Cunningham; 2007), which attempted to utilize the [ETCSL](https://etcsl.orinst.ox.ac.uk/) data set for a corpus-linguistic approach to Sumerian. The volume contains some excellent articles, but did not start a new trend. 
# 
# With input from Data Science, Assyriological data sets enable the search for patterns, not immediately visible to the naked eye (or latent variables, in Data Science speak). Few projects so far have attempted to do so. Saana Svärd and her team (Helsinki University) have worked on word embeddings, using Akkadian data derived from [ORACC](http://oracc.org). The Machine Translation and Automated Analysis of Cuneiform Languages ([MTAAC](https://cdli-gh.github.io/mtaac/)) team (including Emilie Pagé-Peron, Toronto and Bob Englund, UCLA) has received a major grant (2017) to train a neural network in order to translate the 67,000 Ur III documents now available on [CDLI](http://cdli.ucla.edu). Both projects presented initial results in V B Jouloux , A R Gansell & A di Ludovico (eds) , [*CyberResearch on the Ancient Near East and Neighboring Regions*](https://doi.org/10.1163/9789004375086) Brill , Leiden 2018.
# 
# ### 1.1.3 Compass
# 
# The present project, [Computational Assyriology](http://github.com/niekveldhuis/compass),  is intended as an introduction to some of the things one can do computationally with cuneiform text data. Three projects of increasing complexity will be discussed.
# 
# Chapter 3 will ask: what is the overlap between the Sumerian vocabulary of Old Babylonian (ca. 1,800 BCE) lexical texts and the corpus of contemporary literary texts. Old Babylonian lexical texts (lists of words) were used to introduce scribal pupils to reading and writing Sumerian (a dead language by this time). In a more advanced stage of their education, pupils started to copy Sumerian literary texts. It stands to reason, therefore, to see the lexical corpus as a kind of dictionary or concordance, that might have helped pupils to master the literary material. It has long been known, however, that the relationship between literary and lexical vocabulary is not that straightforward - is it possible to express that intuition computationally? And once we are at it, can we dig deeper and see which lexical texts and which literary texts contribute particularly to the overlap - or to the lack of overlap?
# 
# Chapter 4 will focus on the Treasure Archive, a group of administrative texts in Sumerian from the so-called Ur III period (last century of the third millennium). This hroup of documents has been studied in great detail by Paola Paoletti in her book *Der König und sein Kreis*. Goal of the scripts in Chapter 4 will be to create a social network out of the text data and to create interactive visualizations of that network. We will identify various ways to identify the most central actors in that network.
# 
# Chapter 5 will discuss word embeddings for Sumerian. Various types of word embeddings and various ways of representing Sumerian text will be explored. We will use word embeddings to explore the semantics of words for animals.
# 
# Chapter 6, finally, by way of conclusion will reflect on the advantages and disadvantages of a computational approach to Assyriology.
# 
# Before any of this can be done, however, it is necessary to gain access to data. Chapter 2, therefore, deals with data acquisition, with separate discussions of the various online projects ([ORACC](http://oracc.org), [ETCSL](https://etcsl.orinst.ox.ac.uk/), [BDTNS](http://bdtns.filol.csic.es/), and [CDLI](http://cdli.ucla.edu)).
# 
# Each of the chapters will discuss and explain code. More detailed explanations of the code will be found in the [Jupyter Notebooks](http://jupyter.org) that accompany each chapter and that are available on the [Compass](http://github.com/niekveldhuis/compass) github pages. Chapter 2 (Data Acquisition) is more technical than any of the other chapters. Data acquisition, data formatting, and data cleaning are fundamental to any computational project and often take considerably more time than the data analysis. The goal of Chapter 2 (and the accompanying notebooks) is not just to prepare the data for the chapters 3-5, but also to provide the reader with technical means for exploring her own research questions. For an initial exploration of this book one may well skip Chapter 2 and go along with the analyses in the Chapters 3-5. In order to devise your own project, it will be necessary to gain a deeper understanding of how data is acquired and formatted and the (many) options that you have.
# 
# :::{margin}
# See, for instance, Melanie Walsh, *Introduction to Cultural Analytics & Python*, Version 1 (2021), https://doi.org/10.5281/zenodo.4411250.
# :::
# 
# This study, finally, is not an introduction to Python. The chapters and notebooks contain code explanation, but for the fundamentals one would need to consult one of the many excellent introductions to Python, to scripting languages in general, or to data science that are available on the Web or in paper.

# ## 1.2 The Practice of Computational Assyriology
# 
# Computational Assyriology will have to develop a new set of values and practices, combining practices from Assyriology and from Data Science. Data Science commonly embraces three core principles: open data, open code, and reproducibility. How can the practice of Computational Assyriology incorporate these principles?
# 
# ### 1.2.1 Reproducibility
# 
# The discipline of Assyriology evolved over more than 150 years, inheriting some of its practices from other ancient philologies such as Classics and Biblical studies. The common practice of Assyriology builds upon an infrastructure that is rarely questioned or discussed and that includes footnotes, standardized lists of abbreviations, and well-stocked research libraries. Thus, a footnote saying "CT 20 41 K 4432 i 6'" leads a researcher to the hand drawing of a particular cuneiform tablet from Nineveh with omens that is kept in the British Museum and was published by Wallis Budge in 1904 in the series *Cuneiform Texts from Babylonian Tablets in the British Museum* Vol. 20. Column 1 line 6'  presumably supports the author's statement and any Assyriologist can go ahead and see for herself. This, one might say, represents reproducibility in traditional Assyriology and the often very considerable number of footnotes in Assyriological articles and books shows how seriously this is taken (in a more ignominious perspective one might see the flood of footnotes and esoteric abbreviations as effective border markers that keep out the non-initiated). A bottleneck in this approach to reproducibility is the well-stocked library. Researchers who work at smaller institutions or in areas of the world with little tradition in the field of cuneiform studies are essentially left out of the conversation - a problem that is increasingly alleviated by making publications available online.
# 
# :::{margin}
# Justin Kitzes, Daniel Turek, Fatma Deniz (eds); [*The Practice of Reproducible Research: Case Studies and Lessons from the Data-Intensive Sciences*](https://www.practicereproducibleresearch.org/) 2017.
# :::
# 
# In Data Science reproducibility is a core value as well as a core problem. Ideally, reproducibility means that research is published in such a way that any researcher can access the data and run the same code to arrive at the same result. In practice, this ideal is rarely fully realized for a number of reasons. First, the original researcher may not own the data (copyright issues), or the data may be sensitive (for instance, privacy concerns). More relevant for Assyriology, the data may be constantly changing. Currently active projects such as [ORACC](http://oracc.org), [CDLI](http://cdli.ucla.edu), and [BDTNS](http://bdtns.filol.csic.es/) make their data available as time capsules, but do not give easy access to all the previous stages. In practice that means that an analysis based on, say, the [BDTNS](http://bdtns.filol.csic.es/) transliterations of Drehem texts will yield different results when run at different times. This issue could be resolved by including the full data set, as used by the researcher, in the research publication, or in a repository created for that purpose. This may well be how this should be done in the (near) future, but for now, Assyriological journals do not offer such facilities and the data sets easily grow out of proportion for a site like [Github](https://github.com) to offer a real solution.
# 
# More problematic for the present project are the practical limitations in reproducing and rerunning code. Standard Python libraries (such as `Pandas` or `requests`) are usually unproblematic to install and use. Others, such as `fastText` may require some wrangling, the installation of separate software, or the use of more arcane options in a package management system. This, by itself, does not make it impossible to reproduce the analysis, but does put considerable obstacles in the way and may discourage many. Where possible, therefore, Compass will use widely used and robustly supported modules - in Chapter 6 we will not use the original `fasttext` package, but rather the implementation in `gensim`, exactly for that reason. More problematic even are issues of versioning and compatibility. Most Python libraries are under constant development, and so is Python itself. Some developers consistently try to make their software backwards compatible, so that earlier code will run smoothly on later versions - but this is not always the case. A particularly bad example is `folium`, a Python wrapper around `leaflet`, which is a Java Script package for creating interactive maps. Each version of `folium` seems to have its own set of function names, updating `leaflet` is likely to make earlier scripts invalid. It is important, therefore, to mention the version of each library used. In some cases it may be necessary to update or maintain the code (adapt it to new versions of the packages used) - but at the same time such updates will undermine the ideal of reproducibility in that the reader will see a version of the code that was not used in the original research.
# 
# Not all of these problems have a straightforward solution and we may thus conclude that Computational Assyriology should strive for maximal reproducibility, in the awareness that full reproducibility may not be achievable.
# 
# ### 1.2.2 Open Data
# 
# Historically, Assyriologists have been rather protective of their data, guarding data until final publication. All Assyriologists know examples of projects that, in the end, never arrived at that final stage. The bar for print publication was high, and scholars needed time to put their data in the best shape possible.
# 
# This has changed, to some extent, with the arrival of digital publication. Digital publication is not as final as print is, one can publish provisional data sets, in the hope that it is useful to someone, even if it is not perfect. Digital cuneiform data, moreover, are usually a group effort, not as immediately related to a particular author as a print publication is. Digital data, therefore, tend to be perceived as of lesser quality than print data - even if that judgment may frequently be unfair. Most major digital cuneiform projects today have embraced the principle of open data (exceptions are [SEAL](https://seal.huji.ac.il/) and [ARCHIBAB](https://www.archibab.fr/)) and make their data sets available for free.
# 
# Data, however, not only need to be free, they also need to be findable and re-usable. Data Science, fond of acronyms, has introduced the [FAIR](https://www.force11.org/group/fairgroup/fairprinciples) principle (or rather a set of FAIR principles): Findable, Accessible, Interoperable, Re-Usable. The *Findable* principle refers primarily to the availability of metadata and persistent identifiers. Cuneiform studies is in the lucky circumstance of having identifiers in the form of P and S numbers (for cuneiform object and seals, respectively; assigned by [CDLI](http://cdli.ucla.edu)) and Q numbers (for composite texts; assigned by [ORACC](http://oracc.org)). As of January 2020, [epsd2](http://oracc.org/epsd2) is assigning object identifiers to Sumerian words. Ideally, we would also have persistent identifiers for places, persons, etc. Identifiers for places are currently assigned by [Pleiades](https://pleiades.stoa.org/), a gazetteer of ancient place names.  The project started with place names from the ancient Greek and Roman world, but is now also expanding into Ancient Near Eastern place names and is actively used by the [ARMEP](https://www.armep.gwi.uni-muenchen.de/) project for drawing digital maps, showing where cuneiform objects were found. Identifiers for persons and for Akkadian words currently do not exist.
# 
# The *Accessible* principle essentially says that data should be made available in a way that it can always be obtained by humans and machines, without requiring unusual software or techniques. In general, this is not an issue for the cuneiform projects under discussion here. Data can be downloaded over the web directly from the project server or from [Github](https://github.com) in a way that is straightforward and intuitive. Machine accessibility is available for [ORACC](http://oracc.org) and [CDLI](http://cdli.ucla.edu), but currently not for [BDTNS](http://bdtns.filol.csic.es/).
# 
# The *Interoperable* principle requires data and meta-data to be machine-actionable. Here, digital cuneiform does not fare so well, in particular because concepts used in meta-data are not always well-defined or linked to established ontologies.
# 
# Finally the *Re-usable* principle implies that (meta)-data are labeled and described explicitly, so that the data can be used not only by a close colleague, but by anyone who may develop an interest in that data. Here, again, digital Assyriology is not fully compliant.
# 
# The FAIR principles are designed to develop a metric, indicating whether a particular data set is more or less FAIR. Clearly, data sets available through [ORACC](http://oracc.org), [CDLI](http://cdli.ucla.edu), or [BDTNS](http://bdtns.filol.csic.es/) will not receive the maximum score in this metric. A large step forward will be the implementation of unique identifiers for Akkadian words and persons. On the whole, however, keeping in mind that FAIR principles were developed with, for instance, medical data in mind, Assyriology is not doing badly.
# 
# ### 1.2.3 Open Source
# 
# Open Source generally refers to large projects such Python or Linux, which are carried by communities of volunteers who contribute code. Packages in Python and R are developed that way and Jupyter is another example of a successful open source project.
# 
# For [Compass](http://github.com/niekveldhuis/compass) open source simply means that the scripts for data acquisition, formatting, cleaning, and analysis are made available through [Github](https://github.com), at the address http://github.com/niekveldhuis/compass. Github was founded in 2008 and has grown to host the code of millions of users, including [ORACC](https://github.com/oracc/), and [CDLI](https://github.com/cdli-gh); the CDLI repository includes the code of the *Machine Translation and Automated Analysis of Cuneiform Languages* project [MTAAC](https://cdli-gh.github.io/mtaac/). [Github](https://github.com) is thus part of the eco-system that makes Computational Assyriology possible.
# 
# ## 1.3 Why Computational Assyriology?
# 
# ### 1.3.1 Scalability
# 
# ### 1.3.2 Accessibility

# (1.4.1)=
# ## 1.4 The Software
# 
# ### 1.4.1 Compass
# 
# The top right corner of each page of the Compassbook has three symbols: a rocket (run the script on Google Colab or in Binder), a Full Screen symbol, and a Download symbol. Each individual file can be downloaded as an .ipynb file, which can be opened in Jupyter Notebook or Jupyter Lab.
# 
# :::{note}
# Double clicking an .ipynb file does not open it properly. Follow the instructions below for opening Jupyter Lab and open the .ipynb file from within Jupyter Lab.
# :::
# 
# In order to download the entire set of scripts and other files go to http://github.com/niekveldhuis/compass and click the green "Clone or Download" button. Now click "Download Zip" to acquire all the files that belong to the [Compass](http://github.com/niekveldhuis/compass) project. Unzip the files in a convenient place.
# 
# :::{note}
# After installing [Anaconda](http://www.anaconda.com) (section 1.4.2) open Anaconda Prompt (Windows) or the Terminal (Mac OS X) and type `jupyter lab`. Navigate to the place where you unzipped the [Compass](http://github.com/niekveldhuis/compass) files and open the Notebook file (extension `ipynb`) that you wish to run.
# :::
# 
# ### 1.4.2 Anaconda, Python, and Jupyter
# 
# In order to run the scripts in [Compass](http://github.com/niekveldhuis/compass) it is necessary to first install Python and Jupyter/Jupyter Lab. The easiest way to do so is by installing the [Anaconda Distribution](http://www.anaconda.com), a data science platform that includes a host of useful tools. It is important to choose the [Anaconda](http://www.anaconda.com) version with Python 3.7 or higher (if you happen to have 3.6, that should work, too). [Anaconda](http://www.anaconda.com) is available for Windows, Mac OS X, and Linux.
# 
# By installing [Anaconda](http://www.anaconda.com) you will have access to a number of programs and tools, including:
# - **Python 3.x**. This is the programming language used in [Compass](http://github.com/niekveldhuis/compass). Note that the [Compass](http://github.com/niekveldhuis/compass) scripts will not work with Python 2.x and will run into errors with so-called formatted strings in Python 3.5 or lower.
# - **Python Packages**. With [Anaconda](http://www.anaconda.com) you install a host of useful packages such `pandas` (for creating and manipulating tables or dataframes), `requests` (for communicating with a server over the internet), or `re` (for using [regular expressions](https://www.regular-expressions.info/)). A package is a collection of functions, expanding Python's core functionality. [Anaconda](http://www.anaconda.com) installs many such packages for you, but occasionally we will need to install additional ones (see 1.4.3).
# - **Anaconda Navigator**. This is the environment in which you can open Jupyter Notebook, Jupyter Lab, and various other programs by clicking on their icon. Anaconda Navigator is quite slow to start and most of the tools available there are not used in [Compass](http://github.com/niekveldhuis/compass). It is recommended to start Jupyter Notebook or Jupyter Lab through a terminal (see below).
# - **Jupyter Notebook**. Jupter Notebook is an environment in which you can run Python (or any of a host of other programming languages), mixed with explanatory text (in Markdown) and rich output, including graphs. Jupyter Notebook runs on a local web page in your browser. You can start Jupyter Notebook from within Anaconda Navigator, or you can open Anaconda Prompt (Windows) or the Terminal (OS X) and type `jupyter notebook`. Either way, starting Jupyter Notebook will open a directory listing - navigate to the place where you saved the [Compass](http://github.com/niekveldhuis/compass) files and open any file with the `ipynb` extension. For more details see the instructions for [installing](http://jupyter.org/install) and [running](https://jupyter.readthedocs.io/en/latest/running.html) notebooks on the [Jupyter](http://jupyter.org) web site.
# - **Jupyter Lab**. Jupyter Lab is an environment in which you can run Jupyter Notebooks and various other tools, including a Markdown reader and editor. Jupyter Lab is considered the successor to the classical Jupyter Notebook and it is therefore recommended to use Jupyter Lab instead of Jupyter Notebook. You can open Jupyter Lab from within Anaconda Navigator, or you can open Anaconda Prompt (Windows) or the Terminal (OS X) and type `jupyter lab`. Either way, starting Jupyter Lab will open a directory listing - navigate to the place where you saved the [Compass](http://github.com/niekveldhuis/compass) files and open any file with the `ipynb` extension to run a notebook. You may also right click on any file with a `md` extension, select `open with` and choose "Markdown Preview". This will open a text document. For more information about Jupyter Lab, see their [website](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html). Jupyter Lab version 3.0 and higher does not require installation of `nodejs` or the Jupyter widgets extension anymore (see 1.4.2.1). You can tell the Jupyter Lab version by opening Anaconda Navigator. The icon for Jupyter Lab includes a version number.
# - **Anaconda Prompt** (Windows). Anaconda Prompt is the Windows command prompt, to which are added a number of PATHs, so that you have access to all the Anaconda and conda commands. For Windows users it is recommended to use Anaconda Prompt to start Jupyter Lab (or Jupyter Notebook) by typing `jupyter lab` or `jupyter notebook`. Mac OS X users can use the standard Terminal with the same commands.
# 
# #### 1.4.2.1 Installing the Jupyter Lab ipywidgets extension
# If you are running Jupyter Lab 3.0 or higher you may skip this step. Check the version number by opening Anaconda Navigator and inspect the icon for Jupyter Lab or run the following cell.

# In[1]:


get_ipython().system('jupyter lab --version')


# If your Jupyter Lab version is higher than 3.0 you may skip the rest of section 1.4.2.1. If not, you can update Jupyter Lab with the following command: 

# In[ ]:


get_ipython().run_line_magic('conda', 'update jupyterlab')


# Jupyter Lab is designed as an extensible environment; for [Compass](http://github.com/niekveldhuis/compass) to run under earlier versions of Jupyter Lab (<3.0) one will need at least one such [extension](https://jupyterlab.readthedocs.io/en/stable/user/extensions.html) in order to run a pretty progress bar with [tqdm](https://tqdm.github.io/), and use interactive widgets. Before extensions can be installed we need to install `nodejs`. Installing `nodejs` and the extension can be done with running the following cell. For more information about installing the jupyter widgets for Jupyter Lab see the instructions [here](https://ipywidgets.readthedocs.io/en/stable/user_install.html#installing-the-jupyterlab-extension).

# In[ ]:


get_ipython().run_line_magic('conda', 'install nodejs')
get_ipython().run_line_magic('conda', 'install ipywidgets')
get_ipython().system('jupyter labextension install @jupyter-widgets/jupyterlab-manager')


# You may need to close Jupyter Lab and open it again for the widgets extension to take effect. For more information about installing  and activating widgets see the overview [here](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-into-jupyterlab-1-or-2).

# #### 1.4.2.2 Some Trouble Shooting
# 
# If you just installed Anaconda and are new to working in Python or Jupyter, the instructions in 1.4.2 should get you going. If you worked with Python, Jupyter Notebooks or Jupyter Lab before, you may need to update one or more of the components.
# 
# If the `%conda` lines in 1.4.2.1 above do not work, this means that you have an older version of IPython (the Python version that runs in Jupyter Notebooks). Commands that begin with the percentage sign belong to the IPython `magic` functions, expanding on the functionality of standard IPython. In this notebook we will use `%conda` to call the package manager (alternatively, you may use `%pip`). The %conda and %pip functions were introduced in IPython version 7.3. To check the IPython version on your machine, open the terminal (Mac OS X) or the Anaconda Prompt (Windows) and type 
# ```bash
# ipython --version
# ```
# If necessary, update Ipython with the following cell:

# In[ ]:


import sys
get_ipython().system('conda upgrade --yes --prefix {sys.prefix} ipython')


# Other  issues may arise if you have (older) versions of Jupyter Notebook, Jupyter Lab or Jupyter Widgets that are not compatible with each other. Check for compatability by following the instructions [here](https://pypi.org/project/jupyterlab/). Recommended are Jupyter Lab version 3.0 or higher; Jupyter Notebook version 6.0 or higher and Jupyter Widgets version 7.5 or higher. These recommendations, however, may quickly become obsolete as new functionality is developed. To check the versions on your machine you may run the following lines.

# In[2]:


import ipywidgets
get_ipython().system('jupyter lab --version')
get_ipython().system('jupyter notebook --version')
ipywidgets.__version__


# If you need to update any of these, refer to section 1.4.3 below (Installing and Updating Python Packages).

# (1.4.3)=
# ### 1.4.3 Additional Python Packages
# 
# Python libraries or packages are extensions of the Python core that provide useful functionality. A package needs to be *installed* once (after which it may be updated occasionally) but must be *imported* each time a script that uses the package is run. Each script, therefore, starts with a number of import statements that look like: 
# 
# ```python
# import requests   # a library for communicating with servers over the internet
# import pandas as pd # data analytics
# from gensim.models.fasttext import FastText as FT_gensim # word embeddings
# ```
# Anaconda includes a treasure trove of important Python packages, including `Pandas` (for data manipulation), `bokeh` (interactive visualisations), `requests` (for communicating with web sites), `scikit-learn` (machine learning), etc. - those packages are already installed.
# 
# Inevitably, we will be using packages not included in the standard Anaconda distribution. Before they can be imported in a Python script such packages need to be installed. An example of a package that will need to be installed is `pyldavis`, a visualization tool for topic modeling, which we will use in Chapter 5.
# 
# The code for installing a package is
# ```python
# %conda install -c conda-forge [package name]
# ```
# For upgrading a package to the latest version you may use
# ```python
# %conda upgrade -c conda-forge [package name]
# ```
# With pip, upgrading is done as follows:
# ```python
# %pip install [package name] --upgrade
# ```
# 
# Examples:
# ```python
# %conda upgrade jupyterlab
# %conda install nodejs
# %conda install -c conda-forge pyldavis
# %conda upgrade -c conda-forge ipywidgets
# %pip install lexicalrichness --upgrade
# ```
# 
# :::{note}
# In some cases installing and upgrading may take a (very) long time and may result in the installation, removal, upgrading, or downgrading of a host of other packages. This is the case because conda will check for dependencies and for the compatibility of the newly installed software with other available packages. Under some circumstances conda may become entirely unusable. In such cases it may be advisable to install packages with pip.
# :::
# 
# Installing packages can be a rather frustrating experience. The issue is that a computer may have more than one instance of Python installed (this is not unusual). In order to use Python packages within a Jupyter Notebook, they need to be associated with the so-called Python *kernel* that runs in the background of the notebook. For a more technical description of the issue and a solution see the [article](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/) by Jake VanderPlas in his [Pythonic Preambulations](https://jakevdp.github.io/) blog. The solution by VanderPlas is implemented in the IPython "magic" functions `%conda` and `%pip`.

# ### 1.4.4 Windows vs. Mac OS X: Unicode and UTF-8
# 
# [Jupyter](http://jupyter.org) notebooks and Python are largely platform independent and the notebooks in this project are tested for both Windows and Mac OS X. There is one issue that one may encounter with some frequency and that is reading and writing files. Python 3 by default stores any string as Unicode, using the UTF-8 encoding (an encoding is a way to represent a Unicode code point as a set of bytes in memory). Internally, however, Windows uses another kind of encoding (CP-1252), which means that in reading and writing files the option `encoding = "utf-8"` needs to be added explicitly. The option is superfluous in Mac OS X (or in Unix) where `utf-8` is the default, but is added in the notebooks at every place appropriate to ensure interoperability, as in the following examples:  
# 
# ```python
# with open("equivalencies/equivalencies.json", 'r', encoding="utf-8") as f: # reading
#     eq = json.load(f)
# with open('output/alltexts.csv', 'w', encoding="utf-8") as w: # writing
#     df.to_csv(w, index=False)
# ```
# 
# In developing your own code, it is advisable to do so (even if things work fine without the `encoding` option on your computer), to ensure that your code will run for others, too. 
# 
# To complicate matters further, the popular spreadsheet program Excel expects files to be encoded in `utf-16`. Many computers will open `.csv`  files automatically in Excel. Excel will scramble special characters (such as š) unless you tell it explicitly that your file is in `utf-8`. To get around this issue there are three options: 
# 
# - **Recommended**: instead of Excel use Google Sheets, which by default uses the `utf-8` encoding. Keep all files in `utf-8`.
# - Import the file in Excel, following instructions [here](https://www.itg.ias.edu/content/how-import-csv-file-uses-utf-8-character-encoding-0) for Excel 2007. This option also allows you to keep all files in `utf-8`.
# - In writing output files, meant to be read in Excel, use `encoding = 'utf-16'` and open the output file directly in Excel. This option is recommended only if Excel is your end station. If you ever wish to use the file in a Notebook again, you would need to remember its encoding.
# 
# Binary files (such as `ZIP` files, pickled files, or image files) have no encoding since they do not represent characters. They should be opened with the option `rb` (read binary) or `wb` (write binary), which does not allow an `encoding` parameter.
# 
# ```python
# with open("zipfiles/obmc.zip", "rb") as f:
#     z = zipfile.ZipFile(f)
# ```

# In[ ]:




