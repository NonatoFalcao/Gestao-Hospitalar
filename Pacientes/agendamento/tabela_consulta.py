import sqlite3

def criar_tabela_consultas():
    
    conn = sqlite3.connect("Pacientes/pacientes.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER NOT NULL,
        nome_paciente TEXT NOT NULL,
        cpf_paciente TEXT NOT NULL,
        medico TEXT NOT NULL,
        data_consulta TEXT NOT NULL,
        horario TEXT NOT NULL,
        status TEXT DEFAULT 'Agendada'
    )
    """)
    conn.commit()
    conn.close()

