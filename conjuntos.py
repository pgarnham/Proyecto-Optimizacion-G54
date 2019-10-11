# Conjuntos Proyecto Optimización G54

bases = ["Centro_Regulador", "SAMU_Viña_del_Mar", "SAMU_Quintero",
         "SAMU_Quillota", "SAMU_La_Ligua"]

with open("centros_de_salud.csv", "r", encoding="utf-8") as file:
    centros = [linea.split(";")[0] for linea in file if "\ufeffH" not in linea]

with open("periodos.csv", "r", encoding="utf-8") as file:
    periodos = [line.split(";")[0] for line in file if "\ufeffT" not in line]

with open("prestaciones.txt", "r", encoding="utf-8") as file:
    prestaciones = [line.strip() for line in file]
