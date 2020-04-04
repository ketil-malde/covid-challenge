# identify similar articles from word presence absence

import word_importance as W
import mkdict as M
import config as C

def dist_txt(ss, x, y, xsec, ysec):
    xd = M.get_section_dict(x,xsec)
    yd = M.get_section_dict(y,ysec)
    return dist_dict(ss, xd, yd)

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
    return (score-minscore)/(maxscore-minscore)

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
