from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
#from django.contrib.auth.hashers import make_password
from passlib.hash import pbkdf2_sha256
from django.db import connection
from .models import Sola
from .models import Mentor
from .models import Tekmovanje
from .models import Sodeluje

def index(request):
    mentor_id = request.session.get('id', -1)

    #preverjaj sejo
    if not Mentor.objects.filter(ID_Mentor=mentor_id).exists() or mentor_id == -1:
        return HttpResponse("Nimate veljavne seje, prosim prijavite se se enkrat")
        
    mentor = Mentor.objects.filter(ID_Mentor=mentor_id).values()

    #pridobi id sole od mentorja
    sola_id=mentor.first()["sola_id"]

    # pridobi ime šole
    sola = Sola.objects.filter(ID_Sola=sola_id).values().first()["Ime_Sola"]

    #pridobi vse mentorje ki hodijo na isto šolo
    mentorji=Mentor.objects.filter(sola_id=sola_id).values()

    #mentorjem dodaj še vsa tekmovanja na katera so vpisani
    for m in mentorji:
        tmp = ""
        sodeluje=Sodeluje.objects.filter(Mentor_id=m["ID_Mentor"]).values()
        if(len(sodeluje) > 0):
            for s in sodeluje:
                tmp+=Tekmovanje.objects.filter(ID_Tekmovanje=s["Tekmovanje_id"]).values("Ime_Tekmovanje").first()["Ime_Tekmovanje"]+"-"
        else:
            tmp=0

        #če je mentor prijavljen mu dodaj seznam tekmovanj na katera je prijavaljen, če ne pa dodaj 0
        if tmp == 0:
            m["tekmovanja"]=0
        else:
            m["tekmovanja"]=tmp.split("-")
            m["tekmovanja"].pop()

    #ta del kode služi za izpis mentorjev kateri morajo biti še avtenticirani
    

    context = {'ime': mentor.first()["UpIme"],'sola':sola,'mentorji':mentorji}

    return render(request, 'tekmovanja/index.html', context)

def login(request):
    
    if request.session.get('id', None) != None:
        del request.session['id']

    return render(request, 'tekmovanja/login.html')


def registration(request):
    return render(request, 'tekmovanja/registration.html')

def tekmovanja(request):
    mentor_id = request.session.get('id', -1)
    

    #preveri sejo
    if not Mentor.objects.filter(ID_Mentor=mentor_id).exists() or mentor_id == -1:
        return HttpResponse("Nimate veljavne seje, prosim prijavite se se enkrat")
    
    #naloži vsa tekmovanja 
    sez_tek = Tekmovanje.objects.order_by()

    #za vsako tekmovanje preveri ali je mentor že prijaveljen na njega
    sez=[]
    for t in sez_tek:
        if Sodeluje.objects.filter(Tekmovanje_id=t.ID_Tekmovanje,Mentor_id=mentor_id).exists():
            t.sodeluje="0"
        else:
            t.sodeluje="1"

    context = {'sez_tek': sez_tek,'ze_sodeluje':sez,'id':mentor_id}

    return render(request, 'tekmovanja/tekmovanja.html', context)

def profil(request):
    mentor_id = request.session.get('id', -1)
    
    if not Mentor.objects.filter(ID_Mentor=mentor_id).exists() or mentor_id == -1:
        return HttpResponse("Nimate veljavne seje, prosim prijavite se se enkrat")
    

    id_sola = Mentor.objects.filter(ID_Mentor=mentor_id).values().first()["sola_id"]
    sola=Sola.objects.filter(ID_Sola=id_sola).values()
    print(sola.first()["Ime_Sola"])
    
    mentor = Mentor.objects.filter(ID_Mentor=mentor_id).values()
    print( mentor.first()["UpIme"])
    context = {'sola': sola.first()["Ime_Sola"], 'Ime': mentor.first()["Ime"],'Priimek' :mentor.first()["Priimek"],'UpIme' : mentor.first()["UpIme"],'mail':mentor.first()["mail"]}


    return render(request, 'tekmovanja/profil.html', context)



#tukaj dobimo ajax klic iz login page. Vrne ali je prijava uspešna ali ne
#err codes:
#1 username or password not set
#0 username and pss is correct
#2 password error
#3 mentor don't exists
def auth(request):
    usr = request.POST.get('usr', '')
    pss = request.POST.get('pss', '')
    
    if usr == '' or pss == '':
        return HttpResponse("1")

    #če najdeš zadetek vzemi geslo
    mentor = Mentor.objects.filter(UpIme=usr).values()
   
    if mentor:
        if pbkdf2_sha256.verify(pss,mentor.first()["Geslo"]):
        #if mentor.first()["Geslo"] == hash:
            #vtipkal si pravilno ime in geslo
            #čas je za redirect
            request.session['id'] = mentor.first()["ID_Mentor"]
            return HttpResponse("0")
        else:
            return HttpResponse("2")
    else:
        return HttpResponse("3")

#ajax klic za registracijo
#2 sola ne obstaja
def register(request):
    Ime = request.POST.get('Ime', '')
    Priimek = request.POST.get('Priimek', '')
    UpIme = request.POST.get('UpIme', '')
    email = request.POST.get('email', '')
    sola = request.POST.get('sola', '')
    geslo = request.POST.get('geslo', '')
    id_Sola = ''
    
    #preveri parametre
    if len(Ime) == 0 or len(Priimek) == 0 or len(UpIme) == 0 or len(email) == 0 or len(sola) == 0 or len(geslo) == 0:
        return HttpResponse("1")

    #preveri ali mentor z istim up. imenom že obstaja
    if(Mentor.objects.filter(UpIme=UpIme).exists()):
        return HttpResponse("3")

    #preveri ali sola obstaja
    if(Sola.objects.filter(Ime_Sola=sola).exists()):
        id_Sola = Sola.objects.filter(Ime_Sola=sola).values().first()["ID_Sola"]
    else:
        return HttpResponse("2")
 
    #hash = pbkdf2_sha256.encrypt(geslo, rounds=500, salt_size=16)
    hash = pbkdf2_sha256.encrypt(geslo)
    
    #shrani mentorja in solo v kateri uci
    #pss = make_password(geslo, salt=None, hasher='default')
    mentor = Mentor(None,id_Sola,Ime,Priimek,UpIme,hash,email)
    mentor.save()
    mentor_id = Mentor.objects.latest('ID_Mentor')
    
    #uci = Uci(None,mentor_id.ID_Mentor,id_Sola)
    #uci.save()

    return HttpResponse("0")






#ajax klic iz 
def tek_prijava(request):


    mentor_id = request.session.get('id', -1)
    
    #preveri sejo
    if not Mentor.objects.filter(ID_Mentor=mentor_id).exists() or mentor_id == -1:
        return HttpResponse("Nimate veljavne seje, prosim prijavite se se enkrat")


    id_tek = request.POST.get('id_tek', '')
    id_men = request.POST.get('id_men', '')
    

    if id_tek == '' or id_men == '':
        return HttpResponse("1")

    sodeluje = Sodeluje(None,id_men,id_tek)
    sodeluje.save()

    return HttpResponse("0")

def tek_odjava(request):

    mentor_id = request.session.get('id', -1)
    

    #preveri sejo
    if not Mentor.objects.filter(ID_Mentor=mentor_id).exists() or mentor_id == -1:
        return HttpResponse("Nimate veljavne seje, prosim prijavite se se enkrat")



    id_tek = request.POST.get('id_tek', '')
    id_men = request.POST.get('id_men', '')
    

    if id_tek == '' or id_men == '':
        return HttpResponse("1")
    
    Sodeluje.objects.filter(Mentor_id=id_men,Tekmovanje_id=id_tek).delete()
    return HttpResponse("0")


#izpiši vse podatke v xy formatu
def izpis(request):
    if request.user.is_superuser:
        with connection.cursor() as cursor:
            cursor.execute("SELECT m.Ime,m.Priimek,m.UpIme,m.mail, t.Ime_Tekmovanje,so.Ime_Sola FROM `tekmovanja_mentor` m, `tekmovanja_tekmovanje` t, `tekmovanja_sodeluje` s,`tekmovanja_sola` so, `tekmovanja_uci` u WHERE m.ID_Mentor=s.Mentor_id AND t.ID_Tekmovanje=s.Tekmovanje_id AND so.ID_Sola=u.sola_id AND m.ID_Mentor=u.mentor_id ORDER BY t.Ime_Tekmovanje,so.Ime_Sola ")
            rows = cursor.fetchall()
            #tmp="IME PRIIMEK UPIME MAIL IME_TEKMOVANJA IME_SOLA <br><br>"
            #for atr in rows:
            #    tmp+="<br>"+str(atr)
            #return HttpResponse(tmp)          
            context = {'rows':rows}
            return render(request, 'tekmovanja/izpis.html', context)
    else:
        return HttpResponse("Prijavite se kot admin")

def sola(request, sola_id):
    return HttpResponse("ID sole %s." %sola_id)


def izpis_sola(request):
    #sola = request.POST.get('sola', '')
    #sole = Sola.objects.filter(Ime_Sola__contains=sola).values("Ime_Sola")
    sole=Sola.objects.values("Ime_Sola")
    return HttpResponse(json.dumps(list(sole), indent=2))
    #return HttpResponse(list(sole))
    
def test(request):
    return render(request, 'tekmovanja/test.html')

def profil_update(request):
    mentor_id = request.session.get('id', -1)
    
    #preveri sejo
    if not Mentor.objects.filter(ID_Mentor=mentor_id).exists() or mentor_id == -1:
        return HttpResponse("Nimate veljavne seje, prosim prijavite se se enkrat")

    mentor=Mentor.objects.filter(ID_Mentor=mentor_id).values()

    Ime = request.POST.get('Ime', '')
    Priimek = request.POST.get('Priimek', '')
    UpIme = request.POST.get('UpIme', '')
    email = request.POST.get('email', '')
    sola = request.POST.get('sola', '')
    geslo = request.POST.get('geslo', '')
    id_Sola = ''
    
    #preveri ali mentor z istim up. imenom že obstaja
    if(Mentor.objects.filter(UpIme=UpIme).exists()):
        return HttpResponse("3")

    #preveri ali sola obstaja
    #if(Sola.objects.filter(Ime_Sola=sola).exists()):
    #    id_Sola = Sola.objects.filter(Ime_Sola=sola).values().first()["ID_Sola"]
    #else:
    #    return HttpResponse("2")
 
    if(len(Ime) > 0 and mentor.first()["Ime"] != Ime):
        Mentor.objects.filter(ID_Mentor=mentor_id).update(Ime=Ime)
    if(len(Priimek) > 0 and mentor.first()["Priimek"] != Priimek):
        Mentor.objects.filter(ID_Mentor=mentor_id).update(Priimek=Priimek)
    if(len(UpIme) > 0 and mentor.first()["UpIme"] != UpIme):
        Mentor.objects.filter(ID_Mentor=mentor_id).update(UpIme=UpIme)
    if(len(geslo) > 0):
        Mentor.objects.filter(ID_Mentor=mentor_id).update(Geslo=pbkdf2_sha256.encrypt(geslo))
    


    return HttpResponse("0")