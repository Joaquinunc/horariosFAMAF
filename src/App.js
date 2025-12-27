import './App.css';
import { useState } from 'react';

function OptMap({items}){
  return items.map((option, index) => (
    <option key={index} value={option}>{option}</option>
  ));
}

function App() {
  const [carrera, setCarrera] = useState('');
  const [Anio, setAnio] = useState('');
  const [Cuatrimestre, setCuatrimestre] = useState('');
  const [comision, setComision] = useState('');
  const [materia, setMateria]= useState('');
  const [ingreso, setIngreso] = useState(false);
  
  const Carreras = ['Lic. en Matemática','Lic. en Astronomía','Lic. en Física',
                    'Lic. en Cs. de la Computación','Lic. en Matemática Aplicada',
                    'Lic. en Hidrometeorología','Prof. en Matemática',
                    'Prof. en Física','Analista en Computación',
                    'Tec. Un. en Matemática Aplicada','Tec. Un. en Astronomía'
                  ];
  const Anios = ['Primero','Segundo','Tercero','Cuarto','Quinto'];
  const Cuatrimestres =['Primero','Segundo'];
  const Comisiones =['M1','M2', 'M3', 'M4', 'M5', 'M6', 'T1', 'T3','T4', 'T5', 'T6', 'T7','T8', 'T9'];
  const Materias = ['Algoritmos I','Algoritmos II', 'Matematica discreta I','Matematica discreta II'];
  
  return (
    <div className='App'>
      <h1 className='Title'>Horarios FAMAF</h1>
      <div className='subT'>
        <h3>Soy ingresante</h3>
        <input id='checkbox_id' type='checkbox' checked={ingreso} onChange={(e) => setIngreso(e.target.checked)}/>
      </div>
      <form className='elements'>          
          {!ingreso &&(
            <div className='campos'>
              <label className='etiqueta'>Selecciona una Carrera:</label>
              <select value={carrera} onChange={(e) => setCarrera(e.target.value)}>
                <option value="" disabled hidden required></option>
                <OptMap items={Carreras}/>
              </select>
            </div>
          )}
          
          {!ingreso &&(
            <div className='campos'>
              <label className='etiqueta'>Selecciona un año de cursada:</label>
              <select value={Anio} onChange={(e) => setAnio(e.target.value)}>
                <option value="" disabled hidden required></option>
                <OptMap items={Anios}/>
              </select>
            </div>
          )}

          {!ingreso &&(
            <div className='campos'>
              <label className='etiqueta'>Selecciona un cuatrimestre:</label>
              <select value={Cuatrimestre} onChange={(e) => setCuatrimestre(e.target.value)}>
                <option value="" disabled hidden></option>
                <OptMap items={Cuatrimestres}/>
              </select>
            </div>
          )}

          {!ingreso &&(
            <div className='campos'>
              <label className='etiqueta'>Selecciona una Materia:</label>
              <select value={materia} onChange={(e) => setMateria(e.target.value)}>
                <option value="" disabled hidden></option>
                <OptMap items={Materias}/>
              </select>
            </div>
          )}
          
          <div className='campos'>
            <label className='etiqueta'>Selecciona una comision:</label>
            <select value={comision} onChange={(e) => setComision(e.target.value)}>
              <option value="" disabled hidden></option>
              <OptMap items={Comisiones}/>
            </select>
          </div>  
          <button className='button'>Enviar</button>
  
      </form>  
    </div>
  );
}

export default App;
