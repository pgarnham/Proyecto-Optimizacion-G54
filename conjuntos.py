# Conjuntos y Parámetros Proyecto Optimización G54

from random import choice
import googlemaps
from api_key import api_key

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

with open("conjuntos/centros_de_salud.csv", "r", encoding="utf-8") as file:
    centros = [linea.split(";")[0] for linea in file if "\ufeffH" not in linea]

# ---------------------------------------------------------------

# Periodos de Tiempo (un día) -----------------------------------

with open("conjuntos/periodos.csv", "r", encoding="utf-8") as file:
    periodos = [line.split(";")[0] for line in file if "\ufeffT" not in line]

# ---------------------------------------------------------------

# Prestaciones --------------------------------------------------

with open("conjuntos/prestaciones.txt", "r", encoding="utf-8") as file:
    prestaciones = [line.strip() for line in file]

# ---------------------------------------------------------------

# Prioridades Triage | Solicita Clinica Privada -----------------

prioridades = [1, 2, 3, 4, 5]

solicita_privada = [0, 1]

# ---------------------------------------------------------------

# Parámetros cortos o constantes: -------------------------------

Nb = 12

# Fin Parámetros cortos o constantes ----------------------------

# Prestaciones por Centro Médico (parámetro i) ------------------

i_prestaciones = {}

aux_namig = [(f"par_i/{prestacion}.csv", prestacion) for
             prestacion in prestaciones]

for tupla in aux_namig:
    with open(tupla[0], "r", encoding="utf-8") as file:
        for linea in file:
            index_centro, valor_i = linea.split(",")
            if "h" not in linea:
                index_centro = int(index_centro)
                valor_i = int(valor_i)
                if centros[index_centro - 1] not in i_prestaciones.keys():
                    i_prestaciones[centros[index_centro - 1]] = {}
                i_prestaciones[centros[index_centro - 1]][tupla[1]] = valor_i

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

# -----------------------------------------------------------------

# Pacientes (preliminar) ------------------------------------------

pacientes = []

for i in range(200):
    prestacion_r = choice(prestaciones)
    centro_r = choice(centros)
    periodo_r = choice(periodos)
    prioridad_r = choice(prioridades)
    solicita_privada_r = choice(solicita_privada)
    pacientes.append((prestacion_r, centro_r, periodo_r, prioridad_r,
                      solicita_privada_r))


origen_lat = -32.81699
origen_lon = -71.1985
origen = (origen_lat, origen_lon)

destino_lat = -32.78252
destino_lon = -71.19455
destino = (destino_lat, destino_lon)

origen_ = (-33.381059, -70.511721)
destino_ = (-33.385257, -70.518966)

my_dist = gmaps.distance_matrix(origen_, destino_)['rows'][0]['elements'][0]


def duracion(google_output):
    """Retorna tiempo en segundos del trayecto ingresado."""
    return int(google_output["duration"]["value"])


# Printing the result
print(my_dist["duration"]["value"])
