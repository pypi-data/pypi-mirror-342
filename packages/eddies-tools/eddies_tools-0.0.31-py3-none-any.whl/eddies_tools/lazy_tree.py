import sys
import time
from datetime import datetime
from html_builder import *

class LazyTree(Tag):
    def __init__(self,attrs,options):
        idx=attrs['id']
        super().__init__('div')
        if attrs.get('class'):
            attrs['class']+=' _col_ lztre _nslct_'
        else:
            attrs['class']=' _col_ lztre _nslct_'
        self.setAttributes(attrs)
        self.filterCol=self.column({'class':'lztrefltrcol'})
        self.filterCol.attrs['style']={}
        if options.get('filterColumnHeight'):
            self.filterCol.attrs['style']['height']=str(options['filterColumnHeight'])+'px'
        for h in options['headers']:
            row=self.filterCol.row({'class':'lztrfltrrow'})
            row.Input({'type':'text','placeholder':f'🔍 {h}','header':h,'class':'lztrefltr',
               'onkeydown':f"LAZYTREE.filter(event,'{idx}')"})
        self.bodyRow=self.row({'class':'lztrebodyrow',
            'onwheel':f"LAZYTREE.onwheel(event,'{idx}');"
                      f"LAZYTREE.populate('{idx}')"})
        self.bodyCol=self.bodyRow.column({'class':'lztrebodycol',
              'onmousedown':f"LAZYTREE.onmousedownBody(event,'{idx}')"})
        self.yTrack=self.bodyRow.column({'class':'lztreytrk'})
        self.yThumb=self.yTrack.Div({'class':'lztreythmb',
            'onmousedown':f"LAZYTREE.onmousedownThumb(event,'{idx}');"})
        self.infoRow=self.row()
        self.infoRow.P({'text':'⚙️','onclick':f"LAZYTREE.toggleOptionsPanel(event,'{idx}')"})
        col=self.infoRow.popup({'class':'lztreoptpnl',
             'onmouseleave':"this.style.display='none'"})
        for h in options['headers']:
            col.Label({'text':h,
               'onmousedown':f"LAZYTREE.onmousedownColVisInput(event,'{idx}')",
           }).Input({'type':'checkbox',
               'onchange':f"LAZYTREE.toggleColumnVisibility(event,'{idx}')"},['checked'])
        self.infoRow.P({'text':'✔'})
        self.infoRow.P({'text':'0','id':'lztrechkd'+idx})
        js=self.Script()
        js.addLines('{')
        js.addVar('tidx',idx)
        js.addVar('opts',options)
        js.addLines(
            f"LAZYTREE.setMeta(tidx,opts)",
        )
        js.addLines('}')