import requests, os
from pathlib import Path
from dotenv import load_dotenv
from mysite.settings import BASE_DIR
from .models import *
from .msg_personalizada import *


barbearia = ['1', '1.', 'cabelo', 'simulação 1', 'simulacao 1', 'simulaçao 1' , 'simulacão 1', 'barbearia', 'simulaçao1', '1.  simulação 1', 'Agendar horário na barbearia','1.  simulação 1 - agendar horário na barbearia']
pizzaria = ['2', '2.', 'pizza', 'simulação 2', 'simulacao 2', 'simulaçao 2' , 'simulacão 2', 'simulação2', 'pizzaria', '2.  Simulação 2','fazer pedido na pizzaria', 'fazer pedido', 'pedido']
saber_mais = []
fim_simulacao = ['3', '3.', 'finalizar simulação', 'fim da simulação', 'finalizar', 'finaliza simulação', 'finalizar simulacao']

# adicionar essa tag para que nosso projeto encontre o .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

#------------------------------------------------------------------------------------------------------------------

def enviar_mensagem(numero, mensagem):
    headers = {"Authorization": f'Bearer {os.getenv("WHATSAPP_TOLKEN")}'}
    json = {"messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {
                "body": mensagem }
            }

    resposta = requests.post(os.getenv("WHATSAPP_URL"), headers=headers, json=json)
    ans = resposta.json()

    return ans

#------------------------------------------------------------------------------------------------------------------

def tratar_mensagem(whatsapp_cliente, mensagem_cliente, nome_perfil = None, timestamp = None):
    pesq_cliente = Clientes.objects.filter(whatsapp__contains=whatsapp_cliente).exists()
    if pesq_cliente == False:
        Clientes.objects.create(nome=nome_perfil, whatsapp=whatsapp_cliente, status_conversa='cadastrar cliente')

    cliente = Clientes.objects.get(whatsapp__contains=whatsapp_cliente)
    if cliente.status_conversa == 'cadastrar cliente':
        cliente.status_conversa = 'aguardando nome'
        cliente.save()
        resposta = Msg.novo_cliente()


    elif cliente.status_conversa == 'aguardando nome':
        cliente.nome = mensagem_cliente.title()
        cliente.status_conversa = 'aguardando opções'
        cliente.save()
        resposta = Msg.cliente_salvo(cliente.nome)
        enviar_mensagem(whatsapp_cliente, resposta)
        resposta = Msg.saudação(cliente.nome, True)
        enviar_mensagem(whatsapp_cliente, resposta)
        resposta = Msg.opções()


    elif cliente.status_conversa == '--' and mensagem_cliente.lower() not in barbearia or mensagem_cliente.lower() not in pizzaria:
        cliente.status_conversa = 'aguardando opções'
        cliente.save()
        resposta = Msg.saudação(cliente.nome)
        enviar_mensagem(whatsapp_cliente, resposta)
        resposta = Msg.opções()

    elif cliente.status_conversa == 'aguardando opções' or mensagem_cliente.lower() in barbearia or mensagem_cliente.lower() in pizzaria:
        if mensagem_cliente.lower() in barbearia or mensagem_cliente.lower() in pizzaria:
            resposta = Msg.simulacao_inicio()
            enviar_mensagem(whatsapp_cliente, resposta)

            if mensagem_cliente.lower() in barbearia:
                cliente.status_conversa = 'simulação barbearia - opções'
                cliente.save()
                resposta = Msg.barbearia_saudacao(cliente.nome)

            elif mensagem_cliente.lower() in pizzaria:
                cliente.status_conversa = 'simulação pizzaria - opções'
                cliente.save()

        elif mensagem_cliente.lower() in ['3', '3.', 'saber mais', 'sabermais', 'sabe mais', 'saber', 'mais']:
            cliente.status_conversa = 'saber mais'
            cliente.save()
        
        else:
            resposta = Msg.nao_entendi()
            enviar_mensagem(whatsapp_cliente, resposta)
            resposta = Msg.opções()[-106:]

    #SIMULAÇÃO DE BARBEARIA ------------------------------------------------------------------------------------------------------------------

    elif 'barbearia' in cliente.status_conversa:
        if cliente.status_conversa == 'simulação barbearia - inicio':
            cliente.status_conversa = 'simulação barbearia - opções'
            cliente.save()
            resposta = Msg.barbearia_saudacao(cliente.nome)

        elif cliente.status_conversa == 'simulação barbearia - opções':
            if mensagem_cliente.lower() in ['1', '1.', 'agendar atendimento','agenda atendimento', 'agenda', 'agendar', 'atendimento', 'cortar cabelo', 'marcar hr', 'marcar atendimento', '1. agendar atendimento']:
                cliente.status_conversa = 'simulação barbearia - inicio'
                cliente.save()
                resposta = Msg.agenda_hr()

            elif mensagem_cliente.lower() in ['2', '2.', 'saber valores', 'sabervalores', 'sabervalor', 'saber valor', 'Valor', 'valores']:
                cliente.status_conversa = 'simulação barbearia - inicio'
                cliente.save()
                resposta = Msg.valor()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta =Msg.agenda_hr()[8:]
            
            elif mensagem_cliente.lower() in fim_simulacao: 
                cliente.status_conversa = 'aguardando opções'
                cliente.save()
                resposta = Msg.simulacao_fim()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta = Msg.opções()

            else:
                resposta = Msg.nao_entendi()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta = Msg.barbearia_saudacao(cliente.nome)[-68:]


    #SIMULAÇÃO DE PIZZARIA ------------------------------------------------------------------------------------------------------------------
    elif 'pizzaria' in cliente.status_conversa:
        if cliente.status_conversa == 'simulação pizzaria - inicio':
            cliente.status_conversa = 'simulação pizzaria - opções'
            cliente.save()
            resposta = Msg.pizzaria_saudacao(cliente.nome)

        elif cliente.status_conversa == 'simulação pizzaria - opções':
            if mensagem_cliente.lower() in ['1', '1.', 'cardapio', 'cardápio', 'menu', 'cardapiu', 'cardápiu', '1. cardápio']:
                pass



    enviar_mensagem(whatsapp_cliente, resposta)





#11 95844-7515
