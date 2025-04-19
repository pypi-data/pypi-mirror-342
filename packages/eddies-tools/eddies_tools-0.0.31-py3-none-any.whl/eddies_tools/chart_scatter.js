window.ChartScatter=class{
    constructor(canvas,options){
        this.canvas=canvas
        canvas.chart=this
        let rect=this.canvas.getBoundingClientRect()
        this.width=this.canvas.width=rect.width
        this.height=this.canvas.height=rect.height        
        if(options){
            for(let k in options){
                this[k]=options[k]
            }
        }
        this.numXTicks=this.numXTicks||5
        this.numYTicks=this.numYTicks||5
        if(this.markerSize===undefined){
            this.markerSize=2
        }
        this.font=this.font||'10pt Arial'
        this.fontPt=Number(this.font.split('pt')[0])
        this.states=[]
    }
    setData(xs,ys,labels,validate){
        let xs2,ys2,labels2
        let minX=10e10,maxX=-10e10,minY=10e10,maxY=-10e10
        if(validate){
            (xs2=[]).length=xs.length;
            xs2.fill(null);
            (ys2=[]).length=xs.length;
            ys2.fill(null);
            (labels2=[]).length=labels.length;
            labels2.fill(null);
            let cnt=0
            for(let j in xs){
                let x=xs[j],y=ys[j],l=labels[j]
                if(x===null){continue}
                if(y===null){continue}
                xs2[cnt]=x
                ys2[cnt]=y
                labels2[cnt]=l
                if(x<minX){minX=x}
                if(x>maxX){maxX=x}
                if(y<minY){minY=y}
                if(y>maxY){maxY=y}
                cnt+=1
            }
            xs2=xs2.slice(0,cnt)
            ys2=ys2.slice(0,cnt)
            labels2=labels2.slice(0,cnt)
        }else{
            xs2=xs
            ys2=ys
            for(let j in xs){
                let x=xs[j],y=ys[j]
                if(x<minX){minX=x}
                if(x>maxX){maxX=x}
                if(y<minY){minY=y}
                if(y>maxY){maxY=y}
            }
            labels2=labels
        }
        this.xs=xs2
        this.ys=ys2
        this.labels=labels2
        this.minX0=minX
        this.maxX0=maxX
        this.minY0=minY
        this.maxY0=maxY
        if(this.minX0==this.maxX0){
            this.minX0-=1
            this.maxX0+=1
        }
        if(this.minY0==this.maxY0){
            this.minY0-=1
            this.minY0+=1
        }
        this.minX=this.minX0
        this.maxX=this.maxX0
        this.minY=this.minY0
        this.maxY=this.maxY0
        this.needsUpdate=true
    }
    setColors(colorDict){
        this.colors=colorDict
    }
    resize(){
        let rect=this.canvas.getBoundingClientRect()
        this.width=this.canvas.width=rect.width
        this.height=this.canvas.height=rect.height
        this.innerWidth=rect.width-this.leftMargin-this.rightMargin
        this.innerHeight=rect.height-this.topMargin-this.bottomMargin
    }
    calcXYFactors(){
        let xrg=this.maxX-this.minX
        let xfa=this.innerWidth/xrg
        let xfb=-this.innerWidth*this.minX/xrg
        let yrg=this.maxY-this.minY
        let yfa=this.innerHeight/yrg
        let yfb=this.innerHeight*(1+this.minY/yrg)
        return [xfa,xfb,yfa,yfb]
    }
    calcCoords(){
        let xfa,xfb,yfa,yfb
        [xfa,xfb,yfa,yfb]=this.calcXYFactors()
        let xcs
        (xcs=[]).length=this.xs.length
        xcs.fill(null)
        let ycs
        (ycs=[]).length=this.ys.length
        ycs.fill(null)
        let xs=this.xs,ys=this.ys
        for(let j=0;j<xs.length;j++){
            let x=xs[j],y=ys[j]
            xcs[j]=xfa*x+xfb
            ycs[j]=-yfa*y+yfb
        }
        this.xcs=xcs
        this.ycs=ycs
    }
    calcXTicks(ctx){
        let unitX=(this.maxX-this.minX)/this.numXTicks
        let tickDecimal=0
        let ticks=new Set()
        let factor=10**tickDecimal
        let minX=this.minX
        let lastTickWidth
        ctx.font=this.font
        let tickWidths=[]
        for(let j=0;j<this.numXTicks+1;j++){
            let tick=Math.round((minX+unitX*j)*factor)/factor
            ticks.add(tick)
            lastTickWidth=ctx.measureText(tick.toString()).width
            tickWidths.push(lastTickWidth)
        }
        while(ticks.size<this.numXTicks+1){
            tickWidths=[]
            tickDecimal+=1
            ticks=new Set()
            factor=10**tickDecimal
            for(let j=0;j<this.numXTicks+1;j++){
                let tick=Math.round((minX+unitX*j)*factor)/factor
                ticks.add(tick)
                lastTickWidth=ctx.measureText(tick.toString()).width
                tickWidths.push(lastTickWidth)
            }
        }
        let sum=tickWidths.reduce((a,b)=>a+b+10)
        let innerWidth=this.width-this.leftMargin-this.rightMargin
        while(sum>=innerWidth){
            tickWidths.pop()
            sum=tickWidths.reduce((a,b)=>a+b+10)
        }
        this.numXTicks=tickWidths.length-1
        this.lastXTickWidth=lastTickWidth
        this.xTickDecimal=tickDecimal
        this.bottomMargin=this.fontPt*1.3+this.markerSize
        //
        let xrg=(this.maxX0-this.minX0)/(5)
        let exp=-10
        while(10**exp<xrg){
            exp+=1
        }
        exp-=1
        factor=10**exp
        unitX=factor*10/2
        minX=Math.trunc(this.minX0/unitX)*unitX
        let maxX=Math.ceil(this.maxX0/unitX)*unitX
        this.numXTicks=Math.trunc((maxX-minX)/unitX)
        if(this.numXTicks<4){
            unitX=factor*10/5
            minX=Math.trunc(this.minX0/unitX)*unitX
            maxX=Math.ceil(this.maxX0/unitX)*unitX
            this.numnumXTicks=Math.trunc((maxX-minX)/unitX)
        }
        if(this.numXTicks<4){
            unitX=factor
            minX=Math.trunc(this.minX0/unitX)*unitX
            maxX=Math.ceil(this.maxX0/unitX)*unitX
            this.numXTicks=Math.trunc((maxX-minX)/unitX)
        }
        this.minX=minX
        this.maxX=maxX
    }
    calcYTicks(ctx){
        let unitY=(this.maxY-this.minY)/this.numYTicks
        let tickDecimal=0
        let ticks=new Set()
        let factor=10**tickDecimal
        for(let j=0;j<this.numYTicks+1;j++){
            let tick=Math.round((this.minY+unitY*j)*factor)/factor
            ticks.add(tick)
        }
        while(ticks.size<this.numYTicks+1){
            tickDecimal+=1
            ticks=new Set()
            factor=10**tickDecimal
            for(let j=0;j<this.numYTicks+1;j++){
                let tick=Math.round((this.minY+unitY*j)*factor)/factor
                ticks.add(tick)
            }
        }
        this.yTickDecimal=tickDecimal
        let mx=0
        ticks=Array.from(ticks)
        ctx.font=this.font
        for(let tick of ticks){
            let w=ctx.measureText(tick.toString()).width
            if(w>mx){mx=w}
        }
        this.leftMargin=mx+4+this.markerSize
        //
        let yrg=(this.maxY0-this.minY0)/(this.numYTicks-1)
        let exp=-10
        while(10**exp<yrg){
            exp+=1
        }
        exp-=1
        factor=10**exp
        unitY=factor*10/2
        let minY=Math.trunc(this.minY0/unitY)*unitY
        let maxY=Math.ceil(this.maxY0/unitY)*unitY
        this.numYTicks=Math.trunc((maxY-minY)/unitY)
        if(this.numYTicks<5){
            let unitY=factor*10/5
            minY=Math.trunc(this.minY0/unitY)*unitY
            maxY=Math.ceil(this.maxY0/unitY)*unitY
            this.numYTicks=Math.trunc((maxY-minY)/unitY)
        }
        if(this.numYTicks<5){
            let unitY=factor
            minY=Math.trunc(this.minY0/unitY)*unitY
            maxY=Math.ceil(this.maxY0/unitY)*unitY
            this.numYTicks=Math.trunc((maxY-minY)/unitY)
        }
        this.minY=minY
        this.maxY=maxY
    }
    calcTopMargin(ctx){
        if(this.title){
            this.topMargin=this.fontPt+this.markerSize+2
        }else{
            this.topMargin=this.markerSize
        }
    }
    calcRightMargin(ctx){
        this.rightMargin=this.markerSize
    }
    setGridColor(ctx){
        if(this.darkMode){
            ctx.strokeStyle='darkgrey'
        }else{
            ctx.strokeStyle='lightgrey'
        }
    }
    drawXGrid(ctx){
        this.setGridColor(ctx)
        ctx.lineWidth=1
        ctx.save()
        ctx.translate(this.leftMargin,this.topMargin)
        let unitWidth=this.innerWidth/this.numXTicks
        for(let j=0;j<this.numXTicks+1;j++){
            let xc=unitWidth*j
            ctx.beginPath()
            ctx.moveTo(xc,0)
            ctx.lineTo(xc,this.innerHeight)
            ctx.stroke()
        }
        ctx.restore()
    }
    drawYGrid(ctx){
        ctx.lineWidth=1
        this.setGridColor(ctx)
        ctx.save()
        ctx.translate(this.leftMargin,this.topMargin)
        let unitHeight=this.innerHeight/this.numYTicks
        for(let j=0;j<this.numYTicks+1;j++){
            let yc=unitHeight*j
            ctx.beginPath()
            ctx.moveTo(0,yc)
            ctx.lineTo(this.innerWidth,yc)
            ctx.stroke()
        }
        ctx.restore()
    }
    drawPoints(ctx){
        ctx.save()
        ctx.translate(this.leftMargin,this.topMargin)
        let xcs=this.xcs,ycs=this.ycs
        let colors=this.colors,labels=this.labels
        let ms=this.markerSize
        let PI2=Math.PI*2
        let w=this.width
        let h=this.height
        for(let j=0;j<xcs.length;j++){
            let xc=xcs[j],yc=ycs[j]
            if(xc<0){continue}
            if(xc>w){continue}
            if(yc<0){continue}
            if(yc>h){continue}
            ctx.fillStyle=colors[labels[j]]
            ctx.beginPath()
            ctx.arc(xc,yc,ms,0,PI2)
            ctx.fill()
        }
        ctx.restore()
    }
    clearMargins(ctx){
        ctx.clearRect(0,0,this.leftMargin-this.markerSize,this.height)
        ctx.clearRect(0,0,this.width,this.topMargin-this.markerSize)
        ctx.clearRect(0,this.topMargin+this.innerHeight+this.markerSize,this.width,this.height)
        ctx.clearRect(this.leftMargin+this.innerWidth+this.markerSize,0,this.width,this.height)
    }
    getFontColor(ctx){
        if(this.darkMode){
            ctx.fillstyle='lightgrey'
        }else{
            ctx.fillStyle='rgb(50,50,50)'
        }        
    }
    drawXTicks(ctx){
        this.getFontColor(ctx)
        let unitWidth=(this.innerWidth-this.lastXTickWidth)/this.numXTicks
        let unitX=(this.maxX-this.minX)/this.numXTicks
        let tickDecimal=this.xTickDecimal
        let factor=10**tickDecimal
        ctx.font=this.font
        let top=this.topMargin+this.innerHeight+this.fontPt+this.markerSize
        for(let j=0;j<this.numXTicks+1;j++){
            let tick=Math.round((unitX*j)*factor)/factor
            let xc=unitWidth*j+this.leftMargin
            ctx.fillText(tick,xc,top)
        }
    }
    drawYTicks(ctx){
        this.getFontColor(ctx)
        let unitHeight=(this.innerHeight-this.fontPt)/this.numYTicks
        let unitY=(this.maxY-this.minY)/this.numYTicks
        let tickDecimal=this.yTickDecimal
        let factor=10**tickDecimal
        ctx.font=this.font
        ctx.save()
        ctx.translate(0,this.topMargin)
        for(let i=0;i<this.numYTicks+1;i++){
            let tick=Math.round((this.maxY-unitY*i)*factor)/factor
            let yc=unitHeight*i+this.fontPt
            ctx.fillText(tick,2,yc)
        }
        ctx.restore()
    }
    drawTitle(ctx){
        if(this.title){
            this.getFontColor(ctx)
            ctx.font=this.font
            ctx.fillText(this.title,this.leftMargin,this.fontPt)
        }
    }
    _setupTooltipGrid(){
        let numXBins=this.numXBins||10
        let numYBins=this.numYBins||10
        let xBinDim=this.xBinDim=this.innerWidth/numXBins
        let yBinDim=this.yBinDim=this.innerHeight/numYBins
        let grid=this.tooltipGrid={}
        for(let i=0;i<numYBins+1;i++){
            grid[i]={}
            for(let j=0;j<numXBins+1;j++){
                grid[i][j]=[]
            }
        }
    }
    setupTooltipGrid(){
        this._setupTooltipGrid()
        let grid=this.tooltipGrid
        let yBinDim=this.yBinDim
        let xBinDim=this.xBinDim
        let xcs=this.xcs,ycs=this.ycs
        for(let i=0;i<xcs.length;i++){
            let xc=xcs[i],yc=ycs[i]
            let ybin=Math.round(yc/yBinDim)
            if(!grid[ybin]){continue}
            let xbin=Math.round(xc/xBinDim)
            if(!grid[ybin][xbin]){continue}
            grid[ybin][xbin].push(i)
        }
    }
    _draw(ctx){
        this.resize()
        this.drawXGrid(ctx)
        this.drawYGrid(ctx)
        if(this.needsUpdate){
            this.calcCoords()
        }
        this.drawPoints(ctx)
        this.clearMargins(ctx)
        this.drawTitle(ctx)
        this.drawYTicks(ctx)
        this.drawXTicks(ctx)
        this.setupTooltipGrid()
    }
    draw(){
        let ctx=this.canvas.getContext('2d')
        this.calcTopMargin(ctx)
        this.calcRightMargin(ctx)
        this.calcYTicks(ctx)
        this.calcXTicks(ctx)
        this.darkMode=isDarkMode(this.canvas)
        this._draw(ctx)
    }
    findNearest(ev){
        let canvas=ev.target
        let chart=canvas.chart
        let rect=canvas.getBoundingClientRect()
        let xc=ev.pageX-rect.left-chart.leftMargin
        let yc=ev.pageY-rect.top-chart.topMargin
        let xBin=Math.floor((xc)/chart.xBinDim)
        let yBin=Math.floor((yc)/chart.yBinDim)
        let grid=chart.tooltipGrid
        let xcs=chart.xcs
        let ycs=chart.ycs
        let thresh=20*20
        let found=[]
        for(let i=yBin-1;i<=yBin+1;i++){
            if(!grid[i]){continue}
            for(let j=xBin-1;j<=xBin+1;j++){
                if(!grid[i][j]){continue}
                for(let ix of grid[i][j]){
                    let xc2=xcs[ix]
                    let yc2=ycs[ix]
                    let delta=(xc2-xc)*(xc2-xc)+(yc2-yc)*(yc2-yc)
                    if(delta<thresh){
                        found.push([ix,delta])
                    }
                }
            }
        }
        found=found.sort((a,b)=>a[1]-b[1]).slice(0,this.numTooltipPoints||5)
        return found.map(r=>r[0])
    }
    calcBoxZoom(canvas){
        let chart=canvas.chart
        let square=window._grsqr_
        let sRect=square.getBoundingClientRect()
        let rect=canvas.getBoundingClientRect()
        chart.states.push([chart.minX,chart.maxX,chart.minY,chart.maxY])
        let xf1=(sRect.left-rect.left-chart.leftMargin)/chart.innerWidth
        let xf2=(sRect.left+sRect.width-rect.left-chart.leftMargin)/chart.innerWidth
        let yf1=1-(sRect.top+sRect.height-rect.top-chart.topMargin)/chart.innerHeight
        let yf2=1-(sRect.top-rect.top-chart.topMargin)/chart.innerHeight
        let maxX=chart.minX+(chart.maxX-chart.minX)*xf2
        let minX=chart.minX+(chart.maxX-chart.minX)*xf1
        chart.maxX=maxX
        chart.minX=minX
        let maxY=chart.minY+(chart.maxY-chart.minY)*yf2
        let minY=chart.minY+(chart.maxY-chart.minY)*yf1
        chart.maxY=maxY
        chart.minY=minY
        let ctx=canvas.getContext('2d')
        chart._draw(ctx)
    }
    mousedown(ev,cvs){
        window.MOUSEDOWN=true
        window.MOUSEDOWNX=ev.pageX
        window.MOUSEDOWNY=ev.pageY
        window.CURCANVAS=cvs||ev.target
        let canvas=cvs||ev.target
        let chart=canvas.chart
        document.addEventListener('mouseup',chart.mouseup)
        document.addEventListener('mousemove',chart.mousemoveSquare)
        window['_grtltp_'+canvas.id].style.display='none'
    }
    mouseup(ev){
        let canvas=window.CURCANVAS
        window.CURCANVAS=null
        let chart=canvas.chart
        document.removeEventListener('mouseup',chart.mouseup)
        document.removeEventListener('mousemove',chart.mousemoveSquare)
        window.MOUSEDOWN=false
        if(window._grsqr_.style.display!='none'){
            if(ev.pageX<window.MOUSEDOWNX){
                let state=chart.states.pop()
                chart.minX=state[0]
                chart.maxX=state[1]
                chart.minY=state[2]
                chart.maxY=state[3]
                chart._draw(canvas.getContext('2d'))
            }else{
                canvas.chart.calcBoxZoom(canvas)
            }
        }
        window._grsqr_.style.display='none'
    }
    mousemoveSquare(ev){
        if(window.MOUSEDOWN){
            let canvas=ev.target
            if(canvas.tagName!='CANVAS'){
                canvas=window.CURCANVAS
            }
            if(!canvas){return}
            window['_grtltp_'+canvas.id].style.display='none'
            let square=window._grsqr_
            square.style.display='block'
            square.style.backgroundColor='rgba(0,0,0,0.1)'
            let x1,x2,y1,y2
            if(window.MOUSEDOWNX<ev.pageX){
                x1=window.MOUSEDOWNX
                x2=ev.pageX
            }else{
                x1=ev.pageX
                x2=window.MOUSEDOWNX
            }
            if(window.MOUSEDOWNY<ev.pageY){
                y1=window.MOUSEDOWNY
                y2=ev.pageY
            }else{
                y1=ev.pageY
                y2=window.MOUSEDOWNY
            }
            square.style.left=x1-window.scrollX+'px'
            square.style.top=y1-window.scrollY+'px'
            let w=x2-x1
            let h=y2-y1
            square.style.width=w+'px'
            square.style.height=h+'px'
        }
    }
    mousemove(ev,cvs){
        if(!window.MOUSEDOWN){
            let canvas=cvs||ev.target
            let chart=canvas.chart
            window._grsqr_.style.display='none'
            let found=chart.findNearest({target:canvas,
                pageX:ev.pageX-window.scrollX,pageY:ev.pageY-window.scrollY})
            let xcs=chart.xcs
            let ycs=chart.ycs
            let xs=chart.xs
            let ys=chart.ys
            let labels=chart.labels
            let tooltip=window['_grtltp_'+canvas.id]
            while(tooltip.firstChild){
                tooltip.firstChild.remove()
            }
            let offsetLeft=chart.leftMargin
            let offsetTop=chart.topMargin
            let rect=canvas.getBoundingClientRect()
            let left=rect.left
            let top=rect.top
            for(let ix of found){
                let xc=xcs[ix]+offsetLeft+left
                let yc=ycs[ix]+offsetTop+top
                let x=xs[ix]
                let y=ys[ix]
                let label=labels[ix]+' ('+x+', '+y+')'
                let point=document.createElement('div')
                point.style.position='fixed'
                point.style.top=yc-5+'px'
                point.style.left=xc-5+'px'
                point.style.width='10px'
                point.style.height='10px'
                point.style.backgroundColor='rgb(0,255,0)'
                tooltip.appendChild(point)
                let text=document.createElement('p')
                text.innerText=label
                tooltip.appendChild(text)
            }
            tooltip.style.display='flex'
            window.CURCHARTTOOLTIP=tooltip
            tooltip.style.left=ev.pageX+10-window.scrollX+'px'
            tooltip.style.top=ev.pageY+10-window.scrollY+'px'
        }
    }
    setEvents(){
        let idx=this.canvas.id
        this.canvas.addEventListener('mousedown',this.mousedown)
        this.canvas.addEventListener('mousemove',this.mousemove)
        this.canvas.addEventListener('mouseleave',(ev)=>{
            window['_grtltp_'+idx].style.display='none'
            // window._grsqr_.style.display='none'
        })
        this.canvas.addEventListener('dblclick',(ev)=>{
            this.minX=this.minX0
            this.maxX=this.maxX0
            this.minY=this.minY0
            this.maxY=this.maxY0
            let ctx=this.canvas.getContext('2d')
            this._draw(ctx)
        })
        window.CURRESIZEMOUSEUP=window.CURRESIZEMOUSEUP||{}
        function onResize(entries){
            limitFrameRate(idx,()=>{
                let charts=[]
                for(let entry of entries){
                    let canvas=entry.target
                    let chart=canvas.chart
                    charts.push(chart)
                    chart.resize()
                    chart._draw(canvas.getContext('2d'))
                }
                if(window.CURRESIZEMOUSEUP[idx]){
                    document.removeEventListener('mouseup',window.CURRESIZEMOUSEUP[idx])
                }
                let func=(ev)=>{
                    document.removeEventListener('mouseup',func)
                    for(let chart of charts){
                        chart.resize()
                        chart._draw(chart.canvas.getContext('2d'))        
                    }
                }
                window.CURRESIZEMOUSEUP[idx]=func
                document.addEventListener('mouseup',func)
            },500)
        }
        let resizeObserver=new ResizeObserver(onResize)
        resizeObserver.observe(this.canvas)
        if(!window['_grtltp_'+idx]){
            let tooltip=document.createElement('div')
            tooltip.id='_grtltp_'+idx
            tooltip.className='_col_ _popup_'
            tooltip.style.position='fixed'
            tooltip.style.zIndex=99
            tooltip.style.display='none'
            document.body.appendChild(tooltip)
            window['_grtltp_'+idx].addEventListener('mousemove',(ev)=>{
                this.mousemove(ev,this.canvas)
            })
            window['_grtltp_'+idx].addEventListener('mousedown',(ev)=>{
                this.mousedown(ev,this.canvas)
            })
            window['_grtltp_'+idx].addEventListener('dblclick',(ev)=>{
                this.minX=this.minX0
                this.maxX=this.maxX0
                this.minY=this.minY0
                this.maxY=this.maxY0
                let ctx=this.canvas.getContext('2d')
                this._draw(ctx)
            })
        }
        if(!window._grsqr_){
            let square=document.createElement('div')
            square.id='_grsqr_'
            square.style.position='fixed'
            square.style.zIndex=99
            square.style.border='1px solid rgb(125,125,125)'
            document.body.appendChild(square)
            square.addEventListener('mousemove',this.mousemoveSquare)
        }
        if(!window.mouseHasLeftCanvas){
            let func=window.mouseHasLeftCanvas=function(ev){
                let elms=document.elementsFromPoint(ev.pageX-window.scrollX,
                    ev.pageY-window.scrollY)
                let thereIsCanvas=false
                for(let elm of elms){
                    if(elm.tagName=='CANVAS'){
                        thereIsCanvas=true
                    }
                }
                if(!thereIsCanvas&&window.CURCHARTTOOLTIP){
                    window.CURCHARTTOOLTIP.style.display='none'
                }
            }
            document.addEventListener('mousemove',func)
        }
        if(!window.onwheelLeaveCanvas){
            let func=window.onwheelLeaveCanvas=function(ev){
                if(window.CURCHARTTOOLTIP){
                    window.CURCHARTTOOLTIP.style.display='none'
                }
            }
            document.addEventListener('wheel',func)
        }
    }
}