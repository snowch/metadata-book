"""Review semantic change and distinguish approval from release."""
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
    if k=='meaning-question':
        header(d,10,'Same column. Same meaning?','Separate hypothetical change · promised_at keeps name and type')
        for x,a,b in [(64,'ORIGINAL PROMISE','12:00'),(646,'REVISED PROMISE','12:30')]:
            box(d,x,235,552 if x==64 else 570,216)
            text(d,a,x+25,257,25,bold=True,color=RUST);text(d,b,x+25,319,78,serif=True)
        text(d,'Parcel arrives at 12:20.',64,510,44,bold=True)
        text(d,'What changes for classification and the denominator?',64,610,33,bold=True);add(im)
    elif k=='meaning-answer':
        header(d,10,'Both classification and membership change','Same 12:20 arrival; compare which promise the measure uses.')
        for x,a,b,col in [(64,'ORIGINAL · 12:00','Late',RUST),(646,'REVISED · 12:30','On time',GREEN)]:
            box(d,x,235,552 if x==64 else 570,291)
            text(d,a,x+24,261,28,bold=True,color=RUST);text(d,b,x+24,340,52,bold=True,color=col)
        add(im)
        im,d=layer();text(d,'Due by noon: included',88,465,33,bold=True)
        text(d,'Due by noon: excluded',670,465,33,bold=True)
        text(d,'Schema compatibility does not establish agreed meaning.',64,598,33,bold=True,color=GREEN)
        add(im,cue(t,'Changing the promise also'))
    elif k=='release-question':
        header(d,10,'Design approved. May it be published?','Hypothetical C17 alternative · original promised_at retained')
        row(234,'DESIGN APPROVAL','Producer + both consumers · 2 November 2026')
        row(370,'PLANNED EFFECT','5 November 2026 · 13:00 UTC snapshots')
        text(d,'Still required: consumer evidence, validation and rollout plan.',64,558,34,bold=True);add(im)
    elif k=='release-answer':
        header(d,10,'Approved design. Release pending.','Adding revised_promise_at does not migrate consumers.')
        row(234,'STEWARD CONFIRMS','Consumer choices, acceptance and migration evidence')
        row(370,'PRODUCER SUPPLIES','Validation results + rollout plan',SAGE)
        text(d,'After release: attach actual execution and refresh records.',64,570,33,bold=True,color=GREEN);add(im)
    elif k=='history':
        header(d,10,'A restatement preserves the earlier report','Only if definition owners and affected consumers approve.')
        for x,a,b in [(64,'EARLIER PUBLICATION','Retain what readers saw'),(646,'RESTATED PUBLICATION','New output identifier')]:
            box(d,x,250,552 if x==64 else 570,215)
            text(d,a,x+23,275,24,bold=True,color=RUST)
            text(d,b,x+23,348,35,bold=True,width=515)
        text(d,'Link old output, definition, inputs, code and approval.',64,532,35,bold=True,color=GREEN)
        text(d,'Steward coordinates; business teams own their definitions.',64,614,29,color=MUTED);add(im)
    elif k=='practice':
        header(d,10,'What change has the contract agreed?','Map: Data contract → Example record → deliveries-v1')
        row(235,'CURRENT MEANING','promised_at = original customer promise')
        row(379,'CHANGE REQUIREMENT','Agreement with both consuming teams')
        text(d,'Explain compatibility, then check your answer.',64,586,35,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,10);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
