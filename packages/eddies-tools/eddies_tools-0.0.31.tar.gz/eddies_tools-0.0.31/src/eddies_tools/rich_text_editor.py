import sys
import time
from datetime import datetime
from html_builder import *

class RichTextEditor(Tag):
    def __init__(self,attrs):
        super().__init__('div')
        idx=attrs['id']
        if attrs.get('class'):
            attrs['class']+=' _col_ rchtxtedtr'
        else:
            attrs['class']=' _col_ rchtxtedtr'
        self.setAttributes(attrs)
        bar=self.row({'style':{'display':'flex','position':'relative',
                               'white-space':'pre','flex-wrap':'wrap'}})
        bar.Button({'text':'B','style':{'font-weight':'bold'},
                    'onclick':f"RichTextEditor.makeBold(event,'{idx}')"})
        bar.Button({'text':'I','style':{'font-style':'italic'},
                    'onclick':f"RichTextEditor.makeItalic(event,'{idx}')"})
        bar.Button({'text':'U','style':{'text-decoration':'underline'},
                    'onclick':f"RichTextEditor.makeUnderlined(event,'{idx}')"})
        bar.Button({'text':'S','style':{'text-decoration':'line-through'},
                    'onclick':f"RichTextEditor.makeLineThrough(event,'{idx}')"})
        button=bar.Button({'text':'S',
                    'onclick':f"RichTextEditor.makeSuperscript(event,'{idx}')"})
        button.Sup({'text':'x'})
        button=bar.Button({'text':'S',
                    'onclick':f"RichTextEditor.makeSubscript(event,'{idx}')"})
        button.Sub({'text':'x'})
        button=bar.Button({'text':'A','style':{'color':'blue'}})
        button.Input({'type':'color','value':'#0000FF','style':{'width':'calc(var(--fsz) * 2)'},
                      'onchange':f"RichTextEditor.changeFgColor(event,'{idx}')"})
        button=bar.Button({'text':'A','style':{'background-color':'blue','color':'white'}})
        button.Input({'type':'color','value':'#0000FF','style':{'width':'calc(var(--fsz) * 2)'},
                      'onchange':f"RichTextEditor.changeBgColor(event,'{idx}')"})
        bar.Button({'text':'➕▦','onclick':f"RichTextEditor.toggleTablePanel(event,'{idx}')"})
        row=bar.row({'class':'rchtxtedtrtblpnl','style':{'display':'none'}})
        row.Input({'type':'number','style':{'width':'30px'},'placeholder':4,'min':1})
        row.P({'text':'X'})
        row.Input({'type':'number','style':{'width':'30px'},'placeholder':4,'min':1})
        bar.Button({'text':'❌▦','onclick':f"RichTextEditor.deleteTable(event,'{idx}')"})
        row.Button({'text':'✔️','onclick':f"RichTextEditor.addTable(event,'{idx}')"})
        bar.Button({'text':'➕▤','onclick':f"RichTextEditor.addRow(event,'{idx}')"})
        bar.Button({'text':'▤➕','onclick':f"RichTextEditor.addRow(event,'{idx}',true)"})
        bar.Button({'text':'❌▤','onclick':f"RichTextEditor.deleteRow(event,'{idx}')"})
        bar.Button({'text':'➕▥','onclick':f"RichTextEditor.addColumn(event,'{idx}')"})
        bar.Button({'text':'▥➕','onclick':f"RichTextEditor.addColumn(event,'{idx}',true)"})
        bar.Button({'text':'❌▥','onclick':f"RichTextEditor.deleteColumn(event,'{idx}')"})
        self.body=self.Div({'class':'rchtxtedtrcont','contenteditable':'true',
           'onkeydown':f"RichTextEditor.keydown(event,'{idx}')",
           'onpaste':f"RichTextEditor.onpaste(event,'{idx}')",
        })