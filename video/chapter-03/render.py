"""Trace the particular report result back to its retained input and code."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def trail(d, active):
    # These arrows mean investigation through references, not processing order.
    for j,label in enumerate(['Refresh','Output','Run','Input + code']):
        x=64+j*296
        box(d,x,222,264,63,fill=SAGE if j==active else WHITE,outline=GREEN if j==active else LINE)
        text(d,label,x+17,236,28,bold=j==active)
        if j<3:arrow(d,x+268,252,x+290,252)

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0,end=None):layers.append((im,start,end))
    im,d=layer()
    if k=='report-question':
        header(d,3,'Does refreshed mean recalculated?','Service Analytics · completed deliveries only')
        box(d,64,230,1152,235)
        text(d,'100%',100,242,105,serif=True,color=RUST)
        text(d,'Report refreshed at 13:00 UTC',100,386,39,bold=True)
        text(d,'When was this result produced?',64,520,42,bold=True)
        text(d,'Invented incident · pause and explain your answer.',64,594,29,color=MUTED);add(im)
    elif k=='route':
        header(d,3,'Refreshing and calculating are separate','The report reads a stored result; it does not rerun the job.')
        for y,a,b in [(240,'Scheduled job','Saved result'),(425,'Saved result','Report refresh')]:
            box(d,64,y,510,111);box(d,706,y,510,111)
            text(d,a,90,y+33,36,bold=True);text(d,b,732,y+33,36,bold=True);arrow(d,588,y+54,692,y+54)
        text(d,'Investigate the exact output this report read.',64,595,35,bold=True,color=GREEN);add(im)
    elif k=='output':
        header(d,3,'Match the identifier. Follow its producing run.','Investigation: from the report back to its producer')
        trail(d,1)
        box(d,64,317,545,238);box(d,671,317,545,238)
        text(d,'Refresh F1300',86,339,35,bold=True)
        text(d,'summary-R1205',86,403,39,color=RUST,bold=True)
        text(d,'Refreshed 13:00',86,485,31)
        text(d,'Published output',693,339,35,bold=True)
        text(d,'summary-R1205',693,403,39,color=RUST,bold=True)
        text(d,'Published 12:05',693,485,31)
        arrow(d,617,431,663,431);add(im)
        im,d=layer();text(d,'55 minutes earlier · producing run: R1205',64,594,36,bold=True,color=GREEN);add(im,cue(t,'Its matching output'))
    elif k=='run-question':
        header(d,3,'Would today’s table reproduce this result?','Investigation: inspect the run’s retained input and code')
        trail(d,2)
        box(d,410,311,460,86,fill=SAGE);text(d,'Run R1205',438,331,38,bold=True)
        arrow(d,535,407,330,452);arrow(d,745,407,950,452)
        for x,a,b in [(64,'Retained input','S1205'),(652,'Retained code','completed-v1')]:
            box(d,x,462,564,115);text(d,a,x+24,473,28,color=MUTED);text(d,b,x+24,518,38,bold=True)
        text(d,'Explain your answer before continuing.',64,610,32,bold=True,color=RUST);add(im)
    elif k in ('snapshot','calculation'):
        header(d,3,'Inspect the saved input, not today’s table' if k=='snapshot' else 'Reproduce the retained calculation','Input S1205 · captured 12:05 UTC · all four due by noon')
        trail(d,3)
        for x,label in zip([190,490,790,1090],['D101','D102','D103','D104']):text(d,label,x-58,313,28,bold=True)
        parcels(d,y=364,unfinished=2,selected={0,2} if k=='calculation' else None)
        for x,label in zip([190,490,790,1090],['11:50','NULL','11:40','NULL']):text(d,label,x-58,552,28,color=MUTED)
        if k=='snapshot':
            text(d,'Complete example: NULL means unfinished.',64,612,32,bold=True,color=GREEN);add(im)
        else:
            for x in [490,1090]:
                d.line((x-120,342,x+120,543),fill=RUST,width=4);d.line((x+120,342,x-120,543),fill=RUST,width=4)
            add(im)
            im,d=layer();text(d,'2 on time ÷ 2 completed = 100%',64,612,37,bold=True,color=GREEN);add(im,cue(t,'Two out of two'))
    elif k=='meaning':
        header(d,3,'Matching evidence explains this result','Investigation: refresh → output → run → retained input and code')
        trail(d,3)
        for y,a,b in [(322,'Lineage','Data flow and dependencies'),(445,'Provenance','History of a particular dataset or result')]:
            box(d,64,y,1152,105);text(d,a,84,y+9,32,bold=True,color=RUST);text(d,b,84,y+54,32)
        text(d,'The terms overlap. Full definitions are on the page.',64,572,25,color=MUTED);add(im)
        im,d=layer();text(d,'Why 100%? Explained. Still current? Chapter 4.',64,610,33,bold=True,color=GREEN);add(im,cue(t,'Explaining why'))
    elif k=='practice':
        header(d,3,'Try it in the metadata map','Report refresh → Example record → follow the identifiers')
        trail(d,0)
        for j,value in enumerate(['1. Follow the output to Published output.','2. Follow its run to Run.','3. Find the retained input and code version.']):text(d,value,64,327+j*80,36,bold=True)
        text(d,'Explain 100%, then use “Check your answer”.',64,605,33,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,3);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
