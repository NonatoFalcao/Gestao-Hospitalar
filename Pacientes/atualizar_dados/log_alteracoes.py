import sqlite3

con = sqlite3.connect('Pacientes/pacientes.db')
c = con.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS historico_alteracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf TEXT,
    campo_alterado TEXT,
    valor_antigo TEXT,
    valor_novo TEXT,
    data_alteracao date,
    responsavel TEXT
)
""")

con.commit()
con.close()
