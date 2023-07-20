from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, FileResponse
from .funções import *
from pathlib import Path
from dotenv import load_dotenv
from mysite.settings import BASE_DIR
import  os, json

# adicionar essa tag para que nosso projeto encontre o .env
load_dotenv(os.path.join(BASE_DIR, ".env"))


# Create your views here.


def home(request):
    return render(request, 'mysite/index.html', {})


def cardapio_pdf(request):
    pdf = os.path.join('static/staticfiles', 'cardápio.pdf')
    return FileResponse(open(pdf, 'rb'), content_type='application/pdf')



@csrf_exempt
def whatsappwebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status= 200)
        else:
            return HttpResponse('erro', status= 403)
        
    
    if request.method == 'POST':
        dados = json.loads(request.body)
        if 'object' in dados and 'entry' in dados: 
            if dados['object'] == 'whatsapp_business_account':
                try:
                    for dado in dados['entry']:
                        nome_perfil = dado['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsapp_cliente = dado['changes'][0]['value']['contacts'][0]['wa_id']
                        timestamp = dado['changes'][0]['value']['messages'][0]['timestamp']
                        mensagem_cliente = dado['changes'][0]['value']['messages'][0]['text']['body']
                        #numero_envio = dado['changes'][0]['value']['metadata']['display_phone_number']
                        #numero_id = dado['changes'][0]['value']['metadata']['phone_number_id']
                        #mensagem_id = dado['changes'][0]['value']['messages'][0]['id']
                        
                        enviar_mensagem(whatsapp_cliente, mensagem_cliente)
                        #tratar_mensagem(whatsapp_cliente, mensagem_cliente, nome_perfil, timestamp)
                    
                except:
                    pass


        return HttpResponse('sucesso', status= 200)