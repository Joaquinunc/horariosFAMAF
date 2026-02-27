import qrcode
import requests
import os
"""
funcion qr_maker: Genera un codigo qr a partir de 
un texto ingresado por el usuario (website)
in: parametro ingresado por el usuario
out: codigo qr en formato .png
"""
def qr_maker(usr_input:str):
    destination_dir="../../public"
    filename="qr.png"
    pathname=os.path.join(destination_dir, filename)

    # COmprobamos la existencia del sitio web
    resp = requests.get(usr_input, timeout=5)
    # Si existe, creamos el qr, caso contrario levantamos una exception
    if resp.status_code == 200:
        qr = qrcode.make(usr_input)
        qr.save(pathname)
        print("Qr guardado con exito")
    else:
        resp.raise_for_status()
        
#solicitamos al usuario el sitio
#https://joaquinunc.github.io/horariosFAMAF/
text = input("Ingrese el sitio web: ")
try:
    # Creamos el qr del sitio web con qr_maker
    qr_maker(text)
    print(f"Codigo qr del sitio web {text} generado con exito")
except requests.exceptions.HTTPError as err1:
    print(f"Error, URL inexistente: {err1}")
except requests.exceptions.MissingSchema as err2:
    print(f"Error, protocolo HTTP/HTTPS no incluido: {err2} ")
except requests.exceptions.ConnectionError as err3:
    print(f"Ocurrio un error en la conexion: {err3}")

except Exception as e:
    print(f"Error desconocido: {e}")
