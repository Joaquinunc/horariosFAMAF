import pytest
import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from layer_1.parsers import (
    obtener_dia_semana,
    obtener_carrerayanio,
    normalizar_nombre,
    obtener_typ,
    parser_aula,
    comparser,
    comjoiner
)

class TestObtenerDiaSemana:
    def test_dias_validos(self):
        assert obtener_dia_semana("Monday") == "Lunes"
        assert obtener_dia_semana("Tuesday") == "Martes"
        assert obtener_dia_semana("Wednesday") == "Miércoles"
        assert obtener_dia_semana("Thursday") == "Jueves"
        assert obtener_dia_semana("Friday") == "Viernes"
        assert obtener_dia_semana("Saturday") == "Sábado"
        assert obtener_dia_semana("Sunday") == "Domingo"
    
    def test_dia_invalido(self):
        assert obtener_dia_semana("InvalidDay") == "InvalidDay"
    
    def test_dia_vacio(self):
        assert obtener_dia_semana("") == ""


class TestObtenerCarreraYAnio:
    def test_carrera_conocida(self):
        # Mock del gcalendar
        gcalendar = {'x-wr-caldesc': 'Licenciatura en Ciencias de la Computación - Primer año'}
        anio, carrera = obtener_carrerayanio("test_url", gcalendar)
        assert carrera == "Licenciatura en Ciencias de la Computación"
        assert anio == "1° año"
    
    def test_segundo_anio(self):
        gcalendar = {'x-wr-caldesc': 'Licenciatura en Física - Segundo año'}
        anio, carrera = obtener_carrerayanio("test_url", gcalendar)
        assert carrera == "Licenciatura en Física"
        assert anio == "2° año"
    
    def test_quinto_anio(self):
        gcalendar = {'x-wr-caldesc': 'Licenciatura en Matemática - Quinto año'}
        anio, carrera = obtener_carrerayanio("test_url", gcalendar)
        assert carrera == "Licenciatura en Matemática"
        assert anio == "5° año"


class TestNormalizarNombre:
    def test_nombre_con_comision(self):
        assert normalizar_nombre("Álgebra (Com. 1)") == "Álgebra"
        assert normalizar_nombre("Análisis Com. 2") == "Análisis"
    
    def test_nombre_con_aula(self):
        assert normalizar_nombre("Física Aula 14") == "Física"
        assert normalizar_nombre("Química: Aula LEF") == "Química"
    
    def test_nombre_con_teorico_practico(self):
        assert normalizar_nombre("Álgebra Teórico") == "Álgebra"
        assert normalizar_nombre("Cálculo Práctico") == "Cálculo"
    
    def test_nombre_limpio(self):
        assert normalizar_nombre("Análisis Matemático I").strip() != ""
    
    def test_nombre_con_guiones(self):
        assert normalizar_nombre("Base de Datos - ").strip() == "Base de Datos"


class TestObtenerTyp:
    def test_tipo_teorico(self):
        assert obtener_typ("Álgebra Teórico") == "Teórico"
        assert obtener_typ("Física (T)") == "Teórico"
    
    def test_tipo_practico(self):
        assert obtener_typ("Laboratorio Práctico") == "Práctico"
        assert obtener_typ("Ejercicios (P)") == "Práctico"
    
    def test_tipo_no_especificado(self):
        assert obtener_typ("Álgebra") == "T/P"


class TestParserAula:
    def test_aula_simple(self):
        assert "AULA 14" in parser_aula("Clase en AULA 14")
    
    def test_laboratorio(self):
        result = parser_aula("LEF1")
        assert any("LEF" in r for r in result)
    
    def test_multiples_aulas(self):
        result = parser_aula("AULA A1 y LAB 2")
        assert len(result) >= 2
    
    def test_sin_aula(self):
        assert parser_aula("Clase de matemática") == []
    
    def test_aula_virtual(self):
        assert "VIRTUAL" in parser_aula("Clase VIRTUAL")
    
    def test_sala(self):
        result = parser_aula("SALA A")
        assert "SALA A" in result


class TestComparser:
    def test_comision_simple(self):
        result = comparser(
            ["Comisión 1"], 
            "09:00", 
            "11:00", 
            "Teórico", 
            "Lunes", 
            "Álgebra Com. 1 AULA 14"
        )
        assert len(result) == 1
        assert result[0]["Numero_c"] == "1"
        assert result[0]["Detalle"][0]["Horario"] == "09:00 - 11:00"
        assert result[0]["Detalle"][0]["Tipo"] == "Teórico"
        assert result[0]["Detalle"][0]["dias"] == ["Lunes"]
    
    def test_multiples_comisiones(self):
        result = comparser(
            ["Com. 1, Com. 2"], 
            "14:00", 
            "16:00", 
            "Práctico", 
            "Martes", 
            "Física Com. 1 Com. 2 LAB A"
        )
        assert len(result) >= 2
    
    def test_sin_aula_especificada(self):
        result = comparser(
            ["Comisión 1"], 
            "10:00", 
            "12:00", 
            "T/P", 
            "Miércoles", 
            "Química Com. 1"
        )
        assert result[0]["Detalle"][0]["Ubicacion"] == ["No especificada"]


class TestComjoiner:
    def test_agregar_nueva_comision(self):
        materias_agrupadas = {}
        nueva_comision = [{
            "Numero_c": "1",
            "Detalle": [{
                "Ubicacion": ["AULA 14"],
                "Horario": "09:00 - 11:00",
                "Tipo": "Teórico",
                "dias": ["Lunes"]
            }]
        }]
        
        result = comjoiner(nueva_comision, "Álgebra", materias_agrupadas)
        assert "Álgebra" in result
        assert len(result["Álgebra"]) == 1
        assert result["Álgebra"][0]["Numero_c"] == "1"
    
    def test_agregar_dia_a_comision_existente(self):
        materias_agrupadas = {
            "Álgebra": [{
                "Numero_c": "1",
                "Detalle": [{
                    "Ubicacion": ["AULA 14"],
                    "Horario": "09:00 - 11:00",
                    "Tipo": "Teórico",
                    "dias": ["Lunes"]
                }]
            }]
        }
        
        nueva_comision = [{
            "Numero_c": "1",
            "Detalle": [{
                "Ubicacion": ["AULA 14"],
                "Horario": "09:00 - 11:00",
                "Tipo": "Teórico",
                "dias": ["Miércoles"]
            }]
        }]
        
        result = comjoiner(nueva_comision, "Álgebra", materias_agrupadas)
        assert len(result["Álgebra"]) == 1
        assert len(result["Álgebra"][0]["Detalle"]) == 2
    
    def test_no_duplicar_mismo_detalle(self):
        materias_agrupadas = {
            "Física": [{
                "Numero_c": "2",
                "Detalle": [{
                    "Ubicacion": ["LAB A"],
                    "Horario": "14:00 - 16:00",
                    "Tipo": "Práctico",
                    "dias": ["Martes"]
                }]
            }]
        }
        
        # Intentar agregar el mismo detalle
        misma_comision = [{
            "Numero_c": "2",
            "Detalle": [{
                "Ubicacion": ["LAB A"],
                "Horario": "14:00 - 16:00",
                "Tipo": "Práctico",
                "dias": ["Martes"]
            }]
        }]
        
        result = comjoiner(misma_comision, "Física", materias_agrupadas)
        # No debe duplicarse
        assert len(result["Física"][0]["Detalle"]) == 1
    
    def test_agregar_nueva_materia(self):
        materias_agrupadas = {
            "Álgebra": [{
                "Numero_c": "1",
                "Detalle": [{"dias": ["Lunes"]}]
            }]
        }
        
        nueva_comision = [{
            "Numero_c": "1",
            "Detalle": [{
                "Ubicacion": ["AULA A"],
                "Horario": "10:00 - 12:00",
                "Tipo": "Teórico",
                "dias": ["Jueves"]
            }]
        }]
        
        result = comjoiner(nueva_comision, "Análisis", materias_agrupadas)
        assert "Análisis" in result
        assert "Álgebra" in result
        assert len(result.keys()) == 2