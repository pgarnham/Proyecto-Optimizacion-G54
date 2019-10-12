# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
from conjuntos import (centros, periodos, prestaciones, bases,
					   ambulancias, i_prestaciones, ambulancias_por_base)


modelo = Model("Sistema de Atención Médica SAMU")

# Variables ----------------------------------------------

for periodo in periodos:
	for ambulancia in ambulancias:
		