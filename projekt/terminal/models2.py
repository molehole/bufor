from django.db import models
from django.utils import timezone
from datetime import datetime

class Tura(models.Model):
    nr = models.IntegerField()
    data = models.DateField()

    def __str__(self):
        return str(self.nr)

class TA(models.Model):
    tura = models.ForeignKey(Tura)
    nr = models.IntegerField()
    elementy = models.TextField()

    def __str__(self):
        return str(self.nr)

# Create your models here.
class Etykieta(models.Model):
    ta = models.ForeignKey(TA)
    nr = models.IntegerField()
    pozycja = models.IntegerField(null=True)
    element = models.TextField(null=True)

    def __str__(self):
        return str(self.nr)

# Tabela odkladcza na Szwalni
class Wozek(models.Model):
    wozek = models.IntegerField()
    data_dodania = models.DateTimeField(default=timezone.now)
    data_wydania = models.DateTimeField(null=True)
    etykieta = models.ForeignKey(Etykieta)

    def dodaj_do_wozka(self, wozek, etykieta):
        self.wozek = wozek
        self.etykieta = etykieta
        self.save()        

    def __str__(self):
        return str(self.wozek)

#Tabela odkladcza na Stolarni
class Pole(models.Model):
    pole = models.IntegerField()
    data_dodania = models.DateTimeField(default=timezone.now)
    data_wydania = models.DateTimeField(null=True)
    etykieta = models.ForeignKey(Etykieta)

    def __str__(self):
        return str(self.pole)

#Tabela Statusów
class Status(models.Model):
    ta = models.ForeignKey(TA)
    szwalnia = models.BooleanField(default=False)
    stolarnia = models.BooleanField(default=False)
    tapicernia = models.BooleanField(default=False)
    ilosc = models.IntegerField(default=0)

    def __str__(self):
        return str(self.ta.nr)