"""Reinforce the page's denominator example through prediction and checking."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind']; layers=[]
    def add(im,start=0,end=None):layers.append((im,start,end))
    im,d=layer()
    if k=='puzzle':
        header(d,1,'Same deliveries. Two percentages.','Which question does the dashboard answer?')
        for x,value in [(64,'66.7%'),(652,'50.0%')]:
            box(d,x,250,564,220);text(d,value,x+45,293,90,serif=True,color=RUST)
        text(d,'What is included in each calculation?',64,537,42,bold=True)
        text(d,'Invented example · complete records at 13:00',64,612,26,color=MUTED);add(im)
    elif k in ('parcels','predict','completed','due'):
        titles={'parcels':'Four parcels, all due by noon','predict':'Your turn: count completed deliveries','completed':'Completed means all three arrivals','due':'All due includes the unfinished parcel'}
        header(d,1,titles[k],'At 13:00: two on time, one late, one unfinished')
        parcels(d,selected={0,1} if k in ('completed','due') else None);add(im)
        if k=='predict':
            im,d=layer();text(d,'Denominator: 2, 3 or 4?',64,514,49,bold=True,color=RUST)
            text(d,'Choose, then explain. Pause for more time.',64,599,29,color=MUTED);add(im)
        elif k=='completed':
            im,d=layer();bracket(d,3,'3 completed deliveries');add(im)
            im,d=layer();text(d,'2 on time ÷ 3 completed = 66.7%',80,575,43,bold=True,color=RUST);add(im,cue(t,'Two on time'))
        elif k=='due':
            at=cue(t,'The unfinished parcel')
            im,d=layer();bracket(d,3,'3 completed');add(im,0,at)
            im,d=layer();bracket(d,4,'4 deliveries due');add(im,at)
            im,d=layer();text(d,'2 on time ÷ 4 due = 50.0%',80,575,46,bold=True,color=RUST);add(im,cue(t,'Two out of'))
        else:
            im,d=layer();text(d,'Which parcels count? It depends on the question.',64,555,36,bold=True);add(im)
    elif k=='rule':
        header(d,1,'Record what the number means','Definition excerpt · Delivery Operations · all due')
        for j,(a,b) in enumerate([('COUNT','All four due, including unfinished'),('MEASURED AT','13:00 UTC on the reporting date'),('RESPONSIBLE TEAM','Delivery Operations')]):
            y=236+j*111;box(d,64,y,1152,95,fill=SAGE if j==0 else WHITE)
            text(d,a,85,y+12,21,bold=True,color=RUST);text(d,b,85,y+39,34,bold=j==0)
        text(d,'Metadata makes the choice inspectable.',64,599,35,bold=True,color=GREEN);add(im)
    elif k=='challenge':
        header(d,1,'Does a successful query prove it?','Explain your answer before continuing.')
        for x,title,value in [(64,'Definition counts','4 deliveries due'),(652,'Dashboard shows','66.7%')]:
            box(d,x,249,564,226);text(d,title,x+28,273,31,bold=True);text(d,value,x+28,346,45,color=RUST,bold=True)
        text(d,'The query ran successfully.',64,522,40)
        text(d,'Does it follow the recorded rule?',64,591,40,bold=True);add(im)
    elif k=='answer':
        header(d,1,'Successful execution ≠ the right question','Check the filter and the denominator.')
        parcels(d,selected={0,1});bracket(d,4,'Rule: 4 due → 50.0%');add(im)
        im,d=layer();text(d,'Query: only 3 completed → 66.7%',80,575,42,bold=True,color=RUST);add(im,cue(t,'This calculation'))
    elif k=='practice':
        header(d,1,'Try it in the metadata map','On this page: Metric definition → Example record')
        for j,(a,b) in enumerate([('1','What counts?'),('2','When is it measured?'),('3','Which team can explain it?')]):
            text(d,a,72,255+j*88,35,bold=True,color=RUST);text(d,b,137,248+j*88,40)
        text(d,'Does recording the rule prove it is followed?',64,535,35,bold=True,color=GREEN)
        text(d,'Explain, then use “Check your answer” on the page.',64,600,29,color=MUTED);add(im)
    elif k=='end':end_card(d,c,1);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
