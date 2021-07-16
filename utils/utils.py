""" Utilities for Computational Assyriology """
import requests
from tqdm.auto import tqdm
import os
import zipfile
import json
import pandas as pd

def format_project_list(projects):
    project_list = projects.lower().strip().split(',')
    project_list = [project.strip() for project in project_list]
    return(project_list)

def oracc_download(project_list, server = 'penn'):
    """Downloads ZIP with JSON files from
    ORACC servers. First parameter is a list
    with ORACC project names,
    return is the same list of names,
    minus doublets and non-existing
    projects. Second parameter is 'lmu' 
    (first try LMU server) or 'penn' 
    (default: first try Penn server)."""
    
    CHUNK = 1024
    project_list = list(set(project_list)) #remove duplicates
    projects = project_list.copy()
    # the list projects will be changed by the for loop,
    # removing non-existing project names (and then returned).
    # Therefore, it has to be different from project_list, 
    # which is iterated over in the loop.
    for project in project_list:
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

def parsejson(text, meta_d):
    l = []
    capture_field = False
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            l.extend(parsejson(JSONobject, meta_d))
        
        meta_d["label"] = JSONobject.get('label')
       # if "type" in JSONobject and JSONobject["type"] == "field-start": # this is for sign lists, identifying fields such as
       #     meta_d["field"] = JSONobject["subtype"]                    # sign, pronunciation, translation.
        if JSONobject.get("type") == "cell-start":
            capture_field = True
        if JSONobject.get("type") == "cell-end":
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
            lemma["ftype"] = JSONobject.get("ftype")   # capturing words that belong to yearnames
            if capture_field:
                lemma["field"] = meta_d.get("field", "")
            l.append(lemma)
        if JSONobject.get("strict") == "1":
            lemma = {}
            lemma['extent'] = JSONobject['extent']
            lemma['scope'] = JSONobject['scope']
            lemma['state'] = JSONobject['state']
            lemma["id_word"] = JSONobject["ref"]
            lemma["id_text"] = meta_d["id_text"]
            l.append(lemma)
    return l

def get_lemmas(project_list):
    lemm_l = []
    meta_d = {"label": None, "id_text": None}
    for project in project_list:
        file = f"jsonzip/{project.replace('/', '-')}.zip"
        try:
            z = zipfile.ZipFile(file) 
        except:
            e = sys.exc_info() # get error information
            print(file), print(e[0]), print(e[1]) # and print it
            #print(f"{file} does not exist or is not a proper ZIP file")
            continue
        files = z.namelist()
        files = [name for name in files if "corpusjson" in name and name[-5:] == '.json'] 
        for filename in tqdm(files, desc = project):
            id_text = project + filename[-13:-5] 
            meta_d["id_text"] = id_text
            try:
                st = z.read(filename).decode('utf-8')
                data_json = json.loads(st)           
                lemm_l.extend(parsejson(data_json, meta_d))
            except:
                e = sys.exc_info() # get error information
                print(filename), print(e[0]), print(e[1]) # and print it
                #print(f'{id_text} is not available or not complete')
        z.close()
    return(lemm_l)


def dataformat(lemm_list):
    words_df = pd.DataFrame(lemm_list).fillna('')
    findreplace = {' ' : '-', ',' : ''}
    words_df = words_df.replace({'gw' : findreplace, 'sense' : findreplace}, regex=True)
    words_df['id_line'] = [int(wordid.split('.')[1]) for wordid in words_df['id_word']] 
    return(words_df)

def get_data(projects):
    os.makedirs("jsonzip", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    project_list = format_project_list(projects)
    print("Downloading JSON")
    project_list = oracc_download(project_list)
    print("Parsing JSON")
    lemm_list = get_lemmas(project_list)
    words_df = dataformat(lemm_list)
    return(words_df)
    
