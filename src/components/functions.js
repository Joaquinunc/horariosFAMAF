
function OptMap({items}){
  return items.map((option, index) => (
    <option key={index} value={option}>{option}</option>
  ));
}

export function FieldRet({label, atribute, setter, elems}){
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
            <th>Día</th>
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
