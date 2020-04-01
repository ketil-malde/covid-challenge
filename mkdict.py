import config as C
import json
import sys

# Return a dictionary from one input file
def loadfile(f):
    with open(f) as jf:
        x = json.load(jf)
    return(x)

# count words in a string (optionally add to existing dict)import string

def tr(line): return line.translate(str.maketrans('', '', '(), '))
def add_par_dict(s, freq):
    for w in s.split():
        w1 = tr(w)                   # filter bad chars
        freq[w1] = freq.get(w1,0)+1  # increment by one
        
def add_section_dict(x, section, freq):
    for p in x[section]:
        add_par_dict(p['text'], freq)

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
            add_section_dict(x, 'abstract', af)
            add_section_dict(x, 'body_text', bf)
        print()
    return af, bf
        
# testing
test1 = loadfile(C.DATA+'biorxiv_medrxiv/biorxiv_medrxiv/00d16927588fb04d4be0e6b269fc02f0d3c2aa7b.json')
test2 = loadfile(C.DATA+'biorxiv_medrxiv/biorxiv_medrxiv/0015023cc06b5362d332b3baf348d11567ca2fbb.json')

def test():
    a = {}
    add_section_dict(test1, section='abstract', freq=a)
    add_section_dict(test2, section='abstract', freq=a)
    b = {}
    add_section_dict(test2, section='abstract', freq=b)
    add_section_dict(test1, section='abstract', freq=b)
    assert(a==b)

def swap(tup):
    (k,v) = tup
    return (v,k)

def sorted_list(d):
    return sorted(list(d.items()), key = swap)
    
def process_and_save():
    a, b = process_all()
    with open("abstracts_dict.json","w") as f:
        f.write(json.dumps(a))
    with open("body_dict.json","w") as f:
        f.write(json.dumps(b))
