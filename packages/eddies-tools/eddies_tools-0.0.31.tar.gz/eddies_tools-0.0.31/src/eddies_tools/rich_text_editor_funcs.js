window.RichTextEditor={
    toggleTablePanel:function(ev,idx){
        let panel=ev.target.nextSibling
        if(panel.style.display=='none'){
            panel.style.display='flex'
            panel.style.top=ev.pageY+10+'px'
            panel.style.left=ev.pageX+10+'px'
        }else{
            panel.style.display='none'
        }
    },
    saveState:function(idx){
        RichTextEditor.SAVES=RichTextEditor.SAVES||{}
        RichTextEditor.SAVES[idx]=RichTextEditor.SAVES[idx]||[]
        RichTextEditor.CURRENTSTATEIDX=RichTextEditor.CURRENTSTATEIDX||{}
        RichTextEditor.CURRENTSTATEIDX[idx]=RichTextEditor.CURRENTSTATEIDX[idx]||0
        let ctnt=document.getElementById(idx).querySelector('.rchtxtedtrcont').innerHTML
        RichTextEditor.SAVES[idx]=RichTextEditor.SAVES[idx].slice(0,RichTextEditor.CURRENTSTATEIDX[idx])
        RichTextEditor.SAVES[idx].push(ctnt)
        RichTextEditor.CURRENTSTATEIDX[idx]=RichTextEditor.SAVES[idx].length
    },
    loadState:function(idx,increment){
        let stateIdx=RichTextEditor.CURRENTSTATEIDX[idx]=RichTextEditor.CURRENTSTATEIDX[idx]+increment
        if(RichTextEditor.SAVES[idx][stateIdx]){
            let rte=document.getElementById(idx).querySelector('.rchtxtedtrcont')
            rte.innerHTML=RichTextEditor.SAVES[idx][stateIdx]
        }
    },
    keydown:function(ev,idx){
        if(ev.ctrlKey){
            let k=ev.key.toUpperCase()
            let rte=document.getElementById(idx).querySelector('.rchtxtedtrcont')
            if(k=='Y'||(ev.shiftKey&&k=='Z')){
                RichTextEditor.loadState(idx,1)
            }else if(k=='Z'){
                RichTextEditor.loadState(idx,-1)
            }else if(k=='C'){
                let tds=Array.from(rte.querySelectorAll('.rchtxtedtrtdbx'))
                if(tds.length==0){return}
                let tr=tds[0].parentElement
                let lss=[],ls=[]
                for(let td of tds){
                    if(td.parentElement!=tr){
                        tr=td.parentElement
                        lss.push(ls.join('\t'))
                        ls=[]
                    }
                    ls.push(td.innerText)
                }
                lss.push(ls.join('\t'))
                let s=lss.join('\r\n')
                navigator.clipboard.writeText(s)
            }else if(k=='V'){
            }
        }
    },
    onpaste:function(ev,idx){
        let rte=document.getElementById(idx).querySelector('.rchtxtedtrcont')
        let tds=Array.from(rte.querySelectorAll('.rchtxtedtrtdbx'))
        if(tds.length==0){return}
        ev.stopPropagation()
        ev.preventDefault()
        let paste=ev.clipboardData
        let text=paste.getData('Text').split('\n').map(r=>r.trim().split('\t'))
        let td=tds[0]
        let tr=td.parentElement
        let tbody=tr.parentElement
        let trs=tbody.children
        let jx=indexOf(Array.from(tr.children),td)
        let ix=indexOf(Array.from(trs),tr)
        for(let i=0;i<text.length;i++){
            let tr=trs[i+ix]
            if(!tr){continue}
            let tds=tr.children
            for(let j=0;j<text[i].length;j++){
                let td=tds[j+jx]
                if(!td){continue}
                td.innerText=text[i][j]
            }
        }
    },
    splitRangeStart:function(range,tagName) {
        let node=range.startContainer
        let span1=document.createElement('span')
        let text=node.splitText(range.startOffset)
        span1.appendChild(node)
        let span2=document.createElement(tagName)
        span2.appendChild(text)
        range.insertNode(span2)
        range.insertNode(span1)
        return [span1,span2]
    },
    splitRangeEnd:function(range,tagName){
        let node=range.endContainer
        let div=node.parentElement
        let span1=document.createElement(tagName)
        let text=node.splitText(range.endOffset)
        span1.appendChild(node)
        let span2=document.createElement('span')
        span2.appendChild(text)
        div.appendChild(span1)
        div.appendChild(span2)
        return [span1,span2]
    },
    getSelectionAsSpan:function(tagName='span'){
        let sel=window.getSelection()
        let range1=sel.getRangeAt(0)
        let range2=range1.cloneRange()
        let span1,span2
        [span1,span2]=RichTextEditor.splitRangeStart(range1,tagName)
        let span3,span4
        [span3,span4]=RichTextEditor.splitRangeEnd(range2,tagName)
        let spans=[]
        let done=[]
        let func=(node)=>{
            if(node==span3){return node}
            for(let node2 of Array.from(node.children)){
                if(indexOf(done,node2)>-1){continue}
                let node3=func(node2)
                if(node3==span3){return node3}
            }
            spans.push(node)
            if(indexOf(done,node)>-1){
                return
            }
            done.push(node)
            if(node.nextSibling){
                func(node.nextSibling)
            }else if(node.parentElement.nextSibling){
                func(node.parentElement.nextSibling)
            }
        }
        func(span2)
        if(tagName!='span'){
            for(let span of spans){
                span.innerHTML='<'+tagName+'>'+span.innerHTML+'</'+tagName+'>'
            }
        }
        let finalRange=document.createRange()
        finalRange.setStart(span2,0)
        finalRange.collapse(true)
        sel=window.getSelection()
        sel.removeAllRanges()
        sel.addRange(finalRange)
        return [span2,...spans,span3]
    },
    makeBold:function(ev,idx){
        RichTextEditor.saveState(idx)
        let spans=RichTextEditor.getSelectionAsSpan()
        for(let span of spans){
            span.style.fontWeight='bold'
        }
    },
    makeItalic:function(ev,idx){
        RichTextEditor.saveState(idx)
        let spans=RichTextEditor.getSelectionAsSpan()
        for(let span of spans){
            span.style.fontStyle='italic'
        }
    },
    makeUnderlined:function(ev,idx){
        RichTextEditor.saveState(idx)
        let spans=RichTextEditor.getSelectionAsSpan()
        for(let span of spans){
            if(span.style.textDecoration){
                span.style.textDecoration+=' underline'
            }else{
                span.style.textDecoration='underline'
            }
        }
    },
    makeLineThrough:function(ev,idx){
        RichTextEditor.saveState(idx)
        spans=RichTextEditor.getSelectionAsSpan()
        for(let span of spans){
            if(span.style.textDecoration){
                span.style.textDecoration+=' line-through'
            }else{
                span.style.textDecoration='line-through'
            }
        }
    },
    makeSuperscript:function(ev,idx){
        RichTextEditor.saveState(idx)
        span=RichTextEditor.getSelectionAsSpan('sup')
    },
    makeSubscript:function(ev,idx){
        RichTextEditor.saveState(idx)
        span=RichTextEditor.getSelectionAsSpan('sub')
    },
    changeFgColor:function(ev,idx){
        RichTextEditor.saveState(idx)
        let spans=RichTextEditor.getSelectionAsSpan()
        for(let span of spans){
            span.style.color=ev.target.value
        }
    },
    changeBgColor:function(ev,idx){
        RichTextEditor.saveState(idx)
        let spans=RichTextEditor.getSelectionAsSpan()
        for(let span of spans){
            span.style.backgroundColor=ev.target.value
        }
    },
    addTable:function(ev,idx){
        RichTextEditor.saveState(idx)
        let row=ev.target.parentElement
        let inps=Array.from(row.querySelectorAll('input'))
        let numCols=Number(inps[0].value||inps[0].placeholder)
        let numRows=Number(inps[1].value||inps[1].placeholder)
        let range=window.getSelection().getRangeAt(0)
        let table=document.createElement('table')
        range.insertNode(table)
        let tbody=document.createElement('tbody')
        table.appendChild(tbody)
        for(let i=0;i<numRows;i++){
            let tr=document.createElement('tr')
            tbody.appendChild(tr)
            for(let j=0;j<numCols;j++){
                let td=document.createElement('td')
                tr.appendChild(td)
            }
        }
        row.style.display='none'
        table.addEventListener('mousedown',
            (ev)=>RichTextEditor.onmousedownTable(ev,idx))
    },
    deleteTable:function(ev,idx){
        let range=window.getSelection().getRangeAt(0)
        if(!range.startContainer.closest){
            td=range.startContainer.parentElement.closest('td')
        }else{
            td=range.startContainer.closest('td')
        }
        let table=td.closest('table')
        table.remove()
    },
    addColumn:function(ev,idx,after){
        RichTextEditor.saveState(idx)
        let range=window.getSelection().getRangeAt(0)
        if(!range.startContainer.closest){
            td=range.startContainer.parentElement.closest('td')
        }else{
            td=range.startContainer.closest('td')
        }
        let tr=td.parentElement
        let jx=indexOf(Array.from(tr.children),td)
        let tbody=tr.parentElement
        let trs=tbody.children
        for(let tr of Array.from(trs)){
            let td=document.createElement('td')
            if(after){
                tr.children[jx].after(td)
            }else{
                tr.children[jx].before(td)
            }
        }
    },
    addRow:function(ev,idx,after){
        RichTextEditor.saveState(idx)
        let range=window.getSelection().getRangeAt(0)
        if(!range.startContainer.closest){
            td=range.startContainer.parentElement.closest('td')
        }else{
            td=range.startContainer.closest('td')
        }
        let tr=td.parentElement
        let newTr=document.createElement('tr')
        if(after){
            tr.after(newTr)
        }else{
            tr.before(newTr)
        }
        for(let j=0;j<tr.children.length;j++){
            let td=document.createElement('td')
            newTr.appendChild(td)
        }
    },
    deleteColumn:function(ev,idx){
        RichTextEditor.saveState(idx)
        let range=window.getSelection().getRangeAt(0)
        if(!range.startContainer.closest){
            td=range.startContainer.parentElement.closest('td')
        }else{
            td=range.startContainer.closest('td')
        }
        let tr=td.parentElement
        let jx=indexOf(Array.from(tr.children),td)
        let tbody=tr.parentElement
        let trs=tbody.children
        for(let tr of Array.from(trs)){
            tr.children[jx].remove()
        }
    },
    deleteRow:function(ev,idx){
        RichTextEditor.saveState(idx)
        let range=window.getSelection().getRangeAt(0)
        if(!range.startContainer.closest){
            td=range.startContainer.parentElement.closest('td')
        }else{
            td=range.startContainer.closest('td')
        }
        let tr=td.parentElement
        tr.remove()
    },
    onmouseupTable:function(ev){
        document.removeEventListener('mouseup',RichTextEditor.onmouseupTable)
        document.removeEventListener('mousemove',RichTextEditor.onmousemoveTable)
        let startTd=RichTextEditor.CURMOUSEDOWNTD
        let endTd=ev.target
        if(endTd.closest){
            endTd=endTd.closest('td')
        }else{
            endTd=endTd.parentElement.closest('td')
        }
        if(startTd==endTd){
            let tbody=startTd.closest('tbody')
            let tds=Array.from(tbody.querySelectorAll('td'))
            for(let td of tds){
                removeClass(td,'rchtxtedtrtdbxlft')
                removeClass(td,'rchtxtedtrtdbxrght')
                removeClass(td,'rchtxtedtrtdbxtop')
                removeClass(td,'rchtxtedtrtdbxbot')
                removeClass(td,'rchtxtedtrtdbx')
            }
            addClass(startTd,'rchtxtedtrtdbxlft')
            addClass(startTd,'rchtxtedtrtdbxrght')
            addClass(startTd,'rchtxtedtrtdbxtop')
            addClass(startTd,'rchtxtedtrtdbxbot')        
            addClass(startTd,'rchtxtedtrtdbx')        
        }
    },
    onmousemoveTable:function(ev){
        let startTd=RichTextEditor.CURMOUSEDOWNTD
        let endTd=ev.target
        if(endTd.closest){
            endTd=endTd.closest('td')
        }else{
            endTd=endTd.parentElement.closest('td')
        }
        let startTr=startTd.parentElement
        let endTr=endTd.parentElement
        let tbody=startTr.parentElement
        let jx1=indexOf(Array.from(startTr.children),startTd)
        let jx2=indexOf(Array.from(endTr.children),endTd)
        let ix1=indexOf(Array.from(tbody.children),startTr)
        let ix2=indexOf(Array.from(tbody.children),endTr)
        if(jx2<jx1){
            let j=jx1
            jx1=jx2
            jx2=j
        }
        if(ix2<ix1){
            let i=ix1
            ix1=ix2
            ix2=i
        }
        let trs=tbody.children
        let tds=Array.from(tbody.querySelectorAll('td'))
        for(let td of tds){
            removeClass(td,'rchtxtedtrtdbxlft')
            removeClass(td,'rchtxtedtrtdbxrght')
            removeClass(td,'rchtxtedtrtdbxtop')
            removeClass(td,'rchtxtedtrtdbxbot')
            removeClass(td,'rchtxtedtrtdbxbx')
        }
        for(let i=ix1;i<=ix2;i++){
            let tr=trs[i]
            let tds=tr.children
            for(let j=jx1;j<=jx2;j++){
                let td=tds[j]
                if(i==ix1){
                    addClass(td,'rchtxtedtrtdbxtop')
                }
                if(i==ix2){
                    addClass(td,'rchtxtedtrtdbxbot')
                }
                if(j==jx1){
                    addClass(td,'rchtxtedtrtdbxlft')
                }
                if(j==jx2){
                    addClass(td,'rchtxtedtrtdbxrght')
                }
                addClass(td,'rchtxtedtrtdbx')
            }
        }
    },
    onmousedownTable:function(ev,idx){
        if(ev.target.closest){
            RichTextEditor.CURMOUSEDOWNTD=ev.target.closest('td')
        }else{
            RichTextEditor.CURMOUSEDOWNTD=ev.target.parentElement.closest('td')   
        }
        if(RichTextEditor.CURMOUSEDOWNTD){
            document.addEventListener('mouseup',RichTextEditor.onmouseupTable)
            document.addEventListener('mousemove',RichTextEditor.onmousemoveTable)
        }else{
            let cont
            if(ev.target.closest){
                cont=ev.target.closest('.rchtxtedtrcont')
            }else{
                cont=ev.target.parentElement.closest('.rchtxtedtrcont')
            }
            let tbodies=Array.from(cont.querySelectorAll('tbody'))
            for(let tbody of tbodies){
                let tds=Array.from(tbody.querySelectorAll('td'))
                for(let td of tds){
                    removeClass(td,'rchtxtedtrtdbxlft')
                    removeClass(td,'rchtxtedtrtdbxrght')
                    removeClass(td,'rchtxtedtrtdbxtop')
                    removeClass(td,'rchtxtedtrtdbxbot')      
                    removeClass(td,'rchtxtedtrtdbx')      
                }
            }
        }
    },
}
