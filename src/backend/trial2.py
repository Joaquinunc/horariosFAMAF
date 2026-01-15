from icalendar import Calendar
from datetime import datetime
import re
import requests
import json

YEAR = 2025

urls =[
    "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics", # Fisica 
    "https://calendar.google.com/calendar/ical/te92ikk33p99erffndio7n05r4@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/fa5rbun3hjemqcdsdc7jhk2a74@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/v0vq4m435094kh02d2vd8fomj4@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/hrn217r8opp551cdb08i5mpljs@group.calendar.google.com/public/basic.ics", 
    "https://calendar.google.com/calendar/ical/c_efaa9d6520092e37e395ed64ce45a8d4c8703086dcd2711d8504138451882f90%40group.calendar.google.com/public/basic.ics", # Hidro
    "https://calendar.google.com/calendar/ical/c_e84762490ff47889ffcadee6da5159a2dbfd33be72790742e30b78e7d4e10c53%40group.calendar.google.com/public/basic.ics",
     "https://calendar.google.com/calendar/ical/04fes0r88244auclnsi7a9geag%40group.calendar.google.com/public/basic.ics", # Matematica
    "https://calendar.google.com/calendar/ical/n8dofmumb5inooc1dbhufqounk%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/fsp0843069mg9n53dm708gv3r0%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/0u5rpts4snep1jtbkpl87lq4u4%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/mvmg8n9kvv3ti381b904v5er1k%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/unc.edu.ar_3ou3i11f3src055i7t7rkktns4%40group.calendar.google.com/public/basic.ics", # Aplicada
    "https://calendar.google.com/calendar/ical/c_6a7hphesp6bt0rdj26j52f2h1s%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/c_4u4rmb9rkaifj93845b5h0b3ro%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/c_3b9fb3e4da76939f51fc890c4fe6a7e267971f5b22c8106b75c86de96a4701da%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/c_ed5fe5e1aaa4161b5d7cd455c245e43d8cc3929fd8a15d49d6771f6fe76b5c98%40group.calendar.google.com/public/basic.ics", 
    "https://calendar.google.com/calendar/ical/11orna50kpsk2t80mq1fh4lakg%40group.calendar.google.com/public/basic.ics", # Astronomia    
    "https://calendar.google.com/calendar/ical/789234e41th9vdfve6fd3qufo8%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/32rm59ugb2gpisbdfokd232i08%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/fbrtej2h3lprnn1diil0f7klk4%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/roml2gjgis99hi2sj85hkl18d8%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/pllgrunpnaf857a7eteuebgmnc%40group.calendar.google.com/public/basic.ics", # Prof. Fisica
    "https://calendar.google.com/calendar/ical/ov8u23jnph0uul7bku766n1htc%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/ghsr7vbci3rhc04q6r2sd82grc%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/9ckk1fjnijb6oh468lq648davc%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/aa6v2seo6h6joo1g296bmhk3no%40group.calendar.google.com/public/basic.ics", # Prof. Matematica
    "https://calendar.google.com/calendar/ical/4u056joebb5p07f336re5s1vug%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/o1iilesolhpljlouc4k9pmu5lg%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/7ffpuc5jo2kcdv3vab716fd2gk%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/ddlin0p5hh4qg9vokhonpahpmo%40group.calendar.google.com/public/basic.ics", # Compu
    "https://calendar.google.com/calendar/ical/mbnequ9kql1f64mm2ef20gu6lc%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/i5bmod71braqvg4t7gmo6vcpro%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/77ej01t343tkkk3m0juppb4vkc%40group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/s7usfgaqk2phi8l6rvf004fcbg%40group.calendar.google.com/public/basic.ics",
] 

dict_url = {
    "https://calendar.google.com/calendar/ical/c_efaa9d6520092e37e395ed64ce45a8d4c8703086dcd2711d8504138451882f90%40group.calendar.google.com/public/basic.ics" : "Primer año de Licenciatura en Hidrometeorología",
    "https://calendar.google.com/calendar/ical/c_e84762490ff47889ffcadee6da5159a2dbfd33be72790742e30b78e7d4e10c53%40group.calendar.google.com/public/basic.ics" : "Segundo año Licenciatura en Hidrometeorología",
    "https://calendar.google.com/calendar/ical/unc.edu.ar_3ou3i11f3src055i7t7rkktns4%40group.calendar.google.com/public/basic.ics" : "Primer año de Licenciatura en Matemática Aplicada",
    "https://calendar.google.com/calendar/ical/c_6a7hphesp6bt0rdj26j52f2h1s%40group.calendar.google.com/public/basic.ics" : "Segundo año de Licenciatura en Matemática Aplicada",
    "https://calendar.google.com/calendar/ical/c_4u4rmb9rkaifj93845b5h0b3ro%40group.calendar.google.com/public/basic.ics": "Tercer año de Licenciatura en Matemática Aplicada",
    "https://calendar.google.com/calendar/ical/c_ed5fe5e1aaa4161b5d7cd455c245e43d8cc3929fd8a15d49d6771f6fe76b5c98%40group.calendar.google.com/public/basic.ics" : "Quinto año de Licenciatura en Matemática Aplicada",
    "https://calendar.google.com/calendar/ical/11orna50kpsk2t80mq1fh4lakg%40group.calendar.google.com/public/basic.ics": "Primer año de Licenciatura en Astronomía",
    "https://calendar.google.com/calendar/ical/fbrtej2h3lprnn1diil0f7klk4%40group.calendar.google.com/public/basic.ics" : "Cuarto año de Licenciatura en Astronomía",
    "https://calendar.google.com/calendar/ical/4u056joebb5p07f336re5s1vug%40group.calendar.google.com/public/basic.ics" : "Segundo Año de Profesorado en Matemática",
    "https://calendar.google.com/calendar/ical/ghsr7vbci3rhc04q6r2sd82grc%40group.calendar.google.com/public/basic.ics" : "Tercer Año de Profesorado en Física",
    "https://calendar.google.com/calendar/ical/ddlin0p5hh4qg9vokhonpahpmo%40group.calendar.google.com/public/basic.ics" : "Primer Año de Licenciatura en Ciencias de la Computación",
    "https://calendar.google.com/calendar/ical/mbnequ9kql1f64mm2ef20gu6lc%40group.calendar.google.com/public/basic.ics" : "Segundo Año de Licenciatura en Ciencias de la Computación"
}

dict_m = {
    "fís gral": "Física General",
    "fis.gral.": "Física General",
    "física gral": "Física General",
    "an mat": "Análisis Matemático",
    "análisis matemático": "Análisis Matemático",
    "An Numér ": "Análisis Numérico ",
    "An.Numér. ": "Análisis Numérico ",
    "Mat. Disc. I":"Matemática Discreta I",
    "Mat.Discr.I":"Matemática Discreta I"

}

dict_t = {
    "T": "Teórico",
    "P": "Práctico"
}

dict_n = {
    "Primer":"1°",
    "Segundo":"2°",
    "Tercer":"3°",
    "Cuarto": "4°",
    "Quinto":"5°"
}

data_c = {"Licenciatura en Ciencias de la Computación": {}, 
          "Licenciatura en Física": {}, 
          "Licenciatura en Astronomía": {}, 
          "Licenciatura en Matemática": {}, 
          "Licenciatura en Matemática Aplicada": {}, 
          "Licenciatura en Hidrometeorología": {}, 
          "Profesorado en Matemática": {},
          "Profesorado en Física": {}
          }

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
    print(f"nombre1: {nombre}")
    nombre = nombre.strip().rstrip("-").strip()
    print(f"nombre2: {nombre}")
    nombre_lower = nombre.lower()
    print(f"nombre3: {nombre}")
    for clave, valor in dict_m.items():
        if clave.lower() in nombre_lower:
            nombre = re.sub(re.escape(clave), valor, nombre, flags=re.IGNORECASE)
            print(f"nombre4:{nombre}")
    return nombre.strip()

def parser_materia(input_text):
    patron = r"(?:AULA|LAB|LEF|R|PAB|LABORATORIO)\b[\s.:]*[A-Z]?\s*\d*|SALA [A-Z]+|LEF\d?|LABORATORIO [A-Z]+ [A-Z]+ [A-Z]+"
    encontrados = re.findall(patron, input_text, re.IGNORECASE)
    return [res.strip().upper() for res in encontrados if res.strip()]

def comparser(inputcom, starthour, endhour, dtype, inpday):
    datos = []
    for c in inputcom:
        numeros_com = re.findall(r"(?:comisión|com|c\.?)[\s.\-:]*(\d+)", c, re.IGNORECASE)
        aulas = parser_materia(c)
        print(f"numeros_com{numeros_com}")
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
                            print(datacomm)
                            nuevas_comisiones = comparser(datacomm, hora_inicio, hora_fin, tipo_str, dia)
                        else:
                            aulas = parser_materia(summary)
                            for a in aulas:
                                a.upper()
                            nuevas_comisiones = [{
                                "Numero_c": "Unica",
                                "Detalle":[{
                                    "Ubicacion": aulas if aulas else ["No especificada"],
                                    "Horario": f"{hora_inicio}-{hora_fin}",
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