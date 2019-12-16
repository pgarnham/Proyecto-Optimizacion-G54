from math import ceil

# 7 Cuando un vehículo es asignado a un paciente queda ocupado por el tiempo 
# que transcurre hasta que vuelve a la base

# Ocupar la funcion techo (ceil) de math para definir t_serv_a, falta el parametro "m"
# t_serv_a = math.ceil((d_bgt + f_hgt)/3600)

# La funcion min() es para no fallar en los casos borde          
modelo.addConstrs((quicksum(s[periodo, ambulancia] for periodo in periodos[t: min(t + (ceil((f_hgt[paciente][centro] + d_bgt[paciente][base] + m_bht[centro][base])/3600)) + 1,
                                                                                    len(periodos))])
                   <= 1 - quicksum(x[periodos[t], ambulancia, paciente, centro]
                    for paciente in pacientes
                    for centro in centros for base in bases)
                   for t in range(len(periodos))
                   for ambulancia in ambulancias),
                   name="ocupar_ambulancia")



[t: min(t + (ceil((f_hgt[paciente][centro] + d_bgt[paciente][base] + m_bht[centro][base])/3600)) + 1, len(periodos))]


modelo.addConstrs((quicksum(s[periodo, ambulancia] for periodo in periodos if (periodo > t) and (periodo < min(t + (ceil((f_hgt[paciente][centro] + d_bgt[paciente][base] + m_bht[centro][base])/3600)) + 1, len(periodos)))
                   <= 1 - quicksum(x[periodos[t], ambulancia, paciente, centro]
                    for paciente in pacientes
                    for centro in centros for base in bases)
                   for t in range(len(periodos))
                   for ambulancia in ambulancias),
                   name="ocupar_ambulancia")


modelo.addConstrs((quicksum(s[periodo, ambulancia] for periodo in periodos if ((periodo[0] > t[0]) and (periodo[0] < min(t + (ceil((f_hgt[paciente][centro] + d_bgt[paciente][base] + m_bht[centro][base])/3600)) + 1, len(periodos)))))
                   <= 1 - quicksum(x[periodos[t], ambulancia, paciente, centro]
                    for paciente in pacientes
                    for centro in centros for base in bases)
                   for t in periodos.value()
                   for ambulancia in ambulancias),
                   name="ocupar_ambulancia")




modelo.addConstrs((quicksum(s[periodo, ambulancia] for base in bases for periodo, valores in periodos.items() if ((valores[0] > t[0]) and (valores[0] < min(t + (ceil((f_hgt[paciente][centro] + d_bgt[paciente][base] + m_bht[centro][base][periodo])/3600)) + 1, len(periodos)))))
                   <= 1 - quicksum(x[periodos[periodo], ambulancia, paciente, centro]
                    for paciente in pacientes
                    for centro in centros)
                   for t in periodos.values()
                   for ambulancia in ambulancias),
                   name="ocupar_ambulancia")