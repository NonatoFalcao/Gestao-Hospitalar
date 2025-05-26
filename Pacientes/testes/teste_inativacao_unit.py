import pytest

def validar_motivo(motivo):
    motivo = motivo.strip()
    if not motivo:
        return False
    return True

def test_validar_motivo():
    assert validar_motivo("Motivo válido") == True
    assert validar_motivo("  ") == False
    assert validar_motivo("") == False
