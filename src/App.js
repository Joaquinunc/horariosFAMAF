import './App.css';
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

function Minitest(){
  return(
    <div className='lel'>
      <h1>button testing</h1>
    </div>
  );
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
            <article> 
              <FieldRet label="Seleccione una Carrera:" atribute={carrera} setter={setCarrera} elems={Carreras}/>
              <FieldRet label="Seleccione un anio de cursada:" atribute={Anio} setter={setAnio} elems={Anios}/>
              <FieldRet label="Seleccione un cuatrimestre:" atribute={Cuatrimestre} setter={setCuatrimestre} elems={Cuatrimestres}/>
              <FieldRet label="Seleccione una materia:" atribute={materia} setter={setMateria} elems={Materias}/>
            </article>  
          )}         
          <FieldRet label="Seleccione una comision:" atribute={comision} setter={setComision} elems={Comisiones}/>
          <button className='button' onClick={Minitest}>Consultar horarios de la materia</button>
      </form>  
    </div>
  );
}

export default App;
