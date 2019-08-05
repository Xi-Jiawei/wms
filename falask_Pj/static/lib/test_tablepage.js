function test(){alert("测试");};

/*firstPage=function(){
    hide();
    currPageNum = 1;
    showCurrPage(currPageNum);
    showTotalPage();
    for(i = 1; i < pageCount + 1; i++){
        blockTable.rows[i].style.display = "";
    }

    firstText();
    preText();
    nextLink();
    lastLink();
};*/

var currentPageLastRowArrIndex;
var currentPageFirstRowArrIndex;
var currentPageLastRow;
var currentPageFirstRow;

function firstPage(){
    hide();
    currPageNum = 1;
    showCurrPage(currPageNum);
    showTotalPage();
    console.log(blockTable.rows);
    console.log(pageCount);
    /*for(i = 1; i < pageCount + 1; i++){
        console.log(i);
        console.log(blockTable.rows[i]);
        console.log(blockTable.rows[i].style);
        blockTable.rows[i].style.display = "";
    }*/
    var index=0;
    for(var i=0;i<rowCountArr.length;i++){
        index+=rowCountArr[i];
        if(index<=pageCount){
            for(var j=0;j<rowCountArr[i];j++) {
                blockTable.rows[index-rowCountArr[i]+j+1].style.display = "";
            }
        }else break;
    }
    currentPageLastRowArrIndex=i-1;
    currentPageFirstRowArrIndex=0;
    currentPageLastRow=index-rowCountArr[i];
    currentPageFirstRow=1;
    console.log("currentPageFirstRowArrIndex: "+currentPageFirstRowArrIndex);
    console.log("currentPageFirstRow: "+currentPageFirstRow);
    console.log("currentPageLastRowArrIndex: "+currentPageLastRowArrIndex);
    console.log("currentPageLastRow: "+currentPageLastRow);

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
    /*var firstR = firstRow(currPageNum);
    var lastR = lastRow(firstR);
    for(i = firstR; i < lastR; i++){
        blockTable.rows[i].style.display = "";
    }*/

    var index=0;
    for(var i=currentPageFirstRowArrIndex-1;i>=0;i--){
        index+=rowCountArr[i];
        if(index<=pageCount){
            for(var j=0;j<rowCountArr[i];j++) {
                blockTable.rows[currentPageFirstRow-1-(index-rowCountArr[i]+j)].style.display = "";
            }
        }else break;
    }
    currentPageLastRowArrIndex=currentPageFirstRowArrIndex-1;
    currentPageFirstRowArrIndex=i+1;
    currentPageLastRow=currentPageFirstRow-1;
    if(i>=0)currentPageFirstRow=currentPageFirstRow-(index-rowCountArr[i])+1;
    else currentPageFirstRow=currentPageFirstRow-index+1;
    console.log("currentPageFirstRowArrIndex: "+currentPageFirstRowArrIndex);
    console.log("currentPageFirstRow: "+currentPageFirstRow);
    console.log("currentPageLastRowArrIndex: "+currentPageLastRowArrIndex);
    console.log("currentPageLastRow: "+currentPageLastRow);

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
    /*var firstR = firstRow(currPageNum);
    var lastR = lastRow(firstR);
    for(i = firstR; i < lastR; i ++){
        blockTable.rows[i].style.display = "";
    }*/

    console.log("currentPageFirstRowArrIndex: "+currentPageFirstRowArrIndex);
    console.log("currentPageFirstRow: "+currentPageFirstRow);
    console.log("currentPageLastRowArrIndex: "+currentPageLastRowArrIndex);
    console.log("currentPageLastRow: "+currentPageLastRow);
    var index=0;
    for(var i=currentPageLastRowArrIndex+1;i<rowCountArr.length;i++){
        index+=rowCountArr[i];
        console.log("i:"+i);
        console.log("index: "+index);
        if(index<=pageCount){
            for(var j=0;j<rowCountArr[i];j++) {
                console.log("j:"+j);
                console.log(currentPageLastRow+index-rowCountArr[i]+j+1);
                blockTable.rows[currentPageLastRow+index-rowCountArr[i]+j+1].style.display = "";
            }
        }else break;
    }
    currentPageFirstRowArrIndex=currentPageLastRowArrIndex+1;
    currentPageLastRowArrIndex=i-1;
    currentPageFirstRow=currentPageLastRow+1;
    if(i<rowCountArr.length)currentPageLastRow=currentPageLastRow+index-rowCountArr[i];
    else currentPageLastRow=currentPageLastRow+index;
    console.log("currentPageFirstRowArrIndex: "+currentPageFirstRowArrIndex);
    console.log("currentPageFirstRow: "+currentPageFirstRow);
    console.log("currentPageLastRowArrIndex: "+currentPageLastRowArrIndex);
    console.log("currentPageLastRow: "+currentPageLastRow);

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
    /*var firstR = firstRow(currPageNum);
    for(i = firstR; i < numCount + 1; i++){
        blockTable.rows[i].style.display = "";
    }*/

    console.log("pageNum: "+pageNum);
    var index=0,pageN=1,pageRowCount=0;
    for(var i=0;i<rowCountArr.length;i++){
        index+=rowCountArr[i];
        console.log(index);
        //if(Math.floor(index/pageCount)+1>pageN)pageN=Math.floor(index/pageCount)+1;
        pageRowCount+=rowCountArr[i];
        console.log("pageRowCount: "+pageRowCount);
        if(pageRowCount>pageCount) {
            pageN += 1;
            pageRowCount=rowCountArr[i];
        }
        console.log("pageN: "+pageN);
        console.log(pageN==pageNum);
        if(pageN==pageNum){
            for(var j=0;j<rowCountArr[i];j++) {
                blockTable.rows[index-rowCountArr[i]+j+1].style.display = "";
            }
        }else currentPageFirstRowArrIndex=i;
    }
    currentPageFirstRowArrIndex+=1;
    currentPageLastRowArrIndex=rowCountArr.length-1;
    for(var i=currentPageFirstRowArrIndex;i<=currentPageLastRowArrIndex;i++)currentPageFirstRow=index-rowCountArr[i];
    currentPageFirstRow+=1;
    currentPageLastRow=rowCount-1;
    console.log("currentPageFirstRowArrIndex: "+currentPageFirstRowArrIndex);
    console.log("currentPageFirstRow: "+currentPageFirstRow);
    console.log("currentPageLastRowArrIndex: "+currentPageLastRowArrIndex);
    console.log("currentPageLastRow: "+currentPageLastRow);

    firstLink();
    preLink();
    nextText();
    lastText();
}

// 计算将要显示的页面的首行和尾行
function firstRow(currPageNum){
    return pageCount*(currPageNum - 1) + 1;
}

function lastRow(firstRow){
    var lastRow = firstRow + pageCount;
    if(lastRow > numCount + 1){
        lastRow = numCount + 1;
    }
    return lastRow;
}

function showCurrPage(cpn){
    currPageSpan.innerHTML = cpn;
}

function showTotalPage(){
    pageNumSpan.innerHTML = pageNum;
}

//隐藏所有行
function hide(){
    /*for(var i = 1; i < numCount + 1; i ++){
        blockTable.rows[i].style.display = "none";
    }*/
    for(var i = 1; i < rowCount; i ++){
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
