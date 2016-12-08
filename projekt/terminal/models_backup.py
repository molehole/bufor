from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Etykieta(models.Model):
    nr = models.IntegerField()
    ta = models.IntegerField()
    tura = models.IntegerField(null=True)
    pozycja = models.IntegerField(null=True)
    data = models.DateField(null=True)
    elementy = models.TextField(null=True)
    element = models.TextField(null=True)
    ilosc = models.TextField(null=True)

    def informacje(self):
        string = """
<h4>Etykieta %s:</h1>
<p class='mini_info'>------------</p>
<p class='mini_info'>TA: %s</p>
<p class='mini_info'>TURA: %s</p>
<p class='mini_info'>POZYCJA: %s</p>
<p class='mini_info'>DATA: %s</p>
<p class='mini_info'>ELEMENT: %s</p>
<p class='mini_info'>ELEMENTY: %s</p>
        """ % (self.nr, self.ta, self.tura, self.pozycja, datetime.strftime(self.data, '%d-%m-%Y'), self.element, self.elementy)
        # for i in self.elementy:
        #     var ="<p>*  " + i + "</p>"
        #     string =string + var
        return string

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
    ta = models.TextField(null=True, unique=True)
    szwalnia = models.BooleanField(default=False)
    stolarnia = models.BooleanField(default=False)
    tapicernia = models.BooleanField(default=False)
    ilosc = models.IntegerField(default=0)

    def __str__(self):
        return str(self.ta)