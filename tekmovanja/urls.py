from django.urls import path

from . import views

app_name = 'tekmovanja'

urlpatterns = [
    path('index', views.index, name='index'), 
    #path('test', views.IndexView.as_view(), name='index'),
    path('login',views.login, name='login'),
    path('registration',views.registration, name='registration'),
    path('<int:sola_id>/sola/', views.sola, name='sola'),
    path('auth/', views.auth, name='auth'),
    path('tekmovanja',views.tekmovanja,name='tekmovanja'),
    path('tek_prijava',views.tek_prijava,name='prijava'),
    path('tek_odjava',views.tek_odjava,name='odjava'),
    path('izpis',views.izpis, name='izpis'),
    path('register/',views.register, name='register'),
    path('test/',views.test, name='test'),
    path('izpis_sola/',views.izpis_sola, name='izpis_sola'),
    path('profil/',views.profil, name='profil'),
    path('profil_update/',views.profil_update, name='profil_update'),
    
    
    
    
]