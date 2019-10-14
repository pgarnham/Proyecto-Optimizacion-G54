# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
# Agregué el conjunto pacientes a cojuntos
from conjuntos import (centros, periodos, prestaciones, bases,
                       ambulancias, i_prestaciones,
                       ambulancias_por_base, pacientes)

# Al psi le puse una f
from conjuntos import (k_a, i_hf, c_pg, u_h, d_bgt, f_hgt, r_ab,
                        lambda_pf, v_p, l_p)

from tiempo_centro_base import m_bht

modelo = Model("Sistema de Atención Médica SAMU")

# Creación de variables ----------------------------------------------

x = {}

for periodo in periodos:
    for ambulancia in ambulancias:
        for paciente in pacientes:
            name_ = f"x_{periodo}_{ambulancia}_{paciente}"
            x[periodo, ambulancia, paciente] = modelo.addVar(0,
                                                             1,
                                                             vtype=GRB.BINARY,
                                                             name=name_)

y = {}

for periodo in periodos:
    for ambulancia in ambulancias:
        for paciente in pacientes:
            for centro in centros:
                name_ = f"y_{periodo}_{ambulancia}_{paciente}_{centro}"
                y[periodo, ambulancia,
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

modelo.addConstrs((quicksum(x[periodo, ambulancia, paciente] for ambulancia in ambulancias) <= 1
                   for paciente in pacientes
                   for periodo in periodos),
                   name="solo_1_ambulacia")

# 2 Asignar ambu avanzada

modelo.addConstrs((lambda_pf[paciente, i_prestacion] <= quicksum(k_a[ambulancia] * x[periodo, ambulancia, paciente]
                                                                 for ambulancia in ambulancias)
                   for paciente in pacientes
                   for periodo in periodos
                   for i_prestacion in i_prestaciones),
                   name="asigna_avanzada")

# 3 No pueden haber mas ambulancias disponibles que ambulancias

# OBS: parece que no hay ningun parametro para N_a, por eso use len()
# OBS_2: sobra un paratodo en la ecuacion del latex
modelo.addConstrs((quicksum(s[periodo, ambulancia] <= len(ambulancias) for ambulancia in ambulancias)
                   for periodo in periodos),
                   name="max_ambulancias_disponibles")

# 4 No asignar mas ambulancias de las que existen

modelo.addConstrs((quicksum(x[ambulancia, periodo, paciente] <= len(ambulancias)
                            for ambulancia in ambulancias
                            for paciente in pacientes)
                   for periodo in periodos),
                   name="max_ambulancias")

# 5 Atender a un paciente en clinica privada, si así lo desea...

modelo.addConstrs((l_p[paciente] <= quicksum(y[periodo, ambulancia, paciente, centro] * u_h[centro]
                                            for ambulancia in ambulancias
                                            for centro in centros)
                  for paciente in pacientes
                  for periodo in periodos),
                  name="clinica_privada")

# 6 Atender paciente en centro que posee la prestacion

modelo.addConstrs((quicksum(y[periodo, ambulancia, paciente, centro] * i_hf[centro, prestacion]
                            for ambulancia in ambulancias
                            for centro in centros) >= lambda_pf[paciente, prestacion]

                   for periodo in periodos
                   for paciente in pacientes
                   for prestacion in prestaciones),
                   name="prestaciones")

# 7 Solo se asigna un paciente por ambulancia

modelo.addConstrs((quicksum(x[periodo, ambulancia, paciente] for periodo in periodos for paciente in pacientes)
                   <= 1 for ambulancia in ambulancias),
                  name="solo_1_paciente")

# 8 No pueden ser asignadas mas ambulancias de las disponibles

modelo.addConstrs((quicksum(x[periodo, ambulancia, paciente] for paciente in pacientes for ambulancia in ambulancias)
                  <= quicksum(s[periodo, ambulancia] for ambulancia in ambulancias) for periodo in periodos),
                    name="limite_ambulancias")

# 9 Relacion de Variables

modelo.addConstrs((x[periodo, ambulancia, paciente] <= quicksum(y[periodo, ambulancia,
                  paciente, centro] for centro in centros) for periodo in periodos for ambulancia in ambulancias
                            for paciente in pacientes),
                   name="relacion")

# 10 Dejar ocupadas las ambulacias cuando son asignadas

modelo.addConstrs((quicksum(s[periodo, ambulancia])

),)
