var a=1
function help()
{
  if(a==1)
  {
    chrome.tabs.getSelected(null,function(tab) {
      $("#p1").text(tab.url);
      $(".button").text("Go")
    })
    a++;
    return;
  }
  var tablink=$("#p1").html()
  tablink=tablink.split('=')
  // alert(tablink[1])
  var serverurl="http://127.0.0.1:5000/test"
  
  $.get(serverurl, {
      "url": tablink[1]
  },function(data, status) {
    // alert(data.answer);
    // console.log(data)
    var {neutral,positive,negative}=data;
    $("#p1").text(`No of Neutral Comments are ${neutral} , Positive Comments are ${positive}, Negative Comments are ${negative}`);
    var img = document.createElement('img');
    img.src = `C:/Users/hp/Desktop/ytExtension/server/piecharts/${tablink[1]}.png`;
    img.height=200
    img.width=300
    document.getElementById('images').appendChild(img);
    var img2 = document.createElement('img');
    img2.src = `C:/Users/hp/Desktop/ytExtension/server/wordclouds/${tablink[1]}.png`;
    img2.height=200 
    img2.width=300 
    document.getElementById('images').appendChild(img2);
});

}


$(document).ready(function(){
   $("button").click(async function(){	
          await help();
          // // var tablink=document.getElementById("p1").innerText
          // var tablink=$("p1").html()
          // alert(tablink)
      });
});



