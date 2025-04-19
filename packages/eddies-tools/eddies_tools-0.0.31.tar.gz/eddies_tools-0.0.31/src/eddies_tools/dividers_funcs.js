window.Divider={
    onmouseupHor:function(ev){
        document.removeEventListener('mouseup',Divider.onmouseupHor)
        document.removeEventListener('mousemove',Divider.onmousemoveHor)
    },
    onmousemoveHor:function(ev){
        let prev=window.CURDIVIDER.previousSibling
        let next=window.CURDIVIDER.nextSibling
        let prevRect=prev.getBoundingClientRect()
        let nextRect=next.getBoundingClientRect()
        let delta=ev.pageX-window.MOUSEDOWNX
        if(prev.style.width){
            let w=Number(prev.style.width.replace('px',''))
            w+=delta
            prev.style.width=w+'px'
        }else{
            let w=prevRect.width
            w+=delta
            prev.style.width=w+'px'
        }
        if(next.style.width){
            if(next.style.width.indexOf('calc')==-1){
                let w=Number(next.style.width.replace('px',''))
                w-=delta
                next.style.width=w+'px'
            }else{
                let w=Number(next.style.width.split('-')[1].split('px)')[0])
                w+=delta
                next.style.width='calc(100% - '+w+'px)'
            }
        }else{
            let w=nextRect.width
            w-=delta
            next.style.width=w+'px'
        }
        window.MOUSEDOWNX=ev.pageX
    },
    onmousedownHor:function(ev){
        window.CURDIVIDER=ev.target
        window.MOUSEDOWNX=ev.pageX
        document.addEventListener('mouseup',Divider.onmouseupHor)
        document.addEventListener('mousemove',Divider.onmousemoveHor)
    },
    onmouseupVert:function(ev){
        document.removeEventListener('mouseup',Divider.onmouseupVert)
        document.removeEventListener('mousemove',Divider.onmousemoveVert)
    },
    onmousemoveVert:function(ev){
        let prev=window.CURDIVIDER.previousSibling
        let next=window.CURDIVIDER.nextSibling
        let prevRect=prev.getBoundingClientRect()
        let nextRect=next.getBoundingClientRect()
        let delta=ev.pageY-window.MOUSEDOWNY
        if(prev.style.height){
            let w=Number(prev.style.height.replace('px',''))
            w+=delta
            prev.style.height=w+'px'
        }else{
            let w=prevRect.height
            w+=delta
            prev.style.height=w+'px'
        }
        if(next.style.height){
            if(next.style.height.indexOf('calc')==-1){
                let w=Number(next.style.height.replace('px',''))
                w-=delta
                next.style.height=w+'px'
            }else{
                let w=Number(next.style.height.split('-')[1].split('px)')[0])
                w+=delta
                next.style.height='calc(100% - '+w+'px)'
            }
        }else{
            let w=nextRect.height
            w-=delta
            next.style.height=w+'px'
        }
        window.MOUSEDOWNY=ev.pageY
    },
    onmousedownVert:function(ev){
        window.CURDIVIDER=ev.target
        window.MOUSEDOWNY=ev.pageY
        document.addEventListener('mouseup',Divider.onmouseupVert)
        document.addEventListener('mousemove',Divider.onmousemoveVert)
    }
}