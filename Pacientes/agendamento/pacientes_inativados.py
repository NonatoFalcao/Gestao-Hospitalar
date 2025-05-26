import sqlite3

def criar_tabela_inativados():
    
    conn = sqlite3.connect("Pacientes/pacientes.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes_inativados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            cpf TEXT,
            data_inativacao TEXT,
            motivo TEXT,
            responsavel TEXT,
            FOREIGN KEY(id_paciente) REFERENCES pacientes(ID_Paciente)
    )
    """)
    conn.commit()
    conn.close()

criar_tabela_inativados()