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

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.scatter(df_Albufera.index, df_Albufera["Humedad Min (%)"], 
        label="Sa Pobla")

ax.scatter(df_Felanitx.index, df_Felanitx["Humedad Min (%)"], 
        label="Felanitx")
ax.set_xticks(df_Albufera.index[::365]) # 365

fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()

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

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Felanitx['Precipitación (mm)'], 
        label="Felanitx")
ax.plot(df_Albufera['Precipitación (mm)'], 
        label="s'Albufera")

ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("prcp (mm)")

fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()