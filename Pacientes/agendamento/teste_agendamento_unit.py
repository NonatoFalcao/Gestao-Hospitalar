from agendamento_consulta import paciente_ativo, agendar_consulta

def test_paciente_ativo():
    assert paciente_ativo("45678901234") == True
    assert paciente_ativo("11122233344") == False

from agendamento_consulta import agendar_consulta, entry_data, entry_horario, combobox_medico, entry_cpf, buscar_paciente
import sqlite3

def test_agendar_consulta_gui():
    #simular preenchimento dos campos
    entry_cpf.insert(0, "45678901234")
    buscar_paciente()

    entry_data.insert(0, "01/06/2025")
    entry_horario.insert(0, "10:00")
    combobox_medico.set("1 - Dr. João Silva")

    #executa a função que normalmente seria chamada no botão
    agendar_consulta()

    #verificar se foi salvo no banco
    conn = sqlite3.connect("Pacientes/pacientes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM consultas 
        WHERE cpf_paciente = ? AND data_consulta = ? AND horario = ?
    """, ("45678901234", "2025-06-01", "10:00"))

    resultado = cursor.fetchone()
    conn.close()

    assert resultado is not None