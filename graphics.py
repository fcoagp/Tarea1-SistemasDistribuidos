import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./tests.csv")
df = df.iloc[:100000]
#q = df['time'].quantile(0.99)
#df = df[df["time"] < q]

df_db = df[df['source']=='db']
df_redis1 = df[df['source']=='redis1']
df_redis2 = df[df['source']=='redis2']
df_redis3 = df[df['source']=='redis3']

df['time'].quantile(0.99)

#plt.figure(figsize=(150,6))
plt.bar(df_db.index, df_db['time'], label='gRpc', color='blue')
plt.bar(df_redis1.index, df_redis1['time'], label='Redis1', color='green')
plt.bar(df_redis2.index, df_redis2['time'], label='Redis2', color='red')
plt.bar(df_redis3.index, df_redis3['time'], label='Redis3', color='orange')

# Añadiendo títulos y etiquetas
plt.title('Tiempo de Respuesta por Fuente')
plt.legend()
plt.xlabel('Índice')
plt.ylabel('Tiempo')

path_to_save = "./pics/1.png"  # Cambia esta ruta por la que necesites
plt.savefig(path_to_save)

plt.show()  # Muestra el gráfico