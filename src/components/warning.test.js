import { render, screen, fireEvent } from '@testing-library/react';
import { Warningpop } from './warning';

describe('Warningpop Component', () => {
  const mockOnClose = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza el mensaje de advertencia', () => {
    render(
      <Warningpop 
        warningmsg="No hay materias disponibles" 
        onClose={mockOnClose}
      />
    );
    expect(screen.getByText('No hay materias disponibles')).toBeInTheDocument();
  });

  test('renderiza el icono de advertencia', () => {
    render(
      <Warningpop 
        warningmsg="Test" 
        onClose={mockOnClose}
      />
    );
    expect(screen.getByText('⚠️')).toBeInTheDocument();
  });

  test('llama onClose al hacer clic en el botón de cerrar', () => {
    render(
      <Warningpop 
        warningmsg="Test" 
        onClose={mockOnClose}
      />
    );
    const closeButton = screen.getByRole('button', { name: /Cerrar advertencia/i });
    fireEvent.click(closeButton);
    
    setTimeout(() => {
      expect(mockOnClose).toHaveBeenCalled();
    }, 350);
  });

  test('llama onClose al hacer clic en el overlay', () => {
    const { container } = render(
      <Warningpop 
        warningmsg="Test" 
        onClose={mockOnClose}
      />
    );
    const overlay = container.querySelector('.warning-overlay');
    fireEvent.click(overlay);
    
    setTimeout(() => {
      expect(mockOnClose).toHaveBeenCalled();
    }, 350);
  });

  test('no cierra al hacer clic en el modal', () => {
    const { container } = render(
      <Warningpop 
        warningmsg="Test" 
        onClose={mockOnClose}
      />
    );
    const modal = container.querySelector('.warndiv');
    fireEvent.click(modal);
    
    expect(mockOnClose).not.toHaveBeenCalled();
  });
});