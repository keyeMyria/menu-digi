
$(document).ready(function() {
    load_records()
});

socket.onmessage = function(e){
    console.log("message",e)
    var orderDetails = e.data
    load_records()
    M.toast({html: 'New order added!',displayLength:15000})
  }

var load_records = function(){
    $.ajax({
      type: "GET",
      url: "/restaurant/orders-records?&restaurant="+appConfig.restaurantName,
      processData: false,
      contentType: "application/json",
      data: '',
      success: function(r) {
          r = JSON.parse(r)
                    
          if(r.Status==="Error"){
            // console.log(r)
            $("#rec-items").empty()
            $("#rec-items").append(`
                          <tr class="tr-shadow">
                          <td>No record found</td>
                          <td></td>
                          <td></td>
                          <td></td>
                      </tr>
                      <tr class="spacer"></tr>`
                        )
          }
          else{
            // console.log(r)
            $("#rec-items").empty()
            for (var i = 0; i < r.length; i++) {
              $("#rec-items").append(`
            <tr class="tr-shadow">
                <td>`+r[i].table+`</td>
                <td>`+r[i].contact+`</td>
                <td>`+r[i].cost+`</td>
                <td>`+r[i].time+`</td>
                <td>
                    <a class="au-btn au-btn-icon au-btn--blue" href="/restaurant/order-item/`+appConfig.restaurantName+`/`+r[i].id+`">
                        Open
                    </a>
                </td>
            </tr>
            <tr class="spacer"></tr>`
              )
          }
          }   
   },
      error: function(r){
        
          if(r.Status==="Error"){
            console.log(r)
            $("#rec-items").empty()
            $("#rec-items").append(`
                          <tr class="tr-shadow">
                          <td>No record found</td>
                          <td></td>
                          <td></td>
                          <td></td>
                      </tr>
                      <tr class="spacer"></tr>`
                        )
          }
  
      }
  });
  }
  
    
  
  // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  
  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
  }
  
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
  