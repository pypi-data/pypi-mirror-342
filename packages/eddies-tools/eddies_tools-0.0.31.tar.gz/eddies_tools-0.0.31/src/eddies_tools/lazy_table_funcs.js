window.LAZYTABLE={
    setMeta:function(idx,options){
        if(!window.LAZYTABLEMETA){window.LAZYTABLEMETA={}}
        window.LAZYTABLEMETA[idx]=options
        options.checkedRows=new Set()
        let parent=document.getElementById(idx).parentElement
        let resizeObserver=new ResizeObserver(entrires=>{
            LAZYTABLE.resize(idx)
            LAZYTABLE.populate(idx)
        })
        resizeObserver.observe(parent)
    },
    getMeta:function(idx){
        return window.LAZYTABLEMETA[idx]
    },
    resize:function(idx){
        let table=document.getElementById(idx)
        let parent=table.parentElement
        let prect=parent.getBoundingClientRect()
        let trect=table.getBoundingClientRect()
        let td=table.querySelector('.lztbltd')
        let tdrect=td.getBoundingClientRect()
        let tdht=tdrect.height
        let pht=prect.height
        let tht=trect.height
        let cols=Array.from(table.querySelectorAll('.lztblcol'))
        while(pht-tht>tdht){
            for(let col of cols){
                let td=col.children[0]
                td2=td.cloneNode(true)
                col.appendChild(td2)
            }
            let trect=table.getBoundingClientRect()
            tht=trect.height
        }
        while(tht>pht){
            if(cols[0].children.length==1){
                break
            }
            for(let col of cols){
                col.lastChild.remove()
            }
            prect=parent.getBoundingClientRect()
            trect=table.getBoundingClientRect()
            pht=prect.height
            tht=trect.height
        }
    },
    setData:function(idx,data){
        let meta=LAZYTABLE.getMeta(idx)
        meta.origRows=data
        meta.shownRows=meta.origRows
        LAZYTABLE.adjustYThumb(idx)
    },
    adjustYThumb:function(idx){
        let meta=LAZYTABLE.getMeta(idx)
        let table=document.getElementById(idx)
        let cols=Array.from(table.querySelectorAll('.lztbltdcol'))
        let numRows=cols[0].children.length
        let track=table.querySelector('.lztblytrk')
        let thumb=table.querySelector('.lztblythmb')
        let fraction=numRows/meta.shownRows.length
        let trackRect=track.getBoundingClientRect()
        let thumbHeight=trackRect.height*fraction
        if(thumbHeight<0){
            thumb.style.display='none'
        }else{
            thumb.style.display='flex'
            if(thumbHeight<20){thumbHeight=20}
            thumb.style.height=thumbHeight+'px'
        }
    },
    filter:function(ev,idx){
        if(ev.key!='Enter'){return}
        let input=ev.target
        let searchKeys=input.value.toLowerCase().trim().split(',').map(s=>s.trim())
        let th=input.closest('.lztblth')
        let col=th.closest('.lztbltdcoloutout')
        let cols=Array.from(col.parentElement.children)
        let jx=indexOf(cols,col)
        let meta=LAZYTABLE.getMeta(idx)
        if(meta.radios||meta.checks){
            jx-=1
        }
        let rows=meta.origRows
        let newRows=[]
        for(let row of rows){
            let text=row[jx].toString().toLowerCase()
            let bool=false
            for(let sk of searchKeys){
                if(text.indexOf(sk)>-1){
                    bool=true
                    break
                }
            }
            if(bool){
                newRows.push(row)
            }
        }
        meta.shownRows=newRows
        LAZYTABLE.adjustYThumb(idx)
        meta.boxj1=undefined
        meta.boxj2=undefined
        meta.boxi1=undefined
        meta.boxi2=undefined
    },
    sort:function(ev,idx){
        let p=ev.target
        let asc=entityForSymbol(p.innerHTML)=='▼'
        let th=p.closest('.lztblth')
        let col=th.closest('.lztbltdcoloutout')
        let cols=Array.from(col.parentElement.children)
        let jx=indexOf(cols,col)
        let meta=LAZYTABLE.getMeta(idx)
        let rows=meta.shownRows
        if(asc){
            p.innerHTML='▲'
            if(typeof(rows[0][jx])=='number'){
                rows=rows.sort((a,b)=>a[jx]-b[jx])
            }else{
                rows=rows.sort((a,b)=>a[jx].localeCompare(b[jx]))
            }
        }else{
            p.innerHTML='▼'
            if(typeof(rows[0][jx])=='number'){
                rows=rows.sort((a,b)=>b[jx]-a[jx])
            }else{
                rows=rows.sort((a,b)=>b[jx].localeCompare(a[jx]))
            }
        }
        meta.shownRows=rows
        meta.boxj1=undefined
        meta.boxj2=undefined
        meta.boxi1=undefined
        meta.boxi2=undefined
    },
    populate:function(idx){
        let meta=LAZYTABLE.getMeta(idx)
        let table=document.getElementById(idx)
        let cols=Array.from(table.querySelectorAll('.lztbltdcol'))
        if(!meta.shownRows){return}
        let numAllRows=meta.shownRows.length
        let numRows=cols[0].children.length
        let track=table.querySelector('.lztblytrk')
        let thumb=table.querySelector('.lztblythmb')
        let trackRect=track.getBoundingClientRect()
        let thumbRect=thumb.getBoundingClientRect()
        let thumbHeight=thumbRect.height
        let trackHeight=trackRect.height
        let thumbTop=Number(thumb.style.top.replace('px',''))
        let firstRow=Math.round((numAllRows-numRows)*thumbTop/(trackHeight-thumbHeight))
        meta.firstRow=firstRow
        for(let i=0;i<numRows;i++){
            let row=meta.shownRows[i+firstRow]
            if(!row){
                for(let j=0;j<cols.length;j++){
                    cols[j].children[i].innerText=''
                }
            }else{
                for(let j=0;j<cols.length;j++){
                    cols[j].children[i].innerText=row[j]
                }
            }
        }
        let inpCol=table.querySelector('.lztblinpcolinr')
        if(inpCol){
            let inps=Array.from(inpCol.children)
            for(let i=0;i<numRows;i++){
                let inp=inps[i].children[0]
                inp.val=i+firstRow
                if(meta.checkedRows.has(i+firstRow)){
                    inp.checked=true
                }else{
                    inp.checked=false
                }
            }
        }
        document.getElementById('ttl'+idx).innerText=numAllRows
        document.getElementById('rgstrt'+idx).innerText=firstRow+1
        document.getElementById('rgend'+idx).innerText=firstRow+numRows
        document.getElementById('chkd'+idx).innerText=meta.checkedRows.size
        LAZYTABLE.addBoxLines(idx)
    },
    onmouseupThumb:function(ev){
        document.removeEventListener('mouseup',LAZYTABLE.onmouseupThumb)
        document.removeEventListener('mousemove',LAZYTABLE.onmousemoveThumb)
    },
    onmousemoveThumb:function(ev){
        let thumb=window.CURLAZYTABLETHUMB
        let track=thumb.parentElement
        let thumbRect=thumb.getBoundingClientRect()
        let trackRect=track.getBoundingClientRect()
        let delta=ev.pageY-window.CURMOUSEDOWNY
        let top=Number(thumb.style.top.replace('px',''))
        let newTop=top+delta
        if(newTop<0){newTop=0}
        let ul=trackRect.height-thumbRect.height
        if(newTop>ul)[newTop=ul]
        window.CURMOUSEDOWNY=ev.pageY
        thumb.style.top=newTop+'px'
        let table=track.closest('.lztbl')
        let tidx=table.id
        LAZYTABLE.populate(tidx)
    },
    onmousedownThumb:function(ev,idx){
        document.addEventListener('mouseup',LAZYTABLE.onmouseupThumb)
        document.addEventListener('mousemove',LAZYTABLE.onmousemoveThumb)
        window.CURLAZYTABLETHUMB=ev.target
        window.CURMOUSEDOWNY=ev.target.pageY
    },
    onwheel:function(ev,idx){
        ev.stopPropagation()
        ev.preventDefault()
        let table=document.getElementById(idx)
        let track=table.querySelector('.lztblytrk')
        let thumb=table.querySelector('.lztblythmb')
        let trackRect=track.getBoundingClientRect()
        let thumbRect=thumb.getBoundingClientRect()
        let thumbHeight=thumbRect.height
        let trackHeight=trackRect.height
        let dir=ev.deltaY
        let meta=LAZYTABLE.getMeta(idx)
        let cols=Array.from(table.querySelectorAll('.lztbltdcol'))
        let numAllRows=meta.shownRows.length
        let numRows=cols[0].children.length
        let numScrollRows=numAllRows-numRows
        let movableHeight=trackHeight-thumbHeight
        if(thumb.style.display=='none'){
            movableHeight=0
        }
        let unitHeight=movableHeight/numScrollRows
        let thumbTop=Number(thumb.style.top.replace('px',''))
        let newTop
        if(dir>0){
            newTop=thumbTop+unitHeight
        }else{
            newTop=thumbTop-unitHeight
        }
        if(newTop<0){newTop=0}
        if(newTop>movableHeight){newTop=movableHeight}
        thumb.style.top=newTop+'px'
    },
    onclickinput:function(ev,idx){
        let inp=ev.target
        let meta=LAZYTABLE.getMeta(idx)
        if(meta.checks){
            if(inp.checked){
                meta.checkedRows.add(inp.val)
                if(ev.shiftKey&&meta.lastChecked!==undefined){
                    let ix1=Math.min(meta.lastChecked,inp.val)
                    let ix2=Math.max(meta.lastChecked,inp.val)
                    for(let i=ix1;i<=ix2;i++){
                        meta.checkedRows.add(i)
                    }
                    let inps=Array.from(inp.closest('.lztblinpcol').querySelectorAll('input[type=checkbox]'))
                    for(let inp of inps){
                        if(meta.checkedRows.has(inp.val)){
                            inp.checked=true
                        }
                    }
                }
                meta.lastChecked=inp.val
            }else{
                meta.checkedRows.delete(inp.val)
            }
        }else{
            if(inp.checked){
                meta.checkedRows=new Set()
                meta.checkedRows.add(inp.val)
            }
        }
    },
    selectAll:function(idx){
        let meta=LAZYTABLE.getMeta(idx)
        let shownRows=meta.shownRows
        if(meta.checkedRows.size==0){
            for(let i in shownRows){
                meta.checkedRows.add(Number(i))
            }
        }else{
            meta.checkedRows=new Set()
        }
    },
    mouseupCheckbox:function(ev){
        document.removeEventListener('mouseup',LAZYTABLE.mouseupCheckbox)
        document.removeEventListener('mousemove',LAZYTABLE.mousemoveCheckbox)
    },
    mousemoveCheckbox:function(ev){
        let target=ev.target
        let td=target.closest('.lztbltd')
        if(!td){return}
        let ix=indexOf(td.parentElement.children,td)
        let table=td.closest('.lztbl')
        let col=table.querySelector('.lztblinpcolinr')
        let inp=col.children[ix].querySelector('input')
        inp.checked=window.CURLAZYTABLECHECKBOXSTATE
        let meta=LAZYTABLE.getMeta(table.id)
        if(window.CURLAZYTABLECHECKBOXSTATE){
            meta.checkedRows.add(inp.val)
        }else{
            meta.checkedRows.delete(inp.val)
        }
    },
    mousedownCheckbox:function(ev,idx){
        document.addEventListener('mouseup',LAZYTABLE.mouseupCheckbox)
        document.addEventListener('mousemove',LAZYTABLE.mousemoveCheckbox)
        window.CURLAZYTABLECHECKBOXSTATE=!ev.target.checked
        window.CURLAZYTABLECHECKBOX=ev.target
    },
    mouseupBody:function(ev){
        document.removeEventListener('mouseup',LAZYTABLE.mouseupBody)
        document.removeEventListener('mousemove',LAZYTABLE.mousemoveBody)
    },
    getMouseDownIxJx(ev){
        let target=ev.target
        let td=target.closest('.lztbltd')
        let table=td.closest('.lztbl')
        let col=td.parentElement
        let ix=indexOf(col.children,td)
        let meta=LAZYTABLE.getMeta(table.id)
        let firstRow=meta.firstRow
        ix+=firstRow
        let cols=Array.from(table.querySelectorAll('.lztbltdcol'))
        let jx=indexOf(cols,col)
        return [ix,jx]
    },
    getMinMaxIxJx(idx,ix,jx){
        let meta=LAZYTABLE.getMeta(idx)
        if(ix<meta.boxi1){
            meta.boxi2=meta.boxi1
            meta.boxi1=ix
        }else{
            meta.boxi2=ix
        }
        if(jx<meta.boxj1){
            meta.boxj2=meta.boxj1
            meta.boxj1=jx
        }else{
            meta.boxj2=jx
        }
    },
    mousemoveBody:function(ev){
        let table=ev.target.closest('.lztbl')
        if(!table){return}
        if(!hasClass(ev.target,'lztbltd')){return}
        let ix,jx
        [ix,jx]=LAZYTABLE.getMouseDownIxJx(ev)
        let idx=table.id
        LAZYTABLE.getMinMaxIxJx(idx,ix,jx)
        LAZYTABLE.addBoxLines(idx)
    },
    mousedownBody:function(ev,idx){
        let table=ev.target.closest('.lztbl')
        if(!table){return}
        if(!hasClass(ev.target,'lztbltd')){return}
        document.addEventListener('mouseup',LAZYTABLE.mouseupBody)
        document.addEventListener('mousemove',LAZYTABLE.mousemoveBody)
        let meta=LAZYTABLE.getMeta(idx)
        let ix,jx
        [ix,jx]=LAZYTABLE.getMouseDownIxJx(ev)
        if(ev.shiftKey||ev.ctrlKey){
            if(meta.boxi1===undefined){meta.boxi1=ix}
            if(meta.boxj1===undefined){meta.boxj1=jx}
            LAZYTABLE.getMinMaxIxJx(idx,ix,jx)
        }else{
            meta.boxi1=ix
            meta.boxj1=jx
            meta.boxi2=ix
            meta.boxj2=jx
        }
        LAZYTABLE.addBoxLines(idx)
        if(table.keydown){
            document.removeEventListener('keydown',table.keydown)
            delete table.keydown
        }
        document.addEventListener('keydown',LAZYTABLE.keydownBody)
        window.CURLAZYTABLE=table
    },
    mouseleaveBody:function(ev,idx){
        let table=document.getElementById(idx)
        if(table.keydown){
            document.removeEventListener('keydown',table.keydown)
            delete table.keydown
        }        
    },
    keydownBody:function(ev){
        if(ev.ctrlKey){
            let table=window.CURLAZYTABLE
            let idx=table.id
            let meta=LAZYTABLE.getMeta(idx)
            let shownRows=meta.shownRows
            if(ev.key.toUpperCase()=='C'){
                let ix1=meta.boxi1
                let ix2=meta.boxi2
                let jx1=meta.boxj1
                let jx2=meta.boxj2
                let firstRow=meta.firstRow
                let lss=[]
                for(let i=ix1;i<=ix2;i++){
                    let ls=[]
                    let row=shownRows[i]
                    for(let j=jx1;j<=jx2;j++){
                        ls.push(row[j])
                    }
                    lss.push(ls.join('\t'))
                }
                let s=lss.join('\r\n')
                navigator.clipboard.writeText(s)
            }
        }
    },
    addBoxLines:function(idx){
        let meta=LAZYTABLE.getMeta(idx)
        let table=document.getElementById(idx)
        let cols=Array.from(table.querySelectorAll('.lztbltdcol'))
        let firstRow=meta.firstRow
        let ix1=meta.boxi1
        let ix2=meta.boxi2
        let jx1=meta.boxj1
        let jx2=meta.boxj2
        for(let col of cols){
            let tds=Array.from(col.children)
            for(let td of tds){
                removeClass(td,'bxl')
                removeClass(td,'bxr')
                removeClass(td,'bxt')
                removeClass(td,'bxb')
            }
        }
        for(let j=jx1;j<=jx2;j++){
            let col=cols[j]
            let tds=Array.from(col.children)
            for(let i=0;i<tds.length;i++){
                let td=tds[i]
                let ix=i+firstRow
                if(ix==ix1){
                    addClass(td,'bxt')
                }
                if(ix==ix2){
                    addClass(td,'bxb')
                }
                if(ix1<=ix&&ix<=ix2){
                    if(j==jx1){
                        addClass(td,'bxl')
                    }
                    if(j==jx2){
                        addClass(td,'bxr')
                    }
                    if(jx1<=j&&j<=jx2){
                        if(j==jx1){
                            addClass(td,'bxl')
                        }
                        if(j==jx2){
                            addClass(td,'bxr')
                        }    
                    }
                }
            }
        }
    },
    makeEditable:function(ev,idx){
        let td=ev.target.closest('.lztbltd')
        td.contentEditable=true
        td.focus()
        let func=(ev)=>{
            let table=document.getElementById(idx)
            let col=td.closest('.lztbltdcol')
            let ix=indexOf(col.children,td)
            let cols=Array.from(table.querySelectorAll('.lztbltdcol'))
            let jx=indexOf(cols,col)
            let meta=LAZYTABLE.getMeta(idx)
            let firstRow=meta.firstRow
            let shownRows=meta.shownRows
            shownRows[ix+firstRow][jx]=td.innerHTML
            td.contentEditable=false
            td.removeEventListener('blur',func)}
        td.addEventListener('blur',func)
    },
    toggleOptionsPanel:function(ev,idx){
        let panel=ev.target.nextSibling
        if(panel.style.display=='none'){
            panel.style.display='flex'
            let rect=panel.getBoundingClientRect()
            panel.style.top=ev.pageY-10-rect.height+'px'
            panel.style.left=ev.pageX+10+'px'
        }else{
            panel.style.display='none'
        }
    },
    toggleColumnVisibility :function(ev,idx){
        let table=document.getElementById(idx)
        let cols=Array.from(table.querySelectorAll('.lztbltdcoloutout'))
        let meta=LAZYTABLE.getMeta(idx)
        let header=meta.headers
        let h=ev.target.parentElement.innerText
        let jx=indexOf(header,h)
        if(ev.target.checked){
            cols[jx].style.display='flex'
        }else{
            cols[jx].style.display='none'
        }
    }
}