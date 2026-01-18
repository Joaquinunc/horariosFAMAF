
const info = require('../data/comisiones.json');


const Carreras = Object.keys(info);
carr1 = Carreras[1];
console.log(carr1);
// Obtenemos la lista de anios de cursada de una carrera
// Obtenemos la lista de anios de cursada de una carrera
const Anios =  Object.keys(info[carr1]);
//console.log(Anios);
const an1 = Anios[0];
console.log("\t",an1);
const cuatris = Object.keys(info[carr1][an1]);
const cuatri = cuatris[1];
console.log(cuatri);
const materias = Object.keys(info[carr1][an1][cuatri]);
const materia = materias[0];
console.log(materia);
const comisiones = info[carr1][an1][cuatri][materia];
const comision1= comisiones[0];

console.log("\tnumcom: ", comision1.Numero_c, );
aulas = comision1.Detalle.flatMap(d => d.Ubicacion);

console.log("\t\tAulas:", aulas);


const re =/AULA A\d+|AULA B\d+|AULA C\d+|AULA D\d+|AULA R\d+|LEF|LAB|OAC/i;

aulas.forEach(s => {
  const match = s.match(re);
  console.log("Tiene clase en: ",)
});