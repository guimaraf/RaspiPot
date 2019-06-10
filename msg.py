#coding: utf-8
import time, random, datetime, telepot, os, subprocess, json, requests, platform

version = "0.6.1"
dateVersion = "Last day update 10/06/2019"

print("{}\n\nBot of telegram for Raspberry version: {}, created by Frederico Oliveira and Lucas Cassiano.\n".format(time.strftime("%d/%m/%Y %H:%M:%S"), version))

tokenCollectTxtFile = open('token.txt', 'r').read()
so = platform.system()

def handle(msg):
    chat_id = msg['chat']['id']
    user = msg['chat']['username']
    command = msg['text']
    dataMensagem = time.strftime('%d/%m/%Y %H:%M:%S')

    print('Command executed: ', command)
    
    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,10))

    elif command == '/help':
        bot.sendMessage(chat_id, ConsultHelpFile(so))

    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    elif command == '/cput':
        bot.sendMessage(chat_id, CollectTemperatureExternalAPI(so))

    elif command == '/loop':
        bot.sendMessage(chat_id, RandoomPhrases(so))

    elif command == '/weather':
        bot.sendMessage(chat_id, CollectAtmosphericData())

    elif command == '/currency':
        bot.sendMessage(chat_id, PriceDolar())

    elif command == '/uptime':
        bot.sendMessage(chat_id, AmountTimeOn(so))

    elif command == '/version':
        bot.sendMessage(chat_id, "Versão {}, {}".format(version, dateVersion))

    elif command == '/print':
        bot.sendMessage(chat_id, "Loading photo...")
        img = open('img/rola.jpg', 'rb')
        bot.sendPhoto(chat_id, img, caption=None, disable_notification=None, reply_to_message_id=None, reply_markup=None)
        img.close()

    elif command == '/meme':
        bot.sendMessage(chat_id, ImagensRandom())

    else:
        try:
            bot.sendMessage(chat_id, eval(command))
        except:
            bot.sendMessage(chat_id, "Command not registered")

    print(user, dataMensagem)
    RecordLog(so, dataMensagem, user, command) #Always when sending a message will be saved a log

bot = telepot.Bot(tokenCollectTxtFile)
bot.message_loop(handle)

print("Waiting for commands...")
fileLog = open('log.txt', 'a')
fileLog.write('\n\n{} Created by Frederico Oliveira and Lucas Cassiano Current version: {}\n'.format(time.strftime("%d/%m/%Y %H:%M:%S"), version))
fileLog.close()

def RecordLog(logOperatingSystem, dateMessageLog, userLog, commandLog):
    fileLog = open('log.txt', 'a')
    fileLog.write('{} {} command executed {} {}\n'.format(dateMessageLog, userLog, commandLog, logOperatingSystem))
    fileLog.close()

def CollectTemperatureExternalAPI(opSystem):
    try:
        if opSystem == "Windows":
            temperature = "Not implemented hardware temperature data collection in windows." 
        else:
            dataRaspi = "", 
            tempData = ""
            user = ""
            tempUser = ""
            cpu = ""
            gpu = ""
            tempGpu = ""

            tempData = os.system("date > temp/nome.txt")
            dataRaspi = open("temp/nome.txt", "r").read()
            tempUser = os.system("hostname > temp/user.txt")
            user = open("temp/user.txt", "r").read()
            cpu = open("/sys/class/thermal/thermal_zone0/temp").read()
            tempGpu = os.system("/opt/vc/bin/vcgencmd measure_temp  > temp/gpu.txt")
            gpu = open("temp/gpu.txt", "r").read()

            temperature = "{} {} CPU => {:.1f}'C \n GPU => {}".format(dataRaspi, user, float(cpu)/1000, gpu)

        return temperature
        temperature.close()
    except:
        return("Error accessing raspberry hardware temperature data.")

def CollectAtmosphericData():
    try:
        collectedData = ''
        requestJson = requests.get('https://api.hgbrasil.com/weather/?format=json&cid=BRXX0033')
        stringJsonBase = json.loads(requestJson.content)

        previousComplement = ['Temperatura: ', 'Condicao tempo: ', 'Periodo: ', 'Cidade: ', 'Umidade do ar: ', 'Velocidade do vento: ', 'Nascimento do sol: ', 'Por do sol: ']
        dataArray = ['temp','description','currently','city','humidity','wind_speedy','sunrise','sunset']
        finalComplement = ['°C', '', '', '', '%', '', '', '']

        for i in range(0, len(dataArray)):
            collectedData += (previousComplement[i] + str(stringJsonBase['results'][dataArray[i]]) + finalComplement[i] + '\n').replace(',', '')
        
        collectedData += 'Generate with: https://api.hgbrasil.com/weather/ at {} {}'.format((stringJsonBase['results']['date']),(stringJsonBase['results']['time']))
        return collectedData
    except:
        return("Error accessing the Atmospheric Data API.")

def ConsultHelpFile(sistemOP):
    if sistemOP == "Windows":
        helpFile = open('temp/help.txt', 'r', encoding='utf-8').read()
    else:
        helpFile = open('temp/help.txt', 'r').read()
    return helpFile
    helpFile.close()

def RandoomPhrases(sistemOP):
    if sistemOP == "Windows":
        lines = open('temp/frases.txt', 'r', encoding='utf-8').read().splitlines()
    else:
        lines = open('temp/frases.txt', 'r').read().splitlines()
    lines = random.choice(lines)
    return lines
    lines.close()

def PriceDolar():
    try:
        requestJson = requests.get("http://api.promasters.net.br/cotacao/v1/valores")
        stringJsonBase = json.loads(requestJson.text)
        return('Dólar R${}\nEuro R${}\nLibra R${}\nBitcoin R${}\nGenerate by http://api.promasters.net.br/cotacao/'.format(str(stringJsonBase['valores']['USD']['valor']), 
        str(stringJsonBase['valores']['EUR']['valor']), str(stringJsonBase['valores']['GBP']['valor']), str(stringJsonBase['valores']['BTC']['valor'])))
    
    except:
        try:
            requestJsonExtra = requests.get("https://economia.awesomeapi.com.br/json/USD-BRL/1")
            stringJsonBase = json.loads(requestJsonExtra.text)
            return("The current value of the {} é R${}".format(stringJsonBase[0]['name'], stringJsonBase[0]['high']))
        except:
            return("Error accessing standard API and secondary API.")

def AmountTimeOn(opSystem):
    if opSystem == "Windows":
        messageTxt = "Command Not Found in Windows."
    else:
        messageTxt = subprocess.check_output(["uptime"])
    return messageTxt

def ImagensRandom():
    lines = open('temp/imagens.txt', 'r').read().splitlines()
    lines = random.choice(lines)
    return lines
    lines.close()

while 1:
    time.sleep(10)