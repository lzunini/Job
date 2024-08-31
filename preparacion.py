# -*- coding: utf-8 -*-
import os.path
import pandas as pd
from utilidades.parametros import (ruta_input, ruta_output)

############################################################
########### PREPARACION DE DATASET PARA ANALISIS ###########
############################################################


## levanto el diccionario con los cod de defuncion 
dic = pd.read_excel(io = ruta_input + 'tfm_descdef.xlsx', sheet_name = 'CODMUER', header = 0, names=None, index_col=None,engine = 'openpyxl', dtype={'CO': str})

dic.rename(columns={'CODIGO': 'CAUSA'}, inplace=True)
dic.drop_duplicates()
dic.to_csv(ruta_output + 'df_dic.csv', index=False)

df_grupo_tt = None
df_causas_tt = None

## procesamiento de archivos para extraer datos de grupo etarios y causas de defuncion
for ANIO in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26'):
    if os.path.isfile(ruta_input + 'tfm_defweb' + ANIO + '.csv'):
        #Levanto archivo
        df = pd.read_csv(ruta_input + 'tfm_defweb' + ANIO + '.csv')
        df.drop_duplicates()

        #Se Agrupa por CAUSA 
        df_causas = df.groupby(['CAUSA'])['CUENTA'].sum().reset_index()

        ## inner join, se agrega descripcion (VALOR)
        df_causas = pd.merge(dic, df_causas, on='CAUSA', how='inner')
        

        #Se unifica grupo etario, se descartan los sin especificar -no representan gran cantidad- y se agrupa por edad
        df_grupo = df[['GRUPEDAD', 'CUENTA']]

        df_grupo.loc[df_grupo['GRUPEDAD'] == '17_80 y más', 'GRUPEDAD'] = 82
        df_grupo.loc[df_grupo['GRUPEDAD'] == '16_75 a 79', 'GRUPEDAD'] = 77
        df_grupo.loc[df_grupo['GRUPEDAD'] == '15_70 a 74', 'GRUPEDAD'] = 72
        df_grupo.loc[df_grupo['GRUPEDAD'] == '14_65 a 69', 'GRUPEDAD'] = 67
        df_grupo.loc[df_grupo['GRUPEDAD'] == '13_60 a 64', 'GRUPEDAD'] = 62
        df_grupo.loc[df_grupo['GRUPEDAD'] == '12_55 a 59', 'GRUPEDAD'] = 57
        df_grupo.loc[df_grupo['GRUPEDAD'] == '11_50 a 54', 'GRUPEDAD'] = 52
        df_grupo.loc[df_grupo['GRUPEDAD'] == '10_45 a 49', 'GRUPEDAD'] = 47
        df_grupo.loc[df_grupo['GRUPEDAD'] == '09_40 a 44', 'GRUPEDAD'] = 42
        df_grupo.loc[df_grupo['GRUPEDAD'] == '08_35 a 39', 'GRUPEDAD'] = 37
        df_grupo.loc[df_grupo['GRUPEDAD'] == '07_30 a 34', 'GRUPEDAD'] = 32
        df_grupo.loc[df_grupo['GRUPEDAD'] == '06_25 a 29', 'GRUPEDAD'] = 27
        df_grupo.loc[df_grupo['GRUPEDAD'] == '05_20 a 24', 'GRUPEDAD'] = 22
        df_grupo.loc[df_grupo['GRUPEDAD'] == '04_15 a 19', 'GRUPEDAD'] = 17
        df_grupo.loc[df_grupo['GRUPEDAD'] == '03_10 a 14', 'GRUPEDAD'] = 12
        df_grupo.loc[df_grupo['GRUPEDAD'] == '02_1 a 9', 'GRUPEDAD'] = 5
        df_grupo.loc[df_grupo['GRUPEDAD'] == '01_Menor de 1 año', 'GRUPEDAD'] = 0
        df_grupo.loc[df_grupo['GRUPEDAD'] == '99_Sin especificar', 'GRUPEDAD'] = 50

        df_grupo = df_grupo.query('GRUPEDAD != 50')

        df_grupo = df_grupo.groupby(['GRUPEDAD'])['CUENTA'].sum().reset_index()
        df_grupo = df_grupo.sort_values(by=['CUENTA'], ascending=False)

        #Se agrega columna con Porcentajes
        df_causas['PORC'] = df_causas['CUENTA']/(df_causas['CUENTA'].sum())*100
        df_grupo['PORC'] = df_grupo['CUENTA']/(df_grupo['CUENTA'].sum())*100

        #Se agrega la columna anio
        df_grupo['ANIO'] = ANIO
        df_causas['ANIO'] = ANIO

        if df_grupo_tt is not None:
            df_grupo_tt = pd.concat([df_grupo_tt, df_grupo])
        else:
            df_grupo_tt = df_grupo
        
        if df_causas_tt is not None:
            df_causas_tt = pd.concat([df_causas_tt, df_causas])
        else:
            df_causas_tt = df_causas

df_causas_tt['PORCTT'] = df_causas_tt['CUENTA']/(df_causas_tt['CUENTA'].sum())*100
df_causas_tt = df_causas_tt.sort_values(by=['PORCTT'], ascending=False)        

df_grupo_tt['PORCTT'] = df_grupo_tt['CUENTA']/(df_causas_tt['CUENTA'].sum())*100

## guardo en directorio output dataset para analisis

df_grupo_tt.to_csv(ruta_output + 'df_grupo_tt.csv', index=False)


df_causas_tt.to_csv(ruta_output + 'df_causas_tt.csv', index=False)

## proceso archivo naciemitos y guardado en directorio output dataset para analisis
if os.path.isfile(ruta_input + 'tfm_nacidos.csv'):
    df = pd.read_csv(ruta_input + 'tfm_nacidos.csv')
    df.drop_duplicates()
    df_nacimientos = df.groupby(['anio'])['nacimientos_cantidad'].sum().reset_index()
    df_nacimientos.to_csv(ruta_output + 'df_nacimientos_tt.csv', index=False)

## proceso archivo poblacion y guardado en directorio output dataset para analisis
if os.path.isfile(ruta_input + 'tfm_API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv'):
    df = pd.read_csv(ruta_input + 'tfm_API_SP.POP.TOTL_DS2_es_csv_v2_2028466.csv')
    df.drop_duplicates()
    df_poblacion = df.query('Country == "Argentina"')
    df_poblacion.to_csv(ruta_output + 'df_poblacion.csv', index=False)