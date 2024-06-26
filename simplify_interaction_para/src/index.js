
/**
 * 获取选中文本
 */
function getRange(){
  var range = new Range(window.document);

  var sel = window.getSelection();
  if (sel && sel.rangeCount) {
    var firstRange = sel.getRangeAt(0);
    var lastRange = sel.getRangeAt(sel.rangeCount - 1);
    range.setStart(firstRange.startContainer, firstRange.startOffset)
      .setEnd(lastRange.endContainer, lastRange.endOffset);
  }
  // console.log(range)
  
  return range
}

/**
   * 用元素替换被选中的文本
   */
function replaceSelectedStrByEle(className){
  var range = getRange();
 
  range.applyInlineStyle('i', {
    class: className
  });
  // range.removeInlineStyle('i',styles['nite-writer-pen'])

}
function replaceSelectedStrByEle_1(className){
  var range = getRange();
 
  range.removeInlineStyle('i',  className);
  
}




function addUnderline(){
  replaceSelectedStrByEle('custom-underline')
}

function enableNiteWriterPen(){
  replaceSelectedStrByEle('nite-writer-pen')
}

function removeEffect(){
  replaceSelectedStrByEle_1('nite-writer-pen')
  replaceSelectedStrByEle_1('nite-writer-pen_1')
  replaceSelectedStrByEle_1('nite-writer-pen_2')
  replaceSelectedStrByEle_1('nite-writer-pen_3')
}
function getHighlightedText() {
  var highlightedElements = document.querySelectorAll('.nite-writer-pen');
  var highlightedText = [];
  
  highlightedElements.forEach(function(element) {
    highlightedText.push(element.textContent);
  });
  console.log(highlightedText);

  // return highlightedText;
}
function getFirstHighlighterText(){
  var spanElement = document.getElementById('span1');
    var highlightedElements = spanElement.querySelectorAll('.nite-writer-pen, .nite-writer-pen_2');
    var highlightedText = [];
    
    highlightedElements.forEach(function(element) {
        highlightedText.push(element.textContent);
    });

    console.log(highlightedText);
}
// function highlightPartialText(fullText, partialText) {
//   var regex = new RegExp(partialText, 'g');
//   var highlightedText = fullText.replace(regex, '<span class="highlight">' + partialText + '</span>');
//   return highlightedText;
// }
