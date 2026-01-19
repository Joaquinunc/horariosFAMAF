"""
data_sorter: Esta funcion se encarga de ordenar los elementos de la base de datos
concretamente, para cada carrera, anio y cuatrimestre ordena alfabeticamente por materia.
luego numericamente por comision y finalmente por horario.
inout: base de datos en formato diccionario
"""
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
                # 2. Ordenamos las comisiones numericamente
                for nombre_m in materias_nombres_ordenados:
                    comisiones = materias_del_cuatri[nombre_m]
                    comisiones.sort(key=lambda x: (
                        int(x['Numero_c']) if x['Numero_c'].isdigit() else 99
                    ))
                    # 3. Ordenamos por horario (primero maniana luego tarde)
                    for c in comisiones:
                        c['Detalle'].sort(key=lambda d: d['Horario'])
                    sorted_data[carr][y][cuat][nombre_m] = comisiones

    return sorted_data