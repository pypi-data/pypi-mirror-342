import sys
import time
from datetime import datetime
from html_builder import *

class LazyTable(Tag):
    def __init__(self,attrs,options):
        idx=attrs['id']
        super().__init__('div')
        if attrs.get('class'):
            attrs['class']+=' _col_ lztbl _nslct_'
        else:
            attrs['class']=' _col_ lztbl _nslct_'
        self.setAttributes(attrs)
        attrs['onwheel']=f"LAZYTABLE.onwheel(event,'{idx}');"\
                         f"LAZYTABLE.populate('{idx}')"
        self.tableBody=self.row({'onmousedown':f"LAZYTABLE.mousedownBody(event,'{idx}')",
                                 'ondblclick':f"LAZYTABLE.makeEditable(event,'{idx}')",
                                 'onmouseleave':f"LAZYTABLE.mouseleaveBody(event,'{idx}')"})
        if options.get('radios'):
            self.inputCol=self.tableBody.column({'class':'lztblinpcol'})
            th=self.inputCol.Div({'text':'⦿','class':'lztblth'})
            self.inputTdCol=self.inputCol.column({'class':'lztblinpcolinr lztblcol'})
            td=self.inputTdCol.Div({'class':'lztbltd'})
            td.Input({'type':'radio','name':'rdos'+idx,
                      'onchange':f"LAZYTABLE.onclickinput(event,'{idx}');"
                                 f"LAZYTABLE.populate('{idx}')"})
        elif options.get('checks'):
            self.inputCol=self.tableBody.column({'class':'lztblinpcol'})
            th=self.inputCol.row({'text':'✔','class':'lztblth',
                             'onclick':f"LAZYTABLE.selectAll('{idx}');"
                                       f"LAZYTABLE.populate('{idx}')"})
            self.inputTdCol=self.inputCol.column({'class':'lztblinpcolinr lztblcol'})
            td=self.inputTdCol.Div({'class':'lztbltd'})
            td.Input({'type':'checkbox',
                      'onmousedown':f"LAZYTABLE.mousedownCheckbox(event,'{idx}')",
                      'onclick':f"LAZYTABLE.onclickinput(event,'{idx}');"
                                 f"LAZYTABLE.populate('{idx}')"})
        self.tableBodyInner=self.tableBody.row({'class':'lztblbdyinner'})
        for c,h in enumerate(options['headers']):
            bodyCol=self.tableBodyInner.column({'class':'lztbltdcoloutout'})
            if options.get('colWidths'):
                # self.bodyCol.attrs['class']+=' lztblsetwdcol'
                bodyCol.attrs['style']={'width':str(options['colWidths'][c])+'px'}
            th=bodyCol.row({'class':'lztblth'})
            th.P({'text':'▼','class':'lztblsorttgl',
                  'onclick':f"LAZYTABLE.sort(event,'{idx}');"
                            f"LAZYTABLE.populate('{idx}')"})
            th.Input({'type':'text','placeholder':h,'class':'lztblsrch',
                      'onkeydown':f"LAZYTABLE.filter(event,'{idx}');"
                                  f"LAZYTABLE.populate('{idx}')"})
            bodyTdColOuter=bodyCol.column({'class':'lztbltdcolout'})
            if options.get('colWidths'):
                bodyTdColOuter.attrs['class']+=' lztblsetwdcolout'
            else:
                bodyTdColOuter.attrs['class']+=' lztblautowdcolout'
            bodyTdCol=bodyTdColOuter.column({'class':'lztbltdcol lztblcol'})
            if options.get('colWidths'):
                bodyTdCol.attrs['class']+=' lztblsetwdcol'
            else:
                bodyTdCol.attrs['class']+=' lztblautowdcol'
                # bodyTdCol.attrs['style']={'width':str(options['colWidths'][c])+'px'}
            td=bodyTdCol.Div({'class':'lztbltd'})
        ytrack=self.tableBody.column({'id':'ytrk_'+idx,'class':'lztblytrk'})
        ythumb=ytrack.Div({'id':'ythmb_'+idx,'class':'lztblythmb',
                           'onmousedown':f"LAZYTABLE.onmousedownThumb(event,'{idx}')"})
        self.infoRow=self.row({'style':{'position':'relative'}})
        self.infoRow.P({'text':'⚙️','onclick':f"LAZYTABLE.toggleOptionsPanel(event,'{idx}')"})
        col=self.infoRow.popup({'class':'lztbloptpnl',
             'onmouseleave':"this.style.display='none'"})
        for h in options['headers']:
            col.Label({'text':h}).Input({'type':'checkbox',
                 'onchange':f"LAZYTABLE.toggleColumnVisibility(event,'{idx}')"},['checked'])
        self.infoRow.P({'text':'∑'})
        self.infoRow.P({'text':'0','id':'ttl'+idx})
        self.infoRow.P({'text':':&nbsp;'})
        self.infoRow.P({'text':'0','id':'rgstrt'+idx})
        self.infoRow.P({'text':'~'})
        self.infoRow.P({'text':'0','id':'rgend'+idx})
        self.infoRow.P({'text':'&nbsp;✔'})
        self.infoRow.P({'text':'0','id':'chkd'+idx})
        js=self.Script()
        js.addLines('{')
        js.addVar('opts',options)
        js.addVar('tidx',idx)
        js.addLines(
            "LAZYTABLE.setMeta(tidx,opts)"
        )
        js.addLines('}')
