"""Demonstrate stale output and the evidence that recovery reached the report."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def result_card(d,x,y,title,value,note,w=552):
    box(d,x,y,w,238)
    text(d,title,x+25,y+20,32,bold=True)
    text(d,value,x+25,y+78,72,serif=True,color=RUST)
    text(d,note,x+25,y+181,28,width=w-50,color=MUTED)

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0,end=None):layers.append((im,start,end))
    im,d=layer()
    if k=='fresh-question':
        header(d,4,'Refreshed at 13:00. Current result?','Invented incident · 19 October 2026 · all times UTC')
        result_card(d,64,233,'Report refreshed 13:00','100%','Saved input: 2 completed',w=552)
        box(d,646,233,570,238,fill=WASH)
        parcel(d,740,285,RUST);text(d,'12:20',860,272,47,bold=True)
        text(d,'Third parcel arrived late',675,418,30,bold=True)
        text(d,'Is the report showing the current result?',64,549,41,bold=True)
        text(d,'Pause and explain before continuing.',64,615,28,color=MUTED);add(im)
    elif k=='old-result':
        header(d,4,'Same calculation. Different input states.','Completed deliveries only; no rule change')
        result_card(d,64,236,'Saved at 12:05','2 / 2 = 100%','Two arrivals, both on time')
        result_card(d,646,236,'Current delivery records','2 / 3 = 66.7%','Third arrival was late',w=570)
        text(d,'The 13:00 refresh read the older output.',64,552,39,bold=True,color=GREEN)
        text(d,'Correct for saved inputs ≠ current at report refresh',64,616,30,color=MUTED);add(im)
    elif k=='failed-run':
        header(d,4,'The next run failed before publication','Run R1230 · finished 12:30 UTC')
        box(d,64,231,1152,108,fill=WASH)
        text(d,'FAILED · destination write permission denied',87,260,37,bold=True,color=RUST)
        text(d,'Injected fault in the simulation',64,373,31,color=MUTED)
        box(d,64,438,535,105);box(d,680,438,536,105)
        text(d,'Old output · 12:05',86,467,34,bold=True)
        text(d,'Report refresh · 13:00',702,467,32,bold=True);arrow(d,612,489,666,489)
        add(im)
        im,d=layer();text(d,'The refresh record establishes what readers saw.',64,603,33,bold=True,color=GREEN);add(im,cue(t,"The report's refresh"))
    elif k=='recovery-question':
        header(d,4,'Does a successful run prove recovery?','Same calculation · updated input · no further arrivals')
        result_card(d,64,235,'New publication · 13:10','66.7%','Simulated permission problem removed',w=1152)
        text(d,'Has the new result reached the report?',64,546,41,bold=True)
        text(d,'Explain what evidence you would check.',64,614,30,color=MUTED);add(im)
    elif k=='recovery-answer':
        header(d,4,'Verify the publication AND the report read','Match the output reference; status alone is insufficient.')
        for x,a,b in [(64,'Published output','Published 13:10'),(646,'Refresh F1312','Refreshed 13:12')]:
            box(d,x,239,570 if x==646 else 552,242)
            text(d,a,x+24,261,34,bold=True)
            text(d,'summary-R1310',x+24,330,38,bold=True,color=RUST)
            text(d,b,x+24,421,31)
        arrow(d,623,359,638,359);add(im)
        im,d=layer();text(d,'Matching reference: 66.7% reached the report.',64,551,39,bold=True,color=GREEN)
        text(d,'Published 13:10 → read at 13:12',64,616,32,color=MUTED);add(im,cue(t,'Matching that reference'))
    elif k=='limits':
        header(d,4,'Two different questions to investigate','The wrong-filter fault is a separate hypothetical example.')
        for j,(a,b) in enumerate([('RECOVERY','Did the report read the new output?'),('CORRECT LOGIC','Does the calculation follow the definition?')]):
            y=241+j*155;box(d,64,y,1152,129)
            text(d,a,86,y+14,24,bold=True,color=RUST);text(d,b,86,y+60,37,bold=True)
        text(d,'The page shows how to inspect the separate logic fault.',64,604,30,color=MUTED);add(im)
    elif k=='retain':
        header(d,4,'Keep the evidence behind earlier reports','A later result does not invalidate the earlier calculation.')
        for j,(a,b) in enumerate([('WHAT READERS SAW','Earlier output + report refresh'),('HOW TO REPRODUCE IT','Retained input data + executed code')]):
            y=239+j*160;box(d,64,y,1152,133,fill=SAGE if j==1 else WHITE)
            text(d,a,85,y+14,23,bold=True,color=RUST);text(d,b,85,y+65,37,bold=True)
        text(d,'A reference cannot supply deleted input rows.',64,608,34,bold=True,color=GREEN);add(im)
    elif k=='practice':
        header(d,4,'Compare the map with the recovery table','The map contains the earlier evidence, not recovery records.')
        for j,value in enumerate(['1. Map: old Report refresh → Published output → Run','2. Page: find the new publication and refresh','3. Explain what establishes recovery']):
            text(d,value,64,254+j*108,34,bold=True)
        text(d,'Explain first, then use “Check your answer”.',64,604,33,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,4);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
