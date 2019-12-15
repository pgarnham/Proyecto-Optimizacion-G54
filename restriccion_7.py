import math

# 7 Cuando un vehículo es asignado a un paciente queda ocupado por el tiempo 
# que transcurre hasta que vuelve a la base

# Ocupar la funcion techo (ceil) de math para definir t_serv_a, falta el parametro "m"
t_serv_a = math.ceil((d_bgt + f_hgt)/3600)

# La funcion min() es para no fallar en los casos borde          
modelo.addConstrs((quicksum(s[periodo, ambulancia] for periodo in periodos[t: min(t + t_serv_a + 1,
                                                                                    len(periodos))])
                   <= 1 - quicksum(x[periodos[t], ambulancia, paciente, centro]
                    for paciente in pacientes
                    for centro in centros)
                   for t in range(len(periodos))
                   for ambulancia in ambulancias),
                   name="ocupar_ambulancia")