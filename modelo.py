# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
#Agregué el conjunto pacientes a cojuntos
from conjuntos import (centros, periodos, prestaciones, bases,
                       ambulancias, i_prestaciones,
                       ambulancias_por_base, pacientes)

# Al psi le puse una f
from parametros import (k_a, i_hf, c_pg, u_h, d_bgt, f_hgt, m_bht, r_ab,
                        lambda_pf, v_p, l_p)

model = Model("Sistema de Atención Médica SAMU")

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

# Agregar restricciones, están en el orden del informe ----------------------------------------------

#1 Una ambulancia por emergencia
