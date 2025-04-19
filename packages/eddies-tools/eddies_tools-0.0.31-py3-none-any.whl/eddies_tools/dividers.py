from html_builder import Tag
class HorizontalDivider(Tag):
    def __init__(self,attrs=None):
        if not attrs: attrs={}
        if attrs.get('class'):
            attrs['class']+=' _hrzdvdr_'
        else:
            attrs['class']='_hrzdvdr_ '
        attrs['onmousedown']=f"Divider.onmousedownHor(event)"
        super().__init__('div')
        self.setAttributes(attrs)
class VerticalDivider(Tag):
    def __init__(self,attrs=None):
        if not attrs: attrs={}
        if attrs.get('class'):
            attrs['class']+=' _vrtdvdr_'
        else:
            attrs['class']='_vrtdvdr_ '
        attrs['onmousedown']=f"Divider.onmousedownVert(event)"
        super().__init__('div')
        self.setAttributes(attrs)
