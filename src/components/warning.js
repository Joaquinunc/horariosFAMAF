import { useState } from 'react';
import '../styles/warning.css'
/*
Warningpop: esta funcion se encarga de mostrar el mensaje de advertencia para
el caso borde en el que tenemos un cuatrimestre sin materias
in: Mensaje de advertencia, parametro de cierre del mensaje
*/

export function Warningpop({ warningmsg, onClose }) {
    const [isClosing, setIsClosing] = useState(false);

    const handleClose = () => {
        setIsClosing(true);
        setTimeout(() => {
            onClose();
        }, 300); // Duración de la animación
    };

    return (
        <div className={`warning-overlay ${isClosing ? 'closing' : ''}`} onClick={handleClose}>
            <div 
                className={`warndiv ${isClosing ? 'closing' : ''}`}
                onClick={(e) => e.stopPropagation()} // Evita cerrar al hacer clic en el modal
            >
                <span style={{ fontSize: '24px' }}>⚠️</span>
                <p style={{ margin: 0, fontWeight: 'bold', flex: 1 }}>{warningmsg}</p>
                <button 
                    onClick={handleClose}
                    className='warnbutton'
                    aria-label="Cerrar advertencia"
                >
                    ✕
                </button>
            </div>
        </div>
    );
}