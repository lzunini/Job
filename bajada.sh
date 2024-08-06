#!/bin/bash

#######################################################
#######################################################
########## BAJADA #####################################
#######################################################
#######################################################

#Verifica si existe archivo en origen y realiza la bajada

#Levanto parametros
while IFS= read -r line
do
    if [[ "$line" == *"dirSource"* ]]; then
        dirSource=${line#*=}
    fi
    if [[ "$line" == *"pagina_defweb"* ]]; then
        pagina_defweb=${line#*=}
    fi
    if [[ "$line" == *"pagina_nacidos"* ]]; then
        pagina_nacidos=${line#*=}
    fi
    if [[ "$line" == *"pagina_poblacion"* ]]; then
        pagina_poblacion=${line#*=}
    fi
    if [[ "$line" == *"pagina_descdef"* ]]; then
        pagina_descdef=${line#*=}
    fi
done < /home/lucas/parametros.txt

#Buscar archivos defunciones del 2001 al 2026 si los encuentra hace una bajada
fecha=$(date +%Y%m%d%H%M)
for x in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26; do
    pagina="${pagina_defweb}${x}.csv"
    resultado=$(curl -s -I $pagina | head -n 1 | awk '{print $2}')
    echo $pagina
    if [ $resultado == 200 ]; then
        curl -o $dirSource/defweb${x}.csv $pagina
    fi
done

#Buscar archivo nacimientos si lo encuentra hace una bajada
pagina="${pagina_nacidos}"
resultado=$(curl -s -I $pagina | head -n 1 | awk '{print $2}')
echo $pagina
if [ $resultado == 200 ]; then
    curl -o $dirSource/nacidos.csv $pagina
fi

#Buscar archivo poblacion si lo encuentra hace una bajada
pagina="${pagina_poblacion}"
resultado=$(curl -X GET -s -I $pagina | head -n 1 | awk '{print $2}')
echo $pagina
if [ $resultado == 200 ]; then
    curl -o $dirSource/poblacion.zip $pagina
fi

#Buscar archivo descripcion campos si lo encuentra hace una bajada
pagina="${pagina_descdef}"
resultado=$(curl -s -I $pagina | head -n 1 | awk '{print $2}')
echo $pagina
if [ $resultado == 200 ]; then
    curl -o $dirSource/descdef.xlsx $pagina
fi