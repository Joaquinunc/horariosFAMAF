import { urls } from "./constants";

/*
en este modulo se encuentran todas las funciones que se encargan de obtener, procesar y devolver
la ubicacion en una pestania de google maps visible para el usuario
*/

/* 
location_setter: funcion que analiza las ubicaciones de una comision, buscando una coincidencia 
para proporcionar la ubicacion real.
in: Objeto comision
out: clave con ubicacion parcial
*/

function location_setter(Comm){
  if (!Comm || !Comm.Detalle) return [];
  
  const aulas = Comm.Detalle.flatMap(d => d.Ubicacion);
  console.log(aulas);
  //patrones contemplados
  const aulaRegex = 
  /(?<c1>(AULA)\s*(?<l>[A-Z])\d+)|(?<c2>AULA\s*\d+)|(?<c3>LAB)\s*\d+|(?<c4>LEF)\s*\d?|(?<c5>OAC)|(?<c6>HIDRAULICA)|(?<c7>VIRTUAL)|(?<c8>MOSCONI)|(?<c9>IPT)|(?<c10>VAY)|(?<c11>[CP]V\-?\d+)/i;
  // filtrado y definicion de claves de busqueda

  const blksmap = aulas.map(m => {
        
    const check = m.match(aulaRegex);
    const{groups} = check;
    console.log(groups);
    if (groups.c1) return groups.l.toUpperCase(); // Retorna 'A', 'B', etc.
    if (groups.c2 || groups.c11) return 'FAM';               // Retorna 'AULA' para AULA 22
    if (groups.c3) return 'LAB';
    if (groups.c4) return 'LEF';
    if (groups.c5) return 'OAC';
    if (groups.c6) return 'HIDR';
    if (groups.c7) return 'VIRT';
    if (groups.c8) return 'MOSC';
    if (groups.c9) return 'IPT';
    if (groups.c9) return 'VAY';
    
    return null;
    }   
  );
  //ordenamiento de claves
  console.log(blksmap)
  const blksortes = [...new Set(blksmap)].sort();
  return blksortes
}

/*
Locatrion finder: Funcion que se encarga de definir la clave final de las aulas de una comision
que se utilizara para luego proporcionar la ubicacion en google maps
in: Objeto comision
out: Clave de busqueda para obtener la ubicacion final
*/
function location_finder(Comm) {
  const bloques = location_setter(Comm);

  const clave = bloques.join('');

  switch (clave) {
    case 'A':
      return {
        texto: 'Tiene en aulas A',
        mapa: 'A'
      };
    case 'B':
      return {
        texto: 'Tiene en aulas B',
        mapa: 'B'
      };
    case 'C':
      return {
        texto: 'Tiene en aulas C',
        mapa: 'C'
      };  
    case 'D':
      return {
        texto: 'Tiene en aulas D',
        mapa: 'D'
      };
     case 'R':
      return {
        texto: 'Tiene en aulas R',
        mapa: 'R'
      };
    case 'AD':
      return {
        texto: 'Tiene en aulas A y D',
        mapa: 'AD'
      };

    case 'DR':
      return {
        texto: 'Tiene en aulas D y R',
        mapa: 'DR'
      };
    case 'AR':
      return {
        texto: 'Tiene en aulas A y R',
        mapa: 'AR'
      };
    case 'OAC':
      return {
            texto: 'Tiene en Observatorio astronomico de cordoba',
            mapa: 'OAC' 
        };
    case 'LABR':
      return {
        texto: 'Tiene en LABs y R',
        mapa: 'LABR'
      };
    case 'ADLAB':
      return {
        texto: 'Tiene en LABs, Aulas A y D',
        mapa: 'ADLAB'
      };
    case 'ALAB':
      return {
        texto: 'Tiene en LABs y Aulas A',
        mapa: 'ALAB'
      };
    case 'BLAB':
      return {
        texto: 'Tiene en LABs y Aulas A',
        mapa: 'BLAB'
      };
    case 'DLAB':
      return {
        texto: 'Tiene en LABs y Aulas D',
        mapa: 'DLAB'
      };
    case 'HIDR':
      return{
        texto: 'Tiene en LAB fcefyn',
        mapa: 'HIDR'
      }
    case 'ALEF':
      return {
        texto: 'Tiene en LEFs Aulas A',
        mapa: 'ALAB'
      };
    case 'VIRT':
      return {
        texto: 'Tiene Clases virtuales',
        mapa: null
      };
    case 'AFAM':
      return{
        texto: 'Tiene en Aulas A y Famaf',
        mapa: 'ALAB'
      }
    case 'DFAM':
      return{
        texto: 'Tiene en Aulas A y Famaf',
        mapa: 'DLAB'
      }
    case 'FAMR':
      return{
        texto: 'Tiene en Aulas R y Famaf',
        mapa: 'LABR'
      }
    case 'MOSC':
      return{
        texto: 'Tiene en clases en Auditorio Mirtha Mosconi - OAC',
        mapa: 'MOSC'
      }
      default:
      return {
        texto: `Tiene en aulas ${bloques.join(' - ')}`,
        mapa: 'FAMAF'
      };
  }
}

/*
location: funcion que se encarga de devolver la ubicacion en formato google maps visible 
para el usuario en el sitio web
in: Comision
out: iframe de google maps con la ubicacion
*/
export function location_mapper(Comisiones){
  if (!Comisiones) return null;
  
  //obtenemos las aulas a partir del objeto comision
  const {texto, mapa} = location_finder(Comisiones);
  if (mapa === null) return null;
  console.log(texto);
     return (
      <>
        {mapa && (
          <iframe
            src={urls[mapa]}
            title={`Mapa ${mapa}`}
            loading="lazy"
            allowFullScreen
            referrerPolicy="no-referrer-when-downgrade"
            style={{ border: 0, borderRadius: "5px", width: "100%", height: "100%" }}
          ></iframe>
        )}
      </>
  )
}