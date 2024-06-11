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

files = "Dades/IB0*.csv"

arxius = glob.glob(files)

df_Felanitx = pd.DataFrame()
df_Albufera = pd.DataFrame()

for arxiu in arxius:
    df = pd.read_csv(arxiu, sep=";", decimal=",",
                    encoding='UTF-16 LE', index_col="Fecha")
    
    if "Felanitx" in arxiu:
        df_Felanitx = pd.concat( [df_Felanitx, df] )

    elif "Sa Pobla" in arxiu:
        df_Albufera = pd.concat( [df_Felanitx, df] )

df_Felanitx = df_Felanitx.drop_duplicates(keep="first")
df_Albufera = df_Albufera.drop_duplicates(keep="first")