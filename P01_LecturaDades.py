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

files = "Dades/IB05*.csv"

arxius = glob.glob(files)

df = pd.read_csv(arxius[0], sep=";", encoding='latin-1')