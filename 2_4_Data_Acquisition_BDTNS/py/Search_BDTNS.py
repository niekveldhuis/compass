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

def search(s, maxhits, links): 
    s = s.lower().replace('sz', 'š').translate(char).strip()
    s = re.sub(ind, lambda m: m.group().translate(index), s)
    s_l = s.split()
    s_l = [d2.get(s,s) for s in s_l]
    signnames_l = []
    for sign in s_l: 
        if '×' in sign:
            sign_l = sign.replace('|', '').split('×')
            sign_l = [d2.get(sign, sign) for sign in sign_l]
            sign = f"|{'×'.join(sign_l)}|"
            signnames_l.append(sign)
        elif '.' in sign or '+' in sign: 
            for s in separators2:
                sign = sign.replace(s, ' ').strip() 
            sign_l = sign.split()
            signnames_l.extend(sign_l)
        else: 
            signnames_l.append(sign)
    signs = ' '.join(signnames_l).upper()
    signs_esc = re.escape(f' {signs} ')
    signs_esc = signs_esc.replace('\ X\ ', '(?:\ [^ ]+)*\ ')
    show = ['id_text', 'label', 'text', 'date', 'provenance', 'publication']
    results = bdtns.loc[bdtns['sign_names'].str.contains(signs_esc, regex=True), show].copy()
    hits = len(results)
    if maxhits > hits:
        maxhits = hits
    print(signs), print(f"{str(hits)} hits; {str(maxhits)} displayed.")
    results = results.sort_values(by = sortby.value)[:maxhits]
    if links:
        results['id_text'] = [anchor.format(val,val) for val in results['id_text']]
        results = results.style.hide_index().set_properties(subset=['publication'], **{'width': '100px'})
    return results


button = widgets.Button(description='Search')
text = widgets.Text(
        value='',
        description='')
out = widgets.Output()
maxhits = widgets.BoundedIntText(
    value=25,
    min=25,
    max=len(bdtns),
    step=1,
    description='Max hits:')
links = widgets.Checkbox(
    value=True,
    indent = False,
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
col1 = widgets.VBox([text, links, button])
col2 = widgets.VBox([maxhits, sortby])
box = widgets.HBox([col1, col2])
disp = widgets.VBox([box,out])






