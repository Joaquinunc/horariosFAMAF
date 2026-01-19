/*
OptMap: funcion que se encarga de obtener las opciones disponibles de informacion
in: items (opciones)
out: opciones a elegir en formato visible
*/
function OptMap({items}){
  return items.map((option, index) => (
    <option key={index} value={option}>{option}</option>
  ));
}
/*
FieldRet: funcion que se encarga de devolver los campos de seleccion para que el usuario elija 
la informacion que desea averiguar
in: label (descripcion); atribute (elemento de informacion); setter (gestion de opciones) visibles;
elems (opciones disponibles para elegir)
out: Pieza de html en la que el usuario puede seleccionar entre sus opciones la que busca conocer 
*/
export function FieldRet({label, atribute, setter, elems}){
  const nodata = elems.length === 0;
  console.log(nodata);
  return( 
     <div className='campos'>
                <label className='etiqueta'>{label}</label>
                <select className='selector' value={atribute} onChange={(e) => setter(e.target.value)}>
                  <option value="" disabled hidden required></option>
                  <OptMap items={elems}/>
                </select>
      </div>
  );
}
/*
timeRet: Funcion que se encarga de devolver la informacion solicitada por el usuario, en formato de tablas
in: Objeto Comision seleccionado
out: tabla con horarios, dias y ubicacion textual en formato de tablas
*/
export function timeRet(comisionData) {
  // Si no hay datos, evitamos errores
  if (!comisionData) return <p>No hay horarios disponibles para la comisión seleccionada</p>;

  // Verificar si es formato de ingresante (tiene 'clases') o no ingresante (tiene 'Detalle' y 'dias')

    // Formato de respuesta general (comisiones.json)
    return (
     <div className="result">
      <h3>Comisión: {comisionData.Numero_c}</h3>
      
      <table className="tabla-horarios">
        <thead>
          <tr>
            <th>Días</th>
            <th>Horario</th>
            <th>Ubicación</th>
            <th>Tipo</th>
          </tr>
        </thead>
        <tbody>
          
          {comisionData.Detalle.map((detalle, indexDetalle) => 
              <tr key={{indexDetalle}}>
                <td style={{textAlign: 'center' }}>
                  {detalle.dias.join(', ')}
                </td>
                <td style={{textAlign: 'center' }}>{detalle.Horario}</td>
                <td style={{textAlign: 'center' }}>{detalle.Ubicacion.join(", ")}</td>
                <td style={{textAlign: 'center' }}>{detalle.Tipo}</td>
              </tr>
          )}
        </tbody>
      </table>
      </div> 
    );
}
