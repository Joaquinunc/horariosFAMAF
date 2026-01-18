
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
      <table className="tabla-horarios">
        <thead>
          <tr>
            <th>Comisión</th>
            <th>Día</th>
            <th>Horario</th>
            <th>Ubicación</th>
            <th>Tipo</th>
          </tr>
        </thead>
        <tbody>
          {comisionData.Detalle.map((detalle, indexDetalle) => 
            comisionData.dias.map((dia, indexDia) => (
              <tr key={`${indexDetalle}-${indexDia}`}>
                <td style={{textAlign: 'center' }}>
                  {(indexDetalle === 0 && indexDia === 0) ? comisionData.Numero_c : ""} 
                </td>
                <td style={{textAlign: 'center' }}>
                  {indexDia === 0 ? dia : dia}
                </td>
                <td style={{textAlign: 'center' }}>{detalle.Horario}</td>
                <td style={{textAlign: 'center' }}>{detalle.Ubicacion.join(", ")}</td>
                <td style={{textAlign: 'center' }}>{detalle.Tipo}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    );
}
