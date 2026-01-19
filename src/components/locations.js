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
  //patrones contemplados
  const aulaRegex = /(AULA)\s*([A-Z])?\d+|(LAB)\s*\d+|(LEF)\s*\d*|(OAC)|(HIDRAULICA)|(VIRTUAL)/i;
  // filtrado y definicion de claves de busqueda
  const bloquesmatch = aulas.map(a => a.match(aulaRegex));
  const blkfilter = bloquesmatch.filter(Boolean);
  const blksmap = blkfilter.map(m => {
        if (m[2]) return m[2];       // AULA A, B, C, D, R...
        if (m[3]) return 'LAB';
        if (m[4]) return 'LEF';
        if (m[5]) return 'OAC';
        if (m[6]) return 'HIDR';
        if (m[7]) return "VIRT";
        return null;
    }   
  );
  //ordenamiento de claves
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

  console.log(texto);
     return (
      <>
        {mapa && 
          (<iframe src={urls[mapa]} width="580" height="450" style={{border:0, borderRadius:"5px"}} loading="lazy"></iframe>)
        }
      </>
  )
}