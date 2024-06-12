#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P01_LecturaDades.py
@Date    :   2024/06/11 00:48:50
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0
'''

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib as mp
mp.rcParams['mathtext.fontset'] = 'stix'
mp.rcParams['font.family'] = 'STIXGeneral'
mp.rcParams.update({'font.size': 20})

# Obtenim els noms de tots els arxius csv de la nostra carpeta
arxius = glob.glob("Dades/IB0*.csv")

# Cream DataFrames auxiliars per aguardar els resultats
df_Felanitx = pd.DataFrame()
df_Albufera = pd.DataFrame()

# Llegim i extreim l'arxiu al seu DataFrame corresponent
for arxiu in arxius:

    df = pd.read_csv(arxiu, sep=";", decimal=",",
                    encoding='UTF-16 LE', index_col="Fecha")
    
    if "Felanitx" in arxiu:
        df_Felanitx = pd.concat( [df_Felanitx, df] )

    elif "Sa Pobla" in arxiu:
        df_Albufera = pd.concat( [df_Albufera, df] )

# Eliminam dates duplicades
df_Felanitx = df_Felanitx.drop_duplicates(keep="first")
df_Albufera = df_Albufera.drop_duplicates(keep="first")

df_Albufera, df_Felanitx = df_Albufera.align(df_Felanitx,
                                             join='inner', 
                                             axis=0)

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, df_Albufera["Humedad Min (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, df_Felanitx["Humedad Min (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat mínima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmin")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, df_Albufera["Humedad Max (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, df_Felanitx["Humedad Max (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat màxima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmax")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, df_Albufera["Humedad Media (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, df_Felanitx["Humedad Media (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat Mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmean")

difHum = df_Albufera["Humedad Media (%)"]-df_Felanitx["Humedad Media (%)"]

# Precipitació Felanitx
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Felanitx['Precipitación (mm)'])
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("prcp (mm)")
fig.autofmt_xdate() # Formata les dates del fons 

# Precipitació s'Albufera
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera['Precipitación (mm)'])
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("prcp (mm)")
fig.autofmt_xdate() # Formata les dates del fons 

# Precipitació grafics combinats
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera['Precipitación (mm)'], 
        label="s'Albufera", color="midnightblue")
ax.plot(df_Felanitx['Precipitación (mm)'], 
        label="Felanitx", color="yellowgreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("prcp (mm)")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
fig.savefig("Images/Prec.jpg")

# Grafic temperatura combinats
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera['Temp Media (ºC)'], 
        label="s'Albufera", color="gold")
ax.plot(df_Felanitx['Temp Media (ºC)'], 
        label="Felanitx", color="darkred")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("T (ºC)")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
fig.savefig("Images/Temp.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Felanitx['Temp Media (ºC)'], 
        label="Felanitx", color="darkred")
ax.plot(df_Albufera['Temp Media (ºC)'], 
        label="s'Albufera", color="gold")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("T (ºC)")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
fig.savefig("Images/Temp2.jpg")

# Diferencia de Temperatures
dT = df_Felanitx['Temp Media (ºC)']-df_Albufera['Temp Media (ºC)']
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dT, color="midnightblue")
ax.plot([np.nanmedian(dT)]*len(dT), '--')
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel(r"$\Delta$ T (ºC)")
fig.autofmt_xdate() # Formata les dates del fons 
fig.savefig("Images/DTemp.jpg")

##################################################################333
## Sense precipitació

dfAlb2 = df_Albufera[(df_Albufera['Año'] == 2023) & 
                     (df_Albufera['Dia'] > 151) & 
                     (df_Albufera['Dia'] < 184)]