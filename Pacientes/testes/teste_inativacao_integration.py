import sqlite3
import pytest
from datetime import datetime

def criar_tabela_inativados(conexao):
    c = conexao.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS pacientes_inativados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER,
        cpf TEXT,
        data_inativacao TEXT,
        motivo TEXT,
        responsavel TEXT
    )
    """)
    conexao.commit()

def test_inativar_paciente():
    conexao = sqlite3.connect(':memory:')  # banco em memória para teste rápido
    c = conexao.cursor()

    # Cria tabela pacientes e inativados
    c.execute("""
    CREATE TABLE pacientes (
        ID_Paciente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT,
        cpf TEXT UNIQUE
    )
    """)
    criar_tabela_inativados(conexao)

    # Insere paciente ativo
    c.execute("INSERT INTO pacientes (nome_completo, cpf) VALUES (?, ?)", ("Paciente Teste", "12345678900"))
    conexao.commit()

    # Recupera o ID do paciente inserido
    c.execute("SELECT ID_Paciente FROM pacientes WHERE cpf = ?", ("12345678900",))
    paciente_id = c.fetchone()[0]

    # Função simulada de inativação (insere registro na tabela inativados)
    def inativar(id_paciente, cpf, motivo, responsavel):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        c.execute("""
        INSERT INTO pacientes_inativados (id_paciente, cpf, data_inativacao, motivo, responsavel)
        VALUES (?, ?, ?, ?, ?)
        """, (id_paciente, cpf, data_atual, motivo, responsavel))
        conexao.commit()

    # Inativa paciente
    inativar(paciente_id, "12345678900", "Motivo de teste", "admin")

    # Verifica se paciente foi inativado no banco
    c.execute("SELECT * FROM pacientes_inativados WHERE id_paciente = ?", (paciente_id,))
    resultado = c.fetchone()

    assert resultado is not None
    assert resultado[1] == paciente_id
    assert resultado[2] == "12345678900"
    assert resultado[4] == "Motivo de teste"
    assert resultado[5] == "admin"

    conexao.close()
