# RaspiPot

Esta aplicação foi criada como Hobby para estudos com Raspiberry + Python, usando o Telegran, foram adicionados alguns comandos e que retornam informações diversas, conforme lista abaixo.

/roll = Retorna um valor entre 1 ate 10</br>
/time = Retorna a hora do sistema</br>
/cput = Retorna temperatura do processador "Apenas Linux"</br>
/loop = Faz um loop retornando 20 mensagens</br>
/weather = Informações meteorológicas de Belo Horizonte</br>
/currency = Cotacao de moedas (Dólar, Euro, Libra, Bitcoin)</br>
/uptime = Verifica quanto tempo está ligado o equipamento "Apenas Linux"</br>
/version = Versão do Bot</br>
/print = Envia uma imagem de uma rola</br>
/Meme = Envia um link de um meme randômico</br>


Foram utilizados diversos módulos, vários deles já vem instalados por padrão.
time, random, datetime, os, subprocess, platform, telepot, json, requests 

Foi utilizado um exemplo básico de envio de mensagens 

Instalar telepot
https://github.com/nickoala/telepot

Documentação do Modulo Json
https://docs.python.org/3/library/json.html

Como módulo Requests
https://github.com/kennethreitz/requests

Inicialmente para utilizar o bot no Telegran, é necessário ter o token, que é gerado pelo BotFather, instruções no link https://core.telegram.org/bots#6-botfather
Para este Bot, eu utilizei um arquivo externo, que atualmente não está no projeto, sendo necessário que você crie o arquivo com o nome "token.txt", depois inserir o seu token no arquivo na raiz da aplicação.

Foi utilizado outras APIs, com funções diversas como:

Coleta de dados atmosféricos https://api.hgbrasil.com/weather/

Coleta de dados financeiros em relação a moeda brasileira http://api.promasters.net.br/cotacao/

#Organizar o documento posteriormente