"""Keep purpose, identity and actual control/release evidence explicit."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0):layers.append((im,start,None))
    im,d=layer()
    def row(y,label,value,fill=WHITE):
        box(d,64,y,1152,110,fill=fill);text(d,label,86,y+10,23,bold=True,color=RUST);text(d,value,86,y+49,35,bold=True)
    if k=='access-question':
        header(d,11,'Has access control been demonstrated?','Illustrative decision · operational deliveries')
        row(235,'RECORDED CLASSIFICATION','Restricted operational data')
        row(379,'RECORDED PURPOSE','Approved analysts investigate delivery performance')
        text(d,'What evidence would show that controls work?',64,586,35,bold=True);add(im)
    elif k=='access-answer':
        header(d,11,'A label does not enforce access','Connect the approval to implemented controls and tests.')
        for x,a,b in [(64,'DECIDE','Purpose + scope'),(470,'IMPLEMENT','Groups + grants'),(876,'TEST','Allowed + denied')]:
            box(d,x,243,340,147)
            text(d,a,x+18,264,23,bold=True,color=RUST);text(d,b,x+18,326,31,bold=True)
            if x<876:arrow(d,x+351,318,x+390,318)
        for i,label in enumerate(['Database','Search','API','Exports']):
            x=64+i*300;box(d,x,445,252,95,fill=SAGE);text(d,label,x+18,472,34,bold=True)
        text(d,'Revocation does not retrieve a downloaded copy.',64,601,34,bold=True,color=GREEN);add(im)
    elif k=='reuse-question':
        header(d,11,'Which dataset does the publication plan cover?','Compare identity, purpose and actual release status.')
        for x,a,b,z in [(64,'OPERATIONAL','deliveries','Restricted investigation'),(646,'RESEARCH PLAN','Synthetic v1.0','Identifier pending')]:
            box(d,x,244,552 if x==64 else 570,269)
            text(d,a,x+23,267,24,bold=True,color=RUST)
            text(d,b,x+23,344,42,bold=True)
            text(d,z,x+23,449,33,bold=True)
        text(d,'Research plan: proposed CC BY 4.0 · no release yet',64,585,35,bold=True);add(im)
    elif k=='reuse-answer':
        header(d,11,'Separate dataset. Separate permission.','FAIR neither requires public access nor grants permission.')
        row(235,'SYNTHETIC DATASET','Invented parcels; operational export not authorised')
        text(d,'Proposed license + pending ID ≠ completed deposit',64,389,35,bold=True);add(im)
        im,d=layer()
        for i,(letter,label) in enumerate([('F','Findable'),('A','Accessible'),('I','Interoperable'),('R','Reusable')]):
            x=64+i*300;box(d,x,490,252,130,fill=SAGE)
            text(d,letter,x+18,502,27,bold=True,color=RUST);text(d,label,x+18,559,29,bold=True)
        add(im,cue(t,'FAIR means'))
    elif k=='retention':
        header(d,11,'Explain the input without promising a rerun','Agree retention by artifact and purpose, including copies.')
        row(235,'AFTER SNAPSHOT DELETION','Metadata may identify which input was used')
        row(379,'LIMIT','That does not enable an exact rerun')
        text(d,'Deletion audit ≠ proof every unmanaged copy is gone',64,586,34,bold=True,color=GREEN);add(im)
    elif k=='practice':
        header(d,11,'Compare purpose, dataset and status','Map: Access decision → Example record → Reuse description')
        row(235,'ACCESS DECISION','Recorded approval vs evidence of enforced controls')
        row(379,'REUSE DESCRIPTION','Synthetic version · pending ID · proposed license')
        text(d,'Explain the boundary, then check your answer.',64,586,35,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,11);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
