from time import sleep
class Msg():
    sleep(1)

    def novo_cliente():
        return ''' Olá, eu sou o Nil,
Assistente virtual do Danilo.🤖
Antes de prosseguir com o atendimento, 

Digite seu nome.'''


#------------------------------------------------------

    def cliente_salvo(nome):
        return f''' Muito bem {nome}.😊
Já salvei o seu número aqui nos meus contatos.'''
    
#------------------------------------------------------

    def saudação(nome, cliente_novo=False):
        resposta =  f''' Olá {nome}, eu sou o Nil,
Assistente virtual do Danilo.🤖

Já imaginou... 
Um robô que pode fazer todo o trabalho repetitivo por você. 
Por exemplo:

Responder todos os seus clientes. 🗣️

Agendar horários na sua agenda. 📅

Anotar pedidos para o seu estabelecimento. 📝

E muito mais. 😁😁

'''
        if cliente_novo == True:
            resposta = resposta[-229:]

        return resposta

#------------------------------------------------------

    def opções():
        return '''
Quer me ver em ação? 
É só escolher uma das simulações abaixo 
ou clique em saber mais. 👇👇👇

1.  Simulação 1 - Agendar horário na barbearia
2.  Simulação 2 - Fazer pedido na pizzaria
3.  Saber mais

'''

#------------------------------------------------------

    def nao_entendi():
        return '''
Desculpe, não consegui te entender 😞
Digite uma das opções abaixo 👇👇

'''

#------------------------------------------------------

    def simulacao_inicio():
        return'''
Inicializando simulação....
'''
#------------------------------------------------------

    def simulacao_fim():
        sleep(1.5)
        return'''
....Fim da simulação
'''
#SIMULAÇÃO DE BARBEARIA ----------------------------------------------------------------------------------------------------------------

    def barbearia_saudacao(nome):
        sleep(1.5)
        resposta = f'''
Olá {nome}, eu sou o Nil,
Assistente virtual da 
barbearia do seu Zé 🤖 

como posso ajudar?

1. Agendar atendimento 🗓️
2. Saber valores 💲
3. Finalizar simulação
'''

        return resposta

#------------------------------------------------------

    def agenda_hr():
        return '''
Beleza

Para facilitar vou te mandar o link da minha agenda
E você escolhe o melhor dia/hora para o seu atendimento ok?.

Se precisar de mim novamente, é só me chamar 😁😁
Para agendar seu atendimento, é só clicar nesse link 👇

https://calendly.com/danilo-nilsantos

'''

#------------------------------------------------------

    def valor():
        i = '-'
        return f'''
Esses são nossos preços:

Corte padrão {i*13} R$  25,00
Barba, cabelo e bigode {i*3} R$  50,00
Luzes {i*20} R$ 100,00
'''
#SIMULAÇÃO DE PIZZARIA ----------------------------------------------------------------------------------------------------------------

    def pizzaria_saudacao(nome):
        sleep(1.5)
        resposta = f'''
Olá {nome}, eu sou o Nil,
Assistente virtual da 
pizzaria da dona Maria 🤖 

como posso ajudar?

1. Cardápio 👨‍🍳
2. Fazer pedido 😋🍕🍕
3. Meu pedido está atrasado ⏱️😞 
4. Finalizar simulação 
'''

        return resposta
    
#------------------------------------------------------

    def cardapio():
        return '''
Aqui está o nosso cardápio 


Quando estiver pronto para 
fazer o seu pedido,

é só me chamar ok
'''


