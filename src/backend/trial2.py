from icalendar import Calendar
from layer_0.constants import urls, data_c
from layer_1.parsers import obtener_dia_semana, obtener_carrerayanio, normalizar_nombre, parser_aula, comparser, comjoiner, obtener_typ
from layer_1.sorter import data_sorter
import re
import requests
import json
# contante que utilizaremos para filtrar las actividades de un ciclo lectivo determinado
YEAR = 2025

"""
obtener_data()
Funcion principal, se encarga de obtener la informacion de los calendarios de google
analizar sus elementos, organizarlos y finalmente guardarlos en un archivo en formato .json

"""
def obtener_data():
    #abrimos los datos y lo cargamos en info
    try:
        with open("./src/backend/comisiones.json", 'r', encoding='utf-8') as f:
            info = json.load(f)
            print(f"Archivo existente cargado con {len(info)} carreras.")
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, empezamos con un diccionario nuevo
        info = {key : {} for key in data_c}
        print("No se encontró archivo previo o está vacío. Iniciando nueva base de datos.")
    
    #bucle principal, analizamos cada url calendario
    for url in urls:    
        print(f"Procesando: {url}")
        result = requests.get(url)
        # si no hubo error en su obtencion, continuamos
        if result.status_code == 200:
            # obtnemos el contenido de un calendario
            gcal = Calendar.from_ical(result.content) 
            # carrera y anio de cursada
            anio, carrera = obtener_carrerayanio(url, gcal)
            # si el anio no estaba en la carrera, se agrega con sus cuatrimestres
            if anio not in info[carrera]:
                info[carrera][anio]={"Primer Cuatrimestre":{}, "Segundo Cuatrimestre":{}}
            # analisis de cada evento en el calendario
            for component in gcal.walk():
                if component.name == "VEVENT":
                    #fecha de inicio del evento
                    dtstart = component.get('dtstart').dt
                    # filtramos por anio actual
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
                        # Dia de la semana
                        dia_raw = dtstart.strftime("%A")
                        dia = obtener_dia_semana(dia_raw)
                        #revisamos si tiene comisiones la materia, en cuyo caso las obtenemos posteriormente
                        datacomm = re.findall(r"(?:com\.?|comisión|c)\s*\d+[^/]*", summary, re.IGNORECASE)
                        
                        if datacomm:
                            print(f"datacomm: {datacomm}")
                            nuevas_comisiones = comparser(datacomm, hora_inicio, hora_fin, tipo_str, dia, summary)
                        else:
                            # si no hay comisiones, hacemos un parsing mas general
                            aulas = parser_aula(summary)
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
                        # agregamos la materia nueva si no estaba 
                        if nombre_final not in materias_agrupadas:
                            materias_agrupadas[nombre_final] = []
                        # organizamos las comisiones
                        materias_agrupadas = comjoiner(
                            nuevas_comisiones, nombre_final, materias_agrupadas)
        else:
            print(f"Error en URL {url}: {result.status_code}")
    # ordenamos por materia y por comision
    info_ordenada = data_sorter(info)
   
    # Guardar los datos obtenidos en formato json
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