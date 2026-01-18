import './App.css';
import {FieldRet, timeRet} from './components/functions';
import { location_mapper } from './components/locations';
import GralHook from './components/Hook'; 

function App() {

  const {carrera, setCarrera, Anio, setAnio, Cuatrimestre, setCuatrimestre, comision, 
            setComision, materia, setMateria, result, setResult, 
            Carreras, Anios, Cuatrimestres, Materias, Comisiones_nums, ComisionSeleccionada} = GralHook();
  return (
    <div className='App'>
      <h1 className='Title'>Horarios FAMAF</h1>
      <form className='elements' onSubmit={(e) => {e.preventDefault(); setResult(true)}}>          
          {(
            <article> 
              <FieldRet label="Seleccione una Carrera:" atribute={carrera} setter={setCarrera} elems={Carreras}/>
              <FieldRet label="Seleccione un anio de cursada:" atribute={Anio} setter={setAnio} elems={Anios}/>
              <FieldRet label="Seleccione un cuatrimestre:" atribute={Cuatrimestre} setter={setCuatrimestre} elems={Cuatrimestres}/>
              <FieldRet label="Seleccione una materia:" atribute={materia} setter={setMateria} elems={Materias}/>
            </article>  
          )}         
          <FieldRet label="Seleccione una comision:" atribute={comision} setter={setComision} elems={Comisiones_nums}/>
          <button className='button' type='submit'>Consultar horarios de la materia</button>
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
