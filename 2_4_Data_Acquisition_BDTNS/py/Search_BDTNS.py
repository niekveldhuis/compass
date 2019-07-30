#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re
import pickle
from ipywidgets import interact, interact_manual
import ipywidgets as widgets
from IPython.display import display, clear_output

with open('output/ogsl_dict.p', 'rb') as p:
    d2 = pickle.load(p)
bdtns = pd.read_pickle('output/bdtns_tokenized.p')
digi = '0123456789x'
inde = '₀₁₂₃₄₅₆₇₈₉ₓ'
char1 = '{}-cjĝ*'
char2 = '   šŋŋ×'
index = str.maketrans(digi, inde)
char = str.maketrans(char1, char2)
ind = re.compile(r'[a-zŋḫṣšṭA-ZŊḪṢŠṬ][0-9x]{1,2}') 
anchor = '<a href="http://bdtns.filol.csic.es/{}", target="_blank">{}</a>'
separators2 = ['.', '+', '|']  # used in compound signs

def search(search, maxhits, links): 
    search = search.lower().replace('sz', 'š').translate(char).strip()
    search = re.sub(ind, lambda m: m.group().translate(index), search)
    search_l = search.split()
    search_l = [d2.get(s,s) for s in search_l]
    row_l = []
    for sign in search_l: 
        if '.' in sign or '+' in sign: 
            for s in separators2:
                sign = sign.replace(s, ' ').strip() 
                sign_l = sign.split()
            row_l.extend(sign_l)
        elif '×' in sign:
            sign_l = sign.replace('|', '').split('×')
            sign_l = [d2.get(sign, sign) for sign in sign_l]
            sign = '|' + '×'.join(sign_l) + '|'
            row_l.append(sign)
        else: 
            row_l.append(sign)
    signs = ' '.join(row_l).upper()
    signs_esc = re.escape(' ' + signs + ' ')
    signs_esc = signs_esc.replace('\ X\ ', '(?:\ [^ ]+)*\ ')
    show = ['id_text', 'label', 'text', 'date', 'provenance', 'publication']
    results = bdtns.loc[bdtns['sign_names'].str.contains(signs_esc, regex=True), show].copy()
    hits = len(results)
    if maxhits > hits:
        maxhits = hits
    print(signs), print(str(hits) + ' hits; ' + str(maxhits) + " displayed")
    results = results.sort_values(by = sortby.value)[:maxhits]
    if links:
        results['id_text'] = [anchor.format(val,val) for val in results['id_text']]
        results = results.style.hide_index()
    return results


button = widgets.Button(description='Search')
text = widgets.Text(
        value='',
        description='')
out = widgets.Output()
maxhits = widgets.IntSlider(
    value=25,
    min=25,
    max=len(bdtns),
    step=100,
    description='Max hits:')
links = widgets.Checkbox(
    value=True,
    description='Display Links',
        )
sortby = widgets.Dropdown(
    options = ['id_text', 'text', 'label', 'date', 'provenance', 'publication'],
    value = 'id_text',
    description = 'Sort By: ')
def on_button_clicked(_):
    with out:
        clear_output()
        display(search(text.value, maxhits.value, links.value))
button.on_click(on_button_clicked)
line = widgets.HBox([text, maxhits])
line2 = widgets.HBox([links, sortby])
disp = widgets.VBox([line,line2,button,out])







