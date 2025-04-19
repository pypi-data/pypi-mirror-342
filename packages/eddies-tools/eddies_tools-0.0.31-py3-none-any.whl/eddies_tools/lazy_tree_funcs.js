window.LAZYTREE={
    setMeta:function(idx,options){
        if(!window.LAZYTREEMETA){window.LAZYTREEMETA={}}
        let meta=window.LAZYTREEMETA[idx]=options
        meta.hiddenItems=new Set()
        meta.checkedItems=new Set()
        meta.checkedEndItems=new Set()
        meta.toggledItems=new Set()
        meta.setColors={}
        meta.boldItems=new Set()
        let parent=document.getElementById(idx).parentElement
        let resizeObserver=new ResizeObserver(entrires=>{
            // LAZYTREE.resize(idx)
            LAZYTREE.populate(idx)
        })
        resizeObserver.observe(parent)
    },
    getMeta:function(idx){
        return window.LAZYTREEMETA[idx]
    },
    setData:function(idx,data,init=true){
        let meta=LAZYTREE.getMeta(idx)
        if(init&&data){
            meta.origData=data
        }
        if(!data){
            data=meta.data
        }
        meta.data=data
        let dataDict={}
        let headers=meta.headers
        if(meta.shownHeaders){
            headers=meta.shownHeaders
        }
        let cnt=0
        for(let d of data){
            let dd=dataDict
            for(let j in headers){
                let h=headers[j]
                hv=d[h]
                if(j==headers.length-1){
                    dd[hv]=true
                    cnt+=1
                }else{
                    if(!dd[hv]){
                        dd[hv]={}
                        cnt+=1
                    }
                    dd=dd[hv]
                }
            }
        }
        meta.dataDict=dataDict
        meta.itemCount=cnt
    },
    populate:function(idx){
        let meta=LAZYTREE.getMeta(idx)
        if(meta.isRendering){return}
        meta.isRendering=true
        let track=tree.querySelector('.lztreytrk')
        let thumb=tree.querySelector('.lztreythmb')
        let trackRect=track.getBoundingClientRect()
        let trackHeight=trackRect.height
        let thumbRect=thumb.getBoundingClientRect()
        let thumbHeight=thumbRect.height
        let thumbTop=Number(thumb.style.top.replace('px',''))
        let numItems=meta.itemCount
        let numShownItems=meta.numShownItems
        let firstRow
        if(!numShownItems||trackHeight==thumbHeight){
            firstRow=0
        }else{
            firstRow=(numItems-numShownItems)*thumbTop/(trackHeight-thumbHeight)
            firstRow=Math.round(firstRow)
        }
        let dataDict=meta.dataDict
        let hidden=meta.hiddenItems
        let cont=document.getElementById(idx).querySelector('.lztrebodycol')
        while(cont.firstChild){cont.firstChild.remove()}
        let rect=cont.getBoundingClientRect()
        let cnt=0
        let cnt2=0
        let checked=meta.checkedItems
        let addColors=meta.colorSelectors
        let boldITems=meta.boldItems
        function createNode(parent,dd,keyChain){
            for(let hv in dd){
                let nodes=Array.from(cont.querySelectorAll('.lztrend'))
                let lastNode=nodes[nodes.length-1]
                if(lastNode){
                    let lcrect=lastNode.getBoundingClientRect()
                    if(lcrect.top+lcrect.height*2>rect.top+rect.height){return}
                }
                let kc=[...keyChain,hv]
                let kc2=kc.join('|')
                if(!hidden.has(kc2)){
                    if(cnt2>=firstRow){
                        let row=document.createElement('div')
                        row.className='lztrend _row_'
                        row.value=kc2
                        parent.appendChild(row)
                        if(typeof(dd[hv])!='boolean'){
                            let toggle=document.createElement('p')
                            if(meta.toggledItems.has(kc2)){
                                toggle.innerHTML='▶'
                            }else{
                                toggle.innerHTML='▼'
                            }
                            toggle.className='lztrendtgl'
                            row.appendChild(toggle)
                            toggle.onclick=(ev)=>LAZYTREE.toggleItem(ev,idx)
                        }
                        let check=document.createElement('input')
                        check.type='checkbox'
                        check.className='lztrendchk'
                        if(checked.has(kc2)){
                            check.checked=true
                        }
                        check.onchange=(ev)=>LAZYTREE.checkItem(ev,idx)
                        row.appendChild(check)
                        if(addColors){
                            let box=document.createElement('input')
                            box.className='lztreclrbx'
                            box.type='color'
                            if(meta.setColors[kc2]){
                                box.value=meta.setColors[kc2]
                            }else{
                                box.value='#0000FF'
                            }
                            row.appendChild(box)
                            box.onchange=(ev)=>LAZYTREE.setColor(ev,idx)
                        }
                        let nd=document.createElement('div')
                        nd.className='lztrendtext _col_'
                        nd.innerHTML=hv
                        if(boldITems.has(kc2)){
                            addClass(nd,'lztrebldtxt')
                        }
                        nd.onclick=(ev)=>LAZYTREE.toggleBold(ev,idx)
                        row.appendChild(nd)
                        cnt+=1
                    }
                    cnt2+=1
                    let ndchcont=document.createElement('div')
                    ndchcont.className='lztrendchcont _col_'
                    parent.appendChild(ndchcont)
                    if(typeof(dd[hv])!='boolean'){
                        createNode(ndchcont,dd[hv],kc)
                    }
                }
            }
        }
        createNode(cont,dataDict,[])
        meta.numShownItems=cnt
        LAZYTREE.adjustYThumb(idx)
        meta.isRendering=false
        document.getElementById('lztrechkd'+idx).innerText=meta.checkedEndItems.size
    },
    toggleBold:function(ev,idx){
        let nd=ev.target.closest('.lztrend')
        let meta=LAZYTREE.getMeta(idx)
        if(meta.boldItems.has(nd.value)){
            meta.boldItems.delete(nd.value)
            removeClass(ev.target,'lztrebldtxt')
        }else{
            addClass(ev.target,'lztrebldtxt')
            meta.boldItems.add(nd.value)
        }
    },
    setColor:function(ev,idx){
        let nd=ev.target.closest('.lztrend')
        let meta=LAZYTREE.getMeta(idx)
        meta.setColors[nd.value]=ev.target.value
    },
    toggleItem:function(ev,idx){
        let nd=ev.target.closest('.lztrend')
        let meta=LAZYTREE.getMeta(idx)
        let dataDict=meta.dataDict
        let keyChain=nd.value.split('|')
        let hidden=meta.hiddenItems
        let dd=dataDict
        for(let k of keyChain){
            dd=dd[k]
        }
        if(entityForSymbol(ev.target.innerHTML)=='▼'){
            meta.toggledItems.add(nd.value)
            ev.target.innerHTML='▶'
            function recurse(dd,kc){
                for(let k in dd){
                    let kc2=[...kc,k]
                    hidden.add(kc2.join('|'))
                    if(typeof(dd[k]=='object')){
                        recurse(dd[k])
                    }
                }
            }
            recurse(dd,keyChain)
        }else{
            meta.toggledItems.delete(nd.value)
            ev.target.innerHTML='▼'
            function recurse(dd,kc){
                for(let k in dd){
                    let kc2=[...kc,k]
                    hidden.delete(kc2.join('|'))
                    if(typeof(dd[k]=='object')){
                        recurse(dd[k])
                    }
                }
            }
            recurse(dd,keyChain)
        }
        LAZYTREE.populate(idx)
    },
    checkItem:function(ev,idx){
        let nd=ev.target.closest('.lztrend')
        let meta=LAZYTREE.getMeta(idx)
        let keyChain=nd.value.split('|')
        let dd=meta.dataDict
        for(let k of keyChain){
            dd=dd[k]
        }
        if(typeof(dd)=='boolean'){
            if(ev.target.checked){
                meta.checkedEndItems.add(nd.value)
            }else{
                meta.checkedEndItems.delete(nd.value)
            }
        }
        if(ev.target.checked){
            meta.checkedItems.add(nd.value)
            function recurse(dd,kc){
                for(let k in dd){
                    let kc2=[...kc,k]
                    let kc3=kc2.join('|')
                    meta.checkedItems.add(kc3)
                    if(typeof(dd[k])=='object'){
                        recurse(dd[k],kc2)
                    }else{
                        meta.checkedEndItems.add(kc3)
                    }
                }
            }
            recurse(dd,keyChain)
        }else{
            meta.checkedItems.delete(nd.value)
            function recurse(dd,kc){
                for(let k in dd){
                    let kc2=[...kc,k]
                    let kc3=kc2.join('|')
                    meta.checkedItems.delete(kc3)
                    if(typeof(dd[k])=='object'){
                        recurse(dd[k],kc2)
                    }else{
                        meta.checkedEndItems.delete(kc3)
                    }
                }
            }
            recurse(dd,keyChain)
        }
        LAZYTREE.populate(idx)
    },
    adjustYThumb:function(idx){
        let tree=document.getElementById(idx)
        let track=tree.querySelector('.lztreytrk')
        let thumb=tree.querySelector('.lztreythmb')
        let meta=LAZYTREE.getMeta(idx)
        let cnt=meta.itemCount
        let hiddenItems=meta.hiddenItems
        let numItems=cnt-hiddenItems.size
        let numShownItems=meta.numShownItems
        let trackRect=track.getBoundingClientRect()
        let trackHeight=trackRect.height
        let fraction=numShownItems/numItems
        let thumbHeight=trackHeight*fraction
        thumb.style.height=thumbHeight+'px'
    },
    onmouseupThumb:function(ev){
        document.removeEventListener('mouseup',LAZYTREE.onmouseupThumb)
        document.removeEventListener('mousemove',LAZYTREE.onmousemoveThumb)
    },
    onmousemoveThumb:function(ev){
        let thumb=window.CURLAZYTREETHUMB
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
        let tree=track.closest('.lztre')
        let tidx=tree.id
        LAZYTREE.populate(tidx)
    },
    onmousedownThumb:function(ev,idx){
        document.addEventListener('mouseup',LAZYTREE.onmouseupThumb)
        document.addEventListener('mousemove',LAZYTREE.onmousemoveThumb)
        window.CURLAZYTREETHUMB=ev.target
        window.CURMOUSEDOWNY=ev.target.pageY
    },
    onwheel:function(ev,idx){
        ev.stopPropagation()
        ev.preventDefault()
        let meta=LAZYTREE.getMeta(idx)
        let tree=document.getElementById(idx)
        let track=tree.querySelector('.lztreytrk')
        let thumb=tree.querySelector('.lztreythmb')
        let trackRect=track.getBoundingClientRect()
        let thumbRect=thumb.getBoundingClientRect()
        let thumbHeight=thumbRect.height
        let trackHeight=trackRect.height
        let dir=ev.deltaY
        let numItems=meta.itemCount
        let numShownItems=meta.numShownItems
        let numScrollItems=numItems-numShownItems
        let movableHeight=trackHeight-thumbHeight
        if(thumb.style.display=='none'){
            movableHeight=0
        }
        let unitHeight=movableHeight/numScrollItems
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
    filter:function(ev,idx){
        if(ev.key!='Enter'){return}
        let inputs=Array.from(ev.target.closest('.lztrefltrcol').querySelectorAll('input'))
        let searchKeys={}
        for(let input of inputs){
            let header=input.getAttribute('header')
            let sks=input.value.toLowerCase().trim().split(',').map(a=>a.trim())
            searchKeys[header]=sks
        }
        let meta=LAZYTREE.getMeta(idx)
        let origData=meta.origData
        let headers=meta.headers
        if(meta.shownHeaders){
            headers=meta.shownHeaders
        }
        let newData=[]
        for(let d of origData){
            let bools=new Set()
            for(let header of headers){
                let bool=false
                let sks=searchKeys[header]
                if(sks.length==0){continue}
                let text=d[header].toLowerCase()
                for(let sk of sks){
                    if(text.indexOf(sk)>-1){
                        bool=true
                        break
                    }
                }
                bools.add(bool)
            }
            if(!bools.has(false)){
                newData.push(d)
            }
        }
        LAZYTREE.setData(idx,newData,false)
        LAZYTREE.populate(idx)
    },
    onmouseupBody:function(ev){
        document.removeEventListener('mouseup',LAZYTREE.onmouseupBody)
        document.removeEventListener('mousemove',LAZYTREE.onmousemoveBody)
    },
    onmousemoveBody:function(ev){
        let tree=ev.target.closest('.lztre')
        let idx=tree.id
        let nd=ev.target.closest('.lztrend')
        if(!nd){return}
        let inp=nd.querySelector('input[type=checkbox]')
        let meta=LAZYTREE.getMeta(idx)
        inp.checked=meta.lastMouseDownState
        if(meta.lastMouseDownState){
            meta.checkedItems.add(nd.value)
        }else{
            meta.checkedItems.delete(nd.value)
        }
        let keyChain=nd.value.split('|')
        let dd=meta.dataDict
        for(let k of keyChain){
            dd=dd[k]
        }
        if(typeof(dd)=='boolean'){
            if(meta.lastMouseDownState){
                meta.checkedEndItems.add(nd.value)
            }else{
                meta.checkedEndItems.delete(nd.value)
            }
        }
        document.getElementById('lztrechkd'+idx).innerText=meta.checkedEndItems.size
    },
    onmousedownBody:function(ev,idx){
        if(ev.target.tagName!='INPUT'||ev.target.type!='checkbox'){return}
        let meta=LAZYTREE.getMeta(idx)
        meta.lastMouseDownState=!ev.target.checked
        document.addEventListener('mouseup',LAZYTREE.onmouseupBody)
        document.addEventListener('mousemove',LAZYTREE.onmousemoveBody)
    },
    toggleOptionsPanel:function(ev,idx){
        let tree=document.getElementById(idx)
        let panel=tree.querySelector('.lztreoptpnl')
        if(panel.style.display=='none'){
            panel.style.display='flex'
            panel.style.left=ev.pageX+10+'px'
            let rect=panel.getBoundingClientRect()
            panel.style.top=ev.pageY-10-rect.height+'px'
        }else{
            panel.style.display='none'
        }
    },
    toggleColumnVisibility:function(ev,idx){
        let meta=LAZYTREE.getMeta(idx)
        meta.hiddenHeaders=meta.hiddenHeaders||new Set()
        if(ev.target.checked){
            meta.hiddenHeaders.delete(ev.target.parentElement.innerText)
        }else{
            meta.hiddenHeaders.add(ev.target.parentElement.innerText)
        }
        LAZYTREE.setData(idx,null,false)
        LAZYTREE.populate(idx)
    },
    onmouseupColVisInput:function(ev){
        document.removeEventListener('mouseup',LAZYTREE.onmouseupColVisInput)
        document.removeEventListener('mousemove',LAZYTREE.onmousemoveColVisInput)
    },
    onmousemoveColVisInput:function(ev){
        let tree=ev.target.closest('.lztre')
        let idx=tree.id
        let meta=LAZYTREE.getMeta(idx)
        let elm=meta.CURDRAGONCOLVIS
        let rect=elm.getBoundingClientRect()
        let headers=Array.from(elm.parentElement.children).map(e=>e.innerText)
        if(ev.pageY<rect.top-5){
            if(elm.previousSibling){
                elm.previousSibling.before(elm)
            }
            meta.shownHeaders=Array.from(elm.parentElement.children)
            .filter(e=>e.querySelector('input').checked).map(e=>e.innerText)
            LAZYTREE.setData(idx)
            LAZYTREE.populate(idx)
        }else if(ev.pageY>rect.top+rect.height+5){
            if(elm.nextSibling){
                elm.nextSibling.after(elm)
            }
            meta.shownHeaders=Array.from(elm.parentElement.children)
            .filter(e=>e.querySelector('input').checked).map(e=>e.innerText)
            LAZYTREE.setData(idx)
            LAZYTREE.populate(idx)
        }
    },
    onmousedownColVisInput:function(ev,idx){
        let meta=LAZYTREE.getMeta(idx)
        meta.CURDRAGONCOLVIS=ev.target
        document.addEventListener('mouseup',LAZYTREE.onmouseupColVisInput)
        document.addEventListener('mousemove',LAZYTREE.onmousemoveColVisInput)
    },
}