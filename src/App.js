import './App.css';
import info from './data/data.json';
import FAMAPS from './images/FAMAPS.png';
import { useState } from 'react';


function OptMap({items}){
  return items.map((option, index) => (
    <option key={index} value={option}>{option}</option>
  ));
}

function FieldRet({label, atribute, setter, elems}){
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

function timeRet(micomm){
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
        {horarios.map((h, index) =>(
          <tr>
            <td>{h.comision}</td>
            <td>{h.dias}</td>
            <td>{h.hora_inicio}-{h.hora_fin}</td>
            <td>{h.aula}</td>
          </tr>
        ))}
      </tbody>
    </table>
              
  )
}

function location(source){
     return (
    <a href={source} target="_blank" rel="noopener noreferrer">
      <img src={FAMAPS} alt="Ir a Google" style={{ width: '600px', height:'400px', border: 'none' }} />
    </a>
  )
}

function App() {
  const [carrera, setCarrera] = useState('');
  const [Anio, setAnio] = useState('');
  const [Cuatrimestre, setCuatrimestre] = useState('');
  const [comision, setComision] = useState('');
  const [materia, setMateria]= useState('');
  const [ingreso, setIngreso] = useState(false);
  const [result, setResult] = useState(false);
  
  const comisiones = info.Ingreso.horarios_2026.map(h => h.comision);
  const toarrcom = [...new Set(comisiones)];
  
  const Carreras = ['Lic. en Matemática','Lic. en Astronomía','Lic. en Física',
                    'Lic. en Cs. de la Computación','Lic. en Matemática Aplicada',
                    'Lic. en Hidrometeorología','Prof. en Matemática',
                    'Prof. en Física','Analista en Computación',
                    'Tec. Un. en Matemática Aplicada','Tec. Un. en Astronomía'
                  ];
  const Anios = ['Primero','Segundo','Tercero','Cuarto','Quinto'];
  const Cuatrimestres =['Primero','Segundo'];
  const Materias = ['Algoritmos I','Algoritmos II', 'Matematica discreta I','Matematica discreta II'];
  
  return (
    <div className='App'>
      <h1 className='Title'>Horarios FAMAF</h1>
      <div className='subT'>
        <h3>Soy ingresante</h3>
        <input id='checkbox_id' type='checkbox' checked={ingreso} onChange={(e) => setIngreso(e.target.checked)}/>
      </div>
      <form className='elements' onSubmit={(e) => {e.preventDefault(); setResult(true)}}>          
          {!ingreso &&(
            <article> 
              <FieldRet label="Seleccione una Carrera:" atribute={carrera} setter={setCarrera} elems={Carreras}/>
              <FieldRet label="Seleccione un anio de cursada:" atribute={Anio} setter={setAnio} elems={Anios}/>
              <FieldRet label="Seleccione un cuatrimestre:" atribute={Cuatrimestre} setter={setCuatrimestre} elems={Cuatrimestres}/>
              <FieldRet label="Seleccione una materia:" atribute={materia} setter={setMateria} elems={Materias}/>
            </article>  
          )}         
          <FieldRet label="Seleccione una comision:" atribute={comision} setter={setComision} elems={ingreso ? toarrcom : []}/>
          <button className='button' type='submit'>Consultar horarios de la materia</button>
          {result && comision && (
            <>
              {timeRet(comision)}
              {location("https://www.google.com/maps/place/Facultad+de+Matem%C3%A1tica,+Astronom%C3%ADa,+F%C3%ADsica+y+Computaci%C3%B3n+-+FaMAF/@-31.4381225,-64.1941192,17z/data=!4m6!3m5!1s0x9432a2f50c080985:0xec1e4c66fe09e826!8m2!3d-31.4383605!4d-64.1926056!16s%2Fg%2F121qyb2y?entry=ttu&g_ep=EgoyMDI1MTIwOS4wIKXMDSoKLDEwMDc5MjA3M0gBUAM%3D")}
            </>
          )}
      </form>       
    </div>
  );
}

export default App;
