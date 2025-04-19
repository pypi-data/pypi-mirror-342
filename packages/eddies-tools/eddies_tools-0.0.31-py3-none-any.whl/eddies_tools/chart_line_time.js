window.ChartLineTime=class extends(window.ChartLine){
    constructor(canvas,options){
        super(canvas,options)
    }
    calcXTicks(ctx){
        let unitX=(this.maxX-this.minX)/this.numXTicks
        let ticks=new Set()
        let minX=this.minX
        let lastTickWidth
        ctx.font=this.font
        let tickWidths=[]
        for(let j=0;j<this.numXTicks+1;j++){
            let tick=minX+unitX*j
            tick=formatDate(new Date(tick*1000))
            ticks.add(tick)
            lastTickWidth=ctx.measureText(tick).width
            tickWidths.push(lastTickWidth)
        }
        this.tickTime=false
        if(ticks.size<this.numXTicks+1){
            tickWidths=[]
            for(let j=0;j<this.numXTicks+1;j++){
                let tick=minX+unitX*j
                tick=formatDate(new Date(tick*1000),true)
                tick=tick.split(' ')
                lastTickWidth=Math.max(ctx.measureText(tick[0]).width,
                    ctx.measureText(tick[1]).width)
                tickWidths.push(lastTickWidth)
            }
            this.tickTime=true
        }
        let sum=tickWidths.reduce((a,b)=>a+b+10)
        let innerWidth=this.width-this.leftMargin-this.rightMargin
        while(sum>=innerWidth){
            tickWidths.pop()
            sum=tickWidths.reduce((a,b)=>a+b+10)
        }
        this.numXTicks=tickWidths.length-1
        this.lastXTickWidth=lastTickWidth
        if(this.tickTime){
            this.bottomMargin=this.fontPt*2+2+this.markerSize
        }else{
            this.bottomMargin=this.fontPt+this.markerSize
        }
        //
        let xrg=(this.maxX0-this.minX0)/(5)
        let factor
        if(xrg>=3600*24){
            factor=3600*24
        }else if(xrg>=3600*12){
            factor=3600*12
        }else if(xrg>=3600*8){
            factor=3600*8
        }else if(xrg>=3600*6){
            factor=3600*6
        }else if(xrg>=3600*4){
            factor=3600*4
        }else if(xrg>=3600*2){
            factor=3600*2
        }else if(xrg>=3600){
            factor=3600
        }else if(xrg>=60){
            factor=60*5
        }else{
            factor=1*5
        }
        unitX=factor
        minX=Math.trunc(this.minX0/unitX)*unitX
        let maxX=Math.ceil(this.maxX0/unitX)*unitX
        this.numXTicks=Math.trunc((maxX-minX)/unitX)
        this.minX=minX
        this.maxX=maxX
    }
    drawXTicks(ctx){
        this.getFontColor(ctx)
        // let unitWidth=(this.innerWidth-this.lastXTickWidth)/this.numXTicks
        let unitWidth=(this.innerWidth)/this.numXTicks
        let unitX=(this.maxX-this.minX)/this.numXTicks
        ctx.font=this.font
        let top=this.topMargin+this.innerHeight+this.fontPt+this.markerSize
        let minX=this.minX
        let leftMargin=this.leftMargin
        let tickTime=this.tickTime
        let totalXc=0
        for(let j=0;j<this.numXTicks+1;j++){
            let tick=minX+unitX*j
            tick=formatDate(new Date(tick*1000),tickTime)
            let xc=unitWidth*j+leftMargin
            if(xc<=totalXc+10){continue}
            let w
            if(tickTime){
                tick=tick.split(' ')
                w=ctx.measureText(tick[0]).width
                if(xc+w>this.innerWidth+leftMargin){continue}
                ctx.fillText(tick[0],xc,top)
                ctx.fillText(tick[1],xc,top+this.fontPt+2)
            }else{
                w=ctx.measureText(tick).width
                if(xc+w>this.innerWidth+leftMargin){continue}
                ctx.fillText(tick,xc,top)
            }
            totalXc=xc+w
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
            let tooltip=window['_grtltp_'+canvas.id]
            while(tooltip.firstChild){
                tooltip.firstChild.remove()
            }
            let offsetLeft=chart.leftMargin
            let offsetTop=chart.topMargin
            let rect=canvas.getBoundingClientRect()
            let left=rect.left
            let top=rect.top
            for(let label in found){
                let ix=found[label]
                let xc=xcs[label][ix]+offsetLeft+left
                let yc=ycs[label][ix]+offsetTop+top
                let x=xs[label][ix]
                let y=ys[label][ix]
                x=formatDate(new Date(x*1000),true)
                let tooltiptext=label+' ('+x+', '+y+')'
                let point=document.createElement('div')
                point.style.position='fixed'
                point.style.top=yc-5+'px'
                point.style.left=xc-5+'px'
                point.style.width='10px'
                point.style.height='10px'
                point.style.backgroundColor='rgb(0,255,0)'
                tooltip.appendChild(point)
                let text=document.createElement('p')
                text.innerText=tooltiptext
                tooltip.appendChild(text)
            }
            tooltip.style.display='flex'
            tooltip.style.left=ev.pageX+10-window.scrollX+'px'
            tooltip.style.top=ev.pageY+10-window.scrollY+'px'
        }
    }
}