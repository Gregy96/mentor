function login() {


//pridobi podatke iz username in pss
let usr=document.getElementById("usr").value;
let pss=document.getElementById("pss").value;
let status=document.getElementById("status");

//da ne prihaja do CSRFToken errorja(poslati ga moramo prej drugače ne deluje)   
$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
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
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});


//ajax klic za avtentikacijo
$.ajax({
        type:"POST",
        url:"auth/",
        data: {
               'usr': usr,
               'pss': pss,
        },
        success: function(data){
            if(data == '0')
                window.location.replace("index")
            if(data == '1')
                status.innerHTML="Vnesi up. ime ali geslo";
            if(data == '2')
                status.innerHTML="Nepravilno geslo";
            if(data == '3')
                status.innerHTML="Uporabnik "+usr+" ne obstaja"
        }
   });


}


