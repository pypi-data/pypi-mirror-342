window.ChartBar=class extends (window.ChartScatter){
    constructor(canvas,options){
        super(canvas,options)
        this.labels=[]
        this.minX0=10e10
        this.maxX0=-10e10
        this.minY0=10e10
        this.maxY0=-10e10
        this.data={}
        this.markerSize=0
        this.spacingFactor=this.spacingFactor||1
    }
    addDataSet(xs,ys,label){
        let minX=10e10,maxX=-10e10,minY=10e10,maxY=-10e10
        let dd=this.data
        for(let j in xs){
            let x=xs[j],y=ys[j]
            if(x<minX){minX=x}
            if(x>maxX){maxX=x}
            if(y>maxY){maxY=y}
            dd[x]=dd[x]||{}
            dd[x][label]=y
        }
        this.labels.push(label)
        if(minX<this.minX0){this.minX0=minX}
        if(maxX+1>this.maxX0){this.maxX0=maxX+1}
        // if(minY<this.minY0){this.minY0=minY}
        this.minY0=0
        if(maxY>this.maxY0){this.maxY0=maxY}
        this.minX=this.minX0
        this.maxX=this.maxX0
        this.minY=this.minY0
        this.maxY=this.maxY0
        this.needsUpdate=true
    }
    resize(){
        let xs=this.xs=[]
        for(let j=this.minX0;j<this.maxX0;j++){
            xs.push(j)
        }
        let rect=this.canvas.getBoundingClientRect()
        this.width=this.canvas.width=rect.width
        this.height=this.canvas.height=rect.height
        this.innerWidth=rect.width-this.leftMargin-this.rightMargin
        this.innerHeight=rect.height-this.topMargin-this.bottomMargin
        this.barWidthFactor=1
        this.totalFactor=this.spacingFactor*(this.xs.length)
        +this.barWidthFactor*(this.xs.length)*this.labels.length
        this.zoomFactor=(this.maxX-this.minX)/(this.maxX0-this.minX0)
        this.unitWidth=this.innerWidth/this.zoomFactor/this.totalFactor
        this.spacing=this.unitWidth*this.spacingFactor
        // this.innerWidth+=this.spacing
    }
    calcBoxZoom(canvas){
        let chart=canvas.chart
        let square=window._grsqr_
        let sRect=square.getBoundingClientRect()
        let rect=canvas.getBoundingClientRect()
        chart.states.push([chart.minX,chart.maxX,chart.minY,chart.maxY])
        let xf1=(sRect.left-rect.left-chart.leftMargin)/chart.innerWidth
        let xf2=(sRect.left+sRect.width-rect.left-chart.leftMargin)/(chart.innerWidth)
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
    calcXYFactors(){
        let xrg=this.maxX-this.minX
        let xfa=this.innerWidth/xrg
        let xfb=-this.innerWidth*this.minX/xrg
        let yrg=this.maxY-this.minY
        let yfa=this.innerHeight/yrg
        let yfb=this.innerHeight*(1+this.minY/yrg)
        return [xfa,xfb,yfa,yfb]
    }
    mousemoveSquare(ev){
        if(window.MOUSEDOWN){
            let canvas=ev.target
            if(canvas.tagName!='CANVAS'){
                canvas=window.CURCANVAS
            }
            if(!canvas){return}
            let chart=canvas.chart
            let rect=canvas.getBoundingClientRect()
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
            square.style.top=rect.top+chart.topMargin+'px'
            let w=x2-x1
            square.style.width=w+'px'
            square.style.height=rect.height-chart.topMargin-chart.bottomMargin+'px'
        }
    }
    calcCoords(){
        let xfa,xfb,yfa,yfb
        [xfa,xfb,yfa,yfb]=this.calcXYFactors()
        let xcs=this.xcs={}
        let ycs=this.ycs={}
        let data=this.data
        let unitWidth=this.unitWidth
        let labels=this.labels
        let xAndXcs=this.xAndXcs=[]
        for(let x in data){
            x=Number(x)
            let xcs_=xcs[x]={}
            let ycs_=ycs[x]={}
            let xc=xfa*(x)+xfb
            xAndXcs.push([x,xc])
            for(let i=0;i<labels.length;i++){
                let label=labels[i]
                let xc=xfa*(x)+i*unitWidth+xfb
                let yc=-yfa*data[x][label]+yfb
                xcs_[label]=[xc,unitWidth]
                ycs_[label]=[yc,yfb-yc]
            }
        }
    }
    drawXGrid(){

    }
    drawXTicks(ctx){
        let top=this.topMargin+this.innerHeight+this.fontPt
        let totalXc=0
        let xAndXcs=this.xAndXcs
        let halfSpacing=this.spacing/2
        let leftMargin=this.leftMargin+halfSpacing
        let halfWidth=this.barWidthFactor*this.unitWidth/2*this.labels.length
        this.setGridColor(ctx)
        for(let x_xc of xAndXcs){
            let x=x_xc[0]
            let w=ctx.measureText(x).width
            let xc=x_xc[1]+leftMargin+halfWidth-w/2
            if(xc<totalXc+10){continue}
            ctx.fillText(x,xc,top)
            totalXc=xc+w
            xc=x_xc[1]-halfSpacing+leftMargin
            ctx.beginPath()
            ctx.moveTo(xc,top-this.fontPt/2)
            ctx.lineTo(xc,top-this.fontPt)
            ctx.stroke()
        }
        let xc=xAndXcs[xAndXcs.length-1][1]+halfSpacing+leftMargin+halfWidth*2
        ctx.beginPath()
        ctx.moveTo(xc,top-this.fontPt/2)
        ctx.lineTo(xc,top-this.fontPt)
        ctx.stroke()
    }
    drawPoints(ctx){
        ctx.save()
        ctx.translate(this.leftMargin+this.spacing/2,this.topMargin)
        let colors=this.colors,labels=this.labels
        let xcs=this.xcs
        let ycs=this.ycs
        let innerWidth=this.innerWidth
        for(let j=0;j<this.xs.length;j++){
            let x=this.xs[j]
            let xcs_=xcs[x]
            if(!xcs_){continue}
            let ycs_=ycs[x]
            for(let i=0;i<labels.length;i++){
                let label=labels[i]
                let color=colors[label]
                ctx.fillStyle=color
                let xc=xcs_[label]
                let yc=ycs_[label]
                if(xc!==undefined&&yc!==undefined){
                    if(xc[0]+xc[1]<0){continue}
                    if(xc[0]>innerWidth){continue}
                    ctx.fillRect(xc[0],yc[0],xc[1],yc[1])
                }
            }
        }
        ctx.restore()
    }
    clearMargins(ctx){
        ctx.clearRect(0,0,this.leftMargin-this.markerSize,this.height)
        ctx.clearRect(0,0,this.width,this.topMargin-this.markerSize)
        ctx.clearRect(0,this.topMargin+this.innerHeight+this.markerSize,this.width,this.height)
        ctx.clearRect(this.leftMargin+this.innerWidth+this.markerSize,0,this.width,this.height)
    }
    setupTooltipGrid(){
        this.numYBins=1
        this._setupTooltipGrid()
        let grid=this.tooltipGrid
        let xBinDim=this.xBinDim
        let labels=this.labels
        let data=this.data
        let xcs=this.xcs
        for(let j=0;j<this.xs.length;j++){
            let x=this.xs[j]
            let xcs_=xcs[x]
            if(!xcs_){continue}
            let ys_=data[x]
            for(let i=0;i<labels.length;i++){
                let label=labels[i]
                let xc
                if(labels.length%2==1){
                    xc=xcs_[labels[Math.floor(labels.length/2)]]
                    xc=xc[0]+xc[1]/2
                }else{
                    let xc1=xcs_[labels[Math.floor(labels.length/2)-1]]
                    let xc2=xcs_[labels[Math.floor(labels.length/2)]]
                    xc=(xc1[0]+xc2[0]+xc2[1])/2
                }
                let xbin=Math.round(xc/xBinDim)
                let bin=grid[0][xbin]
                if(!bin){continue}
                if(xc!==undefined){
                    let y=ys_[label]
                    bin.push([xc,label,x,y])
                }
            }
        }
    }
    findNearest(ev){
        let canvas=ev.target
        let chart=canvas.chart
        let rect=canvas.getBoundingClientRect()
        let xc=ev.pageX-rect.left-chart.leftMargin
        let yc=ev.pageY-rect.top-chart.topMargin
        let xBin=Math.floor((xc)/chart.xBinDim)
        let grid=chart.tooltipGrid
        let xcs=chart.xcs
        let found={}
        for(let i=0;i<=this.numYBins+1;i++){
            if(!grid[i]){continue}
            for(let j=xBin-1;j<=xBin+1;j++){
                if(!grid[i][j]){continue}
                for(let xc_label_x_y of grid[i][j]){
                    let xc2=xc_label_x_y[0]
                    let label=xc_label_x_y[1]
                    let x=xc_label_x_y[2]
                    let y=xc_label_x_y[3]
                    let delta=Math.abs(xc2-xc)
                    if(!found[label]){
                        found[label]=[delta,x,y]
                    }else{
                        if(delta<found[label][0]){
                            found[label]=[delta,x,y]
                        }
                    }
                }
            }
        }
        for(let label in found){
            found[label]=found[label].slice(1)
        }
        return found
    }
    mousemove(ev,cvs){
        if(!window.MOUSEDOWN){
            let canvas=cvs||ev.target
            let chart=canvas.chart
            window._grsqr_.style.display='none'
            let found=chart.findNearest({target:canvas,
                pageX:ev.pageX-window.scrollX,pageY:ev.pageY-window.scrollY})
            let tooltip=window['_grtltp_'+canvas.id]
            while(tooltip.firstChild){
                tooltip.firstChild.remove()
            }
            for(let label in found){
                let xy=found[label]
                let tooltiptext=label+' ('+xy[0]+', '+xy[1]+')'
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