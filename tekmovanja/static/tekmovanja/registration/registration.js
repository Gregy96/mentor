function reg() {
    alert("dela")
    //spr pove ali naj se izvede ajax klic ali ne
    let err = false;

    //pridobi podatke
    let Ime=document.getElementById("Ime").value;
    let Priimek=document.getElementById("Priimek").value;
    let UpIme=document.getElementById("UpIme").value;
    let email=document.getElementById("email").value;
    let sola=document.getElementById("sola").value;
    let geslo=document.getElementById("geslo").value;
    let geslo_ponovno=document.getElementById("geslo_ponovno").value;
    let status=document.getElementById("status");

    if(Ime.length == 0 || Priimek.length == 0 || UpIme.length == 0 || email.length == 0 || geslo.length == 0 || geslo_ponovno.length == 0)
    {  
        alert("Izpolni vsa polja")
        err = true;
    }

    if(geslo != geslo_ponovno)
    {
        status.innerHTML="Gesli se ne ujemata";
        status.style.color="red";
        err = true;
    }

    
    if(err == false)
    {
        //alert("pride")
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
                url:"register/",
                data: {
                    'Ime': Ime,
                    'Priimek': Priimek,
                    'UpIme': UpIme,
                    'email': email,
                    'sola': sola,
                    'geslo': geslo,
                },
                success: function(data){
                    //alert(data)
                    if(data == '0'){
                        status.innerHTML="Registracija uspešna";
                        status.style.color="green";
                    }
                    if(data == '1')
                    {
                        status.innerHTML="Težava pri procesiranju parametrov";
                        status.style.color="red";
                    }
                    if(data == '2')
                    {
                        status.innerHTML="Šole ni v sistemu, preverite črkovanje.";
                        status.style.color="red";
                    }
                    if(data == '3')
                    {
                        status.innerHTML="Uporabniško ime je že zasedeno.";
                        status.style.color="red";
                    }
                }
        });
        
    }
    }
 
    //prikazuj šole ki ustrezajo vzorcu
    //$('#sol').bind('input', function(){
    /*    if ($("#sol").val().length < 1)
        {
            console.log("Ne zahtevaj klica");
        }
        else
        {*/
           // sola=document.getElementById("sol").value.toUpperCase();
            //alert(sola)
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
            
            //alert("zacenjam s ajax klicem");
            //ajax klic za avtentikacijo
            $.ajax({
                    type:"POST",
                    url:"izpis_sola/",
                    data: {
                        'sola' : 'test',
                    },
                    success: function(data){
                        //alert(data)
                        var jsonData = JSON.parse(data);

                        //$('#sola').empty();
                        for (var i = 0; i < jsonData.length; i++) {
                            let sola = jsonData[i];
                            //$('#sola').append('<option value="'+sola.Ime_Sola+'">'+sola.Ime_Sola+'</option>');
                            let select = document.getElementById("sola");
                            select.options[select.options.length] = new Option(sola.Ime_Sola,sola.Ime_Sola);
                            /*var option = document.createElement('option');
                            option.value = sola;
                            $('#sola').append(option);
                            */
                            //console.log(sola.Ime_Sola);
                        }
                    }
            });
            //console.log($("#sola").val());
        //}//}//);                                                                                                          