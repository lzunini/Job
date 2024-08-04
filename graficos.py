# -*- coding: utf-8 -*-
import os.path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utilidades.parametros import (ruta_output)



## setting y parametros

os.environ["XDG_SESSION_TYPE"] = "xcb"
sns.set(style="darkgrid")





## levanto info a memoria
df_grupo_tt = pd.read_csv(ruta_output + 'df_grupo_tt.csv')
df_causas_tt = pd.read_csv(ruta_output + 'df_causas_tt.csv')
df_poblacion_tt = pd.read_csv(ruta_output + 'df_poblacion.csv')
df_dic = pd.read_csv(ruta_output + 'df_dic.csv')

############################################################
######### GENERACION DE GRAFICOSS POR GRUPO ETAREO #########
############################################################

## GRAFICO DE LINEA CON DATOS ANUALES DE DEFUNCIONES POR GRUPO ETAREO SOBRE DEFUNCIONES EN EL ANIO 
def anulaes_lineas():
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    plt.title("EVOLUCION DE LAS DEFUNCIONES")
    titulo = 'EVOLUCION DEFUNCIONES POR EDAD SOBRE DEFUNCIONES 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2)
    plt.title(titulo)
    plt.xlabel("EDADES")
    plt.ylabel("PORCENTAJE (defunciones por edad sobre defunciones)")
    for ANIO in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26):
        df_grupo = df_grupo_tt.query('ANIO == @ANIO')
        if len(df_grupo)>0:
            df_grupo = df_grupo.sort_values(by=['GRUPEDAD'], ascending=True)
            total_anio = '20'+str(ANIO).zfill(2) + ' DEFUNCIONES: ' + str(df_grupo['CUENTA'].sum())
            GRUPEDAD_line = sns.lineplot(data=df_grupo, x='GRUPEDAD', y='PORC', ax=ax, label=total_anio)
    GRUPEDAD_line.get_figure().savefig(ruta_output + 'EVOLUCION_DEFUNCIONES_GRUPEDAD_DEFUNCIONES_LINE.pdf', format='pdf')

## GRAFICO DE LINEA CON DATOS ANUALES DE DEFUNCIONES POR GRUPO ETAREO SOBRE POBLACION EN EL ANIO 
def total_lineas_poblacion():
    columns_names = df_poblacion_tt.columns.values
    columns_names_list = list(columns_names)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    
    titulo = 'EVOLUCION DEFUNCIONES POR EDAD SOBRE POBLACION 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2)
    plt.title(titulo)
    plt.xlabel("EDADES")
    plt.ylabel("PORCENTAJE (defunciones por edad sobre poblacion)")
    
    for string in ('2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026'):
        if string in columns_names_list:
            poblacion_tt = df_poblacion_tt[string]
            anio=int(string[2:4])
            
            df_grupo = df_grupo_tt.query('ANIO == @anio')
            if len(df_grupo)>0:
                defunciones = df_grupo['CUENTA'].sum()
                porctt = round(int(defunciones)/int(poblacion_tt.iloc[0])*100, 2)

                GRUPEDAD_line_tt = df_grupo.groupby(['GRUPEDAD'])['CUENTA'].sum().reset_index()
                GRUPEDAD_line_tt["poblacion_tt"] = int(poblacion_tt.iloc[0])

                GRUPEDAD_line_tt['PORCTT'] = GRUPEDAD_line_tt['CUENTA']/(GRUPEDAD_line_tt['poblacion_tt'])*100

                total_anio = str(string) + ' DEFUNCIONES: ' + str(df_grupo['CUENTA'].sum()) +' POBLACION: ' + str(int(poblacion_tt.iloc[0])) + ' PORCENTAJE: ' + str(porctt) + '%'
                GRUPEDAD_lin = sns.lineplot(data=GRUPEDAD_line_tt, x='GRUPEDAD', y='PORCTT', ax=ax, label=total_anio)
            
    GRUPEDAD_lin.get_figure().savefig(ruta_output + 'EVOLUCION_DEFUNCIONES_GRUPEDAD_POBLACION_LINE.pdf', format='pdf')

## LINEAS TOTAL ANIOS
def total_lineas():
    GRUPEDAD_line_tt = df_grupo_tt.groupby(['GRUPEDAD'])['CUENTA'].sum().reset_index()
    GRUPEDAD_line_tt['PORCTT'] = GRUPEDAD_line_tt['CUENTA']/(GRUPEDAD_line_tt['CUENTA'].sum())*100

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)

    titulo = 'DEFUNCIONES POR EDAD ACUMULADO SOBRE DEFUNCIONES 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2)
    plt.title(titulo)
    plt.xlabel("EDADES")
    plt.ylabel("PORCENTAJE (defunciones por edad sobre total defunciones)")
    total_anio = ' TOTAL DEFUNCIONES: 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2) + ': ' + str(df_grupo_tt['CUENTA'].sum())
    GRUPEDAD_lin = sns.lineplot(data=GRUPEDAD_line_tt, x='GRUPEDAD', y='PORCTT', ax=ax, label=total_anio)
    GRUPEDAD_lin.get_figure().savefig(ruta_output + 'GRUPEDAD_LINE_DEFUNCIONES_ACUMULADO.pdf', format='pdf')

## GRAFICO DE BARRA CON DATOS ACUMULADOS DE DEFUNCIONES POR GRUPO ETAREO SOBRE DEFUNCIONES ACUMULADAS 
def total_barra():
    GRUPEDAD_bar = df_grupo_tt.groupby(['GRUPEDAD'])['CUENTA'].sum().reset_index()
    GRUPEDAD_bar['PORCTT'] = GRUPEDAD_bar['CUENTA']/(GRUPEDAD_bar['CUENTA'].sum())*100

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    
    titulo = 'DEFUNCIONES POR EDAD ACUMULADO SOBRE DEFUNCIONES 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2)
    total_anio = 'DEFUNCIONES 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2) + ': ' + str(df_grupo_tt['CUENTA'].sum())
    plt.title(titulo + '\n' + total_anio)
    plt.xlabel("EDADES")
    plt.ylabel("PORCENTAJE (defunciones por edad sobre total defunciones)")
    GRUPEDAD_barn = sns.barplot(data=GRUPEDAD_bar, x='GRUPEDAD', y='PORCTT', ax=ax, hue='GRUPEDAD')
    GRUPEDAD_barn.set(xlabel='EDADES', ylabel='PORCENTAJE (defunciones por edad sobre total defunciones)')
    h, l = ax.get_legend_handles_labels()
    ax.legend(h, "", title=None)
    
    GRUPEDAD_barn.get_figure().savefig(ruta_output + 'ACUMULADO_DEFUNCIONES_GRUPEDAD_DEFUNCIONES_BAR.pdf', format='pdf')

############################################################
###### GENERACION DE GRAFICOSS POR CAUSA DE DEFUNCION ######
############################################################

## GRAFICO DE PUNTOS CON DATOS ANUALES DE DEFUNCIONES POR CAUSA (TOP 10) SOBRE DEFUNCIONES ANUALES  
def total_barra_causa():
    CAUSA_bar = df_causas_tt.groupby(['ANIO', 'CAUSA'])['CUENTA'].sum().reset_index()

    top_causas = df_causas_tt.groupby(['CAUSA'])['CUENTA'].sum().reset_index()
    top_causas['PORCTTA'] = top_causas['CUENTA']/(top_causas['CUENTA'].sum())*100
    top_causas = top_causas.sort_values(by=['CUENTA'], ascending=False)
    top_causas = top_causas.head(15)

    titulo = 'CAUSAS DE DEFUNCIONES SOBRE DEFUNCIONES ANUALES 20' + str(CAUSA_bar['ANIO'].min()).zfill(2) + ' a ' + '20' + str(CAUSA_bar['ANIO'].max()).zfill(2) + '\n' + '   TOP 10 DE CADA ANIO'
    fig = plt.figure(figsize=(19, 10))
    ax = fig.add_subplot(1, 2, 1)
    pd.options.mode.chained_assignment = None  # default='warn'
    
    i=0

    for string in ('2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026'):
        anio=int(string[2:4])
        df_CAUSA = CAUSA_bar.query('ANIO == @anio')
        if len(df_CAUSA)>0:

            total_anio = str(string) + ' DEFUNCIONES: ' + str(df_CAUSA['CUENTA'].sum())
            
            df_CAUSA = df_CAUSA
            df_CAUSA['PORCTT'] = df_CAUSA['CUENTA']/(df_CAUSA['CUENTA'].sum())*100
            
            df_CAUSA = df_CAUSA.sort_values(by=['CUENTA'], ascending=False)
            df_CAUSA = df_CAUSA.head(10)

            if i==0:
                df_causa_descr = df_CAUSA
            else:
                df_causa_descr = df_causa_descr._append(df_CAUSA)
            i=i+1

            CAUSA_barn = sns.scatterplot(data=df_CAUSA, x='CAUSA', y='PORCTT', ax=ax, label=total_anio)
            #GRUPEDAD_lin = sns.lineplot(data=GRUPEDAD_line_tt, x='GRUPEDAD', y='PORCTT', ax=ax, label=total_anio)
            CAUSA_barn.set(xlabel='CAUSA', ylabel='PORCENTAJE (defunciones por edad sobre total defunciones)')
    
    ## inner join, se agrega descripcion (VALOR) y porcentaje total
    df_causa_descr = pd.merge(df_dic, df_causa_descr, on='CAUSA', how='inner')
    df_causa_descr = pd.merge(top_causas, df_causa_descr, on='CAUSA', how='inner')
    
    df_causa_descr = df_causa_descr.drop_duplicates(['CAUSA', 'PORCTTA', 'VALOR'])[['CAUSA', 'PORCTTA', 'VALOR']]
    df_causa_descr = df_causa_descr.sort_values(by=['PORCTTA'], ascending=False)
    
    texto = ''
    for h in range(len(df_causa_descr)):
        valor = str(df_causa_descr.iloc[h]['VALOR'])
        if valor == 'nan':
            valor = 'Sin especificar'
        
        texto = texto + str(round(int(df_causa_descr.iloc[h]['PORCTTA']),2)) + '%* ' + str(df_causa_descr.iloc[h]['CAUSA']) + ' ' +  str(valor) + '\n'
    texto = texto + '\n' +'* suma(CAUSAS todos los años)/suma(defunciones todos los años)'

    plt.title(titulo)
    plt.xlabel("CAUSA")
    plt.ylabel("PORCENTAJE (defunciones por causa sobre total defunciones)")
    plt.text(1.1, 0.005, texto, transform = ax.transAxes, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'), fontsize=10)
    ax.legend(bbox_to_anchor=(1.65, 1.05), borderaxespad=5, fancybox=True, framealpha=1, shadow=False, borderpad=1, edgecolor='black')

    
    CAUSA_barn.get_figure().savefig(ruta_output + 'ACUMULADO_DEFUNCIONES_CAUSAS_DEFUNCIONES_PUNT.pdf', format='pdf')
    
    
total_barra_causa()
anulaes_lineas()
#total_lineas()
total_barra()
total_lineas_poblacion()
