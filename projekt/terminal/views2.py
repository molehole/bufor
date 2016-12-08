from django.shortcuts import render, get_object_or_404
from terminal.models import Etykieta, Wozek, Pole, Status, Tura, TA, Kolejnosc
from django.db.models import Count

# Create your views here.
def index_szw(request):
	return render(request, 'terminal/szwalnia/index.html', {})

def przekaz_szw(request):
	return render(request, 'terminal/szwalnia/przekaz.html', {})

def ilosc_szw(request):
	return render(request, 'terminal/szwalnia/ilosc.html', {})

def przekaz_etykiete_szw(request):
	wozek = request.POST['wozek']
	if wozek == "":
		context = {
		'error_message': True
		}
		return render(request, 'terminal/szwalnia/przekaz.html', context)
	nr_etykiety = request.POST['etykieta']
	if not nr_etykiety == "":
		etykieta = get_object_or_404(Etykieta.objects.get(nr=int(nr_etykiety)))
		ta = etykieta.ta.nr
		context = {
		'ta': ta,
		'wozek': wozek,
		'message_variable': True
		}
		w = Wozek(wozek=wozek, etykieta=etykieta)
		w.save()
		status_ta = get_object_or_404(Status.objects.get(ta.nr=ta))
		status_ta.szwalnia = True
		if status_ta.ilosc >= 1:
			status_ta.ilosc -= 1
		status_ta.save()
		return render(request, 'terminal/szwalnia/przekaz.html', context)

def wyszukajWozek(wyszukiwanyNumer):
	if len(wyszukiwanyNumer) == 8: #WyszukiwaneyNumer to Etykieta
		wozki = Etykieta.objects.get_object_or_404(nr = int(wyszukiwanyNumer)).wozek_set.all()
		return wozek
	elif len(wyszukiwanyNumer) == 7: #WyszukiwaneyNumer to TA
		ta = TA.objects.get_object_or_404(nr = wyszukiwanyNumer)
		wozek = Wozek.objects.etykieta.get_object_or_404(nr = )

# -------------------------------------------

def index_sto(request):
	return render(request, 'terminal/stolarnia/index.html')

def przekaz_sto(request):
	return render(request, 'terminal/stolarnia/przekaz.html')

def przekaz_etykiete_sto(request):
	pole = request.POST['pole']
	if pole == "":
		context = {
		'error_message': True
		}
		return render(request, 'terminal/stolarnia/przekaz.html', context)
	nr_etykiety = request.POST['etykieta']
	if not nr_etykiety == "":
		etykieta = get_object_or_404(Etykieta.objects.get(nr=int(nr_etykiety)))
		ta = etykieta.ta
		context = {
		'ta': ta,
		'pole': pole,
		'message_variable': True
		}
		w = Pole(pole=pole, etykieta=etykieta)
		w.save()
		s = Status.objects.get(nr=ta)
		return render(request, 'terminal/stolarnia/przekaz.html', context)


# -------------------------------------------

def info_index(request):
	kolejnosc = Kolejnosc.objects.all()
	lista_kolejnosci = []
	lista_dat = []
	ordered_list = ()
	for each in kolejnosc:
		lista_kolejnosci.append(Tura.objects.get(nr = each.tura, data = each.data))

	context_dict = {
		'tury': lista_kolejnosci
	}
	return render(request, 'terminal/informacje/index.html', context_dict)
