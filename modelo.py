# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
from math import ceil
# Agregué el conjunto pacientes a cojuntos
from conjuntos import (centros, periodos, prestaciones, bases,
                       ambulancias, pacientes)

# Al psi le puse una f
from conjuntos import (k_a, i_h, c_pg, u_h2, r_ab,
                        lambda_p, v_p, l_p)

from tiempo_centro_base import m_bht
from dict_d_bgt import d_bgt
from dict_f_hgt import f_hgt

modelo = Model("Sistema de Atención Médica SAMU")



# Creación de variables ----------------------------------------------

# x = {}

# for periodo in periodos:
#     for ambulancia in ambulancias:
#         for paciente in pacientes:
#             name_ = f"x_{periodo}_{ambulancia}_{paciente}"
#             x[periodo, ambulancia, paciente] = modelo.addVar(0,
#                                                              1,
#                                                              vtype=GRB.BINARY,
#                                                              name=name_)

x = {}

for periodo in periodos:
    for ambulancia in ambulancias:
        for paciente in pacientes:
            for centro in centros:
                name_ = f"x_{periodo}_{ambulancia}_{paciente}_{centro}"
                x[periodo, ambulancia,
                  paciente, centro] = modelo.addVar(0, 1, vtype=GRB.BINARY,
                                                    name=name_)

s = {}

for periodo in periodos:
    for ambulancia in ambulancias:
        name_ = f"s_{periodo}_{ambulancia}"
        s[periodo, ambulancia] = modelo.addVar(0, 1, vtype=GRB.BINARY,
                                               name=name_)

# Agregar variables ----------------------------------------------

modelo.update()

# Agregar restricciones, están en el orden del informe -------------------

# 1 Una ambulancia por emergencia

modelo.addConstrs((quicksum(x[periodo, ambulancia, paciente, centro] for ambulancia in ambulancias
                                                                    for centro in centros) <= 1
                   for paciente in pacientes
                   for periodo in list(periodos.keys())),
                   name="solo_1_ambulacia")

# 2 No pueden haber mas ambulancias disponibles que ambulancias

modelo.addConstrs((quicksum(s[periodo, ambulancia] for ambulancia in ambulancias) <= len(ambulancias) 
                   for periodo in list(periodos.keys())),
                   name="max_ambulancias_disponibles")


# 3 Atender a un paciente en clinica privada, si así lo desea...

modelo.addConstrs((l_p[paciente] <= quicksum(x[periodo, ambulancia, paciente, centro] * u_h2[centro]
                                            for ambulancia in ambulancias
                                            for centro in centros
                                            for periodo in periodos)
                  for paciente in pacientes),
                  name="clinica_privada")

# 4 Atender paciente en centro que posee la prestacion

modelo.addConstrs((lambda_p[paciente] <=  quicksum(x[periodo, ambulancia, paciente, centro] * i_h[centro]
                           for ambulancia in ambulancias
                           for periodo in periodos
                           for centro in centros)
                  for paciente in pacientes),
                  name="prestaciones")


# 5 No pueden ser asignadas mas ambulancias de las disponibles

modelo.addConstrs((quicksum(x[periodo, ambulancia, paciente, centro] for paciente in pacientes
                                                             for ambulancia in ambulancias
                                                             for centro in centros)
                  <= quicksum(s[periodo, ambulancia] for ambulancia in ambulancias)
                   for periodo in periodos),
                   name="limite_ambulancias")

#  6 Relacion de Variables
# HAY QUE ELIMINARLA

# modelo.addConstrs((x[periodo, ambulancia, paciente] == quicksum(y[periodo, ambulancia,
#                   paciente, centro] for centro in centros)
#                    for periodo in periodos
#                    for ambulancia in ambulancias
#                    for paciente in pacientes),
#                    name="relacion")


# 7 Cuando un vehículo es asignado a un paciente queda ocupado por el tiempo 
# que transcurre hasta que vuelve a la base

# modelo.addConstrs((quicksum(s[periodo, ambulancia] for periodo in periodos) 
#                    == 1 - x[periodo, ambulancia, paciente, centro]
#                    for periodo in periodos
#                    for ambulancia in ambulancias
#                    for paciente in pacientes
#                    for centro in centros),
#                   name="ocupar_ambulancia")

modelo.addConstrs((quicksum(s[periodo, ambulancia] for base in bases for period in periodos if (periodos[period][0] > periodos[periodo][0] and periodos[periodo][0] < min(periodos[periodo][0]| + int(ceil((f_hgt[paciente][centro] + d_bgt[paciente][base] + m_bht[base][centro][period])/3600)) + 1, len(periodos)))) 
                   <= 1 - quicksum(x[periodo, ambulancia, paciente, centro]
                    for paciente in pacientes
                    for centro in centros)
                   for periodo in periodos
                   for ambulancia in ambulancias),
                   name="ocupar_ambulancia")


# # 8 No atender más de una vez a un paciente

modelo.addConstrs((quicksum(x[periodo, ambulancia, paciente, centro] for periodo in periodos
                                                             for ambulancia in ambulancias
                                                             for centro in centros)
                   <= 1 
                   for paciente in pacientes),
                  name="solo_1_paciente")

# # # 9 Atender a todos los pacientes

modelo.addConstr((quicksum(x[periodo, ambulancia, paciente, centro] for periodo in periodos
                                                             for paciente in pacientes
                                                             for ambulancia in ambulancias
                                                             for centro in centros) 
                   >= len(pacientes)),
                  name="atender_todos")




# Funcion Objetivo

obj = quicksum(x[periodo, ambulancia, paciente, centro] * v_p[paciente] * r_ab[ambulancia][base] * (
                                                                        f_hgt[paciente][centro] + d_bgt[paciente][base])
               for periodo in periodos
               for ambulancia in ambulancias
               for paciente in pacientes
               for base in bases
               for centro in centros)

modelo.setObjective(obj, GRB.MINIMIZE)

modelo.optimize()

modelo.printAttr("X")

print("\n-------------\n")

# Imprime las holguras de las restricciones (0 significa que la restricción es activa.
# for constr in modelo.getConstrs():
#     print(constr, constr.getAttr("slack"))
