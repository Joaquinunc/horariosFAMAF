import { urls } from "./constants";


function location_setter(Comm){
  if (!Comm || !Comm.Detalle) return [];
  
  const aulas = Comm.Detalle.flatMap(d => d.Ubicacion);
  console.log(aulas);
  const aulaRegex = /(AULA)\s*([A-Z])?\d+|(LAB)\s*\d+|(LEF)\s*\d*|(OAC)/i;

  const bloques = aulas
    .map(a => a.match(aulaRegex))
    .filter(Boolean)
    .map(m => m[2]);
  console.log(bloques);
  const blksortes = [...new Set(bloques)].sort();
  console.log(blksortes) 
  return blksortes
}

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
    
    default:
      return {
        texto: `Tiene en aulas ${bloques.join(' y ')}`,
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
   <iframe src={urls[mapa]} width="600" height="450" style={{border:0}} loading="lazy"></iframe>
  )
}