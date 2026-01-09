import requests
import json
from bs4 import BeautifulSoup


# enlaces de cuyo codigo fuente obtendremos la unformacion mediante scraping
urls = [
"https://www.famaf.unc.edu.ar/academica/grado/licenciatura-en-ciencias-de-la-computaci%C3%B3n/",
"https://www.famaf.unc.edu.ar/academica/grado/licenciatura-en-matem%C3%A1tica-aplicada",
"https://www.famaf.unc.edu.ar/academica/grado/licenciatura-en-matem%C3%A1tica/",
"https://www.famaf.unc.edu.ar/academica/grado/licenciatura-en-astronom%C3%ADa/",
"https://www.famaf.unc.edu.ar/academica/grado/licenciatura-en-f%C3%ADsica/",
"https://www.famaf.unc.edu.ar/academica/grado/licenciatura-en-hidrometeorolog%C3%ADa/",
"https://www.famaf.unc.edu.ar/academica/grado/profesorado-en-matem%C3%A1tica/",
"https://www.famaf.unc.edu.ar/academica/grado/profesorado-en-f%C3%ADsica/"
]

# variable que guardara la informacion total de todas las carreras, con sus anios de cursada
# sus cuatrimestres y sus materias

data_final={
         "Info":[]
    }
# iteramos entre todos los urls y vamos actualizando data_final
for url in urls:
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        carrera = soup.find('h1', class_="title").get_text(strip=True)
        anios = soup.find_all('div', class_="year")
        
        data_carrera = {
            "Nombre_carrera": carrera,
            "Plan_estudios": []
        }
        for anio in anios:
            h2 = anio.find('h2').get_text(strip=True)
            
            if "Febrero" in h2:
                continue
        
            if not h2 and  "title" in anio.find('h2').get("class",[]):
                nombre_a_mostrar = "Optativas"
            else:
                nombre_a_mostrar = h2
            data_anio = {
                "Año": nombre_a_mostrar,
                "Cuatrimestres":  []
            }

            cuatrimestres = anio.find_all('div', class_='quarter')

            for cuatri in cuatrimestres:

                clases = cuatri.get('class', [])
                nombre_cuatri = ""

                if "primer-cuatrimestre" in clases:
                    nombre_cuatri = "Primer cuatrimestre"

                elif "segundo-cuatrimestr" in clases:
                    nombre_cuatri = "Segundo cuatrimestre"

                elif "anual" in clases:
                    nombre_cuatri= "Anual"

                materias = cuatri.find_all('a', class_='load-page')

                data_cuatri = {
                    "Orden": nombre_cuatri,
                    "Materias": []
                }
                data_anio["Cuatrimestres"].append(data_cuatri)

                for materia in materias:
                    m = materia.get_text(strip=True)    
                    data_cuatri["Materias"].append(m)

            data_carrera["Plan_estudios"].append(data_anio)

    else:
        print(f'Hubo un error {respuesta.status_code}') 

    data_final['Info'].append(data_carrera)

with open('src/data/carreras.json', 'w', encoding='utf-8') as f:
            json.dump(data_final, f, ensure_ascii=False, indent=4)