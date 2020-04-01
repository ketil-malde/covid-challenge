# Calculate which words are valuable from dictionaries

import config as C
import mkdict as M

# calculate word score as log count_match - log count_abs - log count_body

# increment word in fd by one
def incr(fd,w):
    fd[w] = fd.get(w,0)+1

import os
from math import log

def process_all():
    count_match = {}
    count_abs = {}
    count_body = {}

    # abs_words = M.loadfile('abstracts_dict.json')

    art_ct = 0
    for d in C.DIRS:
        print(d, end=': ', flush=True)
        for f in os.listdir(C.DATA+d+'/'+d):
            print('.', end='', flush=True)
            art_ct = art_ct + 1
            x = M.loadfile(C.DATA+d+'/'+d+'/'+f)
            af = {}
            M.add_section_dict(x, 'abstract', af)
            bf = {}
            M.add_section_dict(x, 'body_text', bf)
            for w in af.keys():
                incr(count_abs, w)  # 13 sec
                if w in bf.keys():
                    incr(count_match, w) # +22 sec
            for w in bf.keys():  #  & abs_words.keys(): # intersection is slower +32 sec
                incr(count_body, w) # +22 sec
        print('')

    scores = {}
    counts = {}
    for w in count_match.keys():
        cm, ca, cb = count_match.get(w,0), count_abs.get(w,0), count_body.get(w,0)
        # likelihood of word in body/abstract vs likelihood of a random match
        scores[w] = log(art_ct) + log(cm) - log(ca) - log(cb)  # match_keys => all >= 1
        counts[w] = (cm, ca, cb)
    return scores, counts

# testing
# f = C.DATA+'/biorxiv_medrxiv/biorxiv_medrxiv/f734d47a423cbe54ec0cc9b2dee39470cf74fd9b.json'

import json
def process_and_save():
    ss, cs = process_all()
    with open('scores.json','w') as f:
        f.write(json.dumps(ss))
    with open('counts.json','w') as f:
        f.write(json.dumps(cs))
            


        
