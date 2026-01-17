import info2 from '../data/comisiones.json';
import { useState } from "react";

/*
GralHook()
Funcion que se encarga de encapsular todas las constantes que luego se utilizara en App.js
asi como de obtener la informacion de la base de datos.
*/

export default function GralHook(){
    const [carrera, setCarrera] = useState('');
    const [Anio, setAnio] = useState('');
    const [Cuatrimestre, setCuatrimestre] = useState('');
    const [comision, setComision] = useState('');
    const [materia, setMateria]= useState('');
    const [result, setResult] = useState(false);

    // Obtenemos la lista de carreras
    const Carreras = Object.keys(info2);
    console.log(Carreras);
    // Obtenemos la lista de anios de cursada de una carrera
    const Anios = carrera ? Object.keys(info2[carrera]):[];
    console.log(Anios);
    // Lista de cuatrimestres de un anio de cursada
    const Cuatrimestres = carrera && Anio ?Object.keys(info2[carrera][Anio]) : [];
    // Lista de materias de un cuatrimestre
    console.log(Cuatrimestres);
    const Materias = carrera && Anio && Cuatrimestre ? Object.keys(info2[carrera][Anio][Cuatrimestre]):[];
    console.log(Materias);
    // Lista de comisiones para una materia
    const Comisiones = carrera && Anio && Cuatrimestre && materia
    ? info2[carrera][Anio][Cuatrimestre][materia]
    : [];
    console.log(Comisiones);
    // Numeros de comisiones
    const Comisiones_nums = Comisiones.map(c => c.Numero_c);
    console.log(Comisiones_nums);
    
    const ComisionSeleccionada = Comisiones.find(c => c.Numero_c === comision); 
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