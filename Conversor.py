from tkinter.filedialog import askopenfilename
import pandas as pd
from tkinter import *
import sqlite3
import matplotlib.pyplot as plot
import openpyxl

# Restaureo los parámetros rc del estilo predeterminado interno de Matplotlib.
plot.rcdefaults()

root = Tk()
root.withdraw()


class MyFrame(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.master.title("Sqlite - Excel")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W + E + N + S)

        self.button = Button(self, text=" Seleccionar Archivo ", command=self.abrir_Archivo_Sqlite())
        self.button.grid(row=1, column=0, sticky=W)

    def abrir_Archivo_Sqlite(self):
        try:
            # Ruta donde se encuentra la Database .db
            filename = askopenfilename(initialdir="C:/Users/", filetypes=(
                ("Archivos Db", "*.db"), ("Archivos xlsx", "*.xls"), ("Todos los Archivos", "*.*")))

            # Cierro la ventana de Tkinter con root.update()
            root.update()

            # Connexion a la Database
            conexion = sqlite3.connect(filename)

            # Creamos un cursor para ejecutar acciones como consultas, inserciones, actualizaciones
            cursor = conexion.cursor()
            print("Conectado! \n")

            # Nombre de la tabla a consultar y exportar. ej: Modbus_table
            table_name = input("Nombre de la tabla:- ")

            # Nombre que se le dará al archivo cuando se exporte a excel
            excel_name = input("Nombre Archivo Excel:- ")

            # Query que selecciona todos los datos de la tabla que se haya digitado
            df = pd.read_sql_query(""" select * from {}""".format(table_name), conexion)

            # Exporto la tabla a Formato Excel
            writer = pd.ExcelWriter('{}.xlsx'.format(excel_name))
            df.to_excel(writer, index=False)
            writer.save()

            print("\n Archivo Excel Generado!")

            cursor.close()

        except:
            print("\n No se pudieron leer los datos de la tabla:- " + table_name)

        finally:
            if conexion:
                conexion.close()
                print("\n La conexión SQLite se acaba de cerrar")


# Ejecuta las funciones
if __name__ == "__main__":
    MyFrame().mainloop()
