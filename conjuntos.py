# Conjuntos y Parámetros Proyecto Optimización G54

from random import choice
import googlemaps
from api_key import api_key
import time
from datetime import datetime
import csv

# Requires API key
gmaps = googlemaps.Client(key=api_key)

# ---------------------------------------------------------------

# Bases Quinta Región -------------------------------------------

bases = ["Centro Regulador", "SAMU Viña del Mar", "SAMU Quintero",
         "SAMU Quillota", "SAMU La Ligua"]

# ---------------------------------------------------------------

# Ambulancias ---------------------------------------------------

ambulancias = [f"Ambulancia_{str(numero + 1)}" for numero in range(18)]

# ---------------------------------------------------------------

# Centros Medicos -----------------------------------------------

# with open("conjuntos/centros_de_salud_2.csv", "r", encoding="utf-8") as file:
# centros = [linea.split(";")[0] for linea in file if "\ufeffH" not in linea]

centros = {}
with open("conjuntos/centros_de_salud_2.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=';')
    aux = 0
    for linea in csv_reader:
        if aux == 0:
            aux = 1
        else:
            centros[linea[0]] = {"id": linea[1], "lat": linea[2],
                                 "long": linea[3]}

# print(centros)

# ---------------------------------------------------------------

# Periodos de Tiempo (un día) -----------------------------------

with open("conjuntos/periodos.csv", "r", encoding="utf-8") as file:
    periodos_ = [line.split(";")[0] for line in file if "\ufeffT" not in line]
    periodos = {}
    inicio = 0
    fin = 3600
    for period in periodos_:
        periodos[period] = (inicio, fin)
        inicio += 3600
        fin += 3600

# ---------------------------------------------------------------

# Prestaciones --------------------------------------------------
prestaciones = {}
with open("conjuntos/prestaciones_2.csv", "r", encoding="utf-8") as file:
    x = 0
    csv_reader = csv.reader(file, delimiter=';')
    for linea in csv_reader:
        if x == 0:
            x = 1
        else:
            prestaciones[linea[1]] = linea[0]

# ---------------------------------------------------------------

# Prioridades Triage | Solicita Clinica Privada -----------------

prioridades = [1, 2, 3, 4, 5]

solicita_privada = [0, 1]

# ---------------------------------------------------------------

# Parámetros cortos o constantes: -------------------------------

Nb = 12

# Fin Parámetros cortos o constantes ----------------------------

# Prestaciones por Centro Médico (parámetro i) ------------------

#


# aux_namig = [(f"par_i/{prestacion}.csv", prestacion) for
#              prestacion in prestaciones]

# for tupla in aux_namig:
#     with open(tupla[0], "r", encoding="utf-8") as file:
#         for linea in file:
#             index_centro, valor_i = linea.split(",")
#             if "h" not in linea:
#                 index_centro = int(index_centro)
#                 valor_i = int(valor_i)
#                 if centros[index_centro - 1] not in i_prestaciones.keys():
#                     i_prestaciones[centros[index_centro - 1]] = {}
#                 i_prestaciones[centros[index_centro - 1]][tupla[1]] = valor_i

i_prestaciones = {i: {} for i in range(len(centros.keys()) + 1) if i != 0}

with open("conjuntos/centro_salud_prestacion.csv", "r",
          encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=',')
    aux = 0
    for linea in csv_reader:
        if aux == 0:
            aux = 1
        else:
            aux_ = 0
            for elem in linea:
                if aux_ == 0:
                    aux_ = 1
                else:
                    i_prestaciones[int(linea[0])][aux_] = int(elem)
                    aux_ += 1


# -----------------------------------------------------------------

# Ambulancias que hay en cada Base --------------------------------

ambulancias_por_base = {base: set() for base in bases}
ambulancias_por_base["Centro Regulador"].add(ambulancias[0])
ambulancias_por_base["SAMU Viña del Mar"].add(ambulancias[1])
ambulancias_por_base["SAMU Viña del Mar"].add(ambulancias[2])
ambulancias_por_base["SAMU Viña del Mar"].add(ambulancias[3])
ambulancias_por_base["SAMU Viña del Mar"].add(ambulancias[4])
ambulancias_por_base["SAMU Viña del Mar"].add(ambulancias[5])
ambulancias_por_base["SAMU Quintero"].add(ambulancias[6])
ambulancias_por_base["SAMU Quintero"].add(ambulancias[7])
ambulancias_por_base["SAMU Quintero"].add(ambulancias[8])
ambulancias_por_base["SAMU Quintero"].add(ambulancias[9])
ambulancias_por_base["SAMU Quillota"].add(ambulancias[10])
ambulancias_por_base["SAMU Quillota"].add(ambulancias[11])
ambulancias_por_base["SAMU Quillota"].add(ambulancias[12])
ambulancias_por_base["SAMU Quillota"].add(ambulancias[13])
ambulancias_por_base["SAMU La Ligua"].add(ambulancias[14])
ambulancias_por_base["SAMU La Ligua"].add(ambulancias[15])
ambulancias_por_base["SAMU La Ligua"].add(ambulancias[16])
ambulancias_por_base["SAMU La Ligua"].add(ambulancias[17])

ambulancia_avanzada = {}
for ambulancia in ambulancias:
    if ambulancia == "Ambulancia_11":
        ambulancia_avanzada[ambulancia] = 1
    else:
        ambulancia_avanzada[ambulancia] = 0

# -----------------------------------------------------------------

# Pacientes (preliminar) ------------------------------------------

ubicacion_pacientes = {i: {} for i in range(1, 26)}

with open("conjuntos/pacientes_ubicacion.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for paciente in csv_reader:
        if aux == 0:
            aux = 1
        else:
            ubicacion_pacientes[int(paciente[0])]["lat"] = float(paciente[1])
            ubicacion_pacientes[int(paciente[0])]["long"] = float(paciente[1])


pacientes = {i: {} for i in range(1, 26)}

for i in range(200):
    prestacion_r = choice(list(prestaciones.keys()))
    centro_r = choice(centros)
    periodo_r = choice(list(periodos.keys()))
    prioridad_r = choice(prioridades)
    solicita_privada_r = choice(solicita_privada)
    pacientes.append((prestacion_r, centro_r, periodo_r, prioridad_r,
                      solicita_privada_r))


# ------------------ Tiempos de Traslado ----------------------------

dia_base = datetime(2019, 10, 13, 0, 0)  # Día en el que empezamos.
tiempo_base = int(time.mktime(dia_base.timetuple()))


def calc_departure(periodo):
    """Calcula el time_departure segun el periodo ingresado."""
    return tiempo_base + choice(range(periodos[periodo][0],
                                      periodos[periodo][1]))


def duracion(google_output):
    """Retorna tiempo en segundos del trayecto ingresado."""
    return int(google_output["duration"]["value"])

# --------------------------------------------------------------------


# origen_lat = -32.81699
# origen_lon = -71.1985
# origen = (origen_lat, origen_lon)

# destino_lat = -32.78252
# destino_lon = -71.19455
# destino = (destino_lat, destino_lon)

# origen_ = (-33.381059, -70.511721)
# destino_ = (-33.385257, -70.518966)

# my_dist = gmaps.distance_matrix(origen_, destino_)['rows'][0]['elements'][0]


# Printing the result
# print(my_dist["duration"]["value"])
# print([calc_departure(per) for per in periodos])
# print(ambulancia_avanzada)
