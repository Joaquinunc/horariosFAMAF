import './App.css';
import {FieldRet, timeRet} from './components/functions';
import { location_mapper } from './components/locations';
import GralHook from './components/Hook'; 
import { Warningpop } from './components/warning';
import { useState, useEffect } from 'react';

function App() {

  const {carrera, setCarrera, Anio, setAnio, Cuatrimestre, setCuatrimestre, comision, 
            setComision, materia, setMateria, result, setResult, 
            Carreras, Anios, Cuatrimestres, Materias, Comisiones_nums, ComisionSeleccionada, sinmaterias, sinmateriasbul} = GralHook();
    // Estado local para controlar si el pop-up se muestra o no
  const [showWarning, setShowWarning] = useState(false);

  // Cada vez que el hook diga que no hay materias, activamos el pop-up
  useEffect(() => {
    if (sinmateriasbul) {
      setShowWarning(true);
    }
  }, [sinmateriasbul]);
 
            return (
    <div className='App'>
      <h1 className='Title'>Horarios FAMAF</h1>
     {/* Mostramos el Pop-up si ambas condiciones son ciertas */}
      {sinmateriasbul && showWarning && (
        <Warningpop 
          warningmsg={sinmaterias} 
          onClose={() => setShowWarning(false)} 
        />
      )}
      <form className='elements' onSubmit={(e) => {e.preventDefault(); setResult(true)}}>          
      
            <article> 
              <FieldRet label="Seleccione una Carrera:" atribute={carrera} setter={setCarrera} elems={Carreras}/>
              <FieldRet label="Seleccione un año de cursada:" atribute={Anio} setter={setAnio} elems={Anios} />
              <FieldRet label="Seleccione un cuatrimestre:" atribute={Cuatrimestre} setter={setCuatrimestre} elems={Cuatrimestres}/>
              {!sinmateriasbul && (

                <div>  <FieldRet label="Seleccione una materia:" atribute={materia} setter={setMateria} elems={Materias} />
                <FieldRet label="Seleccione una comisión:" atribute={comision} setter={setComision} elems={Comisiones_nums}/></div>
            )
            }
            </article>  
               
          
          {!sinmateriasbul && (<button className='button' type='submit'>Consultar horarios de la materia</button>)}
          {result && comision && (
            <>
              {timeRet(ComisionSeleccionada)}
              {location_mapper(ComisionSeleccionada)}
            </>
          )}
      </form>       
    </div>
  );
}

export default App;
