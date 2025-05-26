import pytest

def valida_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def test_valida_cpf_valido():
    assert valida_cpf("12345678901")

def test_valida_cpf_invalido():
    assert not valida_cpf("123abc")
