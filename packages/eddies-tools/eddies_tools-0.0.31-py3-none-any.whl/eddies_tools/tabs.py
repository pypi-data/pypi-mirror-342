import sys
import time
from datetime import datetime
from html_builder import *
class TabButtons(Tag):
    def __init__(self,tabNames):
        super().__init__('div')
        attrs={'class':'_row_ tbbtnrow'}
        self.setAttributes(attrs)
        mx=0
        for tabName in tabNames:
            lg=len(tabName)
            if lg>mx: mx=lg
        w=f'calc(var(--fsz) * {mx/1.2})'
        for c,tabName in enumerate(tabNames):
            button=self.Button({'text':tabName,'class':'tbbtn',
                'style':{'width':w},
                 'onclick':f"TABS.toggleTab(event)"})
            if c==0:
                button.attrs['class']+=' actv'
class Tabs(Tag):
    def __init__(self,numTabs):
        super().__init__('div')
        attrs={'class':'tbcont'}
        self.setAttributes(attrs)
        for j in range(numTabs):
            if j==0:
                self.column({'style':{'display':'flex'},'class':'_tb_'})
            else:
                self.column({'style':{'display':'none'},'class':'_tb_'})
