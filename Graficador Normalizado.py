from tkinter import *
import sqlite3
import json
from types import SimpleNamespace
import matplotlib.pyplot as plot
import numpy
from sklearn.preprocessing import MinMaxScaler

plot.rcdefaults()

root = Tk()

canvas = Canvas(root, width=30, height=30)
canvas.pack()

listbox = Listbox(root, width=100, height=20)
canvas.create_window(0, 0, window=listbox)

try:
    # Ruta donde se encuentra la Database .db
    conexion = sqlite3.connect('jptdatabase.db')
    cursor = conexion.cursor()
    print("Conectado! \n")

    # Query que selecciona todos los datos de la columna data_table
    sqlite_select_query = """SELECT data_table FROM modbus_table """
    cursor.execute(sqlite_select_query)
    registros = cursor.fetchall()
    # print(registros)
    print("\n")

    cursor.close()

except:
    print("\n No se pudieron leer los datos de la tabla:- ")

finally:
    if conexion:
        conexion.close()
        print("\n La conexión SQLite está cerrada")

print("Total Registros:" + str(len(registros)))


def get_registry():
    index = listbox.curselection()[0]
    registry = registros[index]
    registry_json = json.dumps(registry)

    # SimpleNamespace permite inicializar atributos mientras se construye el objeto también
    modbus_list = json.loads(registry_json, object_hook=lambda d: SimpleNamespace(**d))[0]
    registry_list = json.loads(modbus_list, object_hook=lambda d: SimpleNamespace(**d))[0]

    # Modbus almacena la lista de registros de cada table_modbus
    modbus = registry_list.table_modbus

    # Defino 1 Array para la lista de name del Json y otro para la lista de los values del mismo Json
    name_list = []
    value_list = []

    # Recorre la lista para separar los nombre y los valores de cada registro
    for modbus_index in range(0, len(modbus)):
        name_list.insert(modbus_index, modbus[modbus_index].name)
        value_list.insert(modbus_index, int(modbus[modbus_index].value))

    # Normalización
    sc = MinMaxScaler()

    # Convierte la lista de los valores en un numpy array
    value_list = numpy.array(value_list).reshape(len(value_list), 1)

    # Fit transform realiza la normalización de los valores
    normal_value_list = sc.fit_transform(value_list)
    final_value_list = []

    # Convertir el nummpy array en una lista normal
    for i in normal_value_list:
        final_value_list.insert(index, i[0])

    print(final_value_list)
    # Genera la grafica de barras
    fig, axs = plot.subplots()
    axs.bar(name_list, final_value_list)

    # Se dibuja el histograma
    plot.show()


button = Button(root, text='  Graficar  ', command=get_registry, font=('Arial', 11, 'bold'))
canvas.create_window(0, 15, window=button)

# Insertar los registros en la lista
for r in range(0, len(registros)):
    listbox.insert(r, 'modbus' + str(r))

listbox.pack()

root.mainloop()
