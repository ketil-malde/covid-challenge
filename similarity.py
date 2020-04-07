# identify similar articles from word presence absence

import word_importance as W
import mkdict as M
import config as C

# Calculate distance between two documents using specific sections
# (See test function for how to use it)
def dist_txt(ss, x, y, xsec, ysec):
    xd = M.get_section_dict(x,xsec)
    yd = M.get_section_dict(y,ysec)
    return dist_dict(ss, xd, yd)

# helper function, calculate distance between dictionaries
def dist_dict(ss, xd, yd):
    score = 0
    maxscore = 0
    minscore = 0
    for (k,v) in xd.items():  # all words in first text
        pos_score, neg_score, _counts = ss.get(k,(0,0,None))
        if k in yd:
            score = score + pos_score
        else:
            score = score - neg_score
        maxscore = maxscore + pos_score
        minscore = minscore - neg_score
    if maxscore==minscore: return 0
    else: return (score-minscore)/(maxscore-minscore)

# print a list of articles best matching the abstract
import os
def process_all():
    ss = M.loadfile('scores.json')
    abstracts = {}
    bodies    = {}
    titles = {}
    for d in C.DIRS:
        print(d, end=': ', flush=True)
        for f in os.listdir(C.DATA+d+'/'+d):
            x = M.loadfile(C.DATA+d+'/'+d+'/'+f)
            abstracts[f] = M.get_section_dict(x, 'abstract')
            bodies[f] = M.get_section_dict(x, 'body_text')
            titles[f] = x['metadata']['title']
        print('')
    # print titles of closest matching articles
    for f1, a1 in abstracts.items():
        print(titles[f1],':')
        sim = []
        for f2, b2 in bodies.items():
            score = (dist_dict(ss, a1, b2), titles[f2])
            sim.append(score)
        for s,t in sorted(sim, reverse=True)[0:4]:
            print('- %.2f %s' %(s,t))
    return None

def test():
    t1 = M.test1
    t2 = M.test2
    ss = M.loadfile('scores.json')

    print('t1.abs vs t1.abs', dist_txt(ss, t1, t1, 'abstract', 'abstract'))
    print('t1.abs vs t2.abs', dist_txt(ss, t1, t2, 'abstract', 'abstract'))
    print('t2.abs vs t1.abs', dist_txt(ss, t2, t1, 'abstract', 'abstract'))
    print('t2.abs vs t2.abs', dist_txt(ss, t2, t2, 'abstract', 'abstract'))

    print('t1.abs vs t1.body_text', dist_txt(ss, t1, t1, 'abstract', 'body_text'))
    print('t1.abs vs t2.body_text', dist_txt(ss, t1, t2, 'abstract', 'body_text'))
    print('t2.abs vs t1.body_text', dist_txt(ss, t2, t1, 'abstract', 'body_text'))
    print('t2.abs vs t2.body_text', dist_txt(ss, t2, t2, 'abstract', 'body_text'))

process_all()
