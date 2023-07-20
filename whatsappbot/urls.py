from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'), 
    path('whatsapp-webhook', views.whatsappwebhook, name= 'whatsapp-webhook'),
    path('cardapio_pdf', views.cardapio_pdf, name='cardapio_pdf'),
]