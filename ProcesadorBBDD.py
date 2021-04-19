"""
Análisis :
    Para abordar este problema asumiré que los registros de la BBDD pueden expresarse como una matríz
    fila 1 [  ----- delimitante -------- delimitante -------- delimitante ... n ]
    donde cáda fila se expresa como un registro completo
    id date ... .... .... .... .... ...
    Puedo observar que en el 3 elemento hay una estructura de diccionario dentro de una lista.
    es decir, hay una "lista de diccionarios", cada uno con una clave y valor.
    sin embargo, dichos diccionarios no siempre cumplen con una misma estructura "al menos simetrica".
        1) Los registros clave y valor son indeterminados en cantidad (una función genérica nos podría ayudar a solventar
           el recorrido de dichos elementos , teniendo en cuenta que existen exepciones que deben ser controladas)
        2) para crear las columnas es necesario conocer cuantas claves existen en los diccionarios y anexarlas
        3) recorrer nuevamente todos los elementos "buscando cada coincidencia y agregadolo a su columna"
        así:
            col1 col2 col3
        id  ...    x  ....
        .
        .
        .
        id

        recorrer cada línea y ubicar en cáda columna la coincidencia
"""


def obtener_claves(archivo_cargado):
    """
    Esta función recibe una lista que tiene por indices cada línea de la base de datos,
    su función pretende encontrar todas las claves disponibles en los diccionarios del elemento 3 por registro
    """
    all_keys = []  # crearé una lista donde almacenaré los elementos
    for lineas in archivo_cargado:
        # iteraré sobre todas las líneas y luego las separaré por el deliminate ;
        auto_linea = lineas.split(";")  # auto_linea será de tipo <list>
        try:
            # usaré manejo de excepciones porque es posible que no se pueda separar las líneas
            # que no tengan elementos , podríamos hacer tambien una comprobación verificando
            # si len(auto_linea!=0)
            # usaré manejo de string aunque es posible usar diccionarios para procesarla

            # --------- corrección de linea y eliminación de caracteres para estandarizar estructura ----------#
            linea_corta = auto_linea[
                2]  # obtenemos únicamente el elemento 3 (), es decir, el nombre de la tercera columna : data_table  . -----_>  0=id, 1=date , {2} = data_table
            # print("Linaa Corta: "+linea_corta) # data_table
            new_line = linea_corta[
                       21:]  # eliminaré el valor "[{""table_modbus"": para dejar el [], quiere decir que lo que este antes del indice 21 se eliminará
            # print("New line: "+new_line)
            new_line = new_line.replace("[", "")  # Ahora eliminaré los [ en toda la línea
            new_line.replace("]", "")  # eliminación de ]
            lista = new_line.split(
                ",")  # por último separamos por saltos de línea para obtener una lista de diccionario
            # print(lista)
            # -------- en este punto puedo elegír si continúo el procesamiento mediante diccionarios o cadenas
            # -------- con los diccionarios podría iterar una lista y luego en cada iteración , las claves que estén adentro
            # -------- optaré por el procesamiento usando texto ya que me permite poner en práctica el tratamiento de datos
            # -------- que otras funciones implementadas hacen, para tomar práctica.

            for i in lista:

                # El caso más común es que existan muchas claves que están asociadas a un registro
                # mi intención es filtrar cáda línea  para reducirla hasta obtener una tupla

                str = i.replace('"', "")
                str = str.replace('{', "")
                str = str.replace('}', "")

                # Hasta este punto se reduce a una estructura limpia de esta forma
                # [name:value,name:value,name:value]
                # entonces preguntaré si esa línea poseé claves (name)
                # print("Str final: "+str)

                if "name" in str:
                    # de ser cierto separaré por :
                    name = str.split(":")
                    # En este momento sé qué solo obtendré dos elementos de name [], un elemento es la palabra name y el otro es lo que contiene name que serian cada uno de los nombres (resistivity, capitance-4, etc)
                    tmp_key = name[1]
                    # print("tmp_key:- "+tmp_key)
                    # luego pregunto si ese elemento no existe en la lista que declaré al inicio y la agrego de ser lo contrario.
                    if tmp_key not in all_keys:
                        all_keys.append(tmp_key)  # se agrega

            # print(lista)
        except Exception as e:
            pass
    # --------- imprimo los datos para visualizar ---------#
    c = 1
    for i in all_keys:
        # este ciclo imprime todas los valores que  serán columnas en el excel - csv(sin repetirse)
        # print(c, i)
        c += 1
    return all_keys


def obtenerValue(text):
    # Voy a obtener los valors de la columna id de la bd
    text = text.replace('"', "")
    text = text.replace('{', "")
    text = text.replace('}', "")
    lista = text.split(":")
    # print("Lista: "+lista) # Aquellos id que muestran ;;;;; es porque no contienen clave:valor
    return lista[-1]


def procesar_index_3(index1, index2, index3,
                     elementos_buscados):  # index1: id's , index2:date's , index3:date_Table's, elementos_buscados: Todas las claves
    # buscado1 = "resistivity-1"
    # eliminaré elementos de la cadena
    index3 = index3.replace("[", "")
    index3 = index3.replace("]", "")
    # observo que la estructura la puedo separar por }
    list_index = index3.split("}")
    salida = index1 + ";" + index2
    # print("salida "+salida)

    print("------------- elemento {} --------------".format(index1))
    for buscado in elementos_buscados:
        # iteraremos todos los elementos_buscados, es decir, todas las claves

        for lines in list_index:
            encontrado = False
            # iteramos los elementos del index3
            if buscado in lines:
                # si encontramos el valor lo mostramos
                lines = obtenerValue(lines)
                print(index1, index2, buscado, lines, sep=" | ")
                encontrado = True
                break

            else:
                # print("pass")
                pass
        if encontrado == True:
            salida = salida + ";" + lines
        else:
            salida = salida + ";"

    print("resultado :", salida)
    return salida + "\n"


# --------------------------------- INICIO DE EJECUCIÓN -------------------------------- #

# leeré el archivo de entrada y lo separaré
archivo_cargado = open("modbus_table.csv").read().split("\n")
# crearé el archivo de salida
archivo_salida = open("process_modbus_table.csv", "w")

# cabeceras  del archivo #
salida = "id;fecha"

# obtendré todas las claves necesarias de la función
todas_claves = obtener_claves(archivo_cargado)

# concatenaré la primera línea en base a todas las claves y generaré el indice en el csv
# id    fecha    c1   c2   c3   c4   c5   c6    cn .......

for i in todas_claves:
    salida = salida + ";" + i

# escribiré dicha información
archivo_salida.write(salida)
archivo_salida.write("\n")

# ------------------------------------------------------------------------------------
# las lineas siguientes estan destinadas al procesamiento de cáda elemento
# se buscarán las coincidencias en cáda línea y se agregará a su respectiva columnas
# ------------------------------------------------------------------------------------

contador = 0

for lineas in archivo_cargado:
    # print(lineas)  # mostrar cada línea
    auto_linea = lineas.split(";")

    try:
        print(contador)
        # print("--->" ,auto_linea)
        # separaré los elementos iniciales (id y fecha)
        index_1 = auto_linea[0]
        index_2 = auto_linea[1]
        # el elemento #2 será los diccionarios
        index_3 = auto_linea[2]
        # print(index_3)
        # ---------------------------------------------------------------
        #          LLAMADO DE LA FUNCIÓN QUE PROCESARÁ LOS DATOS
        # ---------------------------------------------------------------
        if contador >= 1:
            respuesta = procesar_index_3(index_1, index_2, index_3, todas_claves)
        contador=contador+1
        # respuesta será un string con la salida en formato x;X;x;x;x;X;x;x s
        # y se realiza la escritura
        archivo_salida.write(respuesta)
    except Exception as e:
        pass

# cerramos el flujo de salida
archivo_salida.close()
print("\n EJECUCIÓN FINALIZADA EXITOSAMENTE")
