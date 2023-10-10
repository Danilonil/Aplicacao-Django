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
atalhos = ['simulação 1', 'barbearia', 'simulação 2', 'pizzaria']


# adicionar essa tag para que nosso projeto encontre o .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

#------------------------------------------------------------------------------------------------------------------

def enviar_mensagem(numero, mensagem= None, pdf= False, botao= False):
    headers = {"Authorization": f'Bearer {os.getenv("WHATSAPP_TOLKEN")}'}
    json = {"messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {
                "body": mensagem }
            }


    if pdf == True:
        json = {"messaging_product": "whatsapp",
            "to": numero,
            "type": "document",
            "document": {
                "link": f"{os.getenv('link_site')}/cardapio_pdf", 
                "filename": "Cardápio.pdf" } 
            }


    if botao == True:
        json = {"messaging_product":  "whatsapp",
            "to":  numero,
            "type": "interactive",
            "interactive": {"type": "button",
                        "body": {"text": Msg.continuar()},
                        "action": {"buttons": [
                            {
                            "type": "reply",
                            "reply": {
                                "id": "UNIQUE_BUTTON_ID_1",
                                "title": "Continuar pedido"
                                }
                            },
                            {
                            "type": "reply",
                            "reply": {
                                "id": "UNIQUE_BUTTON_ID_2",
                                "title": "Finalizar pedido"
                                }   
                            }
                            ]
                        }
                    }
        }



    resposta = requests.post(os.getenv("WHATSAPP_URL"), headers=headers, json=json)
    resposta = resposta.json()

    return resposta

#------------------------------------------------------------------------------------------------------------------

def tratar_mensagem(whatsapp_cliente, mensagem_cliente, nome_perfil, timestamp):
    global barbearia, pizzaria, saber_mais, fim_simulacao, atalhos

    pesq_cliente = Contato.objects.filter(whatsapp__contains=whatsapp_cliente).exists()
    if pesq_cliente == False:
        Contato.objects.create(nome=nome_perfil, whatsapp=whatsapp_cliente, status_conversa='cadastrar cliente')

    cliente = Contato.objects.get(whatsapp__contains=whatsapp_cliente)
    mensagem_cliente = mensagem_cliente.lower()
    
    
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


    elif cliente.status_conversa == '--' and mensagem_cliente not in atalhos or mensagem_cliente in fim_simulacao[2:]:
        cliente.status_conversa = 'aguardando opções'
        cliente.save()
        resposta = Msg.saudação(cliente.nome)
        enviar_mensagem(whatsapp_cliente, resposta)
        resposta = Msg.opções()

    elif cliente.status_conversa == 'aguardando opções' or mensagem_cliente in atalhos:
        if mensagem_cliente in barbearia or mensagem_cliente in pizzaria:
            resposta = Msg.simulacao_inicio()
            enviar_mensagem(whatsapp_cliente, resposta)

            if mensagem_cliente in barbearia:
                cliente.status_conversa = 'simulação barbearia - opções'
                cliente.save()
                resposta = Msg.barbearia_saudacao(cliente.nome)

            elif mensagem_cliente in pizzaria:
                cliente.status_conversa = 'simulação pizzaria - opções'
                cliente.save()
                resposta = Msg.pizzaria_saudacao(cliente.nome)

        elif mensagem_cliente in ['3', '3.', 'saber mais', 'sabermais', 'sabe mais', 'saber', 'mais']:
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
            for i in range(0, 2):
                fim_simulacao[i] = fim_simulacao[i].replace('4','3')

            if mensagem_cliente in ['1', '1.', 'agendar atendimento','agenda atendimento', 'agenda', 'agendar', 'atendimento', 'cortar cabelo', 'marcar hr', 'marcar atendimento', '1. agendar atendimento']:
                cliente.status_conversa = 'simulação barbearia - inicio'
                cliente.save()
                resposta = Msg.agenda_hr()

            elif mensagem_cliente in ['2', '2.', 'saber valores', 'sabervalores', 'sabervalor', 'saber valor', 'Valor', 'valores']:
                cliente.status_conversa = 'simulação barbearia - inicio'
                cliente.save()
                resposta = Msg.valor()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta =Msg.agenda_hr()[8:]
            
            elif mensagem_cliente in fim_simulacao: 
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
            for i in range(0, 2):
                fim_simulacao[i] = fim_simulacao[i].replace('3','4')

            if mensagem_cliente in ['1', '1.', 'cardapio', 'cardápio', 'menu', 'cardapiu', 'cardápiu', '1. cardápio']:
                cliente.status_conversa = 'simulação pizzaria - aguardando pedido'
                cliente.save()
                resposta = Msg.cardapio()
                enviar_mensagem(whatsapp_cliente, pdf=True)

            elif mensagem_cliente in ['2', '2.', 'pedido', 'fazer pedido', '2. fazer pedido', 'pedir', 'novo pedido']:
                cliente.status_conversa = 'simulação pizzaria - pedido/ inicio'
                cliente.save()
                resposta = Msg.pedido(cliente.nome)
            
            elif mensagem_cliente in ['3', '3.', 'meu pedido esta atrasado', 'atrasado', 'atrazado', 'pedido atrasado']:
                cliente.status_conversa = 'simulação pizzaria - inicio'
                cliente.save()
                resposta = Msg.atraso_pedido(cliente.nome)

            elif mensagem_cliente in fim_simulacao:
                cliente.status_conversa = 'aguardando opções'
                cliente.save()
                resposta = Msg.simulacao_fim()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta = Msg.opções()
            
            else:
                resposta = Msg.nao_entendi()
                enviar_mensagem(whatsapp_cliente, resposta)
                resposta = Msg.pizzaria_saudacao(cliente.nome)[-94:]
        
        elif cliente.status_conversa == 'simulação pizzaria - aguardando pedido':
            cliente.status_conversa = 'simulação pizzaria - pedido/ inicio'
            cliente.save()
            resposta = Msg.pedido(cliente.nome)
            
        elif 'simulação pizzaria - pedido/' in cliente.status_conversa:
            if 'inicio' in cliente.status_conversa:
                if mensagem_cliente in ['1', '1.', 'pizza', 'piza', 'pizzas']:
                    cliente.status_conversa = 'simulação pizzaria - pedido/ pizza/ quant sabor'
                    cliente.save()
                    resposta = Msg.quant_sabor()
                
                elif mensagem_cliente in ['2', '2.', 'bebida', 'bebidas']:
                    cliente.status_conversa = 'simulação pizzaria - pedido/ bebida/'
                    cliente.save()
                    resposta = Msg.escolha_bebida()
                
                else:
                    resposta = Msg.nao_entendi()
                    enviar_mensagem(whatsapp_cliente, resposta)
                    resposta = Msg.pedido(cliente.nome)[-25:]
            
            elif 'pizza/' in cliente.status_conversa:
                if 'quant sabor' in cliente.status_conversa:
                    if mensagem_cliente.isnumeric() and int(mensagem_cliente) in range(1, 5):
                        quant_sabor = int(mensagem_cliente)
                        cliente.status_conversa = f'simulação pizzaria - pedido/ pizza/ {quant_sabor} sabor(es) {"x"*quant_sabor}'
                        cliente.save()
                        resposta =  Msg.escolha_sabor(1, sabor_unico = True)
                    
                    else:
                        resposta = Msg.nao_entendi()
                        enviar_mensagem(whatsapp_cliente, resposta)
                        resposta = Msg.quant_sabor()

                elif 'sabor(es)' in cliente.status_conversa:
                    if 'x' in cliente.status_conversa[-5:]:
                        cliente.status_conversa = cliente.status_conversa[::-1].replace('x', '-', 1)[::-1]
                        cliente.save()
                    if 'x' in cliente.status_conversa[-5:]:
                        n = cliente.status_conversa.count('-', -5) +1
                        resposta =  Msg.escolha_sabor(n)
                    
                    else:
                        cliente.status_conversa = 'simulação pizzaria - pedido/ continuar?'
                        cliente.save()
                        enviar_mensagem(whatsapp_cliente, botao= True)
                        
            elif 'bebida/' in cliente.status_conversa:
                cliente.status_conversa = 'simulação pizzaria - pedido/ continuar?'
                cliente.save()
                enviar_mensagem(whatsapp_cliente, botao= True)

            elif 'continuar?' in cliente.status_conversa:
                if mensagem_cliente in ['continuar pedido', 'pedido', 'continuar', 'continua pedido', 'continua']:
                    cliente.status_conversa = 'simulação pizzaria - pedido/ inicio'
                    cliente.save()
                    resposta = Msg.pedido(cliente.nome)[-61:]
                
                elif mensagem_cliente in ['finalizar pedido', 'finalizar', 'finaliza pedido', 'finaliza']:
                    pass

                else:
                    resposta = Msg.nao_entendi()
                    enviar_mensagem(whatsapp_cliente, resposta)
                    resposta = ''
                    enviar_mensagem(whatsapp_cliente, botao= True)


    enviar_mensagem(whatsapp_cliente, resposta)





#11 95844-7515
