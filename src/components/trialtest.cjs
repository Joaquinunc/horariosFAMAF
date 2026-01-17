const trials = require('../data/comisiones.json');

carreras = Object.keys(trials)
//console.log(carreras);

carrera = carreras[0]
anios = Object.keys(trials[carrera]);
//console.log(anios);

anio = anios[0];
cuatris = Object.keys(trials[carrera][anio]);
//console.log(cuatris)

cuatri1 = cuatris[0];
materias = Object.keys(trials[carrera][anio][cuatri1])
console.log(carrera, anio, cuatri1);
materia = materias[0];
console.log(materia);
const ncom = "1";
comisiones = trials[carrera][anio][cuatri1][materia];
const comision = comisiones.find(c => c.Numero_c === ncom);
console.log("\tComisión:", comision.Numero_c);

comision.Detalle.forEach(d => {
  console.log("\t\tTipo:", d.Tipo);
  console.log("\t\t\tHorario:", d.Horario);
  console.log("\t\t\tUbicación:", d.Ubicacion.join(", "));
});
console.log("\tDías:", comision.dias);
