// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Do not like repitive code, but I am lazy
function updateOntrack(k) {
  const projectnumber = k.id;
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/ontrack/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    badge = document.getElementById(k.id.concat("_status_badge"));
    badge.className = "btn btn-sm badge-success";
    badge.innerHTML = "Updated - On Track";
    }

  var data = new FormData();
  data.append('projectnumber', projectnumber);
  request.send(data);
}

function updateOnwatch(k) {
  const projectnumber = k.id;
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/onwatch/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    badge = document.getElementById(k.id.concat("_status_badge"));
    badge.className = "btn btn-sm badge-warning";
    badge.innerHTML = "Updated - On Watch";
    }

  var data = new FormData();
  data.append('projectnumber', projectnumber);
  request.send(data);
}

function updateOfftrack(k) {
  const projectnumber = k.id;
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/offtrack/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    badge = document.getElementById(k.id.concat("_status_badge"));
    badge.className = "btn btn-sm badge-danger";
    badge.innerHTML = "Updated - Off Track";
    }

  var data = new FormData();
  data.append('projectnumber', projectnumber);
  request.send(data);
}

function copyToClipboard(element) {
  console.log('Working'); 
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
}
