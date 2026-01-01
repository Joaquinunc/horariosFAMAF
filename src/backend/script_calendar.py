import requests
from icalendar import Calendar
import re

# funcion que nos permite sacar la informacion de comisiones y aulas dentro de un evento
def event_parser(event):
    
    aulas = re.findall(r'[A-Z]\d+', event)
    ubicacion = ", ".join(aulas) if aulas else "A confirmar"

    # 2. Extraer Comisiones (Busca "Com" seguido de números o rangos)
    com_match = re.search(r'(?:Com|Comisión|Com\.)\s*([\d\s,y\-\&]+)', event, re.IGNORECASE)
    comision_nombre = com_match.group(1).strip() if com_match else "Única"

    # 3. Limpiar Nombre de Materia
    # Cortamos en el primer guion, paréntesis o palabra "Aula"
    nombre_materia = re.split(r'[-–(]|Aula', event, flags=re.IGNORECASE)[0].strip()
    
    return nombre_materia, comision_nombre, ubicacion

url = "https://calendar.google.com/calendar/ical/hrn217r8opp551cdb08i5mpljs@group.calendar.google.com/public/basic.ics"



respuesta = requests.get(url)

if respuesta.status_code == 200:
    gcal = Calendar.from_ical(respuesta.content)
    events = []

    for componente in gcal.walk():
        if componente.name == "VEVENT":
            inicio_obj = componente.get('dtstart').dt

            
            # Filtramos por año 2025
            if hasattr(inicio_obj, 'year') and inicio_obj.year == 2025:
                summary = componente.get('summary').to_ical().decode('utf-8')
                
                nombre, com, aula = event_parser(summary)

                fin_obj = componente.get('dtend').dt
                
                parsed_start = inicio_obj.strftime("%H:%M")
                parsed_end = fin_obj.strftime("%H:%M")
                # Guardamos el OBJETO de fecha para poder ordenar después
                events.append({
                    "materia": nombre,
                    "comision":{
                        "nombre_c":com,
                        "horario": f"{parsed_start} - {parsed_end}",
                        "ubicacion": aula
                    }
                })

    # IMPRIMIR: Formateamos al final
    for e in events:
       print(e)

else:
    print("No se pudo acceder al archivo.")