from icalendar import Calendar
from layer_0.constants import urls, data_c
from layer_1.parsers import obtener_dia_semana, obtener_carrera, normalizar_nombre, parser_materia, comparser, comjoiner, obtener_typ
from layer_1.sorter import data_sorter
import re
import requests
import json

YEAR = 2025

def obtener_data():
    # 1. MOVIDO AFUERA: Diccionario global para acumular todas las URLs

    try:
        with open("./src/backend/comisiones.json", 'r', encoding='utf-8') as f:
            info = json.load(f)
            print(f"Archivo existente cargado con {len(info)} carreras.")
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, empezamos con un diccionario nuevo
        info = {key : {} for key in data_c}
        print("No se encontró archivo previo o está vacío. Iniciando nueva base de datos.")
    for url in urls:    
        print(f"Procesando: {url}")
        result = requests.get(url)
        
        if result.status_code == 200:
            gcal = Calendar.from_ical(result.content) 
            anio, carrera = obtener_carrera(url, gcal)

            if anio not in info[carrera]:
                info[carrera][anio]={"Primer Cuatrimestre":{}, "Segundo Cuatrimestre":{}}

            for component in gcal.walk():
                if component.name == "VEVENT":
                    dtstart = component.get('dtstart').dt
                    
                    if hasattr(dtstart, 'year') and dtstart.year == YEAR:
                        summary = component.get('summary').to_ical().decode('utf-8')
                        # Cuatrimestre
                        # mes para separar en el cuatrimestre
                        nummes = dtstart.month
                        cuatri = "Primer Cuatrimestre" if nummes < 8 else "Segundo Cuatrimestre"
                        materias_agrupadas = info[carrera][anio][cuatri]

                        # Tipo
                        tipo_str = obtener_typ(summary)

                        # Nombre Normalizado
                        nombre_final = normalizar_nombre(summary)
                        print(f"nombre final:{nombre_final}")
                        # Horarios y Comisiones
                        hora_inicio = dtstart.strftime("%H:%M")
                        hora_fin = component.get('dtend').dt.strftime("%H:%M")
                        
                        dia_raw = dtstart.strftime("%A")
                        dia = obtener_dia_semana(dia_raw)
                        datacomm = re.findall(r"(?:com\.?|comisión|c)\s*\d+[^/]*", summary, re.IGNORECASE)
                        
                        if datacomm:
                            print(f"datacomm: {datacomm}")
                            nuevas_comisiones = comparser(datacomm, hora_inicio, hora_fin, tipo_str, dia, summary)
                        else:
                            aulas = parser_materia(summary)
                            for a in aulas:
                                a.upper()
                            nuevas_comisiones = [{
                                "Numero_c": "Unica",
                                "Detalle":[{
                                    "Ubicacion": aulas if aulas else ["No especificada"],
                                    "Horario": f"{hora_inicio} - {hora_fin}",
                                    "Tipo": tipo_str,
                                    "dias": [dia]
                                    }
                                ],
                                
                            }]

                        if nombre_final not in materias_agrupadas:
                            materias_agrupadas[nombre_final] = []

                        materias_agrupadas = comjoiner(
                            nuevas_comisiones, nombre_final, materias_agrupadas)
        else:
            print(f"Error en URL {url}: {result.status_code}")
    
    info_ordenada = data_sorter(info)
   
    # 2. MOVIDO AFUERA DEL BUCLE: Guardar el archivo una sola vez al final
    print("\nGuardando resultados finales...")
    try:
        with open("./src/backend/comisiones.json", 'w', encoding='utf-8') as f:
            json.dump(info_ordenada, f, ensure_ascii=False, indent=4)
            print(f"Archivo 'comisiones.json' generado con {len(info_ordenada)} carreras.")
    except FileNotFoundError:
        # Por si la carpeta no existe
        with open("comisiones.json", 'w', encoding='utf-8') as f:
            json.dump(info_ordenada, f, ensure_ascii=False, indent=4)
            print("Carpeta './src/backend/' no encontrada. Guardado en directorio actual como 'comisiones.json'.")

if __name__ == "__main__":
    obtener_data()