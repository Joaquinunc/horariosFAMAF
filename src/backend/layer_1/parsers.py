import re
from layer_0.constants import dict_url, dict_m, dict_n, dict_t, data_c

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
def obtener_carrera(enlace, gcalendar):
    carrera_rawr = dict_url.get(enlace)
    carrera_raw = None
    if carrera_rawr == None:
        carrera_raw = str(gcalendar.get('x-wr-caldesc'))
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
    return anio, carrera

def normalizar_nombre(nombre_sucio):
    # Usamos \b para "Com" para que no corte en "Compiladores"
    # Agregamos \. para que detecte "Com."
    patron_split = r"\(|\bCom\b|\bCom\.|\bAula\b|:|LEF|Te[óo]rico|Pr[áa]ctico| - "
    
    # Realizamos el split
    partes = re.split(patron_split, nombre_sucio, flags=re.IGNORECASE)
    
    # Tomamos la primera parte
    nombre = partes[0].strip()
    
    # Si por alguna razón el nombre quedó vacío (por ejemplo, empezó con una keyword)
    # podrías tomar la cadena original hasta el primer paréntesis o similar
    if not nombre and len(partes) > 1:
        # Lógica de seguridad: si el split inicial falló, limpiar manualmente
        nombre = nombre_sucio.split('(')[0].strip()

    # Limpieza de guiones y espacios
    nombre = nombre.rstrip("-").strip()
    
    # Normalización con diccionario dict_m
    nombre_lower = nombre.lower()
    for clave, valor in dict_m.items():
        if clave.lower() in nombre_lower:
            # Usamos regex con word boundaries también aquí para evitar reemplazos parciales
            nombre = re.sub(rf"\b{re.escape(clave)}\b", valor, nombre, flags=re.IGNORECASE)
            
    return nombre.strip()

def obtener_typ(clase):
    tipo_match = re.search(r"\(([TP])\)|Te[óo]rico|Pr[áa]ctico", clase, re.IGNORECASE)
    tipo_clase = "T/P"
    if tipo_match:
        letra = (tipo_match.group(1) or tipo_match.group(0)[0]).upper()
        tipo_clase = dict_t.get(letra, tipo_clase)
    
    return tipo_clase 

def parser_materia(input_text):
    patron = r"(?:AULA|LAB|LEF|R|PAB|LABORATORIO|VIRTUAL)\b[\s.:]*[A-Z]?\s*\d*|SALA [A-Z]+|LEF\d?|LABORATORIO [A-Z]+ [A-Z]+ [A-Z]+|OAC|AULA  [A-Z]+|VAY"
    encontrados = re.findall(patron, input_text, re.IGNORECASE)
    #print(f"patrones encontrados: {encontrados}")
    return [res.strip().upper() for res in encontrados if res.strip()]

def comparser(inputcom, starthour, endhour, dtype, inpday, summary):
    datos = []
    aulas = parser_materia(summary)
    for c in inputcom:
        numeros_com = re.findall(r"(?:comisión|com|c\.?)[\s.\-:]*(\d+)", c, re.IGNORECASE)
        
        #print(f"numeros_com{numeros_com} aulas: {aulas}")
        if numeros_com:
            for n in numeros_com:
                datos.append({
                    "Numero_c": n,     
                    "Detalle":[{
                        "Ubicacion": aulas if aulas else ["No especificada"], 
                        "Horario": f"{starthour} - {endhour}",
                        "Tipo": dtype
                    }],                   
                    "dias":[inpday]
                })
    return datos

def comjoiner(dupcomms:dict, nombre_carrera:str, materias_agr: dict):
    for dc in dupcomms:
        # Buscamos si ya existe esta comisión para este día en esta materia
        existente = next((item for item in materias_agr[nombre_carrera] 
                                            if item["Numero_c"] == dc["Numero_c"] and item["dias"] == dc["dias"]), None)
                            
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
                    "dias": dc["dia"]
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