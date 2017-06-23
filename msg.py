#coding: utf-8
import time, random, datetime, telepot, os, subprocess, json, requests, platform

versao = "0.5.6"
dataVersao = "Última atualização dia 18/06/2017, versão 1"

print("{}\n\nBot de telegran para Raspiberry versão: {}, criado por Frederico Oliveira e Lucas Cassiano.\n".format(time.strftime("%d/%m/%Y %H:%M:%S"), versao))

tokenColetaTxt = open('token.txt', 'r').read()
so = platform.system()

def handle(msg):
    chat_id = msg['chat']['id']
    usuario = msg['chat']['username'] #adicionado outra chamada de informações do telegran, agora o username
    command = msg['text']
    dataMensagem = time.strftime('%d/%m/%Y %H:%M:%S')

    print('Comando executado: ', command)
    
    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,10))

    elif command == '/help':
        bot.sendMessage(chat_id, consultarAjuda(so))

    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    elif command == '/cput':
        bot.sendMessage(chat_id, consultarTemperatura(so))

    elif command == '/loop':
        bot.sendMessage(chat_id, frasesAleatorias(so))

    elif command == '/weather':
        bot.sendMessage(chat_id, coletarDadosAtmosfericos())

    elif command == '/currency':
        bot.sendMessage(chat_id, cotacaoDolar())

    elif command == '/uptime':
        bot.sendMessage(chat_id, tempoLigado(so))

    elif command == '/version':
        bot.sendMessage(chat_id, "Versão {}, {}".format(versao, dataVersao))

    elif command == '/print':
        bot.sendMessage(chat_id, "Carregando foto...")
        img = open('img/rola.jpg', 'rb')
        bot.sendPhoto(chat_id, img, caption=None, disable_notification=None, reply_to_message_id=None, reply_markup=None)
        img.close()

    elif command == '/meme':
        bot.sendMessage(chat_id, imagensRandom())

    else:
        bot.sendMessage(chat_id, "Comando não cadastrado")
        
    print(usuario, dataMensagem)
    GravarLog(so, dataMensagem, usuario, command) #Sempre quando enviar uma mensagem será gravado um log

bot = telepot.Bot(tokenColetaTxt)
bot.message_loop(handle)

print("Aguardando comandos...")
arquivolog = open('log.txt', 'a')
arquivolog.write('\n\n{} Criado p Frederico Oliveira e Lucas Cassiano versão atual: {}\n'.format(time.strftime("%d/%m/%Y %H:%M:%S"), versao))
arquivolog.close()

def GravarLog(sistemaOperacionalLog, dataMensagemLog, usuarioLog, commandLog):#Gravando o log de comandos
    arquivolog = open('log.txt', 'a')
    arquivolog.write('{} {} comando executado {} {}\n'.format(dataMensagemLog, usuarioLog, commandLog, sistemaOperacionalLog))
    arquivolog.close()

def consultarTemperatura(sistemaOP):
    if sistemaOP == "Windows":
        temperatura = "Não existe o comando no Windows" 
    else:
        os.system("Shell/my-pi-temp.sh > temp/temp.txt")
        temperatura = open('temp/temp.txt', 'r').read()
    return temperatura
    temperatura.close()

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

def consultarAjuda(sistemOP):
    if sistemOP == "Windows":
        arquivoHelp = open('temp/help.txt', 'r', encoding='utf-8').read()
    else:
        arquivoHelp = open('temp/help.txt', 'r').read()
    return arquivoHelp
    arquivoHelp.close()

def frasesAleatorias(sistemOP):
    if sistemOP == "Windows":
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
        return('Dólar R${}\nEuro R${}\nLibra R${}\nBitcoin R${}\nGenerate by http://api.promasters.net.br/cotacao/'.format(str(resposta['valores']['USD']['valor']), 
        str(resposta['valores']['EUR']['valor']), str(resposta['valores']['GBP']['valor']), str(resposta['valores']['BTC']['valor'])))
    
    except:
        try:
            req = requests.get("https://economia.awesomeapi.com.br/json/USD-BRL/1")
            resposta = json.loads(req.text)
            return("O valor atual do {} é R${}".format(resposta[0]['name'], resposta[0]['high']))
        except:
            return("Erro ao acessar a API padrão e API secundária")

def tempoLigado(sistemaOP):
    if sistemaOP == "Windows":
        mensagemTxt = "Comando não encontrado no Windows"
    else:
        mensagemTxt = subprocess.check_output(["uptime"])
    return mensagemTxt

def imagensRandom():
    lines = open('temp/imagens.txt', 'r').read().splitlines()
    lines = random.choice(lines)
    return lines
    lines.close()

while 1:
    time.sleep(10)