"""Keep dataset identity, source authority and kinds of time distinct."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0,end=None):layers.append((im,start,end))
    im,d=layer()
    if k=='identity-question':
        header(d,5,'Same table name. Same dataset?','A collector reads descriptions and sends them to the catalogue.')
        for x,label in [(64,'PRODUCTION'),(646,'TESTING')]:
            box(d,x,242,570 if x==646 else 552,211)
            text(d,label,x+25,265,25,bold=True,color=RUST)
            text(d,'delivery_summary',x+25,339,39,bold=True)
        text(d,'Is the name enough to join their claims?',64,547,40,bold=True)
        text(d,'Pause and explain what else you need.',64,616,29,color=MUTED);add(im)
    elif k=='identity-answer':
        header(d,5,'Use agreed identities, not just table names','Environment / database / table; resolve different source names.')
        for j,(a,b) in enumerate([('PRODUCTION','prod/parcels/delivery_summary'),('TESTING','test/parcels/delivery_summary')]):
            y=236+j*164;box(d,64,y,1152,135)
            text(d,a,86,y+14,24,bold=True,color=RUST);text(d,b,86,y+66,39,bold=True)
        text(d,'Check renames and replacements before keeping old links.',64,609,30,color=GREEN,bold=True);add(im)
    elif k=='claims':
        header(d,5,'One dataset. Keep the claims separate.','Illustrative entry · 20 October 2026 · sources remain visible')
        box(d,64,222,1152,86,fill=SAGE)
        text(d,'prod/parcels/delivery_summary',86,245,39,bold=True)
        add(im)
        for j,(a,b,phrase) in enumerate([
            ('DATABASE SCAN','Structure: column percentage exists','The database scan'),
            ('SCHEDULER','Reported publication: R0905 → summary-R0905','The scheduler'),
            ('SERVICE ANALYTICS','Meaning: percentage of completed deliveries on time','Service Analytics'),
        ]):
            im,d=layer();y=329+j*99;box(d,64,y,1152,87)
            text(d,a,84,y+7,21,bold=True,color=RUST);text(d,b,84,y+39,31,bold=True)
            add(im,cue(t,phrase))
        im,d=layer();text(d,'One output version does not replace the dataset identity.',64,634,25,color=MUTED);add(im,cue(t,'An output version identifies'))
    elif k=='time-question':
        header(d,5,'When was this column created?','Production database scan · 20 October 2026 · all times UTC')
        for x,label,value in [(64,'OBSERVED','09:00'),(646,'COLLECTED','09:02')]:
            box(d,x,244,570 if x==646 else 552,231)
            text(d,label,x+26,271,26,bold=True,color=RUST);text(d,value,x+26,337,84,serif=True)
        text(d,'What do these times actually establish?',64,550,40,bold=True)
        text(d,'Explain before continuing.',64,618,29,color=MUTED);add(im)
    elif k=='time-answer':
        header(d,5,'Creation time is unknown from this scan','Keep source, observation and collection times labelled.')
        for y,title,left,right in [(244,'SCAN','Observed 09:00','Collected 09:02'),(423,'SCHEDULER','Completed 09:05','Collected 09:06')]:
            text(d,title,64,y,23,bold=True,color=RUST)
            box(d,64,y+43,520,94);box(d,696,y+43,520,94)
            text(d,left,85,y+68,35,bold=True);text(d,right,718,y+68,35,bold=True)
            arrow(d,598,y+89,681,y+89)
        text(d,'Catalogue arrival does not change the source event time.',64,613,31,color=GREEN,bold=True);add(im)
    elif k=='limits':
        header(d,5,'Each source establishes different facts','Keep the source attached to every claim.')
        for j,(a,b) in enumerate([('SCAN','Which columns were observed?'),('SCHEDULER','Which run reported a publication?'),('DEFINITION','Which meaning was agreed?')]):
            y=236+j*114;box(d,64,y,1152,98)
            text(d,a,85,y+10,22,bold=True,color=RUST);text(d,b,85,y+47,35,bold=True)
        text(d,'Last collected does not mean authority for every fact.',64,615,31,color=GREEN,bold=True);add(im)
    elif k=='responsibility':
        header(d,5,'Importing a name does not assign responsibility','Accepted agreement belongs with the definition record.')
        box(d,64,243,1152,213,fill=SAGE)
        text(d,'Service Analytics',88,272,48,bold=True)
        text(d,'Accepted responsibility for the definition',88,366,37,bold=True)
        text(d,'A collected team name alone does not establish agreement.',64,533,32)
        text(d,'Collecting the record does not make its operator responsible.',64,612,30,color=GREEN,bold=True);add(im)
    elif k=='practice':
        header(d,5,'Check scope before joining records','Map: Source observation → Example record → Collection run')
        for x,title,date,note in [(64,'Source observation','20 October 2026','Scan observed percentage'),(646,'Run R1205','19 October 2026','Earlier report incident')]:
            box(d,x,243,570 if x==646 else 552,246)
            text(d,title,x+24,268,34,bold=True)
            text(d,date,x+24,346,36,bold=True,color=RUST)
            text(d,note,x+24,434,29)
        text(d,'Separate examples: joining needs explicit references.',64,545,35,bold=True,color=GREEN)
        text(d,'Explain the scan’s limits, then check your answer.',64,616,29,color=MUTED);add(im)
    elif k=='end':end_card(d,c,5);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
