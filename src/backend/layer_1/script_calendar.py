import requests
from icalendar import Calendar
import json
from layer_0.parser import procesar_materia_compleja, obtener_dia_semana

#variable que guardara la informacion total de todas las materias y sus comisiones
final_array = {
    "info2":{}
}

url = "https://calendar.google.com/calendar/ical/hrn217r8opp551cdb08i5mpljs@group.calendar.google.com/public/basic.ics"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    gcal = Calendar.from_ical(respuesta.content)
    materias_agrupadas = {}

    for componente in gcal.walk():
        if componente.name == "VEVENT":
            inicio_obj = componente.get('dtstart').dt
            
            # Filtramos por año 2025 y aseguramos que sea datetime (algunos eventos son solo date)
            if hasattr(inicio_obj, 'year') and inicio_obj.year == 2025 and hasattr(inicio_obj, 'hour'):
                summary = componente.get('summary').to_ical().decode('utf-8')

                p_start = inicio_obj.strftime("%H:%M")
                p_end = componente.get('dtend').dt.strftime("%H:%M")
                dia = obtener_dia_semana(inicio_obj)
                
                eventos_procesados = procesar_materia_compleja(summary, p_start, p_end, dia)
                
                for ev in eventos_procesados:
                    nom = ev["materia"]
                    if nom not in materias_agrupadas:
                        materias_agrupadas[nom] = {"nombre": nom, "comisiones": []}
                    
                    # Evitamos duplicados exactos
                    if ev["comision"] not in materias_agrupadas[nom]["comisiones"]:
                        materias_agrupadas[nom]["comisiones"].append(ev["comision"])

    # Ordenar las comisiones por número para que el JSON quede prolijo
    for m in materias_agrupadas:
        materias_agrupadas[m]["comisiones"].sort(key=lambda x: x["nombre_c"])

    final_array["info2"] = materias_agrupadas

else:
    print("No se pudo acceder al archivo.")

with open('src/data/comisiones.json', 'w', encoding='utf-8') as f:
            json.dump(final_array, f, ensure_ascii=False, indent=4)