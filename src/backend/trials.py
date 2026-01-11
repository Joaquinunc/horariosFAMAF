import re
from icalendar import Calendar
from datetime import datetime

#url quinto anio Fisica
#url = "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics"
# tercero
reporte = []
materias_raras = [
                  "Física del Estado Sólido - AULA 16", 
                  "Física Computacional - SALA IPT y AULA 32",
                  "Procesamiento de imágenes satelitales meteorológicas con Python - AULA 14",
                  "Agujeros Negros y Singularidades - AULA 21",
                  "Electromagnetismo I - AULA 31 - Práctico Aula 10 y 16",
                  "Física General IV (T) - AULA 27",
                  "Fís Gral IV (P) Com.1 Aula 27/ Com.2 Aula 20"
                  ]
def comparser(input):
    datos = []
    for c in input:
        nombre_c = re.search(r"com\.(\d+)", c, re.IGNORECASE)
        aula = re.findall(r"aula \d+", c, re.IGNORECASE)
        if nombre_c and aula:
            datos.append({
                "comm": nombre_c.group(1),      # solo el número
                "Ubicacion": aula 
            })
    return datos

for m in materias_raras:
    nombre_m = re.split(" - ", m)[0]
    # caso raro 1: Com.1 Aula x/ Com.2 Aula y
    datacomm = re.findall(r"com.\d+ [A-Z]+ \d+", m, re.IGNORECASE)
    comisiones = []
    if datacomm:
        comisiones = comparser(datacomm)
    else:
        aulas = re.findall(r"aula \d+ y \d+|aula \d+|sala [A-Z]+ y aula \d+", m, re.IGNORECASE)
        comisiones = [{
             "comm":"Unica",
             "Ubicacion": aulas
        }]

    reporte.append({
        "nombre": nombre_m,
        "Comisiones":
              comisiones
    })


for r in reporte:
        print(
            f"{r['nombre']}\n"
            f"\tComisiones:"
        )
        for c in r['Comisiones']:
            print(f"\t\tComision: {c['comm']}, Ubicacion: {c['Ubicacion']}")
            