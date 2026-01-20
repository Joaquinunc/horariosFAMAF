import './App.css';
import {FieldRet, timeRet} from './components/functions';
import { location_mapper } from './components/locations';
import GralHook from './components/Hook'; 
import { Warningpop } from './components/warning';
import { useState, useEffect} from 'react';

function App() {

  const {carrera, setCarrera, Anio, setAnio, Cuatrimestre, setCuatrimestre, comision, 
            setComision, materia, setMateria, result, setResult, 
            Carreras, Anios, Cuatrimestres, Materias, Comisiones_nums, ComisionSeleccionada, sinmaterias, sinmateriasbul} = GralHook();
    // Estado local para controlar si el pop-up se muestra o no
  const [showWarning, setShowWarning] = useState(false);
  // estado local para guardar la comision confirmada tras el click
  const [confirmCom, setconfirmCom] = useState(false);
  
  // actalizamos la confirmacion a la com seleccionada
  const handleSearch = (e) => {
    e.preventDefault();
    if(comision){
      setconfirmCom(ComisionSeleccionada);
      setResult(true);
    }

  }; 
  //reseteamos si se cambia la materia o comision
  useEffect(() => {
    setResult(false);
    setconfirmCom(null);
  }, [materia]);

  // Cada vez que el cuatrimestre cambia o sinmateriasbul cambia, actualizamos el warning
  useEffect(() => {
    setShowWarning(sinmateriasbul);
  }, [Cuatrimestre, sinmateriasbul]);
  

  return (
    <div className='App'>
      <h1 className='Title'>FAMAFyC - Buscador de horarios</h1>
     {/* Mostramos el Pop-up si ambas condiciones son ciertas */}
      {sinmateriasbul && showWarning && (
        <div className='warning'>
        <Warningpop 
          warningmsg={sinmaterias} 
          onClose={() => setShowWarning(false)} 
        />
        </div>
      )}
      <form className='elements' onSubmit={handleSearch}>          
      
            <article> 
              <FieldRet label="Selecciona una carrera:" atribute={carrera} setter={setCarrera} elems={Carreras}/>
              <FieldRet label="Selecciona un año de cursada:" atribute={Anio} setter={setAnio} elems={Anios} />
              <FieldRet label="Selecciona un cuatrimestre:" atribute={Cuatrimestre} setter={setCuatrimestre} elems={Cuatrimestres}/>
              {!sinmateriasbul && (

                <div>  <FieldRet label="Selecciona una materia:" atribute={materia} setter={setMateria} elems={Materias} />
                <FieldRet label="Selecciona una comisión:" atribute={comision} setter={setComision} elems={Comisiones_nums}/></div>
            )
            }
            </article>  
               
          
          {!sinmateriasbul && (<button className='button' type='submit' disabled={!comision}>Consultar horarios de la materia</button>)}
          {result && comision && (
            <div className='resultados-container'>
              {timeRet(confirmCom, materia)}
              <div className="map-wrapper">
                {location_mapper(confirmCom)}
              </div>
            </div>
          )}
      </form>       
    </div>
  );
}

export default App;
