$(function () {
  // ============== 약 정보 메뉴바 ==============
  $(document).on('click', '.pill_menu li', function (e) {
    console.log("메뉴클릭");
    var $all_info = $(this).closest('#all_info');
    var $box_info = $all_info.find('.box_info');

    console.log('all_info', $all_info);
    console.log('box_info', $box_info);

    $(this).parent().find('.state').removeClass('state');
    $(this).addClass('state');

    var index = $(this).index();
    console.log(index);

    $box_info.find('.current').removeClass('current');
    $box_info.find('div:nth-child(' + (index + 1) + ')').addClass('current');
  });
  
  $.ajax({
    type: "GET",
    url: "/medicine_detail/",
    dataType: "json",
    success: function (json) {
        setInfo(json)
    },

    error: function (xhr, errmsg, err) {
      console.log(xhr)
      console.log(errmsg)
      console.log(err)
      console.log("실패");
    }
  });
});

function get_infos(infos) {
  console.log(infos)
  console.log(infos.length)

  var info = [];
  for (var i = 0; i < infos.length; i++) {
    info.push(infos[i]);
  }
  info = info.join('<br>');
  return info
}

function setInfo(json) {
  html = '';
  console.log("성공");
  // 분석된 약품 없을시 처리
  console.log(json)
  if (json['message']) {
    console.log('if문')
    alert(json['message']);
  } else {
    html += '<div class="pill_menu"><ul>';
    console.log()
    var keys = Object.keys(json).slice(1,); // context에 names를 추가했기 떄문에, keys 생성시 인덱싱 필요

    for (var i = 0; i < keys.length; i++) {
      // 분석 후 처음보여주는 알약정보메뉴를 나타내기 위함.
      if (i == 0) {
        html += '<li class="pill_name state">' + json[i][0]['약품명'] + '</li>';
      } else {
        html += '<li class="pill_name">' + json[i][0]['약품명'] + '</li>';
      }
    }
    html += '</ul></div>';

    // 알약 정보 리스트
    html += '<div class="box_info">';
    for (var i = 0; i < keys.length; i++) {
      if (i != 0) {
        html += '<div class="pill_info"><h6>약품명</h6><p>' + json[i][0]['약품명'] + '</p><br>';
      } else {
        html += '<div class="pill_info current"><h6>약품명</h6><p>' + json[i][0]['약품명'] + '</p><br>';
      }
      html += '<h6>약품 회사</h6><p>' + json[i][0]['약품회사'] + '</p><br>';
      html += '<h6>효능효과</h6><p>' + get_infos(json[i][0]['효능효과']) + '</p><br>';
      html += '<h6>사용상주의사항</h6><p>' + get_infos(json[i][0]['사용상주의사항']) + '</p><br>';
      html += '</div>';
    }
    html += '</div>';

    $('#all_info').html(html);

  }
}

