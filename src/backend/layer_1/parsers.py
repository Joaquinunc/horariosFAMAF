import re
from layer_0.constants import dict_url, dict_m, dict_n, dict_t, data_c
"""
parsers.py: En este modulo se encuentran todas las funciones que
obtienen y procesan la informacion para crear la base de datos de la cual 
el usuario va a hacer consultas
"""
"""
obtener_dias_semana: devuelve el dia de la semana en castellano
in: dia (ingles)
out: dia (castellano)
"""
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

"""
obtener_carrera: obtiene el nombre de la carrera y el anio de cursada 
in: url, gcalendar
out: nombre de carrera y anio de cursada
"""

def obtener_carrerayanio(enlace, gcalendar):
    # Primero revisamos si el url tiene un nombre en dict_c de constants.py
    carrera_rawr = dict_url.get(enlace)
    carrera_raw = None
    # de no tenerlo, parseamos x-wr-caldesc del calendario de google
    if carrera_rawr == None:
        carrera_raw = str(gcalendar.get('x-wr-caldesc'))
    else:
        carrera_raw = carrera_rawr
    #definimos las variables de salida
    carrera = None
    anio = ""
    
    for carr in data_c.keys():
        # Para cada carrera del diccionario principal, si su nombre esta incluido en el
        # obtenido al parsear carrera_raw, lo asignamos  como salida
        
        if carr in carrera_raw:
            carrera = carr
            # Parseamos el anio de cursada y cambiamos a orden numerico con dict_n
            carrera2 = re.search(r"(Primer|Segundo|Tercer|Cuarto|Quinto)\s+año", carrera_raw, re.IGNORECASE)
            ord_anio = carrera2.group(1)
            num_anio = dict_n.get(ord_anio, ord_anio)
            anio = f"{num_anio} año"
        #print(f"carrera: {carrera}")
    return anio, carrera

"""
normalizar_nombre: toma un texto sucio
y lo analiza en busca del nombre de la materia
in: texto con el nombre de la materia sin analizar
out: nombre de la materia identificado
"""
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

"""
obtener_typ: Analiza un texto en busca de su tipo (teorico o practico)
in: texto con el tipo de clase sin analizar
out: Tipo de clase identificado
"""
def obtener_typ(clase):
    tipo_match = re.search(r"\(([TP])\)|Te[óo]rico|Pr[áa]ctico", clase, re.IGNORECASE)
    tipo_clase = "T/P"
    if tipo_match:
        letra = (tipo_match.group(1) or tipo_match.group(0)[0]).upper()
        tipo_clase = dict_t.get(letra, tipo_clase)
    
    return tipo_clase 

"""
parser_aula:
obtiene la locacion del dictado de una materia a partir de un texto sin analizar
in: texto que incluye la locacion
out: locacion identificada
"""
def parser_aula(input_text):
    patron = r"(?:AULA|LAB|LEF|R|PAB|LABORATORIO|VIRTUAL)\b[\s.:]*[A-Z]?\s*\d*|SALA [A-Z]+|LEF\d?|LABORATORIO [A-Z]+ [A-Z]+ [A-Z]+|OAC|AULA  [A-Z]+|VAY"
    encontrados = re.findall(patron, input_text, re.IGNORECASE)
    return [res.strip().upper() for res in encontrados if res.strip()]

"""
comparser: Se encarga de hallar la/s comision/es dentro de un texto a analizar
junto con horarios, dias y texto completo, y organiza la comision junto con los demas 
parametros recibidos en forma de un array que contiene un diccionario
in: texto que incluye la/s comision/es, summary con el texto completo
inout: diccionario con numero/s de comision/es, horario, ubicaciones, y dias

"""
def comparser(inputcom, starthour, endhour, dtype, inpday, summary):
    #iniciaclizamos los datos a devolver
    datos = []
    # obtenemos las aulas con parser_aula
    aulas = parser_aula(summary)
    for c in inputcom:
        # busqueda de comisiones
        numeros_com = re.findall(r"(?:comisión|com|c\.?)[\s.\-:]*(\d+)", c, re.IGNORECASE)
        
        #print(f"numeros_com{numeros_com} aulas: {aulas}")
        # agregamos las comisiones a los datos a devolver
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

"""
 Agrega nuevas comisiones a una materia, fusionando detalles si la comisión ya existe
para el mismo día.

Args:
    dupcomms: Lista de nuevas comisiones a agregar
    nombre_materia: Nombre de la materia
    materias_agrupadas: Diccionario de materias del cuatrimestre actual
"""
def comjoiner(dupcomms: list, nombre_materia: str, materias_agrupadas: dict):
  
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
