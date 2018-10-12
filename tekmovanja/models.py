from django.db import models

class Sola(models.Model):
    ID_Sola = models.AutoField(primary_key=True)
    Ime_Sola = models.CharField(max_length=50)
    Vrsta_Sola = models.CharField(max_length=5)


class Mentor(models.Model):
    ID_Mentor = models.AutoField(primary_key=True)
    sola = models.ForeignKey(Sola, on_delete=None)
    potrjen = models.IntegerField()
    Ime = models.CharField(max_length=35)
    Priimek = models.CharField(max_length=50)
    UpIme = models.CharField(max_length=35)
    Geslo = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)


    #def __str__(self):
    #   return "test"

class Tekmovanje(models.Model):
    ID_Tekmovanje = models.AutoField(primary_key=True)
    Ime_Tekmovanje = models.CharField(max_length=50)

class Potrditve(models.Model):
    ID_Potrditve = models.AutoField(primary_key=True)
    Zahteva= models.ForeignKey(Mentor, on_delete=None,related_name='Zahteva')
    Potrditelj = models.ForeignKey(Mentor, on_delete=None, related_name='Potrditelj')
#class Uci(models.Model):
#    ID_Uci = models.AutoField(primary_key=True)
    #ID_Uci = models.IntegerField()
    #ID_Sola = models.IntegerField()
#    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
#    sola = models.ForeignKey(Sola, on_delete=models.CASCADE)

class Sodeluje(models.Model):
    ID_Sodeluje = models.AutoField(primary_key=True)
    #ID_Tekmovanje = models.IntegerField()
    #ID_Mentor = models.IntegerField()
    Mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    Tekmovanje =  models.ForeignKey(Tekmovanje, on_delete=models.CASCADE)