from icalendar import Calendar
from datetime import datetime
import re
import requests

YEAR = 2025
#urls de Fisica
#quinto
#url = "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics"
#cuarto
#url = "https://calendar.google.com/calendar/ical/te92ikk33p99erffndio7n05r4@group.calendar.google.com/public/basic.ics"
#tercero 
url = "https://calendar.google.com/calendar/ical/fa5rbun3hjemqcdsdc7jhk2a74@group.calendar.google.com/public/basic.ics"
reporte = []

def parser_materia(input):
    parsed_res = re.findall(r"AULA \d+|SALA [A-Z]+ Y AULA \d+|AULA: \d+|LEF\d+|LEF \d+", input)
    return parsed_res

def comparser(inputcom, starthour, endhour):
    datos = []
    print(f"input:{inputcom}")
    for c in inputcom:
        nombre_c = re.search(r"(?:comisión|com\.?)\s*(\d+)", c, re.IGNORECASE)
        print(f"{nombre_c}")
        aula = re.findall(r"aula\s*\d+|LEF\s*\d*|SALA\s*[A-Z]+", c, re.IGNORECASE)
        if nombre_c and aula:
            datos.append({
                "comm": nombre_c.group(1),      # solo el número
                "Ubicacion": aula, 
                "Horario": f"{starthour} - {endhour}"
            })
    return datos

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
                    # Obtenemos las comisiones de una materia
                    datacomm = re.findall(r"(?:com\.?|comisión)\s*\d+[^/]*", materia_lugar, re.IGNORECASE)
                    print(f"comm: {datacomm}")
                    comisiones = []
                    if datacomm:
                        print("entramos a comparser")
                        comisiones = comparser(datacomm, hora_inicio, hora_fin)
                    else:
                        # procesamos la ubicacion segun cada caso
                        aulas = parser_materia(aulareal)
                        comisiones = [{
                            "comm":"Unica",
                            "Ubicacion": aulas,
                            "Horario": f"{hora_inicio}-{hora_fin}"
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
            print(f"\t\tComision: {c['comm']}, Ubicacion: {c['Ubicacion']}, Horario: {c['Horario']}")
            


def main():
    print("Iniciando proceso de horarios...")
    datos = obtener_data()  # Llama a la función principal del script_calendar.py
    # Aquí llamas a las funciones de tus scripts
    # Ejemplo:
    # datos = procesar_materia_compleja(...)
    pass

if __name__ == "__main__":
    main()