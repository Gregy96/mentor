function prijava(id_tek,id_men) {
    
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
            url:"tek_prijava",
            data: {
                   'id_tek': id_tek,
                   'id_men': id_men,
            },
            success: function(data){
                if(data == '0')
                    alert("Usprešno ste se vpisali")
                    location.reload();
                if(data == '1')
                    alert("Napaka")
            }
       });
    
    
    }
    
    
    function odjava(id_tek,id_men) {
    
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
                url:"tek_odjava",
                data: {
                       'id_tek': id_tek,
                       'id_men': id_men,
                },
                success: function(data){
                    if(data == '0')
                        alert("Usprešno ste se izpisali")
                        location.reload();
                    if(data == '1')
                        alert("Napaka")
                }
           });
        
        
        }
        
        
        