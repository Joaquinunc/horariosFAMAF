from icalendar import Calendar
from datetime import datetime
import re
import requests
import json

YEAR = 2025
urls =[
    "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/te92ikk33p99erffndio7n05r4@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/fa5rbun3hjemqcdsdc7jhk2a74@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/v0vq4m435094kh02d2vd8fomj4@group.calendar.google.com/public/basic.ics",
    "https://calendar.google.com/calendar/ical/hrn217r8opp551cdb08i5mpljs@group.calendar.google.com/public/basic.ics"
]

dict_m = {
    "fís gral": "Física General",
    "fis.gral.": "Física General",
    "física gral": "Física General",
    "an mat": "Análisis Matemático",
    "análisis matemático": "Análisis Matemático"
}

dict_t = {
    "T": "Teorico",
    "P": "Practico"
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
    nombre = re.split(r"\(|Com|Aula|:", nombre_sucio, flags=re.IGNORECASE)[0]
    nombre = nombre.strip().rstrip("-").strip()
    nombre_lower = nombre.lower()
    for clave, valor in dict_m.items():
        if clave.lower() in nombre_lower:
            nombre = re.sub(re.escape(clave), valor, nombre, flags=re.IGNORECASE)
    return nombre.strip()

def parser_materia(input_text):
    patron = r"(?:AULA|LAB|LEF|R|PAB|LABORATORIO)\b[\s.:]*[A-Z]?\s*\d*|SALA [A-Z]+"
    encontrados = re.findall(patron, input_text, re.IGNORECASE)
    return [res.strip() for res in encontrados if res.strip()]

def comparser(inputcom, starthour, endhour, dtype, inpday):
    datos = []
    for c in inputcom:
        numeros_com = re.findall(r"(?:comisión|com\.?)\s*(\d+)", c, re.IGNORECASE)
        aulas = parser_materia(c)
        if numeros_com:
            for n in numeros_com:
                datos.append({
                    "comm": n,     
                    "Ubicacion": aulas if aulas else ["No especificada"], 
                    "Horario": f"{starthour} - {endhour}",
                    "Tipo": dtype,
                    "dia":inpday
                })
    return datos

def obtener_data():
    # 1. MOVIDO AFUERA: Diccionario global para acumular todas las URLs
    materias_agrupadas = {}

    for url in urls:    
        print(f"Procesando: {url}")
        result = requests.get(url)

        if result.status_code == 200:
            gcal = Calendar.from_ical(result.content)    
            for component in gcal.walk():
                if component.name == "VEVENT":
                    dtstart = component.get('dtstart').dt
                    
                    if hasattr(dtstart, 'year') and dtstart.year == YEAR:
                        summary = component.get('summary').to_ical().decode('utf-8')
                        
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
                        datacomm = re.findall(r"(?:com\.?|comisión)\s*\d+[^/]*", summary, re.IGNORECASE)
                        
                        if datacomm:
                            nuevas_comisiones = comparser(datacomm, hora_inicio, hora_fin, tipo_str, dia)
                        else:
                            aulas = parser_materia(summary)
                            nuevas_comisiones = [{
                                "comm": "Unica",
                                "Ubicacion": aulas if aulas else ["No especificada"],
                                "Horario": f"{hora_inicio}-{hora_fin}",
                                "Tipo": tipo_str,
                                "dia": dia
                            }]

                        if nombre_final not in materias_agrupadas:
                            materias_agrupadas[nombre_final] = []
                        materias_agrupadas[nombre_final].extend(nuevas_comisiones)
        else:
            print(f"Error en URL {url}: {result.status_code}")

    # 2. MOVIDO AFUERA DEL BUCLE: Guardar el archivo una sola vez al final
    print("\nGuardando resultados finales...")
    try:
        with open("./src/backend/comisiones.json", 'w', encoding='utf-8') as f:
            json.dump(materias_agrupadas, f, ensure_ascii=False, indent=4)
            print(f"Archivo 'comisiones.json' generado con {len(materias_agrupadas)} materias.")
    except FileNotFoundError:
        # Por si la carpeta no existe
        with open("comisiones.json", 'w', encoding='utf-8') as f:
            json.dump(materias_agrupadas, f, ensure_ascii=False, indent=4)
            print("Carpeta './src/backend/' no encontrada. Guardado en directorio actual como 'comisiones.json'.")

if __name__ == "__main__":
    obtener_data()