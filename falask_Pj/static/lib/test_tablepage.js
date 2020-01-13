function firstPage(){
    hide();
    currPageNum = 1;
    showCurrPage(currPageNum);
    showTotalPage();

    //console.log("pageNum: "+pageNum);
    if(pageNum>1)
        for(var i=0;i<pageRowIndexArr[1];i++){
        blockTable.rows[i].style.display = "";
    }else for(var i=0;i<blockTable.rows.length;i++){
        blockTable.rows[i].style.display = "";
    }

    if(pageNum>1){
        firstText();
        preText();
        nextLink();
        lastLink();
    }
}

function prePage(){
    hide();
    currPageNum--;
    showCurrPage(currPageNum);
    showTotalPage();

    currPageIndex=currPageNum-1;
    console.log("currPageIndex: "+currPageIndex);
    console.log("pageRowIndexArr["+currPageIndex+"]: "+pageRowIndexArr[currPageIndex]);
    console.log("pageRowIndexArr["+(currPageIndex+1)+"]: "+pageRowIndexArr[currPageIndex+1]);
    if(currPageNum!=1)
        for(var i=pageRowIndexArr[currPageIndex];i<pageRowIndexArr[currPageIndex+1];i++){
            blockTable.rows[i].style.display = "";
        }
    else
        for(var i=0;i<pageRowIndexArr[currPageIndex+1];i++){
            blockTable.rows[i].style.display = "";
        }

    if(1 == currPageNum){
        firstText();
        preText();
        nextLink();
        lastLink();
    }else if(pageNum == currPageNum){
        preLink();
        firstLink();
        nextText();
        lastText();
    }else{
        firstLink();
        preLink();
        nextLink();
        lastLink();
    }
}

function nextPage(){
    hide();
    currPageNum++;
    showCurrPage(currPageNum);
    showTotalPage();

    currPageIndex=currPageNum-1;
    console.log("currPageIndex: "+currPageIndex);
    console.log("pageRowIndexArr["+currPageIndex+"]: "+pageRowIndexArr[currPageIndex]);
    if(currPageNum!=pageNum)
        for(var i=pageRowIndexArr[currPageIndex];i<pageRowIndexArr[currPageIndex+1];i++){
            blockTable.rows[i].style.display = "";
        }
    else
        for(var i=pageRowIndexArr[currPageIndex];i<rowsLength;i++){
            blockTable.rows[i].style.display = "";
        }

    if(1 == currPageNum){
        firstText();
        preText();
        nextLink();
        lastLink();
    }else if(pageNum == currPageNum){
        preLink();
        firstLink();
        nextText();
        lastText();
    }else{
        firstLink();
        preLink();
        nextLink();
        lastLink();
    }
}

function lastPage(){
    hide();
    currPageNum = pageNum;
    showCurrPage(currPageNum);
    showTotalPage();

    currPageIndex=currPageNum-1;
    console.log("currPageIndex: "+currPageIndex);
    console.log("pageRowIndexArr["+currPageIndex+"]: "+pageRowIndexArr[currPageIndex]);
    for(var i=pageRowIndexArr[currPageIndex];i<rowsLength;i++){
        blockTable.rows[i].style.display = "";
    }

    firstLink();
    preLink();
    nextText();
    lastText();
}

function showCurrPage(cpn){
    currPageSpan.innerHTML = cpn;
}

function showTotalPage(){
    pageNumSpan.innerHTML = pageNum;
}

//隐藏所有行
function hide(){
    for(var i = 1; i < rowsLength; i ++){
        blockTable.rows[i].style.display = "none";
    }
}

//控制首页等功能的显示与不显示
function firstLink(){firstSpan.innerHTML = "<a href='javascript:firstPage();'>首页</a>";}
function firstText(){firstSpan.innerHTML = "首页";}

function preLink(){preSpan.innerHTML = "<a href='javascript:prePage();'>上一页</a>";}
function preText(){preSpan.innerHTML = "上一页";}

function nextLink(){nextSpan.innerHTML = "<a href='javascript:nextPage();'>下一页</a>";}
function nextText(){nextSpan.innerHTML = "下一页";}

function lastLink(){lastSpan.innerHTML = "<a href='javascript:lastPage();'>末页</a>";}
function lastText(){lastSpan.innerHTML = "末页";}
