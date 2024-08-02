#!/bin/bash

#######################################################
#######################################################
########## BACKUP  ####################################
#######################################################
#######################################################

#Copia a backup los archivos crudos, los mueve a process y comprime backup. 
#En caso de error se inserta en el log

#Levanto parametros
while IFS= read -r line
do
    if [[ "$line" == *"dirSource"* ]]; then
        dirSource=${line#*=}
    fi
    if [[ "$line" == *"dirBackup"* ]]; then
        dirBackup=${line#*=}
    fi
    if [[ "$line" == *"dirProcess"* ]]; then
        dirProcess=${line#*=}
    fi
    if [[ "$line" == *"dirError"* ]]; then
        dirError=${line#*=}
    fi
done < /home/lucas/parametros.txt

fecha=$(date +%Y%m%d%H%M)

for filename in $(ls $dirSource)
do
    if [ -f $dirSource/$filename ]; then
        cp $dirSource/$filename $dirBackup/${fecha}_${filename}
        mv $dirSource/$filename $dirProcess/$filename
    fi
done

{ err=$(gzip -9 $dirBackup/*.csv 2>&1 >&3 3>&-); } 3>&1

if [ ! -z "$err" ]; then
    echo $fecha $err >> $dirError/backup.txt
fi