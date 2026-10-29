"""Choose the right denominator, then verify the publication."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0):layers.append((im,start,None))
    im,d=layer()
    def row(y,label,value,fill=WHITE):
        box(d,64,y,1152,110,fill=fill);text(d,label,86,y+10,23,bold=True,color=RUST);text(d,value,86,y+49,36,bold=True)
    if k=='measure-question':
        header(d,7,'All parcels due. Which denominator?','13:00 · four parcels due by noon · invented teaching example')
        parcels(d,y=245)
        text(d,'Completed-delivery candidate: 2 / 3 = 66.7%',64,505,43,bold=True)
        text(d,'Does it answer the meeting’s question?',64,600,37,bold=True);add(im)
    elif k=='measure-answer':
        header(d,7,'The question includes the unfinished parcel','Choose by meaning; refreshing does not change the rule.')
        parcels(d,y=245,selected=[0,1,2,3])
        bracket(d,4,'All four parcels due belong in the denominator.',y=462);add(im)
        im,d=layer();text(d,'2 / 4 = 50.0%',64,566,62,bold=True,color=GREEN)
        text(d,'Completed: 2 / 3 = 66.7%',640,594,34,color=MUTED)
        add(im,cue(t,'Two out of four'))
    elif k=='checks-question':
        header(d,7,'Checks pass. Is the publication ready?','Illustrative quality review · decision-input-1300 · 19 October')
        row(234,'IDENTIFIERS','4 rows · 4 distinct identifiers')
        row(370,'TIMES','4 promises present · 1 empty completion allowed')
        text(d,'What evidence is still needed for the meeting?',64,581,36,bold=True);add(im)
    elif k=='checks-answer':
        header(d,7,'Checks support a limited conclusion','Preserve the checked input, rule version and check time.')
        row(234,'SUPPORTED FOR THIS INPUT','Uniqueness + required-value completeness',SAGE)
        row(370,'NOT ESTABLISHED BY THESE CHECKS','Right denominator · published output · report read')
        text(d,'A contract states a commitment; evidence tests it.',64,581,35,bold=True);add(im)
    elif k=='decision':
        header(d,7,'The decision remains pending','Delivery Operations confirms all-due and original promise.')
        for i,(a,b) in enumerate([('RULE','All-due'),('VERIFY','50.0%'),('ATTACH','Output ID'),('TRACE','Refresh')]):
            x=64+i*300;box(d,x,270,252,172,fill=SAGE if i==0 else WHITE)
            text(d,a,x+18,294,23,bold=True,color=RUST)
            text(d,b,x+18,360,32,bold=True)
            if i<3:arrow(d,x+261,357,x+287,357)
        text(d,'Reporting engineer: verify and attach the evidence.',64,517,34,bold=True)
        text(d,'Current gap: no verified all-due publication attached.',64,601,31,color=RUST);add(im)
    elif k=='practice':
        header(d,7,'Find the evidence gap and next owner','Map: Quality check → Example record → Decision')
        row(235,'QUALITY CHECK','Expected: 0 duplicates · observed: 4 distinct IDs')
        row(379,'DECISION','Chosen rule → missing evidence → action + owner')
        text(d,'Explain readiness, then check your answer.',64,586,36,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,7);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
