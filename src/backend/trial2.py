from icalendar import Calendar
from datetime import datetime
import re
import requests

YEAR = 2025
#urls de Fisica
#quinto
#url = "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics"
#cuarto
url = "https://calendar.google.com/calendar/ical/te92ikk33p99erffndio7n05r4@group.calendar.google.com/public/basic.ics"
reporte = []

def parser_materia(input):
    parsed_res = re.findall(r"AULA \d+|SALA [A-Z]+ Y AULA \d+|AULA: \d+|LEF\d+|LEF \d+", input)
    return parsed_res
def obtener_data():
# obtenemos el url
    result = requests.get(url)

    # si no hubo errores, continuamos
    if result.status_code == 200:
        #obtenemos la data del calendario
        gcal = Calendar.from_ical(result.content)    
        for component in gcal.walk():
            #buscamos cada VEVENT por separado
            if component.name == "VEVENT":
                #usamos datetime para obtener la fecha y hora de inicio del evento
                index_date = component.get('dtstart').dt
                #filtramos por año 2025
                if hasattr(index_date, 'year') and index_date.year == YEAR:
                    # obtenemos materia y lugar, decodificando el campo Summary del VEVENT
                    materia_lugar = component.get('summary').to_ical().decode('utf-8')
                    # obtenemos el nombre de la materia junto con su hora de inicio/fin y su ubicacion parseada
                    nombre_m = re.split(" - ", materia_lugar)[0]
                    hora_inicio = index_date.strftime("%H:%M")
                    hora_fin = component.get('dtend').dt.strftime("%H:%M")
                    aulareal = materia_lugar.upper()
                    # procesamos la ubicacion segun cada caso
                    aulas = parser_materia(aulareal)
                    
                    reporte.append({
                        "nombre": nombre_m,
                        "Ubicacion":aulas,
                        "horario": f"{hora_inicio} - {hora_fin}"
                    })

    for r in reporte:
        print(
            f"{r['nombre']}\n"
            f"\tUbicación:\t{r['Ubicacion']}\n"
            f"\tHorario:\t{r['horario']}\n"
        )


def main():
    print("Iniciando proceso de horarios...")
    datos = obtener_data()  # Llama a la función principal del script_calendar.py
    # Aquí llamas a las funciones de tus scripts
    # Ejemplo:
    # datos = procesar_materia_compleja(...)
    pass

if __name__ == "__main__":
    main()