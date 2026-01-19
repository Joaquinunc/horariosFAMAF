
import pytest
from .sorter import data_sorter

class TestDataSorter:
   
    def test_ordena_comisiones_numericamente(self):
        data = {
            "Licenciatura en Física": {
                "2° año": {
                    "Primer Cuatrimestre": {
                        "Mecánica": [
                            {"Numero_c": "3", "Detalle": [{"Horario": "10:00"}]},
                            {"Numero_c": "1", "Detalle": [{"Horario": "09:00"}]},
                            {"Numero_c": "2", "Detalle": [{"Horario": "11:00"}]}
                        ]
                    },
                    "Segundo Cuatrimestre": {}
                }
            }
        }
        
        result = data_sorter(data)
        comisiones = result["Licenciatura en Física"]["2° año"]["Primer Cuatrimestre"]["Mecánica"]
        assert comisiones[0]["Numero_c"] == "1"
        assert comisiones[1]["Numero_c"] == "2"
        assert comisiones[2]["Numero_c"] == "3"
    
    def test_ordena_horarios(self):
        data = {
            "Licenciatura en Matemática": {
                "3° año": {
                    "Primer Cuatrimestre": {
                        "Análisis": [
                            {
                                "Numero_c": "1",
                                "Detalle": [
                                    {"Horario": "14:00 - 16:00"},
                                    {"Horario": "09:00 - 11:00"}
                                ]
                            }
                        ]
                    },
                    "Segundo Cuatrimestre": {}
                }
            }
        }
        
        result = data_sorter(data)
        detalles = result["Licenciatura en Matemática"]["3° año"]["Primer Cuatrimestre"]["Análisis"][0]["Detalle"]
        assert detalles[0]["Horario"] == "09:00 - 11:00"
        assert detalles[1]["Horario"] == "14:00 - 16:00"
    
    def test_maneja_comisiones_no_numericas(self):
        data = {
            "Profesorado en Física": {
                "1° año": {
                    "Primer Cuatrimestre": {
                        "Pedagogía": [
                            {"Numero_c": "Única", "Detalle": [{"Horario": "10:00"}]},
                            {"Numero_c": "1", "Detalle": [{"Horario": "09:00"}]}
                        ]
                    },
                    "Segundo Cuatrimestre": {}
                }
            }
        }
        
        result = data_sorter(data)
        comisiones = result["Profesorado en Física"]["1° año"]["Primer Cuatrimestre"]["Pedagogía"]
        # Las numéricas primero, luego las no numéricas
        assert comisiones[0]["Numero_c"] == "1"
        assert comisiones[1]["Numero_c"] == "Única"
    
    def test_preserva_estructura_completa(self):
        data = {
            "Licenciatura en Astronomía": {
                "1° año": {
                    "Primer Cuatrimestre": {
                        "Astrofísica": [
                            {
                                "Numero_c": "1",
                                "Detalle": [
                                    {
                                        "Horario": "09:00 - 11:00",
                                        "Ubicacion": ["AULA 14"],
                                        "Tipo": "Teórico",
                                        "dias": ["Lunes"]
                                    }
                                ]
                            }
                        ]
                    },
                    "Segundo Cuatrimestre": {}
                }
            }
        }
        
        result = data_sorter(data)
        comision = result["Licenciatura en Astronomía"]["1° año"]["Primer Cuatrimestre"]["Astrofísica"][0]
        assert comision["Numero_c"] == "1"
        assert len(comision["Detalle"]) == 1
        assert comision["Detalle"][0]["Ubicacion"] == ["AULA 14"]
    
    def test_ordena_multiples_carreras(self):
        data = {
            "Licenciatura en Física": {
                "1° año": {"Primer Cuatrimestre": {}, "Segundo Cuatrimestre": {}}
            },
            "Licenciatura en Computación": {
                "1° año": {"Primer Cuatrimestre": {}, "Segundo Cuatrimestre": {}}
            },
            "Licenciatura en Astronomía": {
                "1° año": {"Primer Cuatrimestre": {}, "Segundo Cuatrimestre": {}}
            }
        }
        
        result = data_sorter(data)
        carreras = list(result.keys())
        # Verifica que estén ordenadas
        assert carreras == sorted(carreras)
    
    def test_maneja_cuatrimestres_vacios(self):
        data = {
            "Licenciatura en Hidrometeorología": {
                "2° año": {
                    "Primer Cuatrimestre": {},
                    "Segundo Cuatrimestre": {
                        "Climatología": [
                            {"Numero_c": "1", "Detalle": [{"Horario": "10:00"}]}
                        ]
                    }
                }
            }
        }
        
        result = data_sorter(data)
        assert result["Licenciatura en Hidrometeorología"]["2° año"]["Primer Cuatrimestre"] == {}
        assert "Climatología" in result["Licenciatura en Hidrometeorología"]["2° año"]["Segundo Cuatrimestre"]