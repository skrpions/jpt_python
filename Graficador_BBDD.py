import seaborn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ProcesadorBBDD as procesador
import numpy as np


columnas_iniciales = ["id", "fecha"]

# Recogiendo el nombre de las columnas del ProcessadorBBDD
#-----------------------------------------
all_keys = procesador.todas_claves
print(all_keys)


header_columns = np.append(columnas_iniciales, all_keys) # Aquí estoy uniendo los dos array en uno solo, el cual tendrá todas las columnas del csv


#csv = pd.read_csv("process_modbus_table.csv", sep=';', header=0, skipinitialspace=True, usecols=header_columns) # La fila con indice 0 es la cabecera
csv = pd.read_csv("process_modbus_table.csv", sep=';', header=0, skipinitialspace=True, usecols=header_columns) # La fila con indice 0 es la cabecera


# Nombre de la tabla a consultar y exportar. ej: Modbus_table
Columna_a_graficar = input("\n Columna:- ")

# creando una serie booleana False para valores NaN
bool_temperature_1L = pd.notnull(csv[Columna_a_graficar])
#bool_laminar_1L = pd.notnull(csv["laminar_1L"])
# los campos que tengan digan false es porque tiene las celdas vacias o null

# Limpio la columna de todos campos vacios y almaceno solo las filas que no tiene NaN en la columna ingresada
temperature_1l_sin_null = (csv[bool_temperature_1L])


# csv.info()
# Gráfico en el eje  X y Y los registros que no tiene null
res = sns.lineplot(data=temperature_1l_sin_null, x="fecha", y=Columna_a_graficar, color='green', linewidth=1.5,
                   markers=True, dashes=False)
sns.set(style='dark',)
plt.show()
#res.figure.savefig("Grafica.png") Guardo una imagen de la gráfica
