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
                        "Tipo": dtype,
                        "dias":[inpday]
                    }],                                       
                })
    return datos

def comjoiner(dupcomms: list, nombre_materia: str, materias_agrupadas: dict):
    """
    Agrega nuevas comisiones a una materia, fusionando detalles si la comisión ya existe
    para el mismo día.
    
    Args:
        dupcomms: Lista de nuevas comisiones a agregar
        nombre_materia: Nombre de la materia
        materias_agrupadas: Diccionario de materias del cuatrimestre actual
    """
    for dc in dupcomms:
        numero_comision = dc["Numero_c"]
        detalle_nuevo = dc["Detalle"][0]
        dia_nuevo = detalle_nuevo["dias"][0]
        
        # Buscamos si ya existe una comisión con este número
        comision_existente = next(
            (item for item in materias_agrupadas.get(nombre_materia, [])
             if item["Numero_c"] == numero_comision),
            None
        )
        
        if comision_existente:
            # Buscamos si ya existe un detalle para este día
            detalle_existente = next(
                (d for d in comision_existente["Detalle"]
                 if d.get("dias") == [dia_nuevo]),  # Usar .get() en lugar de acceso directo
                None
            )
            
            if detalle_existente:
                # Si el mismo horario/tipo/ubicación ya existe, no duplicar
                if detalle_nuevo not in comision_existente["Detalle"]:
                    comision_existente["Detalle"].append(detalle_nuevo)
            else:
                # Agregar nuevo detalle para este día
                comision_existente["Detalle"].append(detalle_nuevo)
        else:
            # Nueva comisión: la agregamos a la materia
            if nombre_materia not in materias_agrupadas:
                materias_agrupadas[nombre_materia] = []
            
            materias_agrupadas[nombre_materia].append(dc)
    
    return materias_agrupadas

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