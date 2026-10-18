import importlib

import constantes_correos


def test_lee_remitente_y_contrato_del_entorno(monkeypatch):
    monkeypatch.setenv("CORREOS_REMITENTE_NOMBRE", " Ana ")
    monkeypatch.setenv("CORREOS_REMITENTE_DIRECCION", "Calle Inventada 1")
    monkeypatch.setenv("CORREOS_CONTRATO_NUMERO_CLIENTE", "12345")
    c = importlib.reload(constantes_correos)

    assert c.REMITENTE["nombre"] == "Ana"
    assert c.REMITENTE["direccion"] == "Calle Inventada 1"
    assert c.CONTRATO["numero_cliente"] == "12345"


def test_variables_no_definidas_quedan_vacias(monkeypatch):
    for campo in constantes_correos.CAMPOS_REMITENTE:
        monkeypatch.delenv(f"CORREOS_REMITENTE_{campo.upper()}", raising=False)
    c = importlib.reload(constantes_correos)

    assert set(c.REMITENTE) == set(c.CAMPOS_REMITENTE)
    assert all(v == "" for v in c.REMITENTE.values())
