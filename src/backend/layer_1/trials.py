import re

idea ="Primer año de Licenciatura"

dict_n = {
    "Primer":"1°",
    "Segundo":"2°",
    "Tercer":"3°",
    "Cuarto": "4°",
    "Quinto":"5°"
}
idea2 =re.search(r"(Primer|Segundo|Tercer|Cuarto|Quinto)\s+año",idea, re.IGNORECASE)
ord_anio = idea2.group(1)
num_anio = dict_n.get(ord_anio, ord_anio)

ideaf = idea.replace(ord_anio, num_anio, 1)

print(f"{idea} -> {ord_anio}-> {num_anio} -> {ideaf}")


