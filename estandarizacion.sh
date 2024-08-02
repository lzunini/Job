#!/bin/bash

#######################################################
#######################################################
########## ESTANDARIZACION ##########################
#######################################################
#######################################################

#Procesa los archivos y limpia directorio process:
#valida encabezado, separador de linea, encoding, 
#renombra columnas y archivos, hace copia sin duplicados y loguea en caso de error

#Levanto parametros
while IFS= read -r line
do
    if [[ "$line" == *"dirProcess"* ]]; then
        dirProcess=${line#*=}
    fi
    if [[ "$line" == *"dirError"* ]]; then
        dirError=${line#*=}
    fi
    if [[ "$line" == *"dirArch"* ]]; then
        dirArch=${line#*=}
    fi
done < /home/lucas/parametros.txt

fecha=$(date +%Y%m%d%H%M)

for filename in $(ls $dirProcess)
do
    if [[ -f $dirProcess/$filename ]]; then
        #si no tiene encabezado y cambio el separador corregimos
        if [[ $filename == *defweb* ]]; then
            grep -E 'PROVRES' $dirProcess/$filename -q && encabezado=1 || encabezado=0  
            if [ $encabezado == 0 ]; then
                sed -i 's/;/,/g' $dirProcess/$filename
                sed '1i PROVRES,SEXO,CAUSA,MAT,GRUPEDAD,CUENTA' -i $dirProcess/$filename
            fi
        fi

        if [[ $filename == *poblacion* ]]; then
            #se descomprime el archivo de poblacion, 
            #se suprime archivos adicioneas
            #se suprimen las primeras cuatro lineas que no son encabezado ni datos
            #se renombra la columna de paises 
            #se valida encoding y se mueve a carpeta destino
            unzip -o $dirProcess/$filename -d $dirProcess/
            rm $dirProcess/Metadata_Country_API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv
            rm $dirProcess/Metadata_Indicator_API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv
            sed -i '1,4d' $dirProcess/API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv
            sed -i 's/Country Name/Country/g' $dirProcess/API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv
            if [ $(file -ib $dirProcess/API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv | grep utf | wc -c) -ge 1 ]; then
                mv "$dirProcess/API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv" "$dirArch/tfm_API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv"
            else
                iconv -f ISO-8859-1 -t UTF-8 "$dirProcess/API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv" > "$dirArch/tfm_API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv"
                rm $dirProcess/API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv
            fi
        else 
            #se valida duplicados y encoding
            uniq $dirProcess/$filename > $dirArch/$filename 2>> $dirError/uniq.txt
            if [ $(file -ib $dirArch/$filename | grep utf | wc -c) -ge 1 ]; then
                mv "$dirArch/$filename" "$dirArch/tfm_$filename"
            else
                iconv -f ISO-8859-1 -t UTF-8 "$dirArch/$filename" > "$dirArch/tfm_$filename"
                rm $dirArch/$filename
            fi
        fi
        #se limpia la carpeta process
        rm $dirProcess/$filename

    fi
done