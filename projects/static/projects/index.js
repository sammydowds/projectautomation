// using jQuery
//TODO note, this is bad design on the scheduled functions - should not isolate?
function nowScheduled(element, proj_num, milestone) {
  const projectnumber = proj_num;
  console.log(milestone);
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/scheduled/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    card = document.getElementById(element.id.concat('_status'));
    card.className = "badge badge-success";
    card.innerHTML = "Scheduled";
    }
  var data = new FormData();
  data.append('projectnumber', projectnumber);
  data.append('milestone', milestone);
  request.send(data);
}

function notScheduled(element, proj_num, milestone) {
  const projectnumber = proj_num;
  console.log(milestone);
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/notscheduled/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    card = document.getElementById(element.id.concat('_status'));
    card.className = "badge badge-warning";
    card.innerHTML = "Not Scheduled";
    }
  var data = new FormData();
  data.append('projectnumber', projectnumber);
  data.append('milestone', milestone);
  request.send(data);
}

function completeMilestone(k) {
  console.log("TEST");
  const projectnumber = k.id;
  const milestone = k.value;
  const request = new XMLHttpRequest();
  request.open('POST', '/projects/milestonecomplete/');
  var csrftoken = getCookie('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);

  request.onload = function(){
    }

  var data = new FormData();
  data.append('projectnumber', projectnumber);
  data.append('milestone', milestone);
  request.send(data);
  console.log(projectnumber, milestone);
  }


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
    card = document.getElementById(k.id.concat("_card_header"));
    badge.className = "badge badge-sm badge-success text-nowrap";
    card.className = "card-header bg-success text-white";
    badge.innerHTML = "On Track";
    card.innerHTML = "Updated To On Track";
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
    card = document.getElementById(k.id.concat("_card_header"));
    card.className = "card-header bg-warning";
    card.innerHTML = "Updated To On Watch";
    badge = document.getElementById(k.id.concat("_status_badge"));
    badge.className = "badge badge-sm badge-warning text-nowrap";
    badge.innerHTML = "On Watch";
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
    card = document.getElementById(k.id.concat("_card_header"));
    card.className = "card-header bg-danger text-white";
    card.innerHTML = "Updated To Off Track";
    badge = document.getElementById(k.id.concat("_status_badge"));
    badge.className = "badge badge-sm badge-danger text-nowrap";
    badge.innerHTML = "Off Track";
    }

  var data = new FormData();
  data.append('projectnumber', projectnumber);
  request.send(data);
}
