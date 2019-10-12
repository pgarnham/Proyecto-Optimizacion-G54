# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
from conjuntos import (centros, periodos, prestaciones, bases,
					   ambulancias, i_prestaciones, ambulancias_por_base)
