
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


function changestatus(b) {
  const projectnumber = b.id;
  const type = b.name;
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/switch/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    if (b.value == "Yes") {
      b.value = "No";
      b.className = "btn btn-success";
    } else {
      b.value = "Yes";
      b.className = "btn btn-warning";
    }
  }
  var data = new FormData();
  data.append('projectnumber', projectnumber);
  data.append('type', type);
  request.send(data);
}

function updateproject(k) {
  const projectnumber = k.id;
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/update/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    }

  var data = new FormData();
  data.append('projectnumber', projectnumber);
  request.send(data);

}
