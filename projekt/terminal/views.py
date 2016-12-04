from django.shortcuts import render, get_object_or_404
from terminal.models import Etykieta, Wozek, Pole, Status, Tura, TA, Kolejnosc
from django.db.models import Count
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def szwalnia_index(request):
	return render(request, 'terminal/szwalnia/index.html', {})

def szwalnia_przekaz(request):
	return render(request, 'terminal/szwalnia/przekaz.html', {})

def szwalnia_sprawdzenie(request):
	return render(request, 'terminal/szwalnia/wyszukaj.html', {})

def szwalnia_przekazanie_f(request):
	nr_wozka = int(request.POST['wozek'])
	nr_etykiety = int(request.POST['etykieta'])
	try:
		Etyk = Etykieta.objects.get(nr = nr_etykiety)
	except Exception as e:
		return render(request, 'terminal/szwalnia/przekaz.html', context_dict = {'error': True})

	T = Etyk.ta
	w = Wozek(ta = T, wozek = nr_wozka)	
	s = Status.objects.get(ta = T)
	s.szwalnia_ilosc -= 1
	if s.szwalnia_ilosc == 0:
		T.zakonczone = True
	w.save()
	s.save()
	T.save()
	context_dict = {
	'wozek': nr_wozka,
	'ta': T.nr,
	'message_variable': True
	}
	return render(request, 'terminal/szwalnia/przekaz.html', context_dict)

def szwalnia_sprawdzenie_f(request):
	nr_etykiety = int(request.POST['etykieta'])
	E = Etykieta.objects.get(nr = nr_etykiety)
	try:
		wozek = E.ta.wozek_set.all()
	except Exception as e:
		wozek = "BRAK"
	try:
		pole = E.ta.pola_set.all()
	except Exception as e:
		pole = "BRAK"
	context_dict = {
	'nr': E.nr,
	'ta': E.ta,
	'tura': E.ta.tura.nr,
	'elementy': E.ta.etykieta_set.all(),
	'ilosci_szwalnia': E.ta.status_set.all().first().szwalnia_ilosc,
	'ilosci_stolarnia': E.ta.status_set.all().first().stolarnia_ilosc,
	'wozki': wozek,
	'pola': pole,
	'message_variable': True,
	}
	return render(request, 'terminal/szwalnia/szczegoly.html', context_dict)

def informacje_index(request):
	if not request.POST:
		return render(request, 'terminal/informacje/index.html', {})
	try:
		nowa_data = datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
	except ValueError as e:
		return render(request, 'terminal/informacje/index.html', {'alert': "NIE POPRAWNA DATA!"})
	kolejnosc = Kolejnosc.objects.filter(data = nowa_data.strftime('%Y-%m-%d'))
	lista_kolejnosci = []
	lista_dat = []
	ordered_list = ()
	for each in kolejnosc:				
		tury = Tura.objects.get(nr = each.tura, data = each.data)		
		ilosci_pozostale = tury.ta_set.all().filter(zakonczone = True).count()
		try:
			procent = int((ilosci_pozostale/tury.ta_set.all().count())*100)
		except ZeroDivisionError as e:
			procent = 0
		lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
	context_dict = {
		'tury': lista_kolejnosci,
		'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
	}
	return render(request, 'terminal/informacje/index.html', context_dict)
# ---------------------------------------------------------------------------
@csrf_exempt
def Testowa(request):
	try:
		nr_wozka = int(request.POST['wozek'])
		nr_etykiety = int(request.POST['etykieta'])
		Etyk = Etykieta.objects.get(nr = nr_etykiety)
	except Exception as e:
		return render(request, 'terminal/testowa.html', {'error': True,
														'message': 'Niepoprawne dane!'})

	T = Etyk.ta	
	s = Status.objects.get(ta = T)
	if T.zakonczone == True:
		return render(request, 'terminal/testowa.html', {'error': True,
														'message': 'Zlecenie zostalo juz zakończone'})
	else:
		w = Wozek(ta = T, wozek = nr_wozka)	
		s.szwalnia_ilosc -= 1
		if s.szwalnia_ilosc == 0:
			T.zakonczone = True
		w.save()
		s.save()
		T.save()
		message_string = 'Dodano %s na wózek %s' % (T.nr, nr_wozka)
		context_dict = {
		'success': True,
		'message': message_string, 
		}
		return render(request, 'terminal/testowa.html', context_dict)