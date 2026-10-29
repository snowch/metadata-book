"""Preserve separate evidence when records disagree."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0):layers.append((im,start,None))
    im,d=layer()
    def row(y,label,value,fill=WHITE):
        box(d,64,y,1152,110,fill=fill)
        text(d,label,86,y+10,23,bold=True,color=RUST)
        text(d,value,86,y+49,36,bold=True)
    if k=='missing-question':
        header(d,6,'Not mentioned. Deleted?','What else could explain a missing scan result?')
        row(243,'YESTERDAY','delivery_summary observed')
        row(387,'TODAY','No mention of delivery_summary')
        text(d,'Pause and name another explanation.',64,579,38,bold=True);add(im)
    elif k=='missing-answer':
        header(d,6,'Keep evidence. Mark uncertainty.','Check scope, permissions and collection outcome.')
        row(242,'LAST SUCCESSFUL OBSERVATION','delivery_summary was seen')
        row(386,'CURRENT STATUS','Unverified: not observed in today’s collection',SAGE)
        text(d,'Confirmed deletion needs supporting evidence.',64,586,36,bold=True,color=GREEN);add(im)
    elif k=='repeat':
        header(d,6,'One event received twice','21 October 2026 · UTC · scheduler source + stable event ID')
        row(235,'REPORTED EVENT E20','R1000 → summary-R1000 at 10:00')
        row(371,'FIRST RECEIPT','10:01');add(im)
        im,d=layer();box(d,64,507,1152,110,fill=SAGE)
        text(d,'REPEATED RECEIPT · SAME SOURCE AND EVENT E20',86,518,23,bold=True,color=RUST)
        text(d,'10:04 → keep one reported publication',86,558,36,bold=True)
        add(im,cue(t,'then again'))
    elif k=='late':
        header(d,6,'Last arrival belongs to an earlier run','21 October 2026 · UTC · keep event time and receipt time')
        text(d,'EVENT TIME',64,225,24,bold=True,color=RUST)
        text(d,'RECEIPT TIME',822,225,24,bold=True,color=RUST)
        for x,y,a,b in [(64,279,'09:50 · E19','R0950 failed'),(64,433,'10:00 · E20','R1000 publication'),(822,279,'10:01 · E20','First receipt'),(822,433,'10:06 · E19','Delayed receipt')]:
            box(d,x,y,394,122)
            text(d,a,x+18,y+12,30,bold=True)
            text(d,b,x+18,y+64,27)
        arrow(d,473,340,805,495,color=RUST)
        arrow(d,473,495,805,340,color=GREEN)
        text(d,'An old failure does not change a different run.',64,584,36,bold=True,color=GREEN);add(im)
    elif k=='conflict-question':
        header(d,6,'Which output is actually in the table?','21 October 2026 · UTC · same production dataset')
        row(235,'SCHEDULER E20 · REPORTED AT 10:00','Published summary-R1000')
        row(379,'DATABASE SCAN S7 · OBSERVED AT 10:03','Version label: summary-R0940')
        text(d,'Explain what is known. What needs checking?',64,586,36,bold=True);add(im)
    elif k=='conflict-answer':
        header(d,6,'Current published version: disputed','Keep both claims, sources and times.')
        row(235,'SCHEDULER E20','Reports summary-R1000 at 10:00')
        row(379,'DATABASE SCAN S7','Observes summary-R0940 at 10:03')
        text(d,'Neither claim is established as correct here.',64,586,36,bold=True,color=GREEN);add(im)
    elif k=='investigate':
        header(d,6,'Record the reason for a conclusion','Checks to perform; no resolution supplied in this example')
        row(236,'INVESTIGATE','Write logs + saved output versions')
        row(380,'IF RESOLVED','Attach supporting evidence to the conclusion',SAGE)
        text(d,'Duplicate handling ≠ resolving a disagreement',64,586,36,bold=True);add(im)
    elif k=='practice':
        header(d,6,'What would a later omission establish?','Map: Source observation → Example record → Collection run')
        row(236,'MAP EXAMPLE · 20 OCTOBER','Compare Observed at and Collected at')
        row(380,'HYPOTHETICAL LATER SCAN','Dataset omitted: which checks are needed?')
        text(d,'Explain, then use “Check your answer”.',64,586,36,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,6);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
