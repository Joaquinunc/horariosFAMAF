import { render, screen } from '@testing-library/react';
import { FieldRet, timeRet } from './functions';

describe('timeRet Function', () => {
  test('renderiza tabla con datos de comisión', () => {
    const comisionData = {
      Numero_c: 'Única',
      Detalle: [
        {
          dias: ['Lunes'],
          horario: '09:00-11:00',
          Ubicacion: ['AULA A1'],
          tipo: 'Teórico'
        }
      ]
    };
    
    const { container } = render(timeRet(comisionData));
    expect(container.querySelector('.tabla-horarios')).toBeInTheDocument();
    expect(screen.getByText('Lunes')).toBeInTheDocument();
  });

  test('retorna mensaje cuando no hay datos', () => {
    const result = timeRet(null);
    render(result);
    expect(screen.getByText('No hay horarios disponibles para la comisión seleccionada')).toBeInTheDocument();
  });
  
});