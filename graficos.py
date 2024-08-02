# -*- coding: utf-8 -*-
import os.path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utilidades.parametros import (ruta_output)

############################################################
######### GENERACION DE GRAFICOSS POR GRUPO ETAREO #########
############################################################

## setting y parametros

os.environ["XDG_SESSION_TYPE"] = "xcb"
sns.set(style="darkgrid")

params = {0: {'color': 'b', 'label': 'menor a 1'},
        5: {'color': 'g', 'label': '1 a 9'},
        12: {'color': 'r', 'label': '10 a 14'},
        17: {'color': 'c', 'label': '15 a 19'},
        22: {'color': 'm', 'label': '20 a 24'},
        27: {'color': 'y', 'label': '25 a 30'},
        32: {'color': 'k', 'label': '31 a 34'},
        37: {'color': 'g', 'label': '35 a 39'},
        42: {'color': 'b', 'label': '40 a 44'},
        47: {'color': 'g', 'label': '45 a 49'},
        52: {'color': 'r', 'label': '50 a 54'},
        57: {'color': 'c', 'label': '55 a 59'},
        62: {'color': 'm', 'label': '60 a 64'},
        67: {'color': 'y', 'label': '65 a 69'},
        72: {'color': 'k', 'label': '70 a 74'},
        77: {'color': 'g', 'label': '75 a 79'},
        82: {'color': 'b', 'label': '80 mas'}}

## levanto info a memoria
df_grupo_tt = pd.read_csv(ruta_output + 'df_grupo_tt.csv')
df_poblacion_tt = pd.read_csv(ruta_output + 'tfm_poblacion.csv')

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
        #df = pd.read_csv(ruta_output + 'df_grupo_tt.csv', encoding='latin-1')
        df_grupo = df_grupo_tt.query('ANIO == @ANIO')
        if len(df_grupo)>0:
            #df_grupo.to_csv('df_grupo_'+str(ANIO)+'.csv', index=False)
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
   
    GRUPEDAD_barn = sns.barplot(data=GRUPEDAD_bar, x='GRUPEDAD', y='PORCTT', ax=ax)
    GRUPEDAD_barn.set(xlabel='EDADES', ylabel='PORCENTAJE (defunciones por edad sobre total defunciones)')
    GRUPEDAD_barn.get_figure().savefig(ruta_output + 'ACUMULADO_DEFUNCIONES_GRUPEDAD_DEFUNCIONES_BAR.pdf', format='pdf')

    
anulaes_lineas()
#total_lineas()
total_barra()
total_lineas_poblacion()