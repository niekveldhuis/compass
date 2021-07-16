#!/usr/bin/env python
# coding: utf-8

# # 3.4 Overlap in Lexical and Admin Vocabulary
# This notebook use the techniques and the coding developed in 3.1 - 3.3 in order to compare the vocabulary of the Ur III administrative, legal, and epistolary documents with the vocabulary of the Old Babylonian lexical texts. Since there is nothing new about the code, is presented here with minimal comment.
# 
# N.B. Since the Ur III corpus is large, running this notebook may take a long time on older computers.

# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # this suppresses a warning about pandas from tqdm
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from ipywidgets import interact
from tqdm.auto import tqdm
tqdm.pandas() # initiate pandas support in tqdm, allowing progress_apply() and progress_map()
from nltk.tokenize import MWETokenizer
import zipfile
import json
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
from utils import *


# # 1. Download and Parse
# Download the JSON file of the Ur3 corpus (in [epsd2/admin/ur3](http://oracc.org/epsd2/admin/ur3)) and parse the JSON.

# In[ ]:


projects = "epsd2/admin/ur3"
words = get_data(projects)


# # 2 Select for Sumerian and Create Lemma field

# In[ ]:


words = words.loc[words["lang"].str.contains("sux")] 


# In[ ]:


words["lemma"] = words.progress_apply(lambda r: f"{r['cf']}[{r['gw']}]{r['pos']}" 
                            if r["cf"] != '' else f"{r['form']}[NA]NA", axis=1)
words["lemma"] = words["lemma"].str.lower()


# # 3 Represent the Administrative Corpus in Line by Line Format

# In[ ]:


adm_lines = words.groupby([words['id_text'], words['id_line']]).agg({
        'lemma': ' '.join
    }).reset_index()


# # 4. Mark MWEs in Administrative Data

# ## 4.1 Open the List of Lexical Vocabulary
# This list was created in 3.1. It contains all individual words (lemmas), plus all Multiple Word Expressions (= lexical entries). In the MWEs the lemmas are connect by underscores. 

# In[ ]:


with open('output/lex_vocab.txt', 'r', encoding = 'utf8') as r:
    lex_vocab = r.read().splitlines()
lex_vocab.sort()


# ## 4.2 MWEtokenizer
# Split the MWEs at the underscores and transform the resulting lists into tuples. The result is a list of tuples. Remove from the list tuples that contain only a single word. The list of tuples is now fed into the MWEtokenizer.

# In[ ]:


lex = [tuple(item.split("_")) for item in lex_vocab]
lex = [item for item in lex if len(item) > 1]
tokenizer = MWETokenizer(lex)


# ## 4.3 Use Tokenizer to Mark MWEs

# In[ ]:


lemma_list = [lemma.split() for lemma in adm_lines["lemma"]]
lemma_mwe = tokenizer.tokenize_sents(tqdm(lemma_list))
adm_lines["lemma_mwe"] = [' '.join(line) for line in lemma_mwe]


# # 5 Create the Set of Shared Administrative and Lexical Vocabulary

# In[ ]:


adm_lines.to_pickle('output/ur3_lines.p')


# ## 5.1 Create the Set of Administrative Vocabulary

# In[ ]:


adm_words1 = words["lemma"] # individual lemmas
adm_words_s1 = {lemma for lemma in adm_words1 if not '[na]na' in lemma}
adm_words2 = ' '.join(adm_lines['lemma_mwe']).split() # MWEs
adm_words_s2 = {lemma for lemma in adm_words2 if not '[na]na' in lemma}
adm_words_s2 = adm_words_s1 | adm_words_s2 # Union of individual lemmas and MWEs


# ## 5.2 Intersection of Lexical and Administrative Lemmas and MWEs

# In[ ]:


lexical_words_s2 = set(lex_vocab)
adm_lex = list(lexical_words_s2.intersection(adm_words_s2))
adm_lex = [item.replace('_', ' ') for item in adm_lex]
adm_lex.sort()


# # 6. Open Lexical Corpus

# In[ ]:


lex_lines = pd.read_pickle('output/lexlines.p')


# In[ ]:


Ura6 = ["dcclt/P227657",
"dcclt/P227743",
"dcclt/P227791",
"dcclt/P227799",
"dcclt/P227925",
"dcclt/P227927",
"dcclt/P227958",
"dcclt/P227967",
"dcclt/P227979",
"dcclt/P228005",
"dcclt/P228008",
"dcclt/P228200",
"dcclt/P228359",
"dcclt/P228368",
"dcclt/P228488",
"dcclt/P228553",
"dcclt/P228562",
"dcclt/P228663",
"dcclt/P228726",
"dcclt/P228831",
"dcclt/P228928",
"dcclt/P229015",
"dcclt/P229093",
"dcclt/P229119",
"dcclt/P229304",
"dcclt/P229332",
"dcclt/P229350",
"dcclt/P229351",
"dcclt/P229352",
"dcclt/P229353",
"dcclt/P229354",
"dcclt/P229356",
"dcclt/P229357",
"dcclt/P229358",
"dcclt/P229359",
"dcclt/P229360",
"dcclt/P229361",
"dcclt/P229362",
"dcclt/P229365",
"dcclt/P229366",
"dcclt/P229367",
"dcclt/P229890",
"dcclt/P229925",
"dcclt/P230066",
"dcclt/P230208",
"dcclt/P230230",
"dcclt/P230530",
"dcclt/P230586",
"dcclt/P231095",
"dcclt/P231128",
"dcclt/P231424",
"dcclt/P231446",
"dcclt/P231453",
"dcclt/P231458",
"dcclt/P231742",
"dcclt/P266520"]
lex_lines.loc[lex_lines["id_text"].isin(Ura6), "id_text"] = "dcclt/Q000043"


# # 7 Make DTM out of Lexical Corpus
# Use the shared administrative/lexical vocabulary as vocabulary and ngrams from 1 to 5.

# In[ ]:


cv = CountVectorizer(preprocessor = lambda x: x, tokenizer = lambda x: x.split(), vocabulary = adm_lex, ngram_range=(1, 5))
dtm = cv.fit_transform((lex_lines['lemma']))
lex_lines_dtm = pd.DataFrame(dtm.toarray(), columns= cv.get_feature_names(), index=lex_lines["id_text"])
lex_comp_dtm = lex_lines_dtm.groupby('id_text').agg(sum).reset_index()


# # 8 Compute n_matches for each lexical document

# In[ ]:


lex_comp_dtm["n_matches"] = lex_comp_dtm[adm_lex].astype(bool).sum(axis = 1)
lex_comp_dtm["id_text"] = [i[-7:] for i in lex_comp_dtm["id_text"]]


# # 9 Add Lexical Metadata
# From a pickled file, produced in 3.3.

# In[ ]:


lex = pd.read_pickle('output/lexdtm.p')
lex = pd.merge(lex, lex_comp_dtm[['n_matches', 'id_text']], on='id_text', how='inner')


# # 10 Add Normalized Measure

# In[ ]:


lex['norm'] = lex['n_matches'] / lex['length']


# # 11 Explore Results

# In[ ]:


lex.to_pickle('output/adm_lex.p')
anchor = '<a href="http://oracc.org/dcclt/{}", target="_blank">{}</a>'
lex2 = lex.copy()
lex2['id_text'] = [anchor.format(val,val) for val in lex['id_text']]
lex2['PQ'] = ['Composite' if i[0] == 'Q' else 'Exemplar' for i in lex['id_text']]


# In[ ]:


@interact(sort_by = lex2.columns, rows = (1, len(lex2), 1), min_length = (0,500,5), show = ["Exemplars", "Composites", "All"])
def sort_df(sort_by = "norm", ascending = False, rows = 25, min_length = 200, show = 'All'):
    if not show == 'All':
        l = lex2.loc[lex2['PQ'] == show[:-1]]
    else:
        l = lex2
    l = l.drop('PQ', axis = 1)
    l = l.loc[l.length >= min_length].sort_values(by = sort_by, ascending = ascending).reset_index(drop=True)[:rows].style
    return l


# In[ ]:





# In[ ]:




