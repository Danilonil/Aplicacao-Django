from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'), 
    path('cardapio_pdf', views.cardapio_pdf, name='cardapio_pdf'),
    path('whatsapp-webhook', views.whatsappwebhook, name= 'whatsapp-webhook'),
    
]