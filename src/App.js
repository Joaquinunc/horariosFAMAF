import './App.css';
import {FieldRet, timeRet, location} from './components/functions';
import GralHook from './components/constants'; 

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
              {location("https://www.google.com/maps/place/Facultad+de+Matem%C3%A1tica,+Astronom%C3%ADa,+F%C3%ADsica+y+Computaci%C3%B3n+-+FaMAF/@-31.4381225,-64.1941192,17z/data=!4m6!3m5!1s0x9432a2f50c080985:0xec1e4c66fe09e826!8m2!3d-31.4383605!4d-64.1926056!16s%2Fg%2F121qyb2y?entry=ttu&g_ep=EgoyMDI1MTIwOS4wIKXMDSoKLDEwMDc5MjA3M0gBUAM%3D")}
            </>
          )}
      </form>       
    </div>
  );
}

export default App;
