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
  
  const Carreras = ['Lic. en Matemática','Lic. en Astronomía','Lic. en Física',
                    'Lic. en Cs. de la Computación','Lic. en Matemática Aplicada',
                    'Lic. en Hidrometeorología','Prof. en Matemática',
                    'Prof. en Física','Analista en Computación',
                    'Tec. Un. en Matemática Aplicada','Tec. Un. en Astronomía'
                  ];
  const Anios = ['Primero','Segundo','Tercero','Cuarto','Quinto'];
  const Cuatrimestres =['Primero','Segundo'];
  
  return (
    <div className='App'>
      <h1>Horarios FAMAF</h1>
      <div className='elements'>
        <select value={carrera} onChange={(e) => setCarrera(e.target.value)}>
          <option value="" disabled hidden>Selecciona una Carrera</option>
          <OptMap items={Carreras}/>
        </select>

        <select value={Anio} onChange={(e) => setAnio(e.target.value)}>
          <option value="" disabled hidden>Selecciona tu Anio</option>
          <OptMap items={Anios}/>
        </select>

        <select value={Cuatrimestre} onChange={(e) => setCuatrimestre(e.target.value)}>
          <option value="" disabled hidden>Selecciona un cuatrimestre</option>
          <OptMap items={Cuatrimestres}/>
        </select>
        <button className='button'>Enviar</button>
      </div>
    </div>
  );
}

export default App;
