import info2 from '../data/comisiones.json';
import { useState, useEffect } from "react";

/*
GralHook()
Funcion que se encarga de enlazar el frontend con la base de datos, obteniendo la informacion
necesaria para las consultas, fijandose en resetearlas al realizan consultas nuevas
*/

export default function GralHook(){
    // diferentes elementos de la base de datos con su estado
    const [carrera, setCarrera] = useState('');
    const [Anio, setAnio] = useState('');
    const [Cuatrimestre, setCuatrimestre] = useState('');
    const [comision, setComision] = useState('');
    const [materia, setMateria]= useState('');
    const [result, setResult] = useState(false);

    // Resetear estados dependientes cuando cambia la carrera
    useEffect(() => {
        setAnio('');
        setCuatrimestre('');
        setMateria('');
        setComision('');
        setResult(false);
    }, [carrera]);

    // Resetear estados dependientes cuando cambia el año
    useEffect(() => {
        setCuatrimestre('');
        setMateria('');
        setComision('');
        setResult(false);
    }, [Anio]);

    // Resetear estados dependientes cuando cambia el cuatrimestre
    useEffect(() => {
        setMateria('');
        setComision('');
        setResult(false);
    }, [Cuatrimestre]);

    // Resetear comision cuando cambia la materia
    useEffect(() => {
        setComision('');
        setResult(false);
    }, [materia]);

    // Obtenemos la lista de carreras
    const Carreras = Object.keys(info2);
    console.log(Carreras);
    // Obtenemos la lista de anios de cursada de una carrera
    const Anios = carrera && info2[carrera]? Object.keys(info2[carrera]): [];
    console.log(Anios);
    // Lista de cuatrimestres de un anio de cursada
    const Cuatrimestres = carrera && Anio && info2[carrera] && info2[carrera]?.[Anio] ?  Object.keys(info2[carrera][Anio]) : [];
    // Lista de materias de un cuatrimestre
    console.log(Cuatrimestres);
    const Materias = carrera && Anio && Cuatrimestre && info2[carrera] && info2[carrera]?.[Anio] && info2[carrera]?.[Anio]?.[Cuatrimestre] ? Object.keys(info2[carrera][Anio][Cuatrimestre]) : [];
    console.log(Materias);
    // Lista de comisiones para una materia
    const Comisiones = carrera && Anio && Cuatrimestre && materia && info2[carrera] 
    && info2[carrera]?.[Anio] && info2[carrera]?.[Anio]?.[Cuatrimestre] &&
    info2[carrera]?.[Anio]?.[Cuatrimestre]?.[materia] 
    ? info2[carrera][Anio][Cuatrimestre][materia]
    : [];
    console.log(Comisiones);
    // Numeros de comisiones
    const Comisiones_nums = Comisiones && Array.isArray(Comisiones) ? Comisiones.map(c => c.Numero_c) : [];
    console.log(Comisiones_nums);
    
    const ComisionSeleccionada = Comisiones && Array.isArray(Comisiones) ? Comisiones.find(c => c.Numero_c === comision) : null; 
    console.log(ComisionSeleccionada);
    
   return { 
        carrera, setCarrera, 
        Anio, setAnio, 
        Cuatrimestre, setCuatrimestre, 
        comision, setComision, 
        materia, setMateria, 
        result, setResult, 
        Carreras, 
        Anios, 
        Cuatrimestres, 
        Materias, 
        Comisiones, 
        Comisiones_nums,
        ComisionSeleccionada
    }
}