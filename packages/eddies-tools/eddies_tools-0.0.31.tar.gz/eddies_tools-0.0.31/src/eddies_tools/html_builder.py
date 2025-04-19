import json
from collections import deque
class Tag:
    def __init__(self,tagName,singleton=False):
        self.tagName=tagName
        self.singleton=singleton
        self.children=[]
    def setAttributes(self,attrs=None,sattrs=None):
        self.attrs=attrs
        self.sattrs=sattrs
    def appendChild(self,child):
        self.children.append(child)
        child.parent=child.parentElement=self
        return child
    def nextSibling(self):
        parent=self.parent
        children=parent.children
        ix=children.index(self)
        if ix<len(children)-1:
            return children[ix+1]
        return None
    def previousSibling(self):
        parent=self.parent
        children=parent.children
        ix=children.index(self)
        if ix>0:
            return children[ix-1]
        return None
    def before(self,element):
        parent=self.parent
        children=parent.children
        ix=children.index(self)
        children.insert(ix,element)
        return element
    def after(self,element):
        parent=self.parent
        children=parent.children
        ix=children.index(self)
        children.insert(ix+1,element)
        return element
    def _appendStr(self,pre,depth=0):
        # if depth:
        #     pre.append('\n')
        # for d in range(depth):
        #     pre.append('\t')
        pre.append('<')
        pre.append(self.tagName)
        if self.attrs:
            for k,v in self.attrs.items():
                if k=='text': continue
                elif k=='style':
                    pre.append(' style="')
                    for k2,v2 in v.items():
                        pre.append(k2)
                        pre.append(':')
                        pre.append(str(v2))
                        pre.append(';')
                    pre.append('"')
                elif k=='class':
                    pre.append(' ')
                    pre.append(k)
                    pre.append('=')
                    pre.append('"')
                    pre.append(str(v))
                    pre.append('"')
                else:
                    pre.append(' ')
                    pre.append(k)
                    pre.append('=')
                    pre.append('"')
                    pre.append(str(v))
                    pre.append('"')
        if self.sattrs:
            for sa in self.sattrs:
                pre.append(' ')
                pre.append(sa)
        pre.append('>')
        if self.attrs and 'text' in self.attrs and self.tagName!='label':
            pre.append(self.attrs['text'])
        for child in self.children:
            if child.tagName=='script':
                pre.append(child.str())
            elif child.tagName=='style':
                pre.append(child.str())
            else:
                child._appendStr(pre,depth+1)
        if self.attrs and 'text' in self.attrs and self.tagName=='label':
            pre.append(self.attrs['text'])
        if not self.singleton:
            # pre.append('\n')
            # for d in range(depth):
            #     pre.append('\t')
            pre.append(f'</{self.tagName}>')
    def str(self):
        depth=0
        pre=[]
        self._appendStr(pre,depth)
        return ''.join(pre)
    def column(self,attrs=None):
        if not attrs: attrs={}
        if attrs.get('class'):
            attrs['class']+=' _col_'
        else:
            attrs['class']='_col_'
        return self.appendChild(Div(attrs))
    def row(self,attrs=None):
        if not attrs: attrs={}
        if attrs.get('class'):
            attrs['class']+=' _row_'
        else:
            attrs['class']='_row_'
        return self.appendChild(Div(attrs))
    def popup(self,attrs=None):
        if not attrs: attrs={}
        if attrs.get('class'):
            attrs['class']+=' _popup_ _col_'
        else:
            attrs['class']='_popup_ _col_'
        if attrs.get('style'):
            attrs['style']['display']='none'
        else:
            attrs['style']={'display':'none'}
        return self.appendChild(Div(attrs))
    def tooltip(self,attrs=None):
        if not attrs: attrs={}
        if attrs.get('class'):
            attrs['class']+=' _tltptxt_'
        else:
            attrs['class']='_tltptxt_ '
        if self.attrs.get('class'):
            self.attrs['class']+=' _tltp_'
        else:
            self.attrs['class']='_tltp_'
        return self.appendChild(Div(attrs))
    def Area(self,attrs=None,sattrs=None):
        return self.appendChild(Area(attrs,sattrs))
    def Base(self,attrs=None,sattrs=None):
        return self.appendChild(Base(attrs,sattrs))
    def Body(self,attrs=None,sattrs=None):
        return self.appendChild(Body(attrs,sattrs))
    def Br(self,attrs=None,sattrs=None):
        return self.appendChild(Br(attrs,sattrs))
    def Col(self,attrs=None,sattrs=None):
        return self.appendChild(Col(attrs,sattrs))
    def Command(self,attrs=None,sattrs=None):
        return self.appendChild(Command(attrs,sattrs))
    def Embed(self,attrs=None,sattrs=None):
        return self.appendChild(Embed(attrs,sattrs))
    def Hr(self,attrs=None,sattrs=None):
        return self.appendChild(Hr(attrs,sattrs))
    def Img(self,attrs=None,sattrs=None):
        return self.appendChild(Img(attrs,sattrs))
    def Input(self,attrs=None,sattrs=None):
        return self.appendChild(Input(attrs,sattrs))
    def Keygen(self,attrs=None,sattrs=None):
        return self.appendChild(Keygen(attrs,sattrs))
    def Link(self,attrs=None,sattrs=None):
        return self.appendChild(Link(attrs,sattrs))
    def Meta(self,attrs=None,sattrs=None):
        return self.appendChild(Meta(attrs,sattrs))
    def Param(self,attrs=None,sattrs=None):
        return self.appendChild(Param(attrs,sattrs))
    def Source(self,attrs=None,sattrs=None):
        return self.appendChild(Source(attrs,sattrs))
    def Track(self,attrs=None,sattrs=None):
        return self.appendChild(Track(attrs,sattrs))
    def Wbr(self,attrs=None,sattrs=None):
        return self.appendChild(Wbr(attrs,sattrs))
    def A(self,attrs=None,sattrs=None):
        return self.appendChild(A(attrs,sattrs))
    def Abbr(self,attrs=None,sattrs=None):
        return self.appendChild(Abbr(attrs,sattrs))
    def Address(self,attrs=None,sattrs=None):
        return self.appendChild(Address(attrs,sattrs))
    def Article(self,attrs=None,sattrs=None):
        return self.appendChild(Article(attrs,sattrs))
    def Aside(self,attrs=None,sattrs=None):
        return self.appendChild(Aside(attrs,sattrs))
    def Audio(self,attrs=None,sattrs=None):
        return self.appendChild(Audio(attrs,sattrs))
    def B(self,attrs=None,sattrs=None):
        return self.appendChild(B(attrs,sattrs))
    def Bdi(self,attrs=None,sattrs=None):
        return self.appendChild(Bdi(attrs,sattrs))
    def Bdo(self,attrs=None,sattrs=None):
        return self.appendChild(Bdo(attrs,sattrs))
    def Blockquote(self,attrs=None,sattrs=None):
        return self.appendChild(Blockquote(attrs,sattrs))
    def Body(self,attrs=None,sattrs=None):
        return self.appendChild(Body(attrs,sattrs))
    def Button(self,attrs=None,sattrs=None):
        return self.appendChild(Button(attrs,sattrs))
    def Canvas(self,attrs=None,sattrs=None):
        return self.appendChild(Canvas(attrs,sattrs))
    def Caption(self,attrs=None,sattrs=None):
        return self.appendChild(Caption(attrs,sattrs))
    def Cite(self,attrs=None,sattrs=None):
        return self.appendChild(Cite(attrs,sattrs))
    def Colgroup(self,attrs=None,sattrs=None):
        return self.appendChild(Colgroup(attrs,sattrs))
    def Data(self,attrs=None,sattrs=None):
        return self.appendChild(Data(attrs,sattrs))
    def Datalist(self,attrs=None,sattrs=None):
        return self.appendChild(Datalist(attrs,sattrs))
    def Dd(self,attrs=None,sattrs=None):
        return self.appendChild(Dd(attrs,sattrs))
    def Del(self,attrs=None,sattrs=None):
        return self.appendChild(Del(attrs,sattrs))
    def Details(self,attrs=None,sattrs=None):
        return self.appendChild(Details(attrs,sattrs))
    def Dfn(self,attrs=None,sattrs=None):
        return self.appendChild(Dfn(attrs,sattrs))
    def Dialog(self,attrs=None,sattrs=None):
        return self.appendChild(Dialog(attrs,sattrs))
    def Div(self,attrs=None,sattrs=None):
        return self.appendChild(Div(attrs,sattrs))
    def Dl(self,attrs=None,sattrs=None):
        return self.appendChild(Dl(attrs,sattrs))
    def Dt(self,attrs=None,sattrs=None):
        return self.appendChild(Dt(attrs,sattrs))
    def Em(self,attrs=None,sattrs=None):
        return self.appendChild(Em(attrs,sattrs))
    def Fieldset(self,attrs=None,sattrs=None):
        return self.appendChild(Fieldset(attrs,sattrs))
    def Figcaption(self,attrs=None,sattrs=None):
        return self.appendChild(Figcaption(attrs,sattrs))
    def Figure(self,attrs=None,sattrs=None):
        return self.appendChild(Figure(attrs,sattrs))
    def Footer(self,attrs=None,sattrs=None):
        return self.appendChild(Footer(attrs,sattrs))
    def Form(self,attrs=None,sattrs=None):
        return self.appendChild(Form(attrs,sattrs))
    def H1(self,attrs=None,sattrs=None):
        return self.appendChild(H1(attrs,sattrs))
    def H2(self,attrs=None,sattrs=None):
        return self.appendChild(H2(attrs,sattrs))
    def H3(self,attrs=None,sattrs=None):
        return self.appendChild(H3(attrs,sattrs))
    def H4(self,attrs=None,sattrs=None):
        return self.appendChild(H4(attrs,sattrs))
    def H5(self,attrs=None,sattrs=None):
        return self.appendChild(H5(attrs,sattrs))
    def H6(self,attrs=None,sattrs=None):
        return self.appendChild(H6(attrs,sattrs))
    def Head(self,attrs=None,sattrs=None):
        return self.appendChild(Head(attrs,sattrs))
    def Header(self,attrs=None,sattrs=None):
        return self.appendChild(Header(attrs,sattrs))
    def Hgroup(self,attrs=None,sattrs=None):
        return self.appendChild(Hgroup(attrs,sattrs))
    def Html(self,attrs=None,sattrs=None):
        return self.appendChild(Html(attrs,sattrs))
    def I(self,attrs=None,sattrs=None):
        return self.appendChild(I(attrs,sattrs))
    def Iframe(self,attrs=None,sattrs=None):
        return self.appendChild(Iframe(attrs,sattrs))
    def Ins(self,attrs=None,sattrs=None):
        return self.appendChild(Ins(attrs,sattrs))
    def Kbd(self,attrs=None,sattrs=None):
        return self.appendChild(Kbd(attrs,sattrs))
    def Label(self,attrs=None,sattrs=None):
        return self.appendChild(Label(attrs,sattrs))
    def Legend(self,attrs=None,sattrs=None):
        return self.appendChild(Legend(attrs,sattrs))
    def Li(self,attrs=None,sattrs=None):
        return self.appendChild(Li(attrs,sattrs))
    def Main(self,attrs=None,sattrs=None):
        return self.appendChild(Main(attrs,sattrs))
    def Map(self,attrs=None,sattrs=None):
        return self.appendChild(map(attrs,sattrs))
    def Mark(self,attrs=None,sattrs=None):
        return self.appendChild(Mark(attrs,sattrs))
    def Menu(self,attrs=None,sattrs=None):
        return self.appendChild(Menu(attrs,sattrs))
    def Meter(self,attrs=None,sattrs=None):
        return self.appendChild(Meter(attrs,sattrs))
    def Nav(self,attrs=None,sattrs=None):
        return self.appendChild(Nav(attrs,sattrs))
    def Noscript(self,attrs=None,sattrs=None):
        return self.appendChild(Noscript(attrs,sattrs))
    def Object(self,attrs=None,sattrs=None):
        return self.appendChild(Object(attrs,sattrs))
    def Ol(self,attrs=None,sattrs=None):
        return self.appendChild(Ol(attrs,sattrs))
    def Optgroup(self,attrs=None,sattrs=None):
        return self.appendChild(Optgroup(attrs,sattrs))
    def Option(self,attrs=None,sattrs=None):
        return self.appendChild(Option(attrs,sattrs))
    def Output(self,attrs=None,sattrs=None):
        return self.appendChild(Output(attrs,sattrs))
    def P(self,attrs=None,sattrs=None):
        return self.appendChild(P(attrs,sattrs))
    def Picture(self,attrs=None,sattrs=None):
        return self.appendChild(Picture(attrs,sattrs))
    def Pre(self,attrs=None,sattrs=None):
        return self.appendChild(Pre(attrs,sattrs))
    def Progress(self,attrs=None,sattrs=None):
        return self.appendChild(Progress(attrs,sattrs))
    def Q(self,attrs=None,sattrs=None):
        return self.appendChild(Q(attrs,sattrs))
    def Rp(self,attrs=None,sattrs=None):
        return self.appendChild(Rp(attrs,sattrs))
    def Rt(self,attrs=None,sattrs=None):
        return self.appendChild(Rt(attrs,sattrs))
    def Ruby(self,attrs=None,sattrs=None):
        return self.appendChild(Ruby(attrs,sattrs))
    def S(self,attrs=None,sattrs=None):
        return self.appendChild(S(attrs,sattrs))
    def Script(self,attrs=None,sattrs=None):
        return self.appendChild(Script(attrs,sattrs))
    def Search(self,attrs=None,sattrs=None):
        return self.appendChild(Search(attrs,sattrs))
    def Section(self,attrs=None,sattrs=None):
        return self.appendChild(Section(attrs,sattrs))
    def Select(self,attrs=None,sattrs=None):
        return self.appendChild(Select(attrs,sattrs))
    def Small(self,attrs=None,sattrs=None):
        return self.appendChild(Small(attrs,sattrs))
    def Span(self,attrs=None,sattrs=None):
        return self.appendChild(Span(attrs,sattrs))
    def Strong(self,attrs=None,sattrs=None):
        return self.appendChild(Strong(attrs,sattrs))
    def Style(self,attrs=None,sattrs=None):
        return self.appendChild(Style(attrs,sattrs))
    def Sub(self,attrs=None,sattrs=None):
        return self.appendChild(Sub(attrs,sattrs))
    def Summary(self,attrs=None,sattrs=None):
        return self.appendChild(Summary(attrs,sattrs))
    def Sup(self,attrs=None,sattrs=None):
        return self.appendChild(Sup(attrs,sattrs))
    def Svg(self,attrs=None,sattrs=None):
        return self.appendChild(Svg(attrs,sattrs))
    def Table(self,attrs=None,sattrs=None):
        return self.appendChild(Table(attrs,sattrs))
    def Tbody(self,attrs=None,sattrs=None):
        return self.appendChild(Tbody(attrs,sattrs))
    def Td(self,attrs=None,sattrs=None):
        return self.appendChild(Td(attrs,sattrs))
    def Template(self,attrs=None,sattrs=None):
        return self.appendChild(Template(attrs,sattrs))
    def Textarea(self,attrs=None,sattrs=None):
        return self.appendChild(Textarea(attrs,sattrs))
    def Tfoot(self,attrs=None,sattrs=None):
        return self.appendChild(Tfoot(attrs,sattrs))
    def Th(self,attrs=None,sattrs=None):
        return self.appendChild(Th(attrs,sattrs))
    def Thead(self,attrs=None,sattrs=None):
        return self.appendChild(Thead(attrs,sattrs))
    def Time(self,attrs=None,sattrs=None):
        return self.appendChild(Time(attrs,sattrs))
    def Title(self,attrs=None,sattrs=None):
        return self.appendChild(Title(attrs,sattrs))
    def Tr(self,attrs=None,sattrs=None):
        return self.appendChild(Tr(attrs,sattrs))
    def U(self,attrs=None,sattrs=None):
        return self.appendChild(U(attrs,sattrs))
    def Ul(self,attrs=None,sattrs=None):
        return self.appendChild(ul(attrs,sattrs))
    def Var(self,attrs=None,sattrs=None):
        return self.appendChild(Var(attrs,sattrs))
    def Video(self,attrs=None,sattrs=None):
        return self.appendChild(Video(attrs,sattrs))
class Doctype(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('!DOCTYPE html',True)
        self.setAttributes(attrs,sattrs)
class Area(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('area',True)
        self.setAttributes(attrs,sattrs)
class Base(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('base',True)
        self.setAttributes(attrs,sattrs)
class Br(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('br',True)
        self.setAttributes(attrs,sattrs)
class Col(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('col',True)
        self.setAttributes(attrs,sattrs)
class Command(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('command',True)
        self.setAttributes(attrs,sattrs)
class Embed(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('embed',True)
        self.setAttributes(attrs,sattrs)
class Hr(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('hr',True)
        self.setAttributes(attrs,sattrs)
class Img(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('img',True)
        self.setAttributes(attrs,sattrs)
class Input(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('input',True)
        self.setAttributes(attrs,sattrs)
class Keygen(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('keygen',True)
        self.setAttributes(attrs,sattrs)
class Link(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('link',True)
        self.setAttributes(attrs,sattrs)
class Meta(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('meta',True)
        self.setAttributes(attrs,sattrs)
class Param(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('param',True)
        self.setAttributes(attrs,sattrs)
class Source(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('source',True)
        self.setAttributes(attrs,sattrs)
class Track(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('track',True)
        self.setAttributes(attrs,sattrs)
class Wbr(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('wbr',True)
        self.setAttributes(attrs,sattrs)
class A(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('a')
        self.setAttributes(attrs,sattrs)
class Abbr(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('abbr')
        self.setAttributes(attrs,sattrs)
class Address(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('address')
        self.setAttributes(attrs,sattrs)
class Article(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('article')
        self.setAttributes(attrs,sattrs)
class Aside(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('aside')
        self.setAttributes(attrs,sattrs)
class Audio(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('audio')
        self.setAttributes(attrs,sattrs)
class B(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('b')
        self.setAttributes(attrs,sattrs)
class Bdi(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('bdi')
        self.setAttributes(attrs,sattrs)
class Bdo(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('bdo')
        self.setAttributes(attrs,sattrs)
class Blockquote(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('blockquote')
        self.setAttributes(attrs,sattrs)
class Body(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('body')
        self.setAttributes(attrs,sattrs)
class Button(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('button')
        self.setAttributes(attrs,sattrs)
class Canvas(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('canvas')
        self.setAttributes(attrs,sattrs)
class Caption(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('caption')
        self.setAttributes(attrs,sattrs)
class Cite(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('cite')
        self.setAttributes(attrs,sattrs)
class Colgroup(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('colgroup')
        self.setAttributes(attrs,sattrs)
class Data(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('data')
        self.setAttributes(attrs,sattrs)
class Datalist(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('datalist')
        self.setAttributes(attrs,sattrs)
class Dd(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('dd')
        self.setAttributes(attrs,sattrs)
class Del(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('del')
        self.setAttributes(attrs,sattrs)
class Details(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('details')
        self.setAttributes(attrs,sattrs)
class Dfn(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('dfn')
        self.setAttributes(attrs,sattrs)
class Dialog(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('dialog')
        self.setAttributes(attrs,sattrs)
class Div(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('div')
        self.setAttributes(attrs,sattrs)
class Dl(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('dl')
        self.setAttributes(attrs,sattrs)
class Dt(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('dt')
        self.setAttributes(attrs,sattrs)
class Em(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('em')
        self.setAttributes(attrs,sattrs)
class Fieldset(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('fieldset')
        self.setAttributes(attrs,sattrs)
class Figcaption(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('figcaption')
        self.setAttributes(attrs,sattrs)
class Figure(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('figure')
        self.setAttributes(attrs,sattrs)
class Footer(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('footer')
        self.setAttributes(attrs,sattrs)
class Form(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('form')
        self.setAttributes(attrs,sattrs)
class H1(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('h1')
        self.setAttributes(attrs,sattrs)
class H2(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('h1')
        self.setAttributes(attrs,sattrs)
class H3(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('h1')
        self.setAttributes(attrs,sattrs)
class H4(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('h1')
        self.setAttributes(attrs,sattrs)
class H5(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('h1')
        self.setAttributes(attrs,sattrs)
class H6(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('h1')
        self.setAttributes(attrs,sattrs)
class Head(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('head')
        self.setAttributes(attrs,sattrs)
class Header(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('header')
        self.setAttributes(attrs,sattrs)
class Hgroup(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('hgroup')
        self.setAttributes(attrs,sattrs)
class Html(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('html')
        self.setAttributes(attrs,sattrs)
class I(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('i')
        self.setAttributes(attrs,sattrs)
class Iframe(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('iframe')
        self.setAttributes(attrs,sattrs)
class Ins(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('ins')
        self.setAttributes(attrs,sattrs)
class Kbd(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('kbd')
        self.setAttributes(attrs,sattrs)
class Label(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('label')
        self.setAttributes(attrs,sattrs)
class Legend(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('legend')
        self.setAttributes(attrs,sattrs)
class Li(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('li')
        self.setAttributes(attrs,sattrs)
class Main(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('main')
        self.setAttributes(attrs,sattrs)
class Map(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('map')
        self.setAttributes(attrs,sattrs)
class Mark(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('mark')
        self.setAttributes(attrs,sattrs)
class Menu(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('menu')
        self.setAttributes(attrs,sattrs)
class Meter(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('meter')
        self.setAttributes(attrs,sattrs)
class Nav(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('nav')
        self.setAttributes(attrs,sattrs)
class Noscript(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('noscript')
        self.setAttributes(attrs,sattrs)
class Object(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('object')
        self.setAttributes(attrs,sattrs)
class Ol(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('ol')
        self.setAttributes(attrs,sattrs)
class Optgroup(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('optgroup')
        self.setAttributes(attrs,sattrs)
class Option(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('option')
        self.setAttributes(attrs,sattrs)
class Output(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('output')
        self.setAttributes(attrs,sattrs)
class P(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('p')
        self.setAttributes(attrs,sattrs)
class Picture(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('picture')
        self.setAttributes(attrs,sattrs)
class Pre(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('pre')
        self.setAttributes(attrs,sattrs)
class Progress(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('progress')
        self.setAttributes(attrs,sattrs)
class Q(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('q')
        self.setAttributes(attrs,sattrs)
class Rp(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('rp')
        self.setAttributes(attrs,sattrs)
class Rt(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('rt')
        self.setAttributes(attrs,sattrs)
class Ruby(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('ruby')
        self.setAttributes(attrs,sattrs)
class S(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('s')
        self.setAttributes(attrs,sattrs)
class Samp(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('samp')
        self.setAttributes(attrs,sattrs)
class Script(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('script')
        self.setAttributes(attrs,sattrs)
        self.rawlines=[]
    def addLines(self,*lines):
        self.rawlines.extend(lines)
    def addVar(self,varname,value):
        if type(value)==str:
            self.rawlines.append(f"let {varname}='{value}'")
        elif type(value) in (int,float):
            self.rawlines.append(f"let {varname}={value}")
        else:
            self.rawlines.append(f"let {varname}={json.dumps(value)}")
    def addJsFile(self,filepath):
        with open(filepath,'r',encoding='utf8') as fl:
            self.rawlines.append(fl.read())
    def str(self):
        pre=[]
        pre.append('<script')
        if self.attrs:
            for k,v in self.attrs.items():
                pre.append(' ')
                pre.append(k)
                pre.append('=')
                pre.append('"')
                pre.append(str(v))
                pre.append('"')
        pre.append('>')
        for line in self.rawlines:
            pre.append(line)
            pre.append('\n')
        pre.append('</script>')
        return ''.join(pre)
class Search(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('search')
        self.setAttributes(attrs,sattrs)
class Section(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('section')
        self.setAttributes(attrs,sattrs)
class Select(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('select')
        self.setAttributes(attrs,sattrs)
class Small(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('small')
        self.setAttributes(attrs,sattrs)
class Span(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('span')
        self.setAttributes(attrs,sattrs)
class Strong(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('strong')
        self.setAttributes(attrs,sattrs)
class Style(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('style')
        self.setAttributes(attrs,sattrs)
        self.css={}
        self.cssFiles=[]
    def addCss(self,selector,cssDict):
        self.css[selector]=cssDict
    def addCssFile(self,filepath):
        with open(filepath,'r') as fl:
            css=fl.read()
            self.cssFiles.append(css)
    def str(self):
        pre=[]
        pre.append('<style>')
        for selector,cssDict in self.css.items():
            pre.append(selector)
            pre.append('{')
            for k,v in cssDict.items():
                pre.append(k)
                pre.append(':')
                pre.append(str(v))
                pre.append(';')
            pre.append('}')
        for css in self.cssFiles:
            pre.append(css)
        pre.append('</style>')
        return ''.join(pre)
class Sub(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('Sub')
        self.setAttributes(attrs,sattrs)
class Summary(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('summary')
        self.setAttributes(attrs,sattrs)
class Sup(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('sup')
        self.setAttributes(attrs,sattrs)
class Svg(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('svg')
        self.setAttributes(attrs,sattrs)
class Table(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('table')
        self.setAttributes(attrs,sattrs)
class Tbody(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('tbody')
        self.setAttributes(attrs,sattrs)
class Td(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('td')
        self.setAttributes(attrs,sattrs)
class Template(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('template')
        self.setAttributes(attrs,sattrs)
class Textarea(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('textarea')
        self.setAttributes(attrs,sattrs)
class Tfoot(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('tfoot')
        self.setAttributes(attrs,sattrs)
class Th(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('th')
        self.setAttributes(attrs,sattrs)
class Thead(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('thead')
        self.setAttributes(attrs,sattrs)
class Time(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('time')
        self.setAttributes(attrs,sattrs)
class Title(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('title')
        self.setAttributes(attrs,sattrs)
class Tr(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('tr')
        self.setAttributes(attrs,sattrs)
class U(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('u')
        self.setAttributes(attrs,sattrs)
class Ul(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('ul')
        self.setAttributes(attrs,sattrs)
class Var(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('var')
        self.setAttributes(attrs,sattrs)
class Video(Tag):
    def __init__(self,attrs=None,sattrs=None):
        super().__init__('video')
        self.setAttributes(attrs,sattrs)
class HtmlDoc:
    def __init__(self):
        self.doctype=Doctype()
        self.html=self.doctype.appendChild(Html())
        self.head=self.html.appendChild(Head())
        js=self.head.Script()
        js.addLines(
            "window.print=console.log",
            "document.addEventListener('mousedown',(ev)=>{window.MOUSEDOWN=true})",
            "document.addEventListener('mouseup',(ev)=>{window.MOUSEDOWN=false})",
        )
        js.addJsFile('./basic_funcs.js')
        css=self.head.Style()
        css.addCssFile('./css.css')
        self.body=self.html.appendChild(Body())
    def str(self):
        return self.doctype.str()
if __name__=='__main__':
    print(P({'text':'asdf'}).str())
    print(P().str())
    print(HtmlDoc().str())
    pass