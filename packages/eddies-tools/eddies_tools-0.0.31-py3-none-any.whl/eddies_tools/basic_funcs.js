function indexOf(iterable,object){
    for(let j in iterable){
        if(iterable[j]==object){
            return Number(j)
        }
    }
}
function entityForSymbol(symbol) {
    var code = symbol.charCodeAt(0);
    var codeHex = code.toString(16).toUpperCase();
    while (codeHex.length < 4) {
        codeHex = "0" + codeHex;
    }

    return "&#x" + codeHex.toLowerCase();
}
function addClass(element,Class){
    let c=new Set(element.className.split(' '))
    c.add(Class)
    element.className=Array.from(c).join(' ')
}
function removeClass(element,Class){
    let c=new Set(element.className.split(' '))
    c.delete(Class)
    element.className=Array.from(c).join(' ')
}
function hasClass(element,Class){
    if(!element.className){return false}
    let c=new Set(element.className.split(' '))
    return c.has(Class)
}
function isDarkMode(elmOrIdx){
    let elm=elmOrIdx
    if(!elmOrIdx.tagName){
        elm=document.getElementById(elmOrIdx)
    }
    let style=window.getComputedStyle(elm)
    while(elm.parentElement&&style.backgroundColor=='rgba(0, 0, 0, 0)'){
        elm=elm.parentElement
        style=window.getComputedStyle(elm)
    }
    let bg=style.backgroundColor
    if(bg=='rgba(0, 0, 0, 0)'){return false}
    return true
}
function limitFrameRate(idx,func,framerate){
    window.ISOK=window.ISOK||{}
    if(window.ISOK[idx]===undefined){
        window.ISOK[idx]=true
    }
    if(!window.ISOK[idx]){return}
    window.ISOK[idx]=false
    func()
    setTimeout(()=>{
        window.ISOK[idx]=true
    },framerate)
}
function formatDate(date,includeTime,includeMs){
    let y=date.getFullYear()
    let m=(date.getMonth()+1).toString().padStart(2,'0')
    let d=date.getDate().toString().padStart(2,'0')
    let ss=[y,m,d].join('-')
    if(includeTime){
        let h=date.getHours().toString().padStart(2,'0')
        let m=date.getMinutes().toString().padStart(2,'0')
        let s=date.getSeconds().toString().padStart(2,'0')
        ss+=' '+[h,m,s].join(':')
    }
    if(includeMs){
        let ms=date.getMillseconds().toString().padStart(3,'0')
        ss+='.'+ms
    }
    return ss
}