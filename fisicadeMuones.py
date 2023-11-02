import pandas as pd
import matplotlib.pyplot as plt
import math as m
from scipy.optimize import curve_fit
import numpy as np

columnas = ['Time Decay Raw', "fecha"]

df = pd.read_csv('23-10-23-11-08.data', names=columnas, delimiter=' ')
df = df.drop('fecha', axis=1)

df_filtrado = df[df['Time Decay Raw'].astype(int) < 40000].sort_values(by='Time Decay Raw')
df_filtrado.index = range(1, len(df_filtrado) + 1)

df_filtrado["limites"] = list(range(20, 20 * (len(df_filtrado['Time Decay Raw']) + 1), 20))

frecuencias = []

for i in df_filtrado['limites']:
    frecuencia = ((df_filtrado['Time Decay Raw'] >= i - 20) & (df_filtrado['Time Decay Raw'] <= i)).sum()
    frecuencias.append(frecuencia)

df_filtrado['frecuencia'] = frecuencias
df_filtrado['cumulative'] = df_filtrado['frecuencia'].cumsum()
df_filtrado['eso'] = df_filtrado['cumulative'].iloc[-1] - df_filtrado['cumulative']
print(df_filtrado)

x = np.array(df_filtrado["Time Decay Raw"])
y = np.array(df_filtrado["eso"])

def exp_func(t, A, tau):
    return A * np.exp(-t / tau)

params, covariance = curve_fit(exp_func, x, y)

A_opt, tau_opt = params

print("Parámetros óptimos:")
print(f"A = {A_opt}")
