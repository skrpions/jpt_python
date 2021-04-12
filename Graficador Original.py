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

# Mostrar una lista de items
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
    # Metodo para recuperar todas las filas del resultado de la consulta
    registros = cursor.fetchall()
    #print(registros)
    print("\n")


    def get_registry():
        # Recupero el indice del item que sea seleccionado
        index = listbox.curselection()[0]
        # Recupero todos los datos de ese registro seleccionado
        registry = registros[index]
        #print(registry)
        # Obtengo el contenido del JSON en una variable, es decir, Esta devuelve una cadena de texto con el contenido
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

        y_pos = numpy.arange(len(name_list))

        plot.bar(y_pos, value_list, align='center', alpha=0.5)

        # Obtine el objeto axes
        ax = plot.gca()

        # eliminar los ticklabels existentes
        ax.set_xticklabels([])

        # Quita la marca adicional en la barra negativa
        ax.set_xticks([idx for (idx, x) in enumerate(value_list) if x > 0])
        ax.spines["bottom"].set_position(("data", 0))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        # Coloca cada una de las etiquetas del eje x individualmente
        label_offset = 0.5

        for mediciones, (x_position, y_position) in zip(name_list, enumerate(value_list)):
            print(name_list)
            if y_position >= 0:
                label_y = -label_offset
            else:
                label_y = y_position - label_offset
            ax.text(x_position, label_y, mediciones, ha="center", va="top")

        # Colocando la etiqueta del eje x, observe la transformación en las coordenadas de los ejes.
        # previamente coordenadas de datos para las etiquetas x
        ax.text(0.5, -0.05, "Valores", ha="center", va="top", transform=ax.transAxes)

        # Se dibuja el histograma
        plot.show()


    button = Button(root, text='  Graficar  ', command=get_registry, font=('Arial', 11, 'bold'))
    canvas.create_window(0, 15, window=button)

    # Insertar los registros en la lista
    for r in range(0, len(registros)):
        listbox.insert(r, 'modbus' + str(r))

    cursor.close()

except:
    print("\n No se pudieron leer los datos de la tabla:- ")

finally:
    if conexion:
        conexion.close()
        print("\n La conexión SQLite está cerrada")

print("Total Registros:" + str(len(registros)))

listbox.pack()

root.mainloop()
