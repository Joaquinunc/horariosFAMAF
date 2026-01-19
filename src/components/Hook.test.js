import { renderHook, act } from '@testing-library/react';
import GralHook from './Hook';
import * as data from '../backend/comisiones.json';

// Mock del JSON
jest.mock('../backend/comisiones.json', () => ({
  'Licenciatura en Computación': {
    '1° año': {
      'Primer Cuatrimestre': {
        'Álgebra': [
          { Numero_c: 'Única', Detalle: [{ dias: ['Lunes'], horario: '09:00-11:00' }] }
        ]
      }
    }
  }
}));

describe('GralHook', () => {
  test('inicializa estados vacíos', () => {
    const { result } = renderHook(() => GralHook());
    expect(result.current.carrera).toBe('');
    expect(result.current.Anio).toBe('');
    expect(result.current.Cuatrimestre).toBe('');
    expect(result.current.materia).toBe('');
  });

  test('obtiene carreras correctamente', () => {
    const { result } = renderHook(() => GralHook());
    expect(result.current.Carreras).toContain('Licenciatura en Computación');
  });

  test('actualiza carrera y reseta dependientes', () => {
    const { result } = renderHook(() => GralHook());
    
    act(() => {
      result.current.setCarrera('Licenciatura en Computación');
    });
    
    expect(result.current.carrera).toBe('Licenciatura en Computación');
  });

  test('obtiene años según carrera seleccionada', () => {
    const { result } = renderHook(() => GralHook());
    
    act(() => {
      result.current.setCarrera('Licenciatura en Computación');
    });
    
    expect(result.current.Anios).toContain('1° año');
  });



  test('resetea estados cuando cambia carrera', () => {
    const { result } = renderHook(() => GralHook());
    
    act(() => {
      result.current.setCarrera('Licenciatura en Computación');
      result.current.setAnio('1° año');
    });
    
    act(() => {
      result.current.setCarrera('Licenciatura en Física');
    });
    
    expect(result.current.Anio).toBe('');
  });
});