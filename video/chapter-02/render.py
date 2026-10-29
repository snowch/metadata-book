"""Show the difference between permitted structure, meaning and counted rows."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_aid import *

def make(t,c):
    k=t['kind'];layers=[]
    def add(im,start=0,end=None):layers.append((im,start,end))
    im,d=layer()
    if k=='schema':
        header(d,2,'What does a missing time mean?','Column record excerpt · deliveries table · SQLite')
        box(d,64,238,1152,153)
        text(d,'delivered_at',90,258,46,bold=True)
        text(d,'type: TEXT',90,329,32);text(d,'notnull: 0 → NULL allowed',510,329,32)
        text(d,'TEXT does not strictly enforce every stored value.',64,430,32,color=MUTED)
        text(d,'What could NULL mean? Explain your prediction.',64,525,37,bold=True,color=RUST)
        text(d,'Pause for more thinking time.',64,595,28,color=MUTED);add(im)
    elif k=='meaning':
        header(d,2,'Structure permits it. Meaning explains it.','A missing time can have different explanations.')
        for j,(a,b) in enumerate([('Unfinished','Parcel has not arrived'),('Late update','Record has not caught up'),('Unknown','Arrival time unavailable')]):
            y=232+j*100;box(d,64,y,1152,83)
            text(d,a,86,y+21,32,bold=True,color=RUST);text(d,b,410,y+21,32)
        add(im)
        im,d=layer();text(d,'Here: complete invented records → NULL = unfinished',64,579,32,bold=True,color=GREEN);add(im,cue(t,'For this page'))
    elif k=='promise':
        header(d,2,'One arrival. Two possible meanings.','Same column name and type; which promise is stored?')
        arrow(d,135,341,1150,341)
        for x,a,b in [(155,'12:00','Original promise'),(700,'12:20','Parcel arrives'),(1090,'12:30','Revised promise')]:
            d.line((x,327,x,355),fill=INK,width=4)
            text(d,a,x-70,266,38,bold=True,width=170)
            text(d,b,x-125,380,29,width=250)
        add(im)
        im,d=layer();box(d,64,477,555,115,fill=WASH);text(d,'Against noon: late',86,510,36,bold=True,color=RUST);add(im,cue(t,'Against the original'))
        im,d=layer();box(d,645,477,571,115,fill=SAGE);text(d,'Against 12:30: on time',667,510,34,bold=True,color=GREEN);add(im,cue(t,'Against a revised'))
    elif k in ('filter-question','filter-result'):
        header(d,2,'Which parcel does the filter remove?' if k=='filter-question' else 'The filter leaves three completed deliveries','Saved-query excerpt · full SQL stays on the page')
        box(d,64,224,1152,69,fill=WASH)
        text(d,'WHERE delivered_at IS NOT NULL',82,237,37,bold=True,color=RUST)
        parcels(d,y=335,selected={0,1} if k=='filter-result' else None)
        text(d,'NULL',1030,517,32,bold=True,color=MUTED)
        if k=='filter-question':
            text(d,'Point to the row that disappears. Then explain why.',64,590,33,bold=True);add(im)
        else:
            d.line((969,311,1211,504),fill=RUST,width=4);d.line((1211,311,969,504),fill=RUST,width=4)
            add(im)
            im,d=layer();text(d,'2 on time ÷ 3 completed = 66.7%',64,577,43,bold=True,color=GREEN);add(im,cue(t,'Two out of'))
    elif k=='compare':
        header(d,2,'Read the calculation. Check the meaning.','Query result versus Delivery Operations’ definition')
        for x,a,b,col in [(64,'Query: 3 completed','66.7%',RUST),(652,'Rule: all 4 due','50.0%',GREEN)]:
            box(d,x,232,564,195);text(d,a,x+25,254,32,bold=True);text(d,b,x+25,314,68,serif=True,color=col)
        add(im)
        im,d=layer();text(d,'Saved query = metadata about the calculation',64,474,34,bold=True)
        text(d,'Returned percentage = output data',64,535,34,bold=True)
        text(d,'The query does not choose the business rule.',64,601,29,color=MUTED);add(im,cue(t,'The saved query'))
    elif k=='practice':
        header(d,2,'Try it in the metadata map','Column → Example record → delivered_at')
        for j,(a,b) in enumerate([('STRUCTURE','What does TEXT / notnull: 0 permit?'),('MEANING','What does a missing time mean here?'),('CALCULATION','Does the filter follow the definition?')]):
            y=229+j*112;box(d,64,y,1152,98)
            text(d,a,85,y+9,21,bold=True,color=RUST);text(d,b,85,y+41,35)
        text(d,'Compare Saved query with Metric definition.',64,594,32,bold=True,color=GREEN);add(im)
    elif k=='end':end_card(d,c,2);add(im)
    else:raise ValueError(k)
    return layers

if __name__=='__main__':render(Path(__file__).resolve().parent,make)
