#!/usr/bin/env python
# coding: utf-8

# # 2 Data Acquisition
# 
# In this chapter we will discuss data acquisition and data formatting for four online Assyriological projects: [ORACC](http://oracc.org) (2.1), [ETCSL](https://etcsl.orinst.ox.ac.uk/), (2.2) [CDLI](http://cdli.ucla.edu) (2.3) and [BDTNS](http://bdtns.filol.csic.es/) (2.4). 
# 
# The data in [CDLI](http://cdli.ucla.edu) and [BDTNS](http://bdtns.filol.csic.es/) are made available in raw-text format, with transliteration only. For instance (atf text format as used by [CDLI](http://cdli.ucla.edu)):
# 
# ```{admonition} ATF
# :class: tip, dropdown
# ATF is short for ASCII Text Format. [ORACC](http://oracc.org) and [CDLI](http://cdli.ucla.edu) use different versions of the ATF format. The various symbols and conventions are explained [here](http://oracc.org/doc/help/editinginatf/cdliatf/).
# ```

# &P100001 = AAS 013  
# #atf: lang sux  
# @tablet  
# @obverse  
# @column 1  
# $ beginning broken   
# 1'. a2-bi u4 [...] 5(u) 4(disz) 2/3(disz)-kam  
# 2'. 8(gesz2) 3(u) 5(disz) gurusz u4 1(disz)-sze3  
# 3'. si-i3-tum nig2-ka9-ak mu en-mah-gal-an-na ba-hun  
# 4'. 2(asz) 2(barig) sze gur

# This data format is easy to read for humans (those humans who know Sumerian), but less so for computers. It is necessary to tell the software which data elements belong to the text and which do not (for instance, line numbers and surface labels) and what the various non-textual elements mean. We will see examples of how such data sets may be used in the sections 2.3 ([CDLI](http://cdli.ucla.edu)) and 2.4 ([BDTNS](http://bdtns.filol.csic.es/)). Section 2.4 will also demonstrate code for constructing a search engine for [BDTNS](http://bdtns.filol.csic.es/) that ignores sign values - that is, searching for `luh` will also find `sukkal`, etc. The code uses both [BDTNS](http://bdtns.filol.csic.es/) data and the [ORACC Global Sign List](http://orac.org/ogsl), showing how data from different projects can be mashed into a single tool.
# 
# The data in [ORACC](http://oracc.org) and [ETCSL](https://etcsl.orinst.ox.ac.uk/) are made available in [JSON](http://json.org) and [XML](http://xml.org), respectively. Those formats are very explicit and atomistic. They less easy to read for humans, but are very flexible for computational usage and allow for multiple levels of annotation (with e.g. lexical, morphological, and  graphemic information) at the same time. The data in [ORACC](http://oracc.org) and [ETCSL](https://etcsl.orinst.ox.ac.uk/) includes lemmatization, linking each word to an entry in a glossary. The following is an example of a JSON file, one may click on any of the lines with an arrow to expose more or less of the hierarchical structure. The usage of JSON and XML files will be discussed in sections 2.1 and 2.2.

# In[1]:


import json
import panel as pn
pn.extension()
with open('P100001.json', 'r', encoding='utf8') as p:
    P100001 = json.load(p)
json_object = pn.pane.JSON(P100001, name='P100001', depth=1, height=300, width=500, theme = 'light')
json_object


# This represents the same text as the one shown in raw text format above ([P100001 = AAS 13](http://oracc.org/epsd2/P100001)), but in this case provided with lemmatization and explicit information on the various data types.
# 
# ```{admonition} Full JSON file
# :class: tip, dropdown
# To see the full JSON file of P100001 click [here](https://github.com/niekveldhuis/compass/blob/master/2_Data_Acquisition/P100001.json)
# 
# ```
# 
# The Compass project mostly deals with [ORACC](http://oracc.org) data, and much of this chapter will provide code and explanations for how to extract the various types of information that are included in the JSON files. The parsing of the [ETCSL](https://etcsl.orinst.ox.ac.uk/) XML files (section [2.2](2.2) is, to some extent, redundant, because all of the [ETCSL](https://etcsl.orinst.ox.ac.uk/) data have been incorporated into [epsd2/literary](http://oracc.org/epsd2/literary) and can be parsed with the tools for regular [ORACC](http://oracc.org) projects. 
# 
# The Chapters 3-6 of Compass will work with [ORACC](http://oracc.org) data and will parse that data with the tools demonstrated and explained in section [2.1](2.1). Chapter 2 is not needed to follow along in those chapters. The present chapter is primarily meant for researchers who wish to pursue their own computational projects and need a deeper understanding of how the data is acquired and formatted.

# In[ ]:




