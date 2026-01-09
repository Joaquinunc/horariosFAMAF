import FAMAPS from '../images/FAMAPS.png';
import info from '../data/data.json';

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

export function timeRet(micomm) {
  // 1. Buscamos la comisión específica
  const comisionData = info.Ingreso.horarios_2026.find(h => h.comision === micomm);

  // Si no hay datos, evitamos errores
  if (!comisionData) return <p>No hay horarios disponibles para la comisión {micomm}</p>;

  return (
    <table className="tabla-horarios">
      <thead>
        <tr>
          <th>Comision</th>
          <th>Día</th>
          <th>Horario</th>
          <th>Ubicación</th>
        </tr>
      </thead>
      <tbody>
      
        {comisionData.clases.map((clase, indexDia) => (
          // Por cada día (Lunes, Miércoles...), mapeamos sus ubicaciones
          clase.ubicacion.map((loc, indexLoc) => (
            <tr key={`${indexDia}-${indexLoc}`}>
              {/* Solo mostramos el nombre del día en la primera fila de ese día */}
              <td style={{textAlign: 'center' }}>
                {(indexLoc === 0 && indexDia === 0)? micomm: ""} 
              </td>
              <td style={{textAlign: 'center' }}>
                {indexLoc === 0 ? clase.dia : ""}
              </td>
              <td style={{textAlign: 'center' }}>{loc.hora_inicio} - {loc.hora_fin}</td>
              <td style={{textAlign: 'center' }}>{loc.aula}</td>
            </tr>
          ))
        ))}
      </tbody>
    </table>
  );
}

export function location(){
     return (
   <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3404.1165381730643!2d-64.18534552550268!3d-31.438458497316656!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9432a2ee08f5d701%3A0xe2812795e980b012!2sUNC%20-%20Bater%C3%ADas%20de%20Aulas%20de%20Uso%20Com%C3%BAn%20C!5e0!3m2!1ses!2sar!4v1767756195775!5m2!1ses!2sar" width="600" height="450" style={{border:0}} allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  )
}