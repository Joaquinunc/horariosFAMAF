import re
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
    print(f"texto limpio:{texto_limpio} vs texto sucio: {texto_sucio}")
    # Extraemos el nombre base y limpiamos tipos (Teórico/Práctico)
    nombre_base = re.split(r'[-–(]|Aula|Com', texto_limpio, flags=re.IGNORECASE)[0].strip()
    # Limpieza extra para unificar nombres
    nombre_base = re.sub(r'\s+(?:Practico|Práctico|Teórico|Teorico|P|T)$', '', nombre_base, flags=re.IGNORECASE)
    print(f"{nombre_base}")
    # Caso detallado: 'Com 1: AULA A5- Com 2: AULA A7'
    fragmentos_detallados = re.findall(r'(?:Com|Comisión|Com\.)\s*(\d+):?\s*(?:Aula)?\s*([A-Z]\d+)', texto_limpio, re.IGNORECASE)
    print(f"fragmentos: {fragmentos_detallados}")
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
    
 
    # Caso estándar o agrupado: 'Com 1, 2 y 3 - Aula D4'
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