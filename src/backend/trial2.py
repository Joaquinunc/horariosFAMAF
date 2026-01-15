from icalendar import Calendar
from datetime import datetime
from layer_0.constants import urls, dict_url, dict_m, dict_n, dict_t, data_c
import re
import requests
import json

YEAR = 2025


def obtener_dia_semana(dia_ingles):
    dias = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    return dias.get(dia_ingles, dia_ingles)

def normalizar_nombre(nombre_sucio):
    nombre = re.split(r"\(|Com|Aula|:|LEF|Te[óo]rico|Pr[áa]ctico| - ", nombre_sucio, flags=re.IGNORECASE)[0]
    print(f"nombre_sucio: {nombre_sucio}")
    #print(f"nombre1: {nombre}")
    nombre = nombre.strip().rstrip("-").strip()
    #print(f"nombre2: {nombre}")
    nombre_lower = nombre.lower()
    #print(f"nombre3: {nombre}")
    for clave, valor in dict_m.items():
        if clave.lower() in nombre_lower:
            nombre = re.sub(re.escape(clave), valor, nombre, flags=re.IGNORECASE)
            #print(f"nombre4:{nombre}")
    return nombre.strip()

def parser_materia(input_text):
    patron = r"(?:AULA|LAB|LEF|R|PAB|LABORATORIO|VIRTUAL)\b[\s.:]*[A-Z]?\s*\d*|SALA [A-Z]+|LEF\d?|LABORATORIO [A-Z]+ [A-Z]+ [A-Z]+|OAC|AULA  [A-Z]+"
    encontrados = re.findall(patron, input_text, re.IGNORECASE)
    print(f"patrones encontrados: {encontrados}")
    return [res.strip().upper() for res in encontrados if res.strip()]

def comparser(inputcom, starthour, endhour, dtype, inpday, summary):
    datos = []
    aulas = parser_materia(summary)
    for c in inputcom:
        numeros_com = re.findall(r"(?:comisión|com|c\.?)[\s.\-:]*(\d+)", c, re.IGNORECASE)
        
        print(f"numeros_com{numeros_com} aulas: {aulas}")
        if numeros_com:
            for n in numeros_com:
                datos.append({
                    "Numero_c": n,     
                    "Detalle":[{
                        "Ubicacion": aulas if aulas else ["No especificada"], 
                        "Horario": f"{starthour} - {endhour}",
                        "Tipo": dtype
                    }],                   
                    "dia":inpday
                })
    return datos

def comjoiner(dupcomms:dict, nombre_carrera:str, materias_agr: dict):
    for dc in dupcomms:
                            # Buscamos si ya existe esta comisión para este día en esta materia
                            existente = next((item for item in materias_agr[nombre_carrera] 
                                            if item["Numero_c"] == dc["Numero_c"] and item["dia"] == dc["dia"]), None)
                            
                            detalle_actual = dc.get("nuevo_detalle") or dc["Detalle"][0]

                            if existente:
                                # Si ya existe la comisión y el día, solo agregamos el detalle (si no es duplicado)
                                if detalle_actual not in existente["Detalle"]:
                                    existente["Detalle"].append(detalle_actual)
                            else:
                                # Si no existe, preparamos la estructura Detalle y la agregamos
                                if "nuevo_detalle" in dc:
                                    nueva_entrada = {
                                        "Numero_c": dc["Numero_c"],
                                        "Detalle": [dc["nuevo_detalle"]],
                                        "dia": dc["dia"]
                                    }
                                else:
                                    nueva_entrada = dc
                                materias_agr[nombre_carrera].append(nueva_entrada)
    return materias_agr

def data_sorter(data:dict):

    sorted_data = {}
    for carr in sorted(data.keys()):
        sorted_data[carr] = {}
        for y in sorted(data[carr].keys()):
            sorted_data[carr][y] = {}
            for cuat in ["Primer Cuatrimestre", "Segundo Cuatrimestre"]:
                # 1. Ordenamos las materias alfabéticamente por nombre
                materias_del_cuatri = data[carr][y][cuat]
                materias_nombres_ordenados = sorted(materias_del_cuatri.keys())
                
                sorted_data[carr][y][cuat] = {}
                
                for nombre_m in materias_nombres_ordenados:
                    comisiones = materias_del_cuatri[nombre_m]
                    comisiones.sort(key=lambda x: (
                        int(x['Numero_c']) if x['Numero_c'].isdigit() else 99
                    ))

                    for c in comisiones:
                        c['Detalle'].sort(key=lambda d: d['Horario'])
                    sorted_data[carr][y][cuat][nombre_m] = comisiones

    return sorted_data
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
            carrera_rawr = dict_url.get(url)
            carrera_raw = None
            if carrera_rawr == None:
                carrera_raw = str(gcal.get('x-wr-caldesc'))
            else:
                carrera_raw = carrera_rawr
            carrera = None
            anio = ""
            
            for carr in data_c.keys():
            
                if carr in carrera_raw:
                    carrera = carr
                    carrera2 = re.search(r"(Primer|Segundo|Tercer|Cuarto|Quinto)\s+año", carrera_raw, re.IGNORECASE)
                    ord_anio = carrera2.group(1)
                    num_anio = dict_n.get(ord_anio, ord_anio)
                    anio = f"{num_anio} año"
            print(f"carrera: {carrera}")
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
                        tipo_match = re.search(r"\(([TP])\)|Te[óo]rico|Pr[áa]ctico", summary, re.IGNORECASE)
                        tipo_str = "T/P"
                        if tipo_match:
                            letra = (tipo_match.group(1) or tipo_match.group(0)[0]).upper()
                            tipo_str = dict_t.get(letra, tipo_str)

                        # Nombre Normalizado
                        nombre_final = normalizar_nombre(summary)
                        
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
                                    "Tipo": tipo_str}],
                                "dia": dia
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