# Proyecto Optimización G54

from gurobipy import Model, GRB, quicksum
from parametros import Nb
from conjuntos import centros, periodos, prestaciones, bases

ambulancias = [f"Ambulancia_{str(numero + 1)}" for numero in range(18)]

