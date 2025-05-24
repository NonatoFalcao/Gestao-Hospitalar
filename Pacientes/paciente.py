from tkinter import *
import sqlite3

conexao = sqlite3.connect('Pacientes/pacientes.db')

c = conexao.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        ID_Paciente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo VARCHAR(255) NOT NULL,
        data_nascimento DATE NOT NULL,
        cpf VARCHAR(11) NOT NULL,
        sexo VARCHAR(10) NOT NULL,
        telefone VARCHAR(11) NOT NULL,
        endereco VARCHAR(255) NOT NULL
    )
""")

conexao.commit()
conexao.close()

