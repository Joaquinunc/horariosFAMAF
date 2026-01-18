import json



def procesar_estructura(obj):
    if isinstance(obj, dict):
        # Si encontramos una comisión que tiene 'Detalle' y 'dias'
        if "Detalle" in obj and "dias" in obj:
            lista_dias = obj.pop("dias") # Quitamos 'dias' y lo guardamos
            for item in obj["Detalle"]:
                item["dias"] = lista_dias # Lo insertamos en cada detalle
        
        # Seguir buscando en el resto del diccionario
        for key in obj:
            procesar_estructura(obj[key])
    elif isinstance(obj, list):
        for item in obj:
            procesar_estructura(item)


def reorganizar_data():
    # Cargar el archivo
    with open('./src/backend/comisiones.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Ejecutar la transformación
    procesar_estructura(data)

    # Guardar el resultado
    with open('comisiones_actualizado.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
if __name__ == "__main__":
    reorganizar_data()