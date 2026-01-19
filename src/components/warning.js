import '../styles/warning.css'
/*
Warningpop: esta funcion se encarga de mostrar el mensaje de advertencia para
el caso borde en el que tenemos un cuatrimestre sin materias
in: Mensaje de advertencia, parametro de cierre del mensaje
*/
export function Warningpop({ warningmsg, onClose }) {
    return (
        <div className='warndiv'
        >
            <span style={{ fontSize: '20px' }}>⚠️</span>
            <p style={{ margin: 0, fontWeight: 'bold' }}>{warningmsg}</p>
            <button 
                onClick={onClose}
                className='warnbutton'
            >
                ✕
            </button>
        </div>
    );
}