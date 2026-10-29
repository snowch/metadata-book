"""Format, delivery and identity solve separate exchange problems."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0):layers.append((im,start,None))
    im,d=layer()
    def row(y,label,value,fill=WHITE):
        box(d,64,y,1152,110,fill=fill);text(d,label,86,y+10,23,bold=True,color=RUST);text(d,value,86,y+49,34,bold=True)
    if k=='connection-question':
        header(d,9,'A compatible document. A working connection?','Invented exchange example · no running services')
        for x,a,b in [(64,'PRODUCER','Scheduler'),(462,'DOCUMENT','JSON event'),(860,'RECEIVER','Catalogue')]:
            box(d,x,270,356,174)
            text(d,a,x+22,292,23,bold=True,color=RUST);text(d,b,x+22,356,38,bold=True)
        text(d,'?',432,327,37,bold=True);text(d,'?',830,327,37,bold=True)
        text(d,'What must both ends still agree?',64,562,40,bold=True);add(im)
    elif k=='connection-answer':
        header(d,9,'Configure and test the route','Integration observes and emits; receiver checks permission.')
        for i,(a,b) in enumerate([('PRODUCE','Emit event'),('TRANSPORT','Endpoint'),('RECEIVER','Accept'),('RETRIEVE','Queryable?')]):
            x=64+i*300;box(d,x,270,252,172)
            text(d,a,x+17,293,23,bold=True,color=RUST);text(d,b,x+17,358,31,bold=True)
            if i<3:arrow(d,x+261,357,x+287,357)
        text(d,'Accepted does not mean already queryable.',64,516,38,bold=True,color=GREEN)
        text(d,'Check retries and gaps; no exactly-once guarantee.',64,601,32);add(im)
    elif k=='identity-question':
        header(d,9,'Same names. Which execution?','Suppose two schedulers use the same short labels.')
        for x,a in [(64,'SCHEDULER A'),(646,'SCHEDULER B')]:
            box(d,x,251,552 if x==64 else 570,252)
            text(d,a,x+22,273,24,bold=True,color=RUST)
            text(d,'build_delivery_summary',x+22,345,32,bold=True,width=518)
            text(d,'R1205',x+22,427,46,bold=True)
        text(d,'What identity information is missing?',64,585,38,bold=True);add(im)
    elif k=='identity-answer':
        header(d,9,'Retain explicit identities and mappings','Do not infer a match from a short table or run name.')
        row(230,'JOB IDENTITY','Namespace + job name');add(im)
        im,d=layer();row(361,'EXECUTION CORRESPONDENCE','R1205 ↔ exchange run UUID',SAGE);add(im,cue(t,'The page explicitly maps'))
        im,d=layer();row(492,'DATASET CORRESPONDENCE','Output namespace/name ↔ local dataset ID');add(im,cue(t,'Map the output'))
        im,d=layer();text(d,'Same execution: retain UUID. New execution: new identity.',64,630,27,color=MUTED);add(im,cue(t,'Reuse that UUID'))
    elif k=='limits':
        header(d,9,'Completion is a sourced claim','Dataset identities do not preserve the versions used.')
        row(234,'NOT PRESERVED IN THIS EVENT','Input snapshot · code · output version · refresh')
        row(370,'DISTINCT PARTS OF EXCHANGE','Event model · event envelope · query API')
        text(d,'OpenLineage ≠ the page’s illustrative retrieval API',64,582,35,bold=True,color=GREEN);add(im)
    elif k=='practice':
        header(d,9,'Which exchange identities are missing?','Map: Run → Example record → Job')
        row(235,'FOLLOW THE LOCAL REFERENCE','Find run_id and job_name; compare Job’s name')
        row(379,'CHECK WHAT IS NOT SUPPLIED','Job namespace + exchange run UUID')
        text(d,'Explain the mappings, then check your answer.',64,586,35,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,9);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
