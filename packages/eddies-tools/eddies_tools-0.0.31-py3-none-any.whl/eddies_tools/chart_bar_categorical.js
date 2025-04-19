window.ChartBarCategorical=class extends (window.ChartBar){
    constructor(canvas,options){
        super(canvas,options)
    }
    addDataSet(xs,ys,label){
        let minX=10e10,maxX=-10e10,minY=10e10,maxY=-10e10
        let dd=this.data
        this.xs=new Set()
        for(let j=0;j<xs.length;j++){
            let x=xs[j],y=ys[j]
            this.xs.add(x)
            if(j<minX){minX=j}
            if(j>maxX){maxX=j}
            if(y>maxY){maxY=y}
            dd[x]=dd[x]||{}
            dd[x][label]=y
        }
        this.xs=Array.from(this.xs).sort((a,b)=>a.localeCompare(b))
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
    calcCoords(){
        let xfa,xfb,yfa,yfb
        [xfa,xfb,yfa,yfb]=this.calcXYFactors()
        let xcs=this.xcs={}
        let ycs=this.ycs={}
        let data=this.data
        let unitWidth=this.unitWidth
        let labels=this.labels
        let xAndXcs=this.xAndXcs=[]
        for(let j=0;j<this.xs.length;j++){
            let x=this.xs[j]
            let xcs_=xcs[x]={}
            let ycs_=ycs[x]={}
            let xc=xfa*j+xfb
            xAndXcs.push([x,xc])
            for(let i=0;i<labels.length;i++){
                let label=labels[i]
                let xc=xfa*(j)+i*unitWidth+xfb
                let yc=-yfa*data[x][label]+yfb
                xcs_[label]=[xc,unitWidth]
                ycs_[label]=[yc,yfb-yc]
            }
        }
    }
}