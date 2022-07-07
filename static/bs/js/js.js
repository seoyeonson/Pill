// ================= 웹캠 ====================
var myVideoStream = document.getElementById('myVideo')
var myStoredInterval = 0

// 카메라와 캡쳐 상태를 나타내는 변수
var camOn = false;
var snapOk = false;

function getVideo(){
  // 카메라가 꺼져있을 경우에만 카메라를 켤 수 있음.
  if(!camOn){
    // var ocr_imgbox = $('#ocr_imgbox')
    // ocr_imgbox.html('<video id="myVideo"></video>')
    myVideoStream = document.getElementById('myVideo')
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getMedia({video: true, audio: false},
      
      function(stream) {
        // 카메라 상태 켜짐으로 변경.
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
  // 카메라가 꺼져있고, 캡쳐가능한 상태에서 다시시작 가능.
  if(!camOn && snapOk){
    // 카메라를 키고 캡쳐가 되어있지 않은 상태로 변경.
    camOn = true;
    snapOk = false;
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
  // console.log(camOn);

  // 카메라가 켜져있고, 캡쳐되어있지 않은 상태에서만 캡쳐 가능.
  if(camOn && !snapOk){
    // video를 canvas 로 변경
    console.log("실행됌");
    
    var ocr_imgbox = $('#ocr_imgbox');
    ocr_imgbox.html('<canvas id="myCanvas" width="1920" height="1080"></canvas>');
    
    // 캡쳐된 이미지를 넣기.
    var myCanvasElement = document.getElementById('myCanvas');
    var myCTX = myCanvasElement.getContext('2d');
    
    myCTX.drawImage(myVideoStream, 0, 0, myCanvasElement.width, myCanvasElement.height);
    
    console.log(myCTX);
    
    // 캡쳐 완료 후, 카메라가 꺼지고, 캡쳐된 상태로 변경.
    camOn = false;
    snapOk = true
  }
}

// ================ 알약 info =================
$(function(){
  // ============== 처방전 및 알약 분석 ==============
  $("#ocr_start").click(function(){
    // console.log("클릭됌");   
    html2canvas($('#myCanvas').get(0)).then(function (canvas){
        var data = canvas.toDataURL();
        console.log(data);

        // django 서버에서 알약 정보 가져오기.
        // 캡쳐가 된 상태에서만 분석 가능.
        if(snapOk){
          $.ajax({
            type: "POST",
            url: "/ocr_start/",
            data : {data:data},
            dataType: "json", 
            success:function(json){
              html = '';
              console.log("성공");
      
              html += '<div class="pill_menu"><ul>';
              var keys = Object.keys(json);
      
              for (var i=0; i<keys.length; i++) {
                // 분석 후 처음보여주는 알약정보메뉴를 나타내기 위함.
                if(i == 0){
                  html += '<li class="pill_name state">' + keys[i] + '</li>';
                } else{
                  html += '<li class="pill_name">' + keys[i] + '</li>';
                }
              }
              html += '</ul></div>';

              html += '<div class="box_info">';
              for (var i=0; i<keys.length; i++) {
                if(i != 0){
                  html += '<div class="pill_info"><h6>약품명</h6><p>' + json[keys[i]][0]['약품명'] + '</p><br>';
                }else{
                  html += '<div class="pill_info current"><h6>약품명</h6><p>' + json[keys[i]][0]['약품명'] + '</p><br>';
                }
                html += '<h6>약품 회사</h6><p>' + json[keys[i]][0]['약품 회사'] + '</p><br>';
                html += '<h6>효능효과</h6><p>' + get_infos(json[keys[i]][0]['효능효과']) + '</p><br>';
                html += '<h6>사용상주의사항</h6><p>' + get_infos(json[keys[i]][0]['사용상주의사항']) + '</p><br>';
                html += '</div>';
              }
              html += '</div>';
      
              $('#all_info').html(html);
            },
            error : function(xhr,errmsg,err) {
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
                console.log("실패"); 
            }
          })
        }else{
          alert("처방전 및 알약을 캡쳐해주세요.")
        }
        console.log($('.all_info .pill_menu > ul > li'));
      });


      // ============== 약 정보 메뉴바 ==============
      $(document).on('click', '.pill_menu li', function(e) {
          console.log("메뉴클릭");
          var $all_info = $(this).closest('#all_info');
          var $box_info = $all_info.find('.box_info');

          console.log('all_info', $all_info);
          console.log('box_info' ,$box_info);

          $(this).parent().find('.state').removeClass('state');
          $(this).addClass('state');
          
          var index = $(this).index();
          console.log(index);
          
          $box_info.find('.current').removeClass('current');
          $box_info.find('div:nth-child(' + (index + 1) + ')').addClass('current');
      });
      }
    )
});


// ============== 리스트로 된 정보 가져오기 ==============
function get_infos(infos){
  var info = [];
  for(var i = 0; i < infos.length; i++){
    info.push(infos[i]);
  }
  info = info.join('<br>');
  return info
}
