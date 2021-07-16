#!/usr/bin/env python
# coding: utf-8

# # 3.3 Lexical Texts and their Relation to Literary Vocabulary
# 
# In section [3.2](./3_2_Lit_Lex.ipynb) we asked whether we can see differences between Old Babylonian literary compositions in their usage of vocabulary (lemmas and MWEs) attested in the lexical corpus. In this notebook we will change perspective and ask: are there particular lexical texts (or groups of lexical texts) that show a greater engagement with literary vocabulary than others?
# 
# In [3.1](./3_1_Lit_Lex_Vocab.ipynb) and [3.2](./3_2_Lit_Lex.ipynb) we used Multiple Word Expressions, connecting words that are found in a lexical entry by underscores (using `MWEtokenizer()` from the `nltk` module). The lemmas and MWE were visualized in Venn diagrams to illustrate the intersection between lexical and literary vocabulary.
# 
# In this notebook we will use the ngram option of the `CountVectorizer()` function in order to find sequences of lemmas that are shared between lexical and literary texts. A ngram is a continuous sequence of *n* words (or lemmas). 
# 
# In part, this notebook uses the same techniques and the same code as notebook [3.2](./3_2_Lit_Lex.ipynb), and the reader is referred there for further explanation.

# ## 3.3.0 Preparation
# We import the necessary modules and open files that were produced in earlier notebooks.

# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # this suppresses a warning about pandas from tqdm
import pandas as pd
from ipywidgets import interact
from sklearn.feature_extraction.text import CountVectorizer
from tqdm.auto import tqdm
import zipfile
import json


# Open the file `lexlines.p` which was produced in [3_1_Lit_Lex_Vocab.ipynb](./3_1_Lit_Lex_Vocab.ipynb). The file contains the pickled version of the DataFrame `lex_lines` in which the lexical ([dcclt](http://oracc.org/dcclt)) corpus is represented in line-by-line format.

# In[ ]:


lex_lines = pd.read_pickle('output/lexlines.p')


# ### 3.3.0.1 Special Case: OB Nippur Ura 6
# The sixth chapter of the Old Babylonian Nippur version of the thematic list Ura deals with foodstuffs and drinks. This chapter was not standardized (each exemplar has its own order of items and sections) and therefore no composite text has been created in [DCCLT](http://oracc.org/dcclt). Instead, the "composite" of [OB Nippur Ura 6](http://oracc.org/dcclt/Q000043) consists of the concatenation of all known Nippur exemplars of the list of foodstuffs. In our current dataframe, therefore, there are no lines where the field `id_text` equals "Q000043".
# 
# We create a "composite" by changing the field `id_text` in all exemplars of [OB Nippur Ura 6](http://oracc.org/dcclt/Q000043) to "Q000043". 

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


# ### 3.3.0.2 Open Shared Vocabulary List
# The file `lit_lex_vocab` is a list that includes all lemmas and Multiple Word Expressions that are shared by the literary corpus and the lexical corpus. This list was produced in [3_2_Lit_Lex.ipynb](./3_2_Lit_Lex.ipynb). In sections [3.1](./3_1_Lit_Lex_Vocab.ipynb) and [3.2](./3_2_Lit_Lex.ipynb) lexical *entries* were turned into MWEs by connecting the individual lemmas by underscores (as in `amar\[young\]n_ga\[milk\]n_gu\[eat\]v/t`). In this notebook we will take a different approach by using ngrams (sequences of words or lemmas). For that reason we need to replace all underscores by spaces.
# 
# This vocabulary is used in the next section for building a Document Term Matrix.

# In[ ]:


with open('output/lit_lex_vocab.txt', 'r', encoding = 'utf8') as l:
    lit_lex_vocab = l.read().splitlines()
lit_lex_vocab = [v.replace('_', ' ') for v in lit_lex_vocab]
lit_lex_vocab[:25]


# ## 3.3.1 Document Term Matrix: *ngrams*
# 
# The lexical corpus is transformed into a Document Term Matrix (or DTM), in the same way we did in [3.2](./3_2_Lit_Lex.ipynb) for the literary corpus - but with some important differences. 
# 
# First, the parameter `ngram_range` is set to (1, 5). With this parameter, `Countvectorizer()` will create a column for each word (ngram n=1), but also for each sequence of two words (bigram; n=2), or three words (trigram; n=3), etc. 
# 
# Potentially, this results in a very big (and very sparse) matrix. In order to limit its size somewhat we use the vocabulary `lit_lex_vocab` which contains all lemmas and lexical entries shared by the lexical and literary corpora. These are the relevant vocabulary items that we wish to explore.
# 
# Second, instead of creating a DTM for lexical *documents* we will use `CountVectorizer()` on the lexical corpus in *line* format, rather than in document format. This is important, because we do not want the ngrams to jump over line boundaries. The resulting DTM, therefore, is more properly called a Line Term Matrix, providing frequencies of terms (and ngrams) for each line in the lexical corpus. In the next step we group the data by text ID and aggregate the line-based frequencies to create a proper DTM. The `aggregate()` function, in this case, is `sum`: for every word or ngram we need the summation of the frequencies of all the lines of each lexical composition.
# 
# `Countvectorizer()` is used here on the raw data in `lex_lines`, including unlemmatized words. By including the unlemmatized words, we prevent creating articifial ngrams that consist of one term before and one term after an illegible word. Thus, the lemma sequence **dumu\[child\]n x\[na\]na lugal\[king\]n** will *not* match the bigram **dumu\[child\]n lugal\[king\]n**. Since `lit_lex_vocab` has no entries that contain **\[na\]na**, meaningless ngrams such as **dumu\[child\]n x\[na\]na** are filtered out automatically.

# In[ ]:


cv = CountVectorizer(preprocessor = lambda x: x, tokenizer = lambda x: x.split(), vocabulary = lit_lex_vocab, ngram_range=(1, 5))
dtm = cv.fit_transform(lex_lines['lemma'])
lex_lines_dtm = pd.DataFrame(dtm.toarray(), columns= cv.get_feature_names(), index=lex_lines["id_text"])
lex_comp_dtm = lex_lines_dtm.groupby('id_text').agg(sum).reset_index()


# ## 3.3.2 Compute Number of Matches
# The field `n_matches` represents the number of unique words or ngrams that a lexical document shares with the literary corpus. For the code see [3.2](./3_2_Lit_Lex.ipynb) section 3.2.2.

# In[ ]:


lex_comp_dtm["n_matches"] = lex_comp_dtm[lit_lex_vocab].astype(bool).sum(axis = 1)
lex_comp_dtm


# ## 3.3.3 Document Length
# The number of matches is meaningless without a measure of document length. Length is defined here as the number of lemmatized words in a document. We cannot use the DTM for measuring length, because it includes ngrams and excludes words not found in the literary corpus. We therefore must go back to the raw data set in `lex_lines`, group lines to documents and omit non-lemmatized words from the count.

# In[ ]:


lex_comp = lex_lines.groupby(
    [lex_lines["id_text"]]).aggregate(
    {"lemma": ' '.join}).reset_index()


# In[ ]:


def lex_length(lemmas):
    lemmas = lemmas.split()
    lemmas = [lemma for lemma in lemmas if not '[na]na' in lemma] # remove unlemmatized words
    length = len(lemmas)
    return length


# In[ ]:


lex_comp['length'] = lex_comp['lemma'].map(lex_length)


# ## 3.3.3 Remove Duplicates and Empty Documents
# Since the lexical data are drawn from multiple (sub)projects, it is possible that there are duplicate documents. Duplicates have the same P, Q, or X number. We select the version with the largest number of (lemmatized) words and drop others.
# 
# First we add the field `length` from the DataFrame `lex_comp` to the DataFrame `lex_comp_dtm` by merging on the field `id_text`. The merge method is `inner` (only merging those rows that are available in both DataFrames) so that documents that were omitted from `lex_comp` (because of length zero) do not show up again. Second, the field `id_text`, which has the format `dcclt/Q000041` or `dcclt/signlists/P447992`, is reduced to only the last 7 positions (P, Q, or X, followed by six digits). The merged DataFrame is ordered by length (from large to small) and, if duplicate `text_id`s are found, only the first one is kept with the Pandas method `drop_duplicates()`.
# 
# Our data set has data from all Old Babylonian lexical documents currently in [DCCLT](http://oracc.org/dcclt). Not all of these documents are lemmatized. In particular, exemplars that have been linked to a composite text are usually not lemmatized. Such documents have no lemmatized contents and therefore have length 0. These documents are removed.

# In[ ]:


lex_comp_dtm = pd.merge(lex_comp_dtm, lex_comp[['id_text', 'length']], on = 'id_text', how = 'inner')
lex_comp_dtm['id_text'] = lex_comp_dtm['id_text'].str[-7:]
lex_comp_dtm = lex_comp_dtm.sort_values(by = 'length', ascending=False)
lex_comp_dtm = lex_comp_dtm.drop_duplicates(subset = 'id_text', keep = 'first')
lex_comp_dtm = lex_comp_dtm.loc[lex_comp_dtm['length'] > 0] # remove compositions that have no lemmatized content


# ## 3.3.4 Adding Metadata and Normalizing
# The metadata of the lexical texts (such as composition name, etc.) is found in the JSON files for each of the (sub)projects downloaded in section [3.1](./3_1_Lit_Lex_Vocab.ipynb). The code is essentially the same as in [3.2](./3_2_Lit_Lex.ipynb), but since there are multiple (sub)projects involved, it is done in a loop.

# In[ ]:


cat = {}
for proj in ['dcclt', 'dcclt/signlists', 'dcclt/nineveh', 'dcclt/ebla']:
    f = proj.replace('/', '-')
    file = f"jsonzip/{f}.zip" # The ZIP file was downloaded in notebook 3_1
    z = zipfile.ZipFile(file) 
    st = z.read(f"{proj}/catalogue.json").decode("utf-8")
    j = (json.loads(st))
    cat.update(j["members"])
cat_df = pd.DataFrame(cat).T
cat_df["id_text"] = cat_df["id_text"].fillna(cat_df["id_composite"])
cat_df = cat_df.fillna('')
cat_df = cat_df[["id_text", "designation", "subgenre"]]


# ### 3.3.4.1 Merge Metadata
# Now merge `cat_df` with the DataFrame `lex_comp_dtm` on the field `id_text`. Of the DTM we only keep the fields `n_matches` and `length`. The resulting DataFrame contains descriptive information about lexical documents, plus the field `n_matches`, which is relevant only for the current exploration. The DataFrame is saved, minus the  field `n_matches` for use in section 3.4. 
# 
# The DataFrame is shown in descending order of the number of matches.

# In[ ]:


lex = pd.merge(cat_df, lex_comp_dtm[['id_text', 'n_matches', 'length']], on = 'id_text', how = 'inner')
lex.drop('n_matches', axis = 1).to_pickle('output/lexdtm.p')
lex.sort_values(by='n_matches', ascending = False)


# ### 3.3.4.2 Normalizing
# Long lexical documents have more matches than short one. Normalize by dividing the number of matches (`n_matches`) by text length. For very short documents this measure has little value; only longer documents are displayed. Since the number of matches is based on *ngrams*, it is possible that `n_matches` is larger than `length` and that `norm` is higher than 1. This only happens in very short documents.

# In[ ]:


lex['norm'] = lex['n_matches'] / lex['length']
lex = lex.sort_values(by = 'norm', ascending = False)
lex.loc[lex.length > 250]


# ## 3.3.5 Explore the Results
# Explore the results in an interactive table. The slides, the check box, and the pull-down menus allow larger or smaller number of results, higher or lower threshold for text length, including only composites, only exemplars, or all, etc. The text ID numbers in the first column link to their editions in [DCCLT](http://oracc.org/dcclt).

# In[ ]:


lex.to_pickle('output/lex.p')
anchor = '<a href="http://oracc.org/dcclt/{}", target="_blank">{}</a>'
lex2 = lex.copy()
lex2['id_text'] = [anchor.format(val,val) for val in lex['id_text']]
lex2['PQ'] = ['Composite' if i[0] == 'Q' else 'Exemplar' for i in lex['id_text']]


# In[ ]:


@interact(sort_by = lex2.columns, rows = (1, len(lex2), 1), min_length = (0,500,5), show = ["Exemplars", "Composites", "All"])
def sort_df(sort_by = "norm", ascending = False, rows = 25, min_length = 250, show = 'All'):
    if not show == 'All':
        l = lex2.loc[lex2['PQ'] == show[:-1]]
    else:
        l = lex2
    l = l.drop('PQ', axis = 1)
    l = l.loc[l.length >= min_length].sort_values(by = sort_by, ascending = ascending).reset_index(drop=True)[:rows].style
    return l


# ## 3.3.6 Discussion
# When ordered by `norm` the top of the list is formed by lexical compositions such as the sign lists [OB Nippur Ea](http://oracc.org/dcclt/Q000055) and [OB Nippur Diri](http://oracc.org/dcclt/Q000057), the acrographic list/list of professions [OB Nippur Lu](http://oracc.org/dcclt/Q000047), and the acrographic lists [OB Nippur Izi](http://oracc.org/dcclt/Q000050), and [OB Nippur Kagal](http://oracc.org/dcclt/Q000048), or (large) exemplars of such compositions. If we restrict the DataFrame to composites (Q numbers) only, this comes out even clearer. All these lexical texts belong to what Jay Crisostomo has labeled "ALE": Advanced Lexical Exercises ([Translation as Scholarship](https://doi.org/10.1515/9781501509810); SANER 22, 2019). These exercises belong to the advanced first stage of education, just before students would start copying literary texts. The thematic lists collected in [Ura](http://oracc.org/dcclt/Q000039,Q000040,Q000001,Q000041,Q000042,Q000043) (lists of trees, wooden objects, reeds, reed objects, clay, pottery, hides, metals and metal objects, animals, meat cuts, fish, birds, plants, etc.) have much lower `norm` values and thus less overlap with literary vocabulary. The lists that belong to [Ura](http://oracc.org/dcclt/Q000039,Q000040,Q000001,Q000041,Q000042,Q000043) are studied in a more elementary phase of scribal education and are further removed from the literary corpus, both in vocabulary and in curricular terms.

# In[ ]:




