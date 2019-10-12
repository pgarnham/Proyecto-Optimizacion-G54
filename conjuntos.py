# Conjuntos y Parámetros Proyecto Optimización G54

# Bases Quinta Región -------------------------------------------

bases = ["Centro_Regulador", "SAMU_Viña_del_Mar", "SAMU_Quintero",
         "SAMU_Quillota", "SAMU_La_Ligua"]

# ---------------------------------------------------------------

# Ambulancias ---------------------------------------------------

ambulancias = [f"Ambulancia_{str(numero + 1)}" for numero in range(18)]

# ---------------------------------------------------------------

# Centros Medicos -----------------------------------------------

with open("centros_de_salud.csv", "r", encoding="utf-8") as file:
    centros = [linea.split(";")[0] for linea in file if "\ufeffH" not in linea]

# ---------------------------------------------------------------

# Periodos de Tiempo (un día) -----------------------------------

with open("periodos.csv", "r", encoding="utf-8") as file:
    periodos = [line.split(";")[0] for line in file if "\ufeffT" not in line]

# ---------------------------------------------------------------

# Prestaciones --------------------------------------------------

with open("prestaciones.txt", "r", encoding="utf-8") as file:
    prestaciones = [line.strip() for line in file]

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

ambulancias_por_base = {centro: set() for centro in centros}
ambulancias_por_base["Centro_Regulador"].add(ambulancias[0])
ambulancias_por_base["SAMU_Viña_del_Mar"].add(ambulancias[1])
ambulancias_por_base["SAMU_Viña_del_Mar"].add(ambulancias[2])
ambulancias_por_base["SAMU_Viña_del_Mar"].add(ambulancias[3])
ambulancias_por_base["SAMU_Viña_del_Mar"].add(ambulancias[4])
ambulancias_por_base["SAMU_Viña_del_Mar"].add(ambulancias[5])
ambulancias_por_base["SAMU_Quintero"].add(ambulancias[6])
ambulancias_por_base["SAMU_Quintero"].add(ambulancias[7])
ambulancias_por_base["SAMU_Quintero"].add(ambulancias[8])
ambulancias_por_base["SAMU_Quintero"].add(ambulancias[9])
ambulancias_por_base["SAMU_Quillota"].add(ambulancias[10])
ambulancias_por_base["SAMU_Quillota"].add(ambulancias[11])
ambulancias_por_base["SAMU_Quillota"].add(ambulancias[12])
ambulancias_por_base["SAMU_Quillota"].add(ambulancias[13])
ambulancias_por_base["SAMU_La_Ligua"].add(ambulancias[14])
ambulancias_por_base["SAMU_La_Ligua"].add(ambulancias[15])
ambulancias_por_base["SAMU_La_Ligua"].add(ambulancias[16])
ambulancias_por_base["SAMU_La_Ligua"].add(ambulancias[17])

# -----------------------------------------------------------------
