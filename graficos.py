# -*- coding: utf-8 -*-
import os.path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
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
######### GENERACION DE GRAFICOSS POR GRUPO ETARIO #########
############################################################

## GRAFICO DE LINEA CON DATOS ANUALES DE DEFUNCIONES POR GRUPO ETARIO SOBRE DEFUNCIONES EN EL ANIO 
def anulaes_lineas():
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    plotly_fig = go.Figure()
    titulo = 'EVOLUCION DEFUNCIONES POR EDAD SOBRE DEFUNCIONES 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2)
    
    plotly_fig.update_layout(title_text=titulo)
    plotly_fig.update_layout(legend_title_text = "Referencias")
    plotly_fig.update_xaxes(title_text="EDADES")
    plotly_fig.update_yaxes(title_text="PORCENTAJE (defunciones por edad sobre defunciones)")

    plt.title(titulo)
    plt.xlabel("EDADES")
    plt.ylabel("PORCENTAJE (defunciones por edad sobre defunciones)")
    for ANIO in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26):
        df_grupo = df_grupo_tt.query('ANIO == @ANIO')
        if len(df_grupo)>0:
            df_grupo = df_grupo.sort_values(by=['GRUPEDAD'], ascending=True)
            total_anio = '20'+str(ANIO).zfill(2) + ' DEFUNCIONES: ' + str(df_grupo['CUENTA'].sum())
            GRUPEDAD_line = sns.lineplot(data=df_grupo, x='GRUPEDAD', y='PORC', ax=ax, label=total_anio)
            plotly_fig.add_trace(go.Scatter(x=df_grupo["GRUPEDAD"], y=df_grupo["PORC"], mode="lines", marker=dict(color=df_grupo["GRUPEDAD"]),  name=total_anio, hovertemplate="Contestant=%s<br>Edades=%%{x}<br>Defunciones por Edad/Defunciones=%%{y}<extra></extra>"% total_anio ))
    GRUPEDAD_line.get_figure().savefig(ruta_output + 'EVOLUCION_DEFUNCIONES_GRUPEDAD_DEFUNCIONES_LINE.pdf', format='pdf')
    plotly_fig.write_html(ruta_output + "EVOLUCION_DEFUNCIONES_GRUPEDAD_DEFUNCIONES_LINE_HTML.html")


## GRAFICO DE LINEA CON DATOS ANUALES DE DEFUNCIONES POR GRUPO ETARIO SOBRE POBLACION EN EL ANIO 
def total_lineas_poblacion():
    columns_names = df_poblacion_tt.columns.values
    columns_names_list = list(columns_names)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    titulo = 'EVOLUCION DEFUNCIONES POR EDAD SOBRE POBLACION 20' + str(df_grupo_tt['ANIO'].min()).zfill(2) + ' a ' + '20' + str(df_grupo_tt['ANIO'].max()).zfill(2)

    plotly_fig = go.Figure()

    plotly_fig.update_layout(title_text=titulo)
    plotly_fig.update_layout(legend_title_text = "Referencias")
    plotly_fig.update_xaxes(title_text="EDADES")
    plotly_fig.update_yaxes(title_text="PORCENTAJE (defunciones por edad sobre poblacion)")
    
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
                plotly_fig.add_trace(go.Scatter(x=GRUPEDAD_line_tt["GRUPEDAD"],  y=GRUPEDAD_line_tt["PORCTT"], mode="lines", marker=dict(color=GRUPEDAD_line_tt["GRUPEDAD"]), name=total_anio, hovertemplate="Contestant=%s<br>Edades=%%{x}<br>Defunciones/Poblacion=%%{y}<extra></extra>"% total_anio  ))
            
    GRUPEDAD_lin.get_figure().savefig(ruta_output + 'EVOLUCION_DEFUNCIONES_GRUPEDAD_POBLACION_LINE.pdf', format='pdf')
    plotly_fig.write_html(ruta_output + "EVOLUCION_DEFUNCIONES_GRUPEDAD_POBLACION_LINE_HTML.html")

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

## GRAFICO DE BARRA CON DATOS ACUMULADOS DE DEFUNCIONES POR GRUPO ETARIO SOBRE DEFUNCIONES ACUMULADAS 
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


    plotly_fig=go.Figure(data=go.Bar(x=GRUPEDAD_bar["GRUPEDAD"], y=GRUPEDAD_bar["PORCTT"],  marker=dict(color=GRUPEDAD_bar["GRUPEDAD"])))
    plotly_fig.update_layout(title_text=titulo + '\n' + total_anio)
    plotly_fig.update_xaxes(title_text="EDADES")
    plotly_fig.update_yaxes(title_text="PORCENTAJE (defunciones por edad sobre total defunciones)")
    
    
    plotly_fig.write_html(ruta_output + "ACUMULADO_DEFUNCIONES_GRUPEDAD_DEFUNCIONES_BAR_HTML.html")


############################################################
###### GENERACION DE GRAFICOSS POR CAUSA DE DEFUNCION ######
############################################################

## GRAFICO DE PUNTOS CON DATOS ANUALES DE DEFUNCIONES POR CAUSA (TOP 10) SOBRE DEFUNCIONES ANUALES  
def total_pont_causa():
    CAUSA_bar = df_causas_tt.groupby(['ANIO', 'CAUSA'])['CUENTA'].sum().reset_index()

    top_causas = df_causas_tt.groupby(['CAUSA'])['CUENTA'].sum().reset_index()
    top_causas['PORCTTA'] = top_causas['CUENTA']/(top_causas['CUENTA'].sum())*100
    top_causas = top_causas.sort_values(by=['CUENTA'], ascending=False)
    top_causas = top_causas.head(15)

    titulo = 'CAUSAS DE DEFUNCIONES SOBRE DEFUNCIONES ANUALES 20' + str(CAUSA_bar['ANIO'].min()).zfill(2) + ' a ' + '20' + str(CAUSA_bar['ANIO'].max()).zfill(2) + '\n' + '   TOP 10 DE CADA ANIO'
    fig = plt.figure(figsize=(19, 10))
    ax = fig.add_subplot(1, 2, 1)
    plotly_fig = go.Figure()
    
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

            CAUSA_punt = sns.scatterplot(data=df_CAUSA, x='CAUSA', y='PORCTT', ax=ax, label=total_anio)
            #GRUPEDAD_lin = sns.lineplot(data=GRUPEDAD_line_tt, x='GRUPEDAD', y='PORCTT', ax=ax, label=total_anio)
            CAUSA_punt.set(xlabel='CAUSA', ylabel='PORCENTAJE (defunciones por edad sobre total defunciones)')
            plotly_fig.add_trace(go.Scatter(x=df_CAUSA["CAUSA"], y=df_CAUSA["PORCTT"],  mode="markers", marker=dict(color=i),  name=total_anio, hovertemplate="Contestant=%s<br>Causa=%%{x}<br>Defunciones por Causa/Defunciones=%%{y}<extra></extra>"% total_anio ))
            
    
    ## inner join, se agrega descripcion (VALOR) y porcentaje total
    df_causa_descr = pd.merge(df_dic, df_causa_descr, on='CAUSA', how='inner')
    df_causa_descr = pd.merge(top_causas, df_causa_descr, on='CAUSA', how='inner')
    
    df_causa_descr = df_causa_descr.drop_duplicates(['CAUSA', 'PORCTTA', 'VALOR'])[['CAUSA', 'PORCTTA', 'VALOR']]
    df_causa_descr = df_causa_descr.sort_values(by=['PORCTTA'], ascending=False)
    
    texto = ''
    espacio = '                                                    '
    texto_html = '                                    Top Acumulado de Todos los años' + '<br>' + espacio
    for h in range(len(df_causa_descr)):
        valor = str(df_causa_descr.iloc[h]['VALOR'])
        if valor == 'nan':
            valor = 'Sin especificar**'
        
        texto =  texto + str(round(int(df_causa_descr.iloc[h]['PORCTTA']),2)) + '%* ' + str(df_causa_descr.iloc[h]['CAUSA']) + ' ' +  str(valor) + '\n'
        texto_html =  texto_html + str(round(int(df_causa_descr.iloc[h]['PORCTTA']),2)) + '%* ' + str(df_causa_descr.iloc[h]['CAUSA']) + ' ' +  str(valor) + '<br>' + espacio 
    texto = texto + '\n' +'*    Suma(CAUSAS todos los años)/suma(defunciones todos los años)'
    texto = texto + '\n' +'**   Sgún CIE, U00–U99 son Códigos para propósitos especiales,' 
    texto = texto + '\n' + 'U00–U49 Asignación provisoria de nuevas afecciones de etiología incierta'
    texto_html = texto_html + '<br>' +  '                                    ' + '*    Suma(CAUSAS todos los años)/suma(defunciones todos los años)'
    texto_html = texto_html + '<br>' +  '                                    ' + '**   Sgún CIE, U00–U99 son Códigos para propósitos especiales,' 
    texto_html = texto_html + '<br>' +  '                                    ' + 'U00–U49 Asignación provisoria de nuevas afecciones de etiología incierta'


    
    plt.title(titulo)
    plt.xlabel("CAUSA")
    plt.ylabel("PORCENTAJE (defunciones por causa sobre total defunciones)")
    plt.text(1.1, 0.005, texto, transform = ax.transAxes, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'), fontsize=11)
    ax.legend(bbox_to_anchor=(1.65, 1.05), borderaxespad=5, fancybox=True, framealpha=1, shadow=False, borderpad=1, edgecolor='black')

    CAUSA_punt.get_figure().savefig(ruta_output + 'ACUMULADO_DEFUNCIONES_CAUSAS_DEFUNCIONES_PUNT.pdf', format='pdf')

    plotly_fig.update_xaxes(title_text="CAUSA")
    plotly_fig.update_yaxes(title_text="PORCENTAJE (defunciones por causa sobre total defunciones)")
    plotly_fig.update_layout(legend_title_text = "Referencias")
    plotly_fig.update_layout(title_text='<br>' +'<br>' +'<br>' +titulo +'<br>' +'<br>' + '<br>' + '<br>' + texto_html, title_x=.15, title_xanchor='left')
    plotly_fig.write_html(ruta_output + "ACUMULADO_DEFUNCIONES_CAUSAS_DEFUNCIONES_PUNT_HTML.html")
#title = {
#         'text': "Plot Title",
#         'y':0.9, # new
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top' # new
#        }
total_pont_causa()
anulaes_lineas()
#total_lineas()
total_barra()
total_lineas_poblacion()

