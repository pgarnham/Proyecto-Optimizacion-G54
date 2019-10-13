from random import choice

#vCargar los lugares relevantes, donde podrian producirse accidentes
with open("lugares_accidentes.txt", "r", encoding="utf-8") as archivo:
    lugares_de_accidentes = [(linea.strip().split(",")[1], linea.strip().split(",")[2]) for linea in archivo]


# Generar muestra aleatoria de los datos cargados
print(lugares_de_accidentes)
lugares_de_accidentes2 = [choice(lugares_de_accidentes) for i in range(25)]

# Guardar en formato .csv (ID, lat, lon)
with open("exel_form.csv", "w", encoding="utf-8") as archivo:
    t = 1 # Imprime el ID
    for i in lugares_de_accidentes2:
        archivo.write(
            f"{t},{i[0]},{i[1]}\n"
        )
        t += 1