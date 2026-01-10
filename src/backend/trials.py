import re
from icalendar import Calendar
from datetime import datetime

#url quinto anio Fisica
url = "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics"
reporte = []
materias_raras = [
                  "Física del Estado Sólido - AULA 16", 
                  "Física Computacional - SALA IPT y AULA 32",
                  "Procesamiento de imágenes satelitales meteorológicas con Python - AULA 14",
                  "Agujeros Negros y Singularidades - AULA 21"
                  ]

for m in materias_raras:
    nombre_m = re.split(" - ", m)[0]
    aulareal = m.upper()
    aulas = re.findall(r"AULA \d+|SALA [A-Z]+ Y AULA \d+", aulareal)   
    reporte.append({
        "nombre": nombre_m,
        "Ubicacion":aulas
    })

print(f"{reporte}")