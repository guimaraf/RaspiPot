#coding: utf-8
import time, random, datetime, telepot, os, subprocess, json, requests, platform

versao = "0.5.3"
dataVersao = "Última atualização dia 12/06/2017, versão 1"

print(time.strftime("%d/%m/%Y %H:%M:%S"), "Bot de telegran para Raspi versão: ",versao,"Criado por Frederico Oliveira e Lucas Cassiano")

tokenColetaTxt = open('token.txt', 'r')
idToken = tokenColetaTxt.read()

def handle(msg):
    chat_id = msg['chat']['id']
    usuario = msg['chat']['username'] #adicionado outra chamada de informações do telegran, agora o username
    command = msg['text']
    dataMensagem = time.strftime('%d/%m/%Y %H:%M:%S')
    sistemaOperacional = verificarSistemaOperacional() #Detectando a versão do sistema operacional e retornando uma string

    global versao, dataVersao

    print('Comando executado: ', command)
    
    if (command == '/roll'):
        bot.sendMessage(chat_id, random.randint(1,10))

    elif(command == '/help' or command == '/start'):
        helpLeitura = consultarAjuda(sistemaOperacional)
        bot.sendMessage(chat_id, helpLeitura)

    elif (command == '/time'):
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    elif (command == '/cput'):
        mensagemTxt = consultarTemperatura(sistemaOperacional)
        bot.sendMessage(chat_id, mensagemTxt)

    elif (command == '/loop'):
        linhas = frasesAleatorias(sistemaOperacional)
        bot.sendMessage(chat_id, linhas)
	
    elif (command == '/weather'):
        dadosColetados = coletarDadosAtmosfericos()
        bot.sendMessage(chat_id, dadosColetados)

    elif (command == '/currency'):
        mensagemTxt = cotacaoDolar()
        bot.sendMessage(chat_id, mensagemTxt)
	
    elif (command == '/uptime'):
        mensagemTxt = tempoLigado(sistemaOperacional)
        bot.sendMessage(chat_id, mensagemTxt)

    elif (command == '/version'):
        mensagemTxt = "Versão " + versao + ", " + dataVersao
        bot.sendMessage(chat_id, mensagemTxt)
    
    elif (command == '/print'):
        bot.sendMessage(chat_id, "Carregando foto...")
        img = open('img/rola.jpg', 'rb')
        bot.sendPhoto(chat_id, img, caption=None, disable_notification=None, reply_to_message_id=None, reply_markup=None)
        img.close()
        
    elif (command == '/meme'):
        mensagemTxt = imagensRandom()
        bot.sendMessage(chat_id, mensagemTxt)

    else:
        bot.sendMessage(chat_id, "Comando não cadastrado")
        
    print(usuario, dataMensagem, '\n')
    GravarLog(sistemaOperacional, dataMensagem, usuario, command) #Sempre quando enviar uma mensagem será gravado um log

bot = telepot.Bot(idToken)
bot.message_loop(handle)

#Gerando o log inicial
print("Aguardando comandos...")
arquivolog = open('log.txt', 'a')
arquivolog.write('\n\n' + time.strftime("%d/%m/%Y %H:%M:%S") +  " Criado p Frederico Oliveira e Lucas Cassiano versão atual: " + versao) #Log inicial
arquivolog.close()

'''
Todas as funções abaixo foram criadas para deixar o código principal limpo, sendo necessário apenas fazer a chamada das funções e aguardar o retorno
'''
#Gravando o log de comandos
def GravarLog(sistemaOperacionalLog, dataMensagemLog, usuarioLog, commandLog):
    arquivolog = open('log.txt', 'a')
    arquivolog.write('\n'+ dataMensagemLog + ' ' + usuarioLog + ' comando executado: ' + commandLog + ' ' + sistemaOperacionalLog)
    arquivolog.close()

#Foi criado esta função para que seja chamada no início do código, futuramente estruturar o código para verificar o sistema operacional
def verificarSistemaOperacional():
    so = platform.system()
    if (so == 'Windows'):
        print("") #Deixei esta parte do código imprimindo vazio, apenas para guardar o bloco
    else:
        print("")
    return so

#EM DESENVOLVIMENTO falta testar no raspi, no windows está retornando normalmente
def consultarTemperatura(sistemaOP):
    if(sistemaOP == "Windows"):
        temperatura = "Nao existe o comando no Windows" 
    else:
        os.system("Shell/my-pi-temp.sh > temp/temp.txt")
        temperatura = open('temp/temp.txt', 'r').read()
    return temperatura
    temperatura.close()

#Coletando dados atmoféricos
def coletarDadosAtmosfericos():
    try:
        dadosColetados = ''
        url = requests.get('https://api.hgbrasil.com/weather/?format=json&cid=BRXX0033')
        teste = json.loads(url.content)

        dados_array = ['temp','description','currently','city','humidity','wind_speedy','sunrise','sunset']
        informacao_user = ['Temperatura: ', 'Condicao tempo: ', 'Periodo: ', 'Cidade: ', 'Umidade do ar: ', 'Velocidade do vento: ', 'Nascimento do sol: ', 'Por do sol: ']
        completa = ['°C', '', '', '', '%', '', '', '']

        for i in range(0, len(dados_array)):
            dadosColetados += (informacao_user[i] + str(teste['results'][dados_array[i]]) + completa[i] + '\n').replace(',', '')
        
        dadosColetados += 'Generate with: https://api.hgbrasil.com/weather/ at {} {}'.format((teste['results']['date']),(teste['results']['time']))
        return dadosColetados
    except:
        return("Erro ao acessar a API de dados atmosféricos")

#Consultando ajuda no
def consultarAjuda(sistemOP):
    if (sistemOP == "Windows"):
        arquivoHelp = open('temp/help.txt', 'r', encoding='utf-8').read()
    else:
        arquivoHelp = open('temp/help.txt', 'r').read()
    return arquivoHelp
    arquivoHelp.close()

def frasesAleatorias(sistemOP):
    if(sistemOP == "Windows"):
        lines = open('temp/frases.txt', 'r', encoding='utf-8').read().splitlines()
    else:
        lines = open('temp/frases.txt', 'r').read().splitlines()
            
    lines = random.choice(lines)
    return lines
    lines.close()

def cotacaoDolar():
    try:
        requisicao = requests.get("http://api.promasters.net.br/cotacao/v1/valores")
        resposta = json.loads(requisicao.text)
        valores = ''
        valores += ('Dólar R$' + str(resposta['valores']['USD']['valor']) + '\n'+
                'Euro R$' + str(resposta['valores']['EUR']['valor']) + '\n'+
                'Libra R$' + str(resposta['valores']['GBP']['valor']) + '\n'+
                'Bitcoin R$' + str(resposta['valores']['BTC']['valor']) + '\n\n' +
                'Generate by http://api.promasters.net.br/cotacao/')
        return(valores)
    
    except:
        return("Erro ao acessar a API cotação de moedas")
        #Pode ser colocado outra API na consulta, assim sempre o código vai retornar alguma informação

def tempoLigado(sistemaOP):
    if (sistemaOP == "Windows"):
        mensagemTxt = "Comando não encontrado no Windows"
    else:
        os.system("uptime > temp/temp.txt")
        #os.system("./Shell/my-pi-temp.sh")
        mensagemTxt = open('temp/temp.txt', 'r').read()
        arquivo = open('temp.txt', 'r') 
    return mensagemTxt
    arquivo.close()

def imagensRandom():
    lines = open('temp/imagens.txt', 'r').read().splitlines()
    lines = random.choice(lines)
    return lines
    lines.close()

while 1:
    time.sleep(10)