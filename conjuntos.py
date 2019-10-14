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

localizacion_bases = {}
with open("conjuntos/bases_localizacion.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=";")
    aux = 0
    for center in csv_reader:
        if aux == 0:
            aux = 1
            localizacion_bases["SAMU Viña del Mar"] = (float(center[1]),
                                                       float(center[2]))
        else:
            localizacion_bases[center[0]] = (float(center[1]),
                                             float(center[2]))


# ---------------------------------------------------------------

# Ambulancias ---------------------------------------------------

ambulancias = [f"ambulancia_{str(numero + 1)}" for numero in range(18)]

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
# u_h2 reemplaza a u_h, ya esta importado a modelo.py
u_h2 = {}
is_priv =[]

with open("conjuntos/privado_publico.csv", "r", encoding="utf-8") as file:
    l = file.readlines()
    for ln in l[1:]:
        a = ln.strip().split(",")[1]
        is_priv.append(a)


with open("conjuntos/centros_de_salud_2.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=';')
    aux = 0
    t = 0
    for linea in csv_reader:
        if aux == 0:
            aux = 1
        else:
            u_h2[linea[0]] = is_priv[t]
            t += 1

# ---------------------------------------------------------------

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
            prestaciones[f"prestacion_{linea[1]}"] = linea[0]

# ---------------------------------------------------------------

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

i_hf = {f"{centro}": {f"prestacion_{i}": 0 for i in range(len(prestaciones))} for centro in centros}

with open("conjuntos/centro_salud_prestacion.csv", "r",
          encoding="utf-8") as file:
    lines = file.readlines()
    inx = 1
    for centro in centros:
        bool_prestaciones = lines[inx].strip().split(",")
        for i in range(len(prestaciones)):
            i_hf[f"{centro}"][f"prestacion_{i}"] = int(bool_prestaciones[i])

print(i_hf)

# -----------------------------------------------------------------

lambda_pf = {f"paciente_{i}": {} for i in range(1, 26)}
# Después podemos hacer un set si son varias prestaciones

with open("conjuntos/paciente_prestacion_lambda.csv", "r",
          encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    for nro, linea in enumerate(csv_reader):
        if nro == 0:
            pass
        else:
            for prest, elem in enumerate(linea):
                if prest == 0:
                    pass
                else:
                    lambda_pf[f"paciente_{nro}"][f"prestacion_{prest}"] = elem


# Ambulancias que hay en cada Base --------------------------------

r_ab = {}

with open("conjuntos/ambulancia_base.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for linea in csv_reader:
        if aux == 0:
            aux = 1
        else:
            r_ab[f"ambulancia_{int(linea[0])}"] = {bases[i - 1]: linea[i]
                                                   for i in range(1, 6)}
# print(r_ab)

k_a = {}
for ambulancia in ambulancias:
    if ambulancia == "ambulancia_11":
        k_a[ambulancia] = 1
    else:
        k_a[ambulancia] = 0

# -----------------------------------------------------------------

# Pacientes (preliminar) ------------------------------------------

c_pg = {f"paciente_{i}": {} for i in range(1, 26)}

with open("conjuntos/pacientes_ubicacion.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for paciente in csv_reader:
        if aux == 0:
            aux = 1
        else:
            c_pg[f"paciente_{int(paciente[0])}"]["lat"] = float(paciente[1])
            c_pg[f"paciente_{int(paciente[0])}"]["long"] = float(paciente[2])


l_p = {f"paciente_{i}": {} for i in range(1, 26)}

with open("conjuntos/paciente_privada.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for paciente in csv_reader:
        if aux == 0:
            aux = 1
        else:
            l_p[f"paciente_{int(paciente[0])}"] = int(paciente[1])


v_p = {f"paciente_{i}": {} for i in range(1, 26)}

with open("conjuntos/prioridad_paciente.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for paciente in csv_reader:
        if aux == 0:
            aux = 1
        else:
            v_p[f"paciente_{int(paciente[0])}"] = int(paciente[1])


u_h = {f"paciente_{i}": {} for i in range(1, 28)}

with open("conjuntos/privado_publico.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for paciente in csv_reader:
        if aux == 0:
            aux = 1
        else:
            u_h[f"paciente_{int(paciente[0])}"] = int(paciente[1])


pacientes = {f"paciente_{i}": i for i in range(1, 26)}

# for i in range(200):
#     prestacion_r = choice(list(prestaciones.keys()))
#     centro_r = choice(centros)
#     periodo_r = choice(list(periodos.keys()))
#     prioridad_r = choice(prioridades)
#     solicita_privada_r = choice(solicita_privada)
#     pacientes.append((prestacion_r, centro_r, periodo_r, prioridad_r,
#                       solicita_privada_r))


# ------------------ Tiempos de Traslado ----------------------------

dia_base = datetime(2019, 11, 13, 0, 0)  # Día en el que empezamos.
tiempo_base = int(time.mktime(dia_base.timetuple()))


def calc_departure(periodo):
    """Calcula el time_departure segun el periodo ingresado."""
    return tiempo_base + choice(range(periodos[periodo][0],
                                      periodos[periodo][1]))


def duracion(origen_, destino_, tiempo):
    """Entrega el output de google."""
    g_out = gmaps.distance_matrix(origen_,
                                  destino_,
                                  departure_time=tiempo)['rows'][0]['elements'][0]
    # print(g_out)
    if g_out == {"status": "ZERO_RESULTS"}:
        return float("inf")
    else:
        return int(g_out["duration_in_traffic"]["value"])


# --------------------------------------------------------------------

periodo_accidente = {f"paciente__{i}": {} for i in range(1, 26)}
with open("conjuntos/periodo_accidente.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    for nro_paciente, periodo in csv_reader:
        periodo_accidente[f"paciente_{nro_paciente}"] = periodo


d_bgt = {f"paciente_{i}": {} for i in range(1, 26)}
f_hgt = {f"paciente_{i}": {} for i in range(1, 26)}
# m_bht = {base: {centro: {} for centro in centros} for base in bases}

for paciente, latlong in c_pg.items():
    inicio = calc_departure(periodo_accidente[paciente])
    loc_paciente = (latlong["lat"], latlong["long"])
    for base, loc_base in localizacion_bases.items():
        # d_bgt[paciente][base] = duracion(loc_base, loc_paciente, inicio)
        pass
    for centro, latlong in centros.items():
        loc_centro = (latlong["lat"], latlong["long"])
        # f_hgt[paciente][centro] = duracion(loc_paciente, loc_centro, inicio)

# for base, loc_base in localizacion_bases.items():
#     for centro, latlong in centros.items():
#         coord_centro = (latlong["lat"], latlong["long"])
#         for period in periodos:
#             inicio = calc_departure(periodo)
#             m_bht[base][centro][period] = duracion(loc_base, coord_centro,
#                                                    inicio)

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
