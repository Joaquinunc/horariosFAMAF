import re
from icalendar import Calendar
from datetime import datetime
import requests

#url quinto anio Fisica
#url = "https://calendar.google.com/calendar/ical/qikesifu31eutm83pj8ieg55rc@group.calendar.google.com/public/basic.ics"
# url hidro
url = "https://calendar.google.com/calendar/ical/c_e84762490ff47889ffcadee6da5159a2dbfd33be72790742e30b78e7d4e10c53%40group.calendar.google.com/public/basic.ics"

dict_url = {
    "https://calendar.google.com/calendar/ical/c_efaa9d6520092e37e395ed64ce45a8d4c8703086dcd2711d8504138451882f90%40group.calendar.google.com/public/basic.ics" : "Primer año de Licenciatura en Hidrometeorología",
    "https://calendar.google.com/calendar/ical/c_e84762490ff47889ffcadee6da5159a2dbfd33be72790742e30b78e7d4e10c53%40group.calendar.google.com/public/basic.ics" : "Segundo año Licenciatura en Hidrometeorología"
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

def asignar_cuatris(carrs: dict):
    cuatris_materias = obtener_cuatri(url)
    carrera = str(obtener_carrera(url))
    print(carrera)
    for i in carrs:
        if i in carrera:
            carrera_list =carrera.split(" ")
            anio = ' '.join(carrera_list[0:2])
            print(carrera, anio)
            
            if anio not in carrs[i]:
                carrs[i][anio] = {}
            
            carrs[i][anio].update(cuatris_materias)
            break
    print(f"cuatris separados: {carrs}")

def obtener_carrera(enlace):
    #print("ejecutando funcion...")
    result = requests.get(enlace)
    #print(f"result: {result}")
    if result.status_code == 200:
        gcal = Calendar.from_ical(result.content)
        #print(f"calendar:{gcal}")
        description = gcal.get('x-wr-caldesc')
        #print(f"description: {description}")   OK
        #description_list = description.split(" ")
        #descr_year = ' '.join(description_list[0:2])
        #print(descr_year)
        if description is not None:
            print("entrando al caso bueno")
            return description
        else:
            print("no tiene caldesc, obteniendo diccionario del url")
            descr2 = dict_url.get(enlace)
            return descr2

def obtener_cuatri(enlace):
    separador_cuatris = {"Primer cuatrimestre":[], "Segundo cuatrimestre": []}
    result = requests.get(enlace)
    if result.status_code == 200:
        gcal = Calendar.from_ical(result.content)
    
        for component in gcal.walk():
            carrera = component.get('')
            if component.name == "VEVENT":
                dtstart = component.get('dtstart').dt
                if hasattr(dtstart, 'year') and dtstart.year == 2025:
                    summary = component.get('summary').to_ical().decode('utf-8')
                    #month = dtstart.strftime("%B")
                    nummes = dtstart.month
                    #print(f"evento: {summary}, mes: ({nummes}) {month}")
                    if nummes < 8:
                        separador_cuatris["Primer cuatrimestre"].append(summary)
                    else:
                        separador_cuatris["Segundo cuatrimestre"].append(summary)
        return separador_cuatris


reporte = []
materias_raras = [
                  "Física del Estado Sólido - AULA 16", 
                  "Física Computacional - SALA IPT y AULA 32",
                  "Procesamiento de imágenes satelitales meteorológicas con Python - AULA 14",
                  "Agujeros Negros y Singularidades - AULA 21",
                  "Electromagnetismo I - AULA 31 - Práctico Aula 10 y 16",
                  "Física General IV (T) - AULA 27",
                  "Fís Gral IV (P) Com.1 Aula 27/ Com.2 Aula 20",
                  "Física Experimental IV - Comisión 1 (LEF )",
                  "Física Experimental IV - Comisión 2 (LEF )",
                  "Física Experimental IV - Comisión 3 (LEF )",
                  "Física Experimental IV - Teórico -Aula 16"
                  ]
def comparser(input):
    datos = []
    for c in input:
        nombre_c = re.search(r"(?:comisión|com\.?)\s*(\d+)", c, re.IGNORECASE)
        aula = re.findall(r"aula\s*\d+|LEF\s*\d*", c, re.IGNORECASE)
        print(f"{nombre_c};{aula}")
        if nombre_c and aula:
            datos.append({
                "comm": nombre_c.group(1),      # solo el número
                "Ubicacion": aula 
            })
    return datos

def mparser():
    for m in materias_raras:
        nombre_m = re.split(r"| - ", m)[0]
        
        # caso raro 1: Com.1 Aula x/ Com.2 Aula y
        datacomm = re.findall(r"(?:com\.?|comisión)\s*\d+[^/]*", m, re.IGNORECASE)
        print(f"{datacomm}")
        comisiones = []
        if datacomm:
            comisiones = comparser(datacomm)
        else:
            aulas = re.findall(r"aula \d+ y \d+|aula \d+|sala [A-Z]+ y aula \d+", m, re.IGNORECASE)
            comisiones = [{
                "comm":"Unica",
                "Ubicacion": aulas
            }]

        reporte.append({
            "nombre": nombre_m,
            "Comisiones":
                comisiones
        })


    for r in reporte:
            print(
                f"{r['nombre']}\n"
                f"\tComisiones:"
            )
            for c in r['Comisiones']:
                print(f"\t\tComision: {c['comm']}, Ubicacion: {c['Ubicacion']}")


if __name__ == "__main__":
    print("ejecutando programa...")
   # obtener_cuatri(url)
    asignar_cuatris(data_c)
    #obtener_carrera(url)
