window.ChartLine=class extends(window.ChartScatter){
    constructor(canvas,options){
        super(canvas,options)
        this.xs={}
        this.ys={}
        this.labels=[]
        this.minX0=10e10
        this.maxX0=-10e10
        this.minY0=10e10
        this.maxY0=-10e10
        this.boxes=[]
        this.boxXcs=[]
    }
    addDataSet(xs,ys,label,validate){
        let xs2,ys2
        let minX=10e10,maxX=-10e10,minY=10e10,maxY=-10e10
        if (validate){
            (xs2=[]).length=xs.length;
            xs2.fill(null);
            (ys2=[]).length=xs.length;
            ys2.fill(null);
            let cnt=0
            for(let j in xs){
                let x=xs[j],y=ys[j]
                if(x===null){continue}
                if(y===null){continue}
                xs2[cnt]=x
                ys2[cnt]=y
                if(x<minX){minX=x}
                if(x>maxX){maxX=x}
                if(y<minY){minY=y}
                if(y>maxY){maxY=y}
                cnt+=1
            }
            xs2=xs2.slice(0,cnt)
            ys2=ys2.slice(0,cnt)
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
        }
        this.xs[label]=xs2
        this.ys[label]=ys2
        this.labels.push(label)
        if(minX<this.minX0){this.minX0=minX}
        if(maxX>this.maxX0){this.maxX0=maxX}
        if(minY<this.minY0){this.minY0=minY}
        if(maxY>this.maxY0){this.maxY0=maxY}
        this.minX=this.minX0
        this.maxX=this.maxX0
        this.minY=this.minY0
        this.maxY=this.maxY0
        this.needsUpdate=true
    }
    calcCoords(){
        let xfa,xfb,yfa,yfb
        [xfa,xfb,yfa,yfb]=this.calcXYFactors()
        let xcs={},ycs={}
        for(let label of this.labels){
            let xs=this.xs[label],ys=this.ys[label]
            let ls;
            (ls=[]).length=xs.length
            ls.fill(null)
            let xc=xcs[label]=ls;
            (ls=[]).length=ys.length
            ls.fill(null)
            let yc=ycs[label]=ls;
            for(let j=0;j<xs.length;j++){
                let x=xs[j],y=ys[j]
                xc[j]=xfa*x+xfb
                yc[j]=-yfa*y+yfb
    
            }
        }
        this.xcs=xcs
        this.ycs=ycs
        for(let x1_x2 of this.boxes){
            let xc1=xfa*x1_x2[0]+xfb
            let xc2=xfa*x1_x2[1]+xfb
            this.boxXcs.push([xc1,xc2-xc1])
        }
    }
    drawPoints(ctx){
        ctx.save()
        ctx.translate(this.leftMargin,this.topMargin)
        let colors=this.colors,labels=this.labels
        let ms=this.markerSize
        let lw=this.lineWidth||2
        let boxXcs=this.boxXcs
        let boxes=this.boxes
        let h=this.innerHeight
        for(let j=0;j<boxes.length;j++){
            let color=boxes[j][2]
            let xc=boxXcs[j][0]
            let w=boxXcs[j][1]
            ctx.fillStyle=color
            ctx.fillRect(xc,0,w,h)
        }
        ctx.lineWidth=lw
        let PI2=Math.PI*2
        let w=this.width
        for(let label of labels){
            let xcs=this.xcs[label],ycs=this.ycs[label]
            ctx.fillStyle=colors[label]
            ctx.strokeStyle=colors[label]
            ctx.beginPath()
            let xycs=[]
            let j=0
            while(xcs[j]<=0){
                j+=1
            }
            j-=1
            let xc=xcs[j],yc=ycs[j]
            ctx.moveTo(xc,yc)
            for(let j2=j;j2<xcs.length;j2++){
                let xc=xcs[j2],yc=ycs[j2]
                ctx.lineTo(xc,yc)
                if(ms){
                    xycs.push([xc,yc])
                }
                if(xc>w){break}
            }
            ctx.stroke()
            if(ms){
                for(let xyc of xycs){
                    ctx.beginPath()
                    ctx.arc(...xyc,ms,0,PI2)
                    ctx.fill()    
                }
            }
        }
        ctx.restore()
    }
    setupTooltipGrid(){
        this.numYBins=1
        this._setupTooltipGrid()
        let grid=this.tooltipGrid
        let yBinDim=this.yBinDim
        let xBinDim=this.xBinDim
        let labels=this.labels
        for(let label of labels){
            let xcs=this.xcs[label],ycs=this.ycs[label]
            for(let i=0;i<xcs.length;i++){
                let xc=xcs[i],yc=ycs[i]
                let ybin=Math.round(yc/yBinDim)
                if(!grid[ybin]){continue}
                let xbin=Math.round(xc/xBinDim)
                if(!grid[ybin][xbin]){continue}
                grid[ybin][xbin].push([label,i])
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
        let ycs=chart.ycs
        let found={}
        for(let i=0;i<=this.numYBins+1;i++){
            if(!grid[i]){continue}
            for(let j=xBin-1;j<=xBin+1;j++){
                if(!grid[i][j]){continue}
                for(let label_ix of grid[i][j]){
                    let label=label_ix[0]
                    let ix=label_ix[1]
                    let xc2=xcs[label][ix]
                    let delta=Math.abs(xc2-xc)
                    if(!found[label]){
                        found[label]=[ix,delta]
                    }else{
                        if(delta<found[label][1]){
                            found[label]=[ix,delta]
                        }
                    }
                }
            }
        }
        let found2={}
        for(let label in found){
            let ix=found[label][0]
            let yc2=ycs[label][ix]
            if(yc2<0){continue}
            if(yc2>this.innerHeight){continue}    
            found2[label]=ix
        }
        return found2
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
    addBox(x1,x2,color){
        this.boxes.push([x1,x2,color])
    }
}