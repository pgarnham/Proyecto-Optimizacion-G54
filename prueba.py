import csv

centros = {}
with open("conjuntos/centros_de_salud_2.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=';')
    aux = 0
    for linea in csv_reader:
        if aux == 0:
            aux = 1
        else:
            centros[linea[0]] = {"id": linea[1], "lat": linea[2],
                                 "long": linea[3]}


i_h = {centro: {} for centro in centros}

with open("conjuntos/centro_salud_reducido.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    aux = 0
    for centro in csv_reader:
        if aux == 0:
            aux = 1
        else:
          i_h[centro[0]] = int(centro[1])

print(i_h)