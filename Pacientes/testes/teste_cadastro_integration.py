# testes/test_cadastro_integration.py
import sqlite3

def test_cadastro_paciente_integração():
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()
    
    # Inserção de teste
    c.execute("""
        INSERT INTO pacientes (
            nome_completo, data_nascimento, cpf, sexo, telefone, endereco, email, tipo_sanguineo, alergias
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Teste Integração", "2000-01-01", "11122233344", "Masculino",
        "91999990000", "Rua Teste, 123", "teste@email.com", "A+", "Nenhuma"
    ))
    conexao.commit()

    # Verificação
    c.execute("SELECT * FROM pacientes WHERE cpf = ?", ("11122233344",))
    resultado = c.fetchone()
    conexao.close()

    assert resultado is not None