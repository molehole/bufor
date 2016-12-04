"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from terminal import views

urlpatterns = [
    url(r'^szwalnia/$', views.szwalnia_index, name='szwalnia_index'),
    url(r'^szwalnia/przekaz/$', views.szwalnia_przekaz, name='szwalnia_przekaz'),
    url(r'^szwalnia/przekaz/szwalnia_przekazanie_f$', views.szwalnia_przekazanie_f, name='szwalnia_przekazanie_f'),
    url(r'^szwalnia/wyszukaj/$', views.szwalnia_sprawdzenie, name='szwalnia_wyszukaj'),
    url(r'^szwalnia/szwalnia_sprawdzenie_f/$', views.szwalnia_sprawdzenie_f, name='szwalnia_sprawdzenie_f'),    
    url(r'^informacje/$', views.informacje_index, name='informacje_index'),    
    url(r'^testowa/$', views.Testowa, name='strona_testowa_index'),
]
