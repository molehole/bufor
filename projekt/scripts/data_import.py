# -*- coding: utf-8 -*-
import time
import re
import csv
from stat import S_ISREG, ST_CTIME, ST_MODE
import os
from datetime import datetime
from terminal.models import Etykieta, Status
from django.db.models import Count


# Timer
start_time = time.time()

# Zmienne
elementy_regex = '(?<=\^FN921\^FD)(.*)(?=\^FS)'
element_regex = '(?<=\^FN922\^FD)(.*)(?=\^FS)'
informacje_regex = '(?<=\^FN949\^FD)(.*)(?=\^FS)'
nr_regex = '(?<=\^FN929\^FD)(.*)(?=\^FS)'
ilosc_regex = '(?<=\^FN934\^FD)(.*)(?= von 001\^FS)'
etykieta = '\^XF\S+.ZPL(.*?)\^FX End of job'

tablica_etykiet = []
tablica_kontrolna = []
tablica_ta = []

main_path = '//jan-svr-nas01/domowy/Labeo/Planowanie/TXT/'

# domowa sciezka do wykasowania
# main_path = os.path.join('d:','TXT')


class Etykieta_txt():
    ta = ''
    data = ''
    nr = ''
    tura = ''
    elementy = ''
    pozycja = ''
    element = ''
    ilosc = ''

    def setValues(self, nr, ta, tura, pozycja, data, elementy, element, ilosc):
        self.ta = ta
        self.nr = nr
        self.tura = tura
        self.pozycja = pozycja
        self.data = data
        self.elementy = elementy
        self.element = element
        self.ilosc = ilosc

    def __init__(self, nr, ta, tura, pozycja, data, elementy, element, ilosc):
        self.ta = ta
        self.nr = nr
        self.tura = tura
        self.pozycja = pozycja
        self.data = data
        self.elementy = elementy
        self.element = element
        self.ilosc = ilosc

# Funkcja do wyswietlania i sprawdzania dancyh etykiet
def pokazInformacje(Etykieta):
    print("""
Etykieta %s:
------------
TA: %s
TURA: %s
POZYCJA: %s
DATA: %s
ILOŚĆ: %s
ELEMENT: %s
ELEMENTY:
    """ % (Etykieta.nr, Etykieta.ta, Etykieta.tura, Etykieta.pozycja, datetime.strftime(Etykieta.data, '%d-%m-%Y'), Etykieta.ilosc, Etykieta.element))
    for i in Etykieta.elementy:
        print("*  ", i)


def czytajPlikEtykiet(plik):
    with open(plik, 'r', encoding="utf8") as f:
        match = re.findall(etykieta, f.read(), re.DOTALL) #Wyszukanie wszystkich etykiet
        for i in match:
            nr_regex_match = re.search(nr_regex, i)
            elementy_match = re.search(elementy_regex, i)
            element_match = re.search(element_regex, i)
            informacje_match = re.search(informacje_regex, i)
            ilosc_match = re.search(ilosc_regex, i)
            info_splited = informacje_match.group(0).split('/')
            elementy_splited = elementy_match.group(0).split(',')

            #zmienne
            nr = int(nr_regex_match.group(0))
            ta = info_splited[3].strip()
            tura = info_splited[1].strip()
            pozycja = info_splited[4].strip()
            data = datetime.strptime(info_splited[2].strip(), "%d.%m.%Y")
            elementy = elementy_splited
            element = element_match.group(0).strip()
            ilosc = ilosc_match.group(0)


            if (nr not in tablica_kontrolna): #sprawdzenie czy dane TA juz nie wystapilo
                tablica_kontrolna.append(nr)
                tablica_etykiet.append(Etykieta_txt(nr = nr,
                                            ta = ta,
                                            tura = tura,
                                            pozycja = pozycja,
                                            data = data,
                                            elementy = elementy,
                                            element = element,
                                            ilosc = ilosc))
            else: # Aktualizacja danych istniejacego TA
                for e in tablica_etykiet:
                    if (e.nr == nr):
                        e.setValues(nr = nr,
                                    ta = ta,
                                    tura = tura,
                                    pozycja = pozycja,
                                    data = data,
                                    elementy = elementy,
                                    element = element,
                                    ilosc = ilosc)

def wyszukajPlikiPoDacie(sciezka):
    entries = (os.path.join(sciezka, fn) for fn in os.listdir(sciezka))
    entries = ((os.stat(path), path) for path in entries)
    entries = ((stat[ST_CTIME], path)
       for stat, path in entries if S_ISREG(stat[ST_MODE]))
    return entries

def dodaDoBazyDanych(etykieta):
    if not Etykieta.objects.filter(nr = etykieta.nr):
        e = Etykieta(nr = etykieta.nr,
                 ta = etykieta.ta,                 tura = etykieta.tura,
                 data = etykieta.data,
                 elementy = etykieta.elementy,
                 element = etykieta.element,
                 ilosc = etykieta.ilosc)
        e.save()
        return True
    else:
        return False

def WyszukajIlosci(Etykieta_ta):
    ilosc = []
    Ta_dict = Etykieta.objects.filter(ta = Etykieta_ta).values('ta', 'element').annotate(Ilosci=Count('ta'))
    for row in Ta_dict:
        ilosc.append(row['Ilosci'])
    return min(ilosc)

def UzupelnijStatus(Etykieta_ta):
    try:
        Status.objects.get(ta = Etykieta_ta)
    except Exception as e:
        a = Status()
        a.ta = Etykieta_ta
        a.ilosc = WyszukajIlosci(Etykieta_ta)
        a.save()

for T, filenames in sorted(wyszukajPlikiPoDacie(main_path)):
    czytajPlikEtykiet(filenames)

dodano = 0
pominieto = 0

for each in tablica_etykiet:
    if dodaDoBazyDanych(each):
        dodano += 1
    else:
        pominieto += 1        
        
print('ZAKONCZONO DODAWANIE ETYKIET...')
print('GENEROWANIE STATUSOW....')
for each in tablica_etykiet:
    UzupelnijStatus(each.ta)

print('DODANO:', dodano)
print('POMINIETO:', pominieto)
print("--- %s seconds ---" % (time.time() - start_time))