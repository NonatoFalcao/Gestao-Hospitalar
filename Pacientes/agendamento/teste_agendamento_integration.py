import sqlite3
from datetime import date, timedelta
from medico import criar_tabela_medicos


def criar_tabela_pacientes():
    conn = sqlite3.connect("Pacientes/pacientes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        ID_Paciente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL
    )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM pacientes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pacientes (nome_completo, cpf) VALUES (?, ?)",
                       ("Maria Teste", "12345678900"))
        conn.commit()
    conn.close()

def criar_tabela_consultas():
    conn = sqlite3.connect("Pacientes/pacientes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER,
        nome_paciente TEXT,
        cpf_paciente TEXT,
        medico TEXT,
        data_consulta DATE,
        horario TEXT,
        status TEXT DEFAULT 'Agendada'
    )
    """)
    conn.commit()
    conn.close()

def testar_agendamento():

    criar_tabela_medicos()
    criar_tabela_pacientes()
    criar_tabela_consultas()

    conn = sqlite3.connect("Pacientes/pacientes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ID_Paciente, nome_completo, cpf FROM pacientes WHERE cpf = ?", ("67867867867",))
    paciente = cursor.fetchone()
    assert paciente is not None, "Paciente não encontrado!"
    id_paciente, nome, cpf = paciente

    cursor.execute("SELECT nome FROM medicos LIMIT 1")
    medico = cursor.fetchone()
    assert medico is not None, "Nenhum médico encontrado!"
    medico_nome = medico[0]

    data = (date.today() + timedelta(days=1)).isoformat()
    horario = "10:00"

    cursor.execute("""
        INSERT INTO consultas (id_paciente, nome_paciente, cpf_paciente, medico, data_consulta, horario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_paciente, nome, cpf, medico_nome, data, horario))
    conn.commit()

    # verifica inserção
    cursor.execute("""
        SELECT * FROM consultas
        WHERE id_paciente = ? AND medico = ? AND data_consulta = ? AND horario = ?
    """, (id_paciente, medico_nome, data, horario))
    consulta = cursor.fetchone()

    assert consulta is not None, "Consulta não foi agendada corretamente!"

    conn.close()

if __name__ == "__main__":
    testar_agendamento()
