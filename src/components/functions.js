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

export function timeRet(micomm){
  const horarios = info.Ingreso.horarios_2026.filter(h => h.comision === micomm);
  return(
    <table>
      <thead>
        <tr>
          <th>Comision</th>
          <th>Dias</th>
          <th>Horario</th>
          <th>Ubicacion</th>
        </tr>
      </thead>
      <tbody>
        {horarios.map((h) =>(
          <tr>
            <td>{h.comision}</td>
            <td>{h.dias}</td>
            <td>{h.hora_inicio} - {h.hora_fin}</td>
            <td>{h.aula}</td>
          </tr>
        ))}
      </tbody>
    </table>
              
  )
}

export function location(source){
     return (
    <a href={source} target="_blank" rel="noopener noreferrer">
      <img src={FAMAPS} alt="Ir a Google" style={{ width: '600px', height:'400px', border: 'none' }} />
    </a>
  )
}