#!/bin/bash
# variaveis para definir e organizar nomes, datas e logs
#`date +%d/%m/%Y`=DATA
function Agora(){
    date +%H:%M:%S
    }

D=`date +%d%m%Y`
LOG=/media/USBHDD1/shares/zbkp.log

echo -e "`Agora`:log de atividade"   
sleep 1
echo "horas" `date +%H:%M:%S` 
sleep 1
echo -e "`Agora`:log de atividade"




