#!/usr/bin/env python
# coding: utf-8

# # 2.4.3 Search BDTNS
# In order to run the code below, first run [2_4_1_Data_Acquisition_BDTNS.ipynb](./2_4_1_Data_Acquisition_BDTNS.ipynb) and [2_4_2_Build_Sign_Search.ipynb](./2_4_2_Build_Sign_Search.ipynb) in that order. These notebooks produce two files (`bdtns_tokenized.p` and `ogsl_dict.p`) that are used by the present code. You can re-run those notebooks to capture the latest data in [BDTNS](http://bdtns.filol.csic.es/) and [OGSL](http://oracc.org/ogsl).
# 
# The search function is different from the search on the [BDTNS](http://bdtns.filol.csic.es/) web site in that it searches for a sequence of **signs** (within a single line) irrespective of reading.

# In[1]:


get_ipython().run_line_magic('run', 'py/Search_BDTNS.py')
disp


# # Search Instructions
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
# - To search for a compound sign by sign name, enter it between pipes (|) and use the [OGSL](http://oracc.org/ogsl) operators ., &, %, etc. The "times" sign may be represented by \* (enter |UR₂×A| or |UR₂\*A|, but not |URxA|).
# 
# - Wildcard: x or X, represents any number of signs in between (e.g. ku6-x-muszen will find all lines where HA is followed by HU with zero or more signs in between).
# 
# - For large numbers of hits, the clickable links to [BDTNS](http://bdtns.filol.csic.es/) editions will make display very slow. Unclick the check box to display [BDTNS](http://bdtns.filol.csic.es/) numbers only, without links.

# In[ ]:




