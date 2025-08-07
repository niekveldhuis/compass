#!/usr/bin/env python
# coding: utf-8

import pandas as pd
pd.set_option('display.max_rows', None)
import re
import pickle
import ipywidgets as widgets
from IPython.display import display, clear_output

# Load data
with open('output/osl_dict.p', 'rb') as p:
    d2 = pickle.load(p)
bdtns = pd.read_pickle('output/bdtns_tokenized.p')

# Character translation setup
digi = '0123456789x'
inde = '₀₁₂₃₄₅₆₇₈₉ₓ'
char1 = '{}-cjĝ*'
char2 = '   šŋŋ×'
index = str.maketrans(digi, inde)
char = str.maketrans(char1, char2)
ind = re.compile(r'[a-zŋḫṣšṭA-ZŊḪṢŠṬ][0-9x]{1,2}') 
anchor = '<a href="http://bdtns.cesga.es/{}", target="_blank">{}</a>'
separators2 = ['.', '+', '|']

# Search function
def search(s, Maxh=25, Links=True, Sortby='id_text'): 
    s = s.lower().replace('sz', 'š').translate(char).strip()
    s = re.sub(ind, lambda m: m.group().translate(index), s)
    s_l = s.split()
    s_l = [d2.get(s, s) for s in s_l]
    
    signnames_l = []
    for sign in s_l: 
        if '×' in sign:
            sign_l = sign.replace('|', '').split('×')
            sign_l = [d2.get(s, s) for s in sign_l]
            sign_l = [f'({s[1:-1]})' if len(s) > 1 and s[0] == '|' else s for s in sign_l]
            sign = f"|{'×'.join(sign_l)}|"
        elif '.' in sign or '+' in sign: 
            for sep in separators2:
                sign = sign.replace(sep, ' ').strip() 
            sign_l = sign.split()
            sign_l = [d2.get(s, s) for s in sign_l]
            signnames_l.extend(sign_l)
            continue
        sign = d2.get(sign, sign) 
        signnames_l.append(sign)
    
    signnames = f" {' '.join(signnames_l).upper()} "
    signnames_wildcard = signnames.replace(' X ', r'(?: [^ ]+)* ')
    signs_esc = re.escape(signnames_wildcard).replace(
        re.escape(r'(?: [^ ]+)* '), r'(?: [^ ]+)* ')

    show = ['id_text', 'label', 'text', 'date', 'provenance', 'publication']
    results = bdtns.loc[bdtns['sign_names'].str.contains(signs_esc, regex=True), show].copy()
    
    hits = len(results)
    Maxh = min(Maxh, hits)
    print(signnames)
    print(f"{hits} hit{'s' if hits != 1 else ''}; {Maxh} displayed.")
    
    results = results.sort_values(by=Sortby)[:Maxh]
    
    if Links:
        results['id_text'] = [anchor.format(val, val) for val in results['id_text']]
        results = results.style.hide(axis="index").set_properties(subset=['publication'], **{'width': '200px'})
    
    return results

# Widgets
text = widgets.Text(value='', description='Query:')
text.continuous_update = False

maxhits = widgets.BoundedIntText(
    value=25, min=0, max=len(bdtns), step=1, description='Max hits:')

links = widgets.Checkbox(value=True, description='Display Links')

sortby = widgets.Dropdown(
    options=['id_text', 'text', 'date', 'provenance', 'publication'],
    value='id_text', description='Sort By:')

button = widgets.Button(description='Search')
out = widgets.Output()

# Event handlers
def submit_search(change=None):
    with out:
        clear_output()
        display(search(text.value, maxhits.value, links.value, sortby.value))

def update_maxhits(change):
    links.value = maxhits.value < 250
    submit_search()

# Attach handlers
button.on_click(submit_search)
text.observe(submit_search, names='value')
sortby.observe(submit_search, names='value')
maxhits.observe(update_maxhits, names='value')

# Display layout
#col1 = widgets.VBox([text, links, button])
#col2 = widgets.VBox([maxhits, sortby])
#box = widgets.HBox([col1, col2])
#display(widgets.VBox([box, out]))

def main():
    col1 = widgets.VBox([text, links, button])
    col2 = widgets.VBox([maxhits, sortby])
    box = widgets.HBox([col1, col2])
    display(widgets.VBox([box, out]))

if __name__ == "__main__":
    main()
