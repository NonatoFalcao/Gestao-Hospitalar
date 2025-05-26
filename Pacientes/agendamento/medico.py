import sqlite3

def criar_tabela_medicos():
    conn = sqlite3.connect("Pacientes/pacientes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM medicos")
    if cursor.fetchone()[0] == 0:
        medicos = [("Dra. Ana Maria",), ("Dr. João Silva",), ("Dr. Pedro Henrique",)]
        cursor.executemany("INSERT INTO medicos (nome) VALUES (?)", medicos)
        conn.commit()

    conn.close()
