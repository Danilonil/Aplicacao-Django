import requests, os
from pathlib import Path
from dotenv import load_dotenv
from mysite.settings import BASE_DIR
from .models import *
from .msg_personalizada import *



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
        resposta = Msg.saudação(cliente.nome, cliente_novo=True)
        enviar_mensagem(whatsapp_cliente, resposta)
        resposta = Msg.opções()


    elif cliente.status_conversa == '--' and mensagem_cliente not in ['Simulação 1', 'Barbearia']:
        cliente.status_conversa = 'aguardando opções'
        cliente.save()
        resposta = Msg.saudação(cliente.nome, cliente_novo=False)
        enviar_mensagem(whatsapp_cliente, resposta)
        resposta = Msg.opções()

    elif cliente.status_conversa == 'aguardando opções' or mensagem_cliente in ['Simulação 1', 'Barbearia']:
        if mensagem_cliente.capitalize() in ['1', '1.', 'Cabelo', 'Simulação 1', 'Simulacao 1', 'Simulaçao 1' , 'Simulacão 1', 'Barbearia', 'Simulaçao1']:
            cliente.status_conversa = 'simulação barbearia - opções'
            cliente.save()
            resposta = Msg.simulacao_inicio()
            enviar_mensagem(whatsapp_cliente, resposta)
            resposta = Msg.barbearia_saudacao(cliente.nome)

        elif mensagem_cliente.capitalize() in['2', '2.', 'Pizza', 'Simulação 2', 'Simulacao 2', 'Simulaçao 2' , 'Simulacão 2', 'Simulação2', 'Pizzaria']:
            cliente.status_conversa = 'simulação pizzaria'
            cliente.save()
            resposta = Msg.simulacao_inicio()
            enviar_mensagem(whatsapp_cliente, resposta)
        
        elif mensagem_cliente.capitalize() in ['3', '3.', 'Saber mais', 'Sabermais', 'Sabe mais', 'Saber', 'Mais']:
            cliente.status_conversa = 'saber mais'
            cliente.save()
        
        else:
            resposta = Msg.nao_entendi()


    elif 'simulação barbearia' in cliente.status_conversa:
        if cliente.status_conversa == 'simulação barbearia - inicio':
            cliente.status_conversa = 'simulação barbearia - opções'
            cliente.save()
            resposta = Msg.barbearia_saudacao(cliente.nome)

        elif cliente.status_conversa == 'simulação barbearia - opções':
            if mensagem_cliente.capitalize() in ['1', '1.', 'Agendar atendimento','Agenda atendimento', 'Agenda', 'Agendar', 'Atendimento', 'Cortar cabelo']:
                cliente.status_conversa = 'simulação barbearia - inicio'
                cliente.save()
                resposta = Msg.agenda_hr()

            elif mensagem_cliente.capitalize() in ['2', '2.', 'Saber valores', 'Sabervalores', 'Saber valor', 'Valor', 'Valores']:
                cliente.status_conversa = 'simulação barbearia - inicio'
                cliente.save()
                resposta = Msg.valor()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta =Msg.agenda_hr()[-143:]
            
            elif mensagem_cliente.capitalize() in ['3', '3.', 'Finalizar simulação', 'Fim da simulação', 'Finalizar', 'Finaliza simulação', 'Finalizar simulacao']: 
                cliente.status_conversa = 'aguardando opções'
                cliente.save()
                resposta = Msg.simulacao_fim()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta = Msg.opções()

            else:
                resposta = Msg.nao_entendi()






    enviar_mensagem(whatsapp_cliente, resposta)





#11 95844-7515
