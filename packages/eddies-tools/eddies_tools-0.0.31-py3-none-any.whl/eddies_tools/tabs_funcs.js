window.TABS={
    toggleTab:function(ev){
        let button=ev.target.closest('button')
        let buttonRow=button.parentElement
        let buttons=Array.from(buttonRow.children)
        let jx=indexOf(buttons,button)
        for(let button of buttons){
            removeClass(button,'actv')
        }
        addClass(button,'actv')
        let tabCont=buttonRow.nextSibling
        let tabs=tabCont.children
        for(let tab of tabs){
            tab.style.display='none'
        }
        tabs[jx].style.display='flex'
    }
}