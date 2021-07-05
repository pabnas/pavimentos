function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function enviar()
{ 
  url = 'validarlogin';
  $.ajax(url, {
    type: "POST",
    data:{
        "correo": $("#login").val(),
        "password": $("#password").val(),
    },
    error: function(data){
      console.log("");
    },
    success: function(data)
    {
      document.cookie = "user="+$("#login").val()+ ";  max-age=86400; path=/";
      if(data.url != "/") {
        window.location = data.url;
      }
      else {
        alert(data.msg);
      }
    }
  });
}

$(document).ready(function() {
  document.addEventListener('keydown', onKeyDown);
});

function onKeyDown(e) {
  //console.log(e.code);
  if(e.code=="Enter" && $("#login").val()!="" && $("#password").val()!="")
  {
    enviar();
  }
}
