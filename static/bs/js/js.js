// ================= 웹캠 ====================
var myVideoStream = document.getElementById('myVideo')     // make it a global variable
var myStoredInterval = 0

function getVideo(){
  navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
  navigator.getMedia({video: true, audio: false},
                   
  function(stream) {
      myVideoStream.srcObject = stream;   
      myVideoStream.play();
  }, 
                   
  function(error) {
    alert('webcam not working');
  });
}
function restart(){
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

function takeSnapshot() {
 var ocr_imgbox = $('#ocr_imgbox')
 ocr_imgbox.html('<canvas id="myCanvas" width="1920" height="1080"></canvas>')
 var myCanvasElement = document.getElementById('myCanvas');
 var myCTX = myCanvasElement.getContext('2d');
 myCTX.drawImage(myVideoStream, 0, 0, myCanvasElement.width, myCanvasElement.height);
}

// function takeAuto() {
//   takeSnapshot() // get snapshot right away then wait and repeat
//   clearInterval(myStoredInterval)
//   myStoredInterval = setInterval(function(){                                                                                         
//      takeSnapshot()
//  }, document.getElementById('myInterval').value);        
// }


// ================ 분석 =================
function ocr_start(){
  // 분석해서 name들을 리턴한다.
  return '종근당염산에페드린정'
}
// ================ 알약 info =================
// https://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem?serviceKey=aS44rJLF1zAyKGhSpnEpW5PMzxPKl0lbazmPlGKUfvYqYWQY37xmDvJmCBjco6mtNWiwUfIbBDZygIEzFmJHHg%3D%3D&item_name=%EC%A2%85%EA%B7%BC%EB%8B%B9%EC%97%BC%EC%82%B0%EC%97%90%ED%8E%98%EB%93%9C%EB%A6%B0%EC%A0%95&entp_name=(%EC%A3%BC)%EC%A2%85%EA%B7%BC%EB%8B%B9&item_permit_date=19550117&pageNo=1&numOfRows=3&bar_code=8806433032005&item_seq=195500002&start_change_date=20151216&end_change_date=20160101&order=Y
var api_key = "NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki%2FrukB%2BuBNnRNn3w%2BCqhYPd6HiH28HI9hyih5KppfWIC%2FN3w%3D%3D";
// var api_key = "NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki/rukB+uBNnRNn3w+CqhYPd6HiH28HI9hyih5KppfWIC/N3w==";

$(function(){
  $("#ocr_start").click(function(){
    var pillNm = ocr_start();
    console.log(pillNm);
    
    // http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem?serviceKey=NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki%2FrukB%2BuBNnRNn3w%2BCqhYPd6HiH28HI9hyih5KppfWIC%2FN3w%3D%3D&item_name=종근당염산에페드린정
    var req_url = "http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem?serviceKey=" + api_key + "&item_name=" + pillNm;
    // req_url = decodeURIComponent(req_url);
    // console.log(req_url)

		$.ajax({
			url: req_url,
      headers: {
        'Access-Control-Allow-Origin': req_url,
      },
			type: "GET",
      cache: false,
			success: function(data, status){
				if(status == "success") parseXML(data);
			},
      complete: function(data){
        console.log("실행");
      },
      error:function(request, status, error){
        console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
      },
		})

	});
});

function parseXML(xmlDOM) {
	$(xmlDOM).find("item").each(function(){
    console.log("들어옴");
		value = $(this).find("MATERIAL_NAME").text();
    console.log(value);
	});


	$("#pill_info").html(value);
}
