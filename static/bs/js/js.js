// ================= 웹캠 ====================
var myVideoStream = document.getElementById('myVideo')     // make it a global variable
var myStoredInterval = 0
var camOn = false;

function getVideo(){
  if(!camOn){
    var ocr_imgbox = $('#ocr_imgbox')
    ocr_imgbox.html('<video id="myVideo"></video>')
    myVideoStream = document.getElementById('myVideo')
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getMedia({video: true, audio: false},
      
      function(stream) {
        camOn = true;
        myVideoStream.srcObject = stream;   
        myVideoStream.play();
    }, 
                     
    function(error) {
      alert('webcam not working');
    });
  }
}
function restart(){
  if(!camOn){
    camOn = true;
    var ocr_imgbox = $('#ocr_imgbox')
    ocr_imgbox.html('<video id="myVideo"></video>')
    myVideoStream = document.getElementById('myVideo')
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getMedia({video: true, audio: false},
                     
    function(stream) {
        myVideoStream.srcObject = stream;   
        myVideoStream.play();
        $("#all_info").empty();
    }, 
                     
   function(error) {
     alert('webcam not working');
    });
  }
}

function takeSnapshot() {
  console.log(camOn);

  if(camOn){
    var ocr_imgbox = $('#ocr_imgbox');
    ocr_imgbox.html('<canvas id="myCanvas" width="1920" height="1080"></canvas>');
    var myCanvasElement = document.getElementById('myCanvas');
    var myCTX = myCanvasElement.getContext('2d');
    myCTX.drawImage(myVideoStream, 0, 0, myCanvasElement.width, myCanvasElement.height);
    camOn = false;
  }
}

// ================ 알약 info =================
$(function(){
  $("#ocr_start").click(function(){
    console.log("클릭됌");
  
		$.ajax({
      type: "GET",
      url: "/ocr_start/",
      dataType: "json", 
      success:function(json){
        html = '';
        console.log("성공");

        html += '<div><ul>';
        var keys = Object.keys(json);
        console.log(json)
        console.log(keys)
        console.log(json[keys[1]][0]['약품명'])

        for (var i=0; i<keys.length; i++) {
          if(i == 0){
            html += '<li class="pill_name state">' + keys[i] + '</li>';
          } else{
            html += '<li class="pill_name">' + keys[i] + '</li>';
          }
        }
        html += '</ul></div>';
        for (var i=0; i<keys.length; i++) {
          html += '<div id="pill_info"><h6>약품명</h6><p>' + json[keys[i]][0]['약품명'] + '</p>';
          html += '<h6>약품 회사</h6><p>' + json[keys[i]][0]['약품 회사'] + '</p>';
          // html += '<h6>효능효과</h6><p>' + json[keys[i]]['효능효과'] + '</p>';
          html += '</div>';
        }

        $('#all_info').html(html);
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr)
          console.log(errmsg)
          console.log(err)
          console.log("실패"); 
      }
		})
	});
});
