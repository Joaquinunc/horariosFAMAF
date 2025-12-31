import carreras from '../data/carreras.json';
import info from '../data/data.json';
import { useState } from "react";

export default function GralHook(){
    const [carrera, setCarrera] = useState('');
    const [Anio, setAnio] = useState('');
    const [Cuatrimestre, setCuatrimestre] = useState('');
    const [comision, setComision] = useState('');
    const [materia, setMateria]= useState('');
    const [ingreso, setIngreso] = useState(false);
    const [result, setResult] = useState(false);
    
    const comisiones = info.Ingreso.horarios_2026.map(h => h.comision);
    const toarrcom = [...new Set(comisiones)];
    
    const Carreras = carreras.Info.map(c => c.Nombre_carrera);
    const datosCarreraSeleccionada = carreras.Info.find(c => c.Nombre_carrera === carrera);
    console.log(carrera);

    
    const Anios =datosCarreraSeleccionada ? datosCarreraSeleccionada.Plan_estudios.map(p => p.Año) : [];
    console.log(Anios)

    const Anioselec = datosCarreraSeleccionada?.Plan_estudios.find(a => a.Año === Anio) 
    console.log(Anioselec);
    
    const Cuatrimestres = Anioselec ? Anioselec.Cuatrimestres.map(c => c.Orden) : []; 

    const cuatriselec = Anioselec?.Cuatrimestres.find(c => c.Orden === Cuatrimestre);
    console.log(cuatriselec);

    const Materias = cuatriselec? cuatriselec.Materias : [];

    return { carrera, setCarrera, Anio, setAnio, Cuatrimestre, setCuatrimestre, comision, 
            setComision, materia, setMateria, ingreso, setIngreso, result, setResult, Carreras, Anios, Cuatrimestres, Materias, toarrcom}
}