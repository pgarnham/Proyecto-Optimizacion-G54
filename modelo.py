# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
#Agregué el conjunto pacientes a cojuntos
from conjuntos import (centros, periodos, prestaciones, bases,
					   ambulancias, i_prestaciones, ambulancias_por_base, pacientes)

# Al psi le puse una f
from parametros import (k_a, i_hf, c_pg, u_h, d_bgt, f_hgt, m_bht, r_ab, lambda_pf, v_p, l_p)

modelo = Model("Sistema de Atención Médica SAMU")

# Creación de variables ----------------------------------------------

x = {}

for periodo in periodos:
	for ambulancia in ambulancias:
		for paciente in pacientes:
			x[periodo, ambulancia, paciente] = model.addVar(0,1, vtype = GRB.BINARY, name = "x_{}_{}_{}".format(periodo, ambulancia, paciente))

y = {}

for periodo in periodos:
	for ambulancia in ambulancias:
		for paciente in pacientes:
			for centro in centros:
				y[periodo, ambulancia, paciente, centro] = model.addVar(0,1, vtype = GRB.BINARY, name = "y_{}_{}_{}_{}".format(periodo, ambulancia, paciente, centro))

s = {}

for periodo in periodos:
	for ambulancia in ambulancias:
		s[periodo, ambulancia] = model.addVar(0,1, vtype = GRB.BINARY, name = "s_{}_{}".format(periodo, ambulancia))

# Agregar variables ----------------------------------------------

model.update()

# Agregar restricciones, están en el orden del informe ----------------------------------------------

#1 Una ambulancia por emergencia
