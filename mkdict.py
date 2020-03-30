import config as C
import json
import sys

# Return a dictionary from one input file
def loadfile(f):
    with open(f) as jf:
        x = json.load(jf)
    return(x)

# count words in a string (optionally add to existing dict)import string

def tr(line): return line.translate(str.maketrans('', '', '(),'))
def mkdict(s, freq = {}):
    f = freq
    for w in s.split():
        f[tr(w)] = f.get(w,0)+1  # increment by one, filter bad chars
    return f
        
def get_dict(x, section='abstract', freq = {}):
    f = freq
    for p in x[section]:
        f = mkdict(p['text'], f)
    return f

# prettyprint dict
def print_dict(d):
    for v, k in sorted(((v,k) for k,v in d.items()), reverse=True):
        print("%s: %d" % (k,v))

import os        
def process_all():
    af = {} # abstracts
    bf = {} # body texts
    for d in C.DIRS:
        print(d, end=': ', flush=True)
        for f in os.listdir(C.DATA+d+'/'+d):
            print('.', end='', flush=True)
            x = loadfile(C.DATA+d+'/'+d+'/'+f)
            af = get_dict(x, 'abstract', af)
            bf = get_dict(x, 'body_text', bf)
        print()
    return af, bf
        
# testing
# x = loadfile(C.DATA+'biorxiv_medrxiv/biorxiv_medrxiv/00d16927588fb04d4be0e6b269fc02f0d3c2aa7b.json')

def process_and_save():
    a, b = process_all()
    with open("abstracts_dict.json","w") as f:
        f.write(json.dumps(a))
    with open("body_dict.json","w") as f:
        f.write(json.dumps(b))
