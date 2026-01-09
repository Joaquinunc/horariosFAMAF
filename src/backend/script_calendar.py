import requests
from icalendar import Calendar
import re
import json

#variable que guardara la informacion total de todas las materias y sus comisiones
final_array = {
    "info2":{}
}
# Función para traducir el día de la semana
def obtener_dia_semana(fecha_obj):
    dias = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    nombre_ingles = fecha_obj.strftime("%A")
    return dias.get(nombre_ingles, nombre_ingles)

# Nueva función para expandir "1, 2 y 3" en [1, 2, 3]
def expandir_comisiones(nombre_sucio):
    numeros = re.findall(r'\d+', nombre_sucio)
    return numeros if numeros else [nombre_sucio]

def procesar_materia_compleja(texto_sucio, hora_inicio, hora_fin, dia):
    resultados = []
    texto_limpio = texto_sucio.replace('\\,', ',').strip()
    
    # 1. Extraemos el nombre base y limpiamos tipos (Teórico/Práctico)
    nombre_base = re.split(r'[-–(]|Aula|Com', texto_limpio, flags=re.IGNORECASE)[0].strip()
    # Limpieza extra para unificar nombres
    nombre_base = re.sub(r'\s+(?:Practico|Práctico|Teórico|Teorico|P|T)$', '', nombre_base, flags=re.IGNORECASE)

    # 2. Caso detallado: 'Com 1: AULA A5- Com 2: AULA A7'
    fragmentos_detallados = re.findall(r'(?:Com|Comisión|Com\.)\s*(\d+):?\s*(?:Aula)?\s*([A-Z]\d+)', texto_limpio, re.IGNORECASE)
    
    if fragmentos_detallados:
        for num_com, aula in fragmentos_detallados:
            resultados.append({
                "materia": nombre_base,
                "comision": {
                    "nombre_c": num_com,
                    "dia": dia,
                    "horario": f"{hora_inicio} - {hora_fin}",
                    "ubicacion": aula
                }
            })
    
    # 3. Caso estándar o agrupado: 'Com 1, 2 y 3 - Aula D4'
    if not resultados:
        aulas = re.findall(r'[A-Z]\d+', texto_limpio)
        ubicacion = ", ".join(aulas) if aulas else "A confirmar"
        
        com_match = re.search(r'(?:Com|Comisión|Com\.)\s*([\d\s,y\-\&]+)', texto_limpio, re.IGNORECASE)
        texto_comisiones = com_match.group(1).strip() if com_match else "Única"
        
        # EXPANSIÓN: Aquí convertimos "1, 2 y 3" en múltiples entradas
        for n in expandir_comisiones(texto_comisiones):
            resultados.append({
                "materia": nombre_base,
                "comision": {
                    "nombre_c": n,
                    "dia": dia,
                    "horario": f"{hora_inicio} - {hora_fin}",
                    "ubicacion": ubicacion
                }
            })
        
    return resultados

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