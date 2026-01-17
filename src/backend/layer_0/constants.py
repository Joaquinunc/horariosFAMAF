"""
Capa 0: constants.py
En este archivo se encuentran la mayoria de las constantes 
utilizadas para obtener y procesar la informacion
"""
# Diccionario principal, cada fuente de info agregara su data a cada carrera en especifico
# Segun el nombre de la carrera
data_c = {
    "Licenciatura en Ciencias de la Computación": {}, 
    "Licenciatura en Física": {}, 
    "Licenciatura en Astronomía": {}, 
    "Licenciatura en Matemática": {}, 
    "Licenciatura en Matemática Aplicada": {}, 
    "Licenciatura en Hidrometeorología": {}, 
    "Profesorado en Matemática": {},
    "Profesorado en Física": {}
}

# Enlaces a calendarios de google de todas las carreras con toda la informacion
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

# EN algunos enlaces de "urls", no se encuentra el campo con el nombre de la carrera
# Tales enlaces son los que se encuentran en este diccionario que define los nombres
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

# Diccionario con nombres completos para aquellas que estan escritas diferente
dict_m = {
    "fís gral": "Física General",
    "fis.gral.": "Física General",
    "física gral": "Física General",
    "an mat": "Análisis Matemático",
    "análisis matemático": "Análisis Matemático",
    "An Numér ": "Análisis Numérico ",
    "An.Numér. ": "Análisis Numérico ",
    "Mat. Disc. I":"Matemática Discreta I",
    "Mat.Discr.I":"Matemática Discreta I",
    "Psic.del Aprend":"Psicología del Aprendizaje"

}
# Identificador de clases teoricas y practicas
dict_t = {
    "T": "Teórico",
    "P": "Práctico"
}

# Redefinicion numerica para los anios de cursada
dict_n = {
    "Primer":"1°",
    "Segundo":"2°",
    "Tercer":"3°",
    "Cuarto": "4°",
    "Quinto":"5°"
}
