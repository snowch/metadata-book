"""Evaluate evidence and maintenance within the pilot's scope."""
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
    if k=='coverage-question':
        header(d,8,'A collector is installed. Enough evidence?','Invented one-week pilot · engineer + independent reviewer')
        row(235,'TWO PILOT QUESTIONS','Choose meeting measure · explain older 100%')
        row(379,'DATABASE COLLECTOR SUPPLIES','Table and view structure')
        text(d,'What evidence is missing for the incident?',64,586,36,bold=True);add(im)
    elif k=='coverage-answer':
        header(d,8,'Test whether the evidence can be opened','Trace the incident; do not stop at visible links.')
        for i,(a,b) in enumerate([('REFRESH','Read output'),('OUTPUT','From run'),('RUN','Used'),('RETAINED','Input + code')]):
            x=64+i*300;box(d,x,260,252,173)
            text(d,a,x+18,282,23,bold=True,color=RUST);text(d,b,x+18,350,30,bold=True)
            if i<3:arrow(d,x+261,345,x+287,345)
        text(d,'Then inspect the later failed run.',64,500,38,bold=True,color=GREEN)
        text(d,'Export must preserve source IDs, times and versions.',64,599,32,color=MUTED);add(im)
    elif k=='choice-question':
        header(d,8,'What choice follows from these results?','Invented assessment · tested questions, accounts and paths pass')
        text(d,'Weekly maintenance',64,234,31,bold=True)
        text(d,'120 min budget',907,234,31,bold=True,width=309)
        box(d,64,291,1152,84,fill=WHITE)
        d.rounded_rectangle((64,291,928,375),radius=16,fill=SAGE,outline=GREEN,width=2)
        text(d,'90 min observed',86,311,32,bold=True)
        row(421,'FRESHNESS','Same working day · limit: 1 working day')
        text(d,'Choose an arrangement. State its limits.',64,592,37,bold=True);add(im)
    elif k=='choice-answer':
        header(d,8,'Keep reviewed documents + SQLite','Only for the two pilot questions; no product assessed.')
        row(235,'REMAINING GAPS','Manual job/report updates · other sources untested')
        text(d,'Review weekly.',64,394,35,bold=True);add(im)
        im,d=layer();box(d,64,470,1152,146,fill=SAGE)
        text(d,'TRIGGER A CATALOGUE TRIAL',86,485,23,bold=True,color=RUST)
        text(d,'Maintenance > 2 hours/week OR updates > 1 working day',86,536,32,bold=True)
        add(im,cue(t,'Trial a catalogue'))
    elif k=='operate':
        header(d,8,'Operating work continues after setup','Collection maintenance and definition responsibility are separate.')
        row(234,'REPORTING ENGINEER','Collection failures + age of last observation')
        row(370,'RELEVANT BUSINESS TEAM','Responsibility for its definition')
        text(d,'Protect metadata across search, links, exports and APIs.',64,582,33,bold=True,color=GREEN);add(im)
    elif k=='practice':
        header(d,8,'What does this collector actually supply?','Map: Collection run → Example record → Responsible team')
        row(235,'COLLECTION RUN','Name a supported fact and missing evidence')
        row(379,'RESPONSIBLE TEAM','Who owns meaning? Who maintains collection?')
        text(d,'Explain the limits, then check your answer.',64,586,36,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,8);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
