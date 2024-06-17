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

#####################################################################
############# HUMITAT RELATIVA 
#####################################################################

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, df_Albufera["Humedad Min (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, df_Felanitx["Humedad Min (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat relativa mínima")
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
ax.set_title("Humitat relativa màxima")
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
ax.set_title("Humitat relativa Mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmean")

#####################################################################
############# HUMITAT ESPECIFICA 
#####################################################################

def f_q(T, HR, P=1013):      
    """
        Funció per a calcular la humitat especifica a partir
        de la humitat relativa.

        S'ha extret del treball anterior
    """
    alfa = 18.0153e-3 / 28.9644e-3
    e_sat = 6.112 * np.exp( 17.67 * T/(T + 243.5) )

    rsat = alfa * e_sat / (P - e_sat)

    q = 0.001 * HR / rsat

    return q

###############################################################
# Mitjana

q_Alb = f_q(df_Albufera["Temp Media (ºC)"], 
            df_Albufera["Humedad Media (%)"])
q_Fel = f_q(df_Felanitx["Temp Media (ºC)"], 
            df_Felanitx["Humedad Media (%)"])


fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, q_Alb, 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, q_Fel, 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (g/Kg)")
ax.set_title("Humitat Especifica Mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Specific_Hmean.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, q_Alb-q_Fel, color="midnightblue")
ax.plot(df_Albufera.index, [np.mean(q_Alb-q_Fel)]*len(df_Albufera),
        color="lightcyan", linestyle="--")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel(r"$\Delta$ H (g/Kg)")
ax.set_title("Diferencies d'humitat especifica mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
fig.savefig("Images/Diff_H.jpg")

###############################################################
# Mínima

q_Alb = f_q(df_Albufera["Temp Mínima (ºC)"], 
            df_Albufera["Humedad Min (%)"])
q_Fel = f_q(df_Felanitx["Temp Mínima (ºC)"], 
            df_Felanitx["Humedad Min (%)"])

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, q_Alb, 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, q_Fel, 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (g/Kg)")
ax.set_title("Humitat Especifica Mínima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Specific_Hmin.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, q_Alb-q_Fel, color="midnightblue")
ax.plot(df_Albufera.index, [np.mean(q_Alb-q_Fel)]*len(df_Albufera),
        color="lightcyan", linestyle="--")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel(r"$\Delta$ H (g/Kg)")
ax.set_title("Diferencies d'humitat especifica mínima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
fig.savefig("Images/Diff_Hmin.jpg")

###############################################################
# Máxima

q_Alb = f_q(df_Albufera["Temp Max (ºC)"], 
            df_Albufera["Humedad Max (%)"])
q_Fel = f_q(df_Felanitx["Temp Max (ºC)"], 
            df_Felanitx["Humedad Max (%)"])

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, q_Alb, 
        label="Sa Pobla", color="teal")
ax.plot(df_Felanitx.index, q_Fel, 
        label="Felanitx", color="palegreen")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel("H (g/Kg)")
ax.set_title("Humitat Especifica Màxima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Specific_Hmax.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(df_Albufera.index, q_Alb-q_Fel, color="midnightblue")
ax.plot(df_Albufera.index, [np.mean(q_Alb-q_Fel)]*len(df_Albufera),
        color="lightcyan", linestyle="--")
ax.set_xticks(df_Albufera.index[::365]) # 365
ax.set_ylabel(r"$\Delta$ H (g/Kg)")
ax.set_title("Diferencies d'humitat especifica màxima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
fig.savefig("Images/Diff_Hmax.jpg")

difHum = df_Albufera["Humedad Media (%)"]-df_Felanitx["Humedad Media (%)"]

#####################################################################
############# PRECIPITACIÓ
#####################################################################

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

#####################################################################
############# TEMPERATURES
#####################################################################


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

dfAl = df_Albufera[(df_Albufera['Año'] == 2023) & 
                     (df_Albufera['Dia'] > 61) & 
                     (df_Albufera['Dia'] < 334)]

dfFe = df_Felanitx[(df_Felanitx['Año'] == 2023) & 
                     (df_Felanitx['Dia'] > 61) & 
                     (df_Felanitx['Dia'] < 334)]

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, dfAl["Humedad Min (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(dfFe.index, dfFe["Humedad Min (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat relativa mínima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmin2")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, dfAl["Humedad Max (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(dfFe.index, dfFe["Humedad Max (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat relativa màxima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmax2")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, dfAl["Humedad Media (%)"], 
        label="Sa Pobla", color="teal")
ax.plot(dfFe.index, dfFe["Humedad Media (%)"], 
        label="Felanitx", color="palegreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("H (%)")
ax.set_title("Humitat relativa mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Hmean2")

# Grafic temperatura combinats
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl['Temp Media (ºC)'], 
        label="s'Albufera", color="gold")
ax.plot(dfFe['Temp Media (ºC)'], 
        label="Felanitx", color="darkred")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("T (ºC)")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
fig.savefig("Images/Temp12.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfFe['Temp Media (ºC)'], 
        label="Felanitx", color="darkred")
ax.plot(dfAl['Temp Media (ºC)'], 
        label="s'Albufera", color="gold")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("T (ºC)")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
fig.savefig("Images/Temp22.jpg")

# Diferencia de Temperatures
dT = dfFe['Temp Media (ºC)']-dfAl['Temp Media (ºC)']
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dT, color="midnightblue")
ax.plot([np.nanmedian(dT)]*len(dT), '--')
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel(r"$\Delta$ T (ºC)")
fig.autofmt_xdate() # Formata les dates del fons 
fig.savefig("Images/DTemp2.jpg")

# Grafic de Evotranspiració
fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfFe['EtPMon'], 
        label="Felanitx", color="navy")
ax.plot(dfAl['EtPMon'], 
        label="s'Albufera", color="darkseagreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("Eto (mm)")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
fig.savefig("Images/Eto.jpg")


q_Alb = f_q(dfAl["Temp Media (ºC)"], 
            dfAl["Humedad Media (%)"])
q_Fel = f_q(dfFe["Temp Media (ºC)"], 
            dfFe["Humedad Media (%)"])


fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, q_Alb, 
        label="Sa Pobla", color="navy")
ax.plot(dfFe.index, q_Fel, 
        label="Felanitx", color="darkseagreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("H (g/Kg)")
ax.set_title("Humitat Especifica Mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Specific_Hmean2.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, q_Alb-q_Fel, color="maroon")
ax.plot(dfAl.index, [np.mean(q_Alb-q_Fel)]*len(dfAl),
        color="darkblue", linestyle="--")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel(r"$\Delta$ H (g/Kg)")
ax.set_title("Diferencies d'humitat especifica mitjana")
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
fig.savefig("Images/Diff_H2.jpg")

###############################################################
# Mínima

q_Alb = f_q(dfAl["Temp Mínima (ºC)"], 
            dfAl["Humedad Min (%)"])
q_Fel = f_q(dfFe["Temp Mínima (ºC)"], 
            dfFe["Humedad Min (%)"])

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, q_Alb, 
        label="Sa Pobla", color="navy")
ax.plot(dfAl.index, q_Fel, 
        label="Felanitx", color="darkseagreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("H (g/Kg)")
ax.set_title("Humitat Especifica Mínima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Specific_Hmin2.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, q_Alb-q_Fel, color="maroon")
ax.plot(dfAl.index, [np.mean(q_Alb-q_Fel)]*len(dfAl),
        color="darkblue", linestyle="--")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel(r"$\Delta$ H (g/Kg)")
ax.set_title("Diferencies d'humitat especifica mínima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
fig.savefig("Images/Diff_Hmin2.jpg")

###############################################################
# Máxima

q_Alb = f_q(dfAl["Temp Max (ºC)"], 
            dfAl["Humedad Max (%)"])
q_Fel = f_q(dfFe["Temp Max (ºC)"], 
            dfFe["Humedad Max (%)"])

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, q_Alb, 
        label="Sa Pobla", color="navy")
ax.plot(dfFe.index, q_Fel, 
        label="Felanitx", color="darkseagreen")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel("H (g/Kg)")
ax.set_title("Humitat Especifica Màxima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.legend()
plt.show()
fig.savefig("Images/Specific_Hmax2.jpg")

fig, ax = plt.subplots(figsize=(15, 8), dpi=300) 
ax.plot(dfAl.index, q_Alb-q_Fel, color="maroon")
ax.plot(dfAl.index, [np.mean(q_Alb-q_Fel)]*len(dfAl),
        color="darkblue", linestyle="--")
ax.set_xticks(dfAl.index[::12]) # 365
ax.set_ylabel(r"$\Delta$ H (g/Kg)")
ax.set_title("Diferencies d'humitat especifica màxima")
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
fig.savefig("Images/Diff_Hmax2.jpg")