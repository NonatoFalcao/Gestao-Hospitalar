from tkinter import *
import sqlite3

conexao = sqlite3.connect('Pacientes/pacientes.db')

c = conexao.cursor()

c.execute("""CREATE TABLE paciente(
          nome_completo VARCHAR(255),
          data_nascimento date,
          cpf VARCHAR(11),
          sexo varchar(10),
          telefone (11),
          endereco VARCHAR(255)
          )""")

conexao.commit()
conexao.close()

