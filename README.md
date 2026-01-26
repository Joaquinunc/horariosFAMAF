# Proyecto: Buscador de horarios de FAMAF

Bienvenidos, en este repositorio se encuentra el proyecto que pretende mostrar los horarios de cursado de todas las carreras y años que se dictan en la Facultad de Matemática, Astronomía, Física y Computación para un ciclo lectivo determinado (actualmente se pueden consultar datos del 2025 para las carreras de grado y los redictados, y los horarios del 2026 para el Ingreso en modalidad intensiva). Todo esto a fin de facilitar al alumnado el conocimiento de adónde debe dirigirse para cursar.

**DISCLAIMER:** Si bien este  proyecto está basado en datos oficiales, su desarrollo es de caracter particular, y no esta exento a posibles fallos.

## Funcionamiento

Este proyecto fue creado con base de [Aplicación de React](https://github.com/facebook/create-react-app) para el frontend, y con [Python](https://www.python.org/) para el backend.

### Frontend

Se leen datos de un archivo en formato .json y se muestran en pantalla, primero como campos de selección, luego como respuesta a los campos seleccionados, con estilos visuales y animaciones.

#### Comandos importantes

`npm install:` Esencial, instala las dependencias necesarias para el funcionamiento local.

`npm start:` Corre la aplicación en modo desarrollador. Se puede ver abriendo el navegador y buscando [http://localhost:3000](http://localhost:3000).

Los cambios que se realizan se guardan automáticamente, y los mensajes de error son inmediatos.

`npm test`: Corre los test realizados en modo interactivo

Mas información en [correr test](https://facebook.github.io/create-react-app/docs/running-tests).

`npm run build:`
Monta la aplicacion para producción en la carpeta `build`. Empaqueta correctamente React en modo de producción y optimiza el build para mejor desempeño.

El montaje está minimizado y los nombres de los archivos incluyen los hashes. En este punto la app está lista para desplegarse.

`npm run deploy`:
Despliegue de la app para que sea visible en github pages. Conoce mas en [deployment](https://facebook.github.io/create-react-app/docs/deployment).

### Backend

La base de datos se obtuvo mediante scrapping de los calendarios que se encuentran en el sitio oficial de [Horarios de cursado](https://www.famaf.unc.edu.ar/la-facultad/institucional/secretar%C3%ADas/secretaria-academica/horarios-de-cursado/) de la Facultad de Matemática, Astronomía, Física y Computación. Para ello se recomienda tener instalado python en su ultima versión: `sudo apt install python3.`

#### Comandos importantes

`sudo apt install python3-icalendar`: Paquete para poder procesar calendarios de Google.

`python3 src/backend/main.py`: Ejecucion de scripts del backend para obtener la información, que se guardará en un archivo en formato .json.

## Mas información

Se puede obtener mas información en la [Documentación de React](https://facebook.github.io/create-react-app/docs/getting-started), y el sitio oficial de [Python](https://www.python.org/).

#### Contribuciones

Cualquier colaboración es bienvenida mediante una **pull request.**

#### Propuestas

Nuevas ideas para el proyecto son aceptadas mediante **issues.**
