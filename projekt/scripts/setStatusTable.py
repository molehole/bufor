from terminal.models import Etykieta, Status
from django.db.models import Count

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