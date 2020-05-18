""" Utilities for Computational Assyriology """
import requests
from tqdm.auto import tqdm
import os
import errno
import zipfile
import json
import pandas as pd

lemm_l = []
meta_d = {"label": None, "id_text": None}
dollar_keys = ["extent", "scope", "state"]

def make_dirs(x):
    """Check for existence of directories
    create those if they do not exist
    otherwise do nothing. Parameter is a list
    with directory names"""
    for dir in x:
        try:
            os.mkdir(dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass

def format_project_list(x):
    p = x.lower().strip().split(',')
    p = [x.strip() for x in p]
    return(p)

def oracc_download(p, server = 'penn'):
    """Downloads ZIP with JSON files from
    ORACC servers. First parameter is a list
    with ORACC project names,
    return is the same list of names,
    minus doublets and non-existing
    projects. Second parameter is 'lmu' 
    (first try LMU server) or 'penn' 
    (default: first try Penn server)."""
    
    CHUNK = 1024
    p = list(set(p)) #remove duplicates
    projects = p.copy()
    for project in p:
        proj = project.replace('/', '-')
        build = f"http://build-oracc.museum.upenn.edu/json/{proj}.zip"
        oracc = f"http://oracc.org/{project}/json/{proj}.zip"
        lmu = f"http://oracc.ub.uni-muenchen.de/{project}/json/{proj}.zip"
        file = f"jsonzip/{proj}.zip"
        servers = [build, oracc, lmu]
        if server == 'lmu':
            servers = [lmu, build, oracc]
        for url in servers:
            with requests.get(url, stream=True) as r:
                if r.status_code == 200:
                    print(r.status_code)
                    tqdm.write(f"Saving {url} as {file}.")
                    total_size = int(r.headers.get('content-length', 0))
                    t=tqdm(total=total_size, unit='B', unit_scale=True, desc = project)
                    with open(file, 'wb') as f:
                        for c in r.iter_content(chunk_size=CHUNK):
                            t.update(len(c))
                            f.write(c)
                    break
                else:
                    if url == servers[-1]: #last server in the list was tried
                        tqdm.write(f"WARNING {url} does not exist.")
                        projects.remove(project)
    return projects

def parsejson(text):
    capture_field = False
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            parsejson(JSONobject)
        if "label" in JSONobject:
            meta_d["label"] = JSONobject['label']
       # if "type" in JSONobject and JSONobject["type"] == "field-start": # this is for sign lists, identifying fields such as
       #     meta_d["field"] = JSONobject["subtype"]                    # sign, pronunciation, translation.
        if "type" in JSONobject and JSONobject["type"] == "cell-start":
            capture_field = True
        if "type" in JSONobject and JSONobject["type"] == "cell-end":
            capture_field = False
        if capture_field:
            if "subtype" in JSONobject:
                meta_d["field"] = JSONobject["subtype"]                    # sign, pronunciation, translation.
                
        #if "type" in JSONobject and JSONobject["type"] == "field-end":
        #    meta_d.pop("field", None)                           # remove the key "field" to prevent it from being copied 
                                                              # to all subsequent lemmas (which may not have fields)
        if "f" in JSONobject:
            lemma = JSONobject["f"]
            lemma["id_word"] = JSONobject["ref"]
            lemma['label'] = meta_d["label"]
            lemma["id_text"] = meta_d["id_text"]
            if capture_field:
                lemma["field"] = meta_d["field"]
            lemm_l.append(lemma)
        if "strict" in JSONobject and JSONobject["strict"] == "1":
            lemma = {key: JSONobject[key] for key in dollar_keys}
            lemma["id_word"] = JSONobject["ref"]
            lemma["id_text"] = meta_d["id_text"]
            lemm_l.append(lemma)
    return

def get_lemmas(p):
    for project in p:
        file = f"jsonzip/{project.replace('/', '-')}.zip"
        try:
            z = zipfile.ZipFile(file) 
        except:
            print(f"{file} does not exist or is not a proper ZIP file")
            continue
        files = z.namelist()
        files = [name for name in files if "corpusjson" in name and name[-5:] == '.json'] 
        for filename in tqdm(files, desc = project):
            id_text = project + filename[-13:-5] 
            meta_d["id_text"] = id_text
            try:
                st = z.read(filename).decode('utf-8')
                data_json = json.loads(st)           
                parsejson(data_json)
            except:
                print(f'{id_text} is not available or not complete')
        z.close()
    return(lemm_l)


def dataformat(lemm_list):
    words_df = pd.DataFrame(lemm_list).fillna('')
    findreplace = {' ' : '-', ',' : ''}
    words_df = words_df.replace({'gw' : findreplace, 'sense' : findreplace}, regex=True)
    words_df['id_line'] = [int(wordid.split('.')[1]) for wordid in words_df['id_word']] 
    return(words_df)

def get_data(x):
    make_dirs(["jsonzip", "output"])
    p = format_project_list(x)
    print("Downloading JSON")
    p = oracc_download(p)
    print("Parsing JSON")
    lemm_list = get_lemmas(p)
    words_df = dataformat(lemm_list)
    return(words_df)
    
