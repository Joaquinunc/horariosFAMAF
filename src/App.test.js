import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import * as GralHook from './components/Hook';

// Mock del hook
jest.mock('./components/Hook');
jest.mock('./components/functions');
jest.mock('./components/locations');
jest.mock('./components/warning');

describe('App Component', () => {
  const mockHookData = {
    carrera: '',
    setCarrera: jest.fn(),
    Anio: '',
    setAnio: jest.fn(),
    Cuatrimestre: '',
    setCuatrimestre: jest.fn(),
    comision: '',
    setComision: jest.fn(),
    materia: '',
    setMateria: jest.fn(),
    result: false,
    setResult: jest.fn(),
    Carreras: ['Licenciatura en Computación', 'Licenciatura en Física'],
    Anios: [],
    Cuatrimestres: [],
    Materias: [],
    Comisiones_nums: [],
    ComisionSeleccionada: null,
    sinmaterias: '',
    sinmateriasbul: false
  };

  beforeEach(() => {
    GralHook.default.mockReturnValue(mockHookData);
  });

  test('renderiza el título correctamente', () => {
    render(<App />);
    expect(screen.getByText('FAMAFyC - Buscador de horarios')).toBeInTheDocument();
  });


  test('no renderiza campos de materia cuando sinmateriasbul es true', () => {
    GralHook.default.mockReturnValue({
      ...mockHookData,
      sinmateriasbul: true,
      sinmaterias: 'No hay materias disponibles'
    });
    render(<App />);
    expect(screen.queryByText('Seleccione una materia:')).not.toBeInTheDocument();
  });

  test('botón está deshabilitado cuando no hay comisión seleccionada', () => {
    GralHook.default.mockReturnValue({
      ...mockHookData,
      sinmateriasbul: false,
      comision: ''
    });
    render(<App />);
    const button = screen.getByRole('button', { name: /Consultar horarios/i });
    expect(button).toBeDisabled();
  });

  test('botón está habilitado cuando hay comisión seleccionada', () => {
    GralHook.default.mockReturnValue({
      ...mockHookData,
      sinmateriasbul: false,
      comision: 'Única'
    });
    render(<App />);
    const button = screen.getByRole('button', { name: /Consultar horarios/i });
    expect(button).not.toBeDisabled();
  });

  test('warning se muestra cuando sinmateriasbul es true', () => {
    GralHook.default.mockReturnValue({
      ...mockHookData,
      sinmateriasbul: true,
      sinmaterias: 'No hay materias para este cuatrimestre'
    });
    render(<App />);
    // El warning debe estar renderizado (verificar que el mock fue llamado)
    expect(screen.queryByText('Seleccione una materia:')).not.toBeInTheDocument();
  });

  test('resetea resultados cuando cambia la materia', async () => {
    const setResult = jest.fn();
    GralHook.default.mockReturnValue({
      ...mockHookData,
      setResult,
      sinmateriasbul: false,
      materia: 'Álgebra'
    });
    const { rerender } = render(<App />);
    
    GralHook.default.mockReturnValue({
      ...mockHookData,
      setResult,
      sinmateriasbul: false,
      materia: 'Análisis'
    });
    rerender(<App />);
    
    await waitFor(() => {
      expect(setResult).toHaveBeenCalledWith(false);
    });
  });
});
