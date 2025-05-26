from datetime import datetime
import re
from tkinter import *
from tkinter import messagebox
import sqlite3


janela = Tk()
janela.title("Atualizar Dados de Paciente")
janela.geometry("450x500")


def registrar_alteracao(cpf, campo_alterado, valor_antigo, valor_novo, responsavel="admin"):
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()
    
    c.execute("""
    INSERT INTO historico_alteracoes 
    (cpf, campo_alterado, valor_antigo, valor_novo, data_alteracao, responsavel)
    VALUES (?, ?, ?, ?, datetime('now'), ?)
    """, (cpf, campo_alterado, valor_antigo, valor_novo, responsavel))
    
    conexao.commit()
    conexao.close()


def buscar_paciente():
    global paciente_original  
    
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()
    cpf = entry_busca_cpf.get().strip()

    if not cpf:
        messagebox.showwarning("Atenção", "Preencha o campo de CPF.")
        return

    c.execute("SELECT * FROM pacientes WHERE cpf = ?", (cpf,))
    resultado = c.fetchone()

    if resultado:
        paciente_original = {
            'nome': resultado[1],
            'nascimento': resultado[2],
            'cpf': resultado[3],
            'sexo': resultado[4],
            'telefone': resultado[5],
            'endereco': resultado[6],
            'email': resultado[7],
            'tipo_sanguineo': resultado[8],
            'alergias': resultado[9]
        }

        entry_nome.delete(0, END)
        entry_nome.insert(0, resultado[1])

        entry_nascimento.delete(0, END)
        entry_nascimento.insert(0, resultado[2])

        entry_cpf.delete(0, END)
        entry_cpf.insert(0, resultado[3])

        entry_sexo.delete(0, END)
        entry_sexo.insert(0, resultado[4])

        entry_telefone.delete(0, END)
        entry_telefone.insert(0, resultado[5])

        entry_endereco.delete(0, END)
        entry_endereco.insert(0, resultado[6])

        entry_email.delete(0, END)
        entry_email.insert(0, resultado[7])

        entry_sangue.delete(0, END)
        entry_sangue.insert(0, resultado[8])

        entry_alergias.delete(0, END)
        entry_alergias.insert(0, resultado[9])


        conexao.close()

    else:
        messagebox.showerror("Erro", "Paciente não encontrado.")


def atualizar_paciente():
    global paciente_original 
    
    #verifica se há um paciente carregado
    if not paciente_original:
        messagebox.showwarning("Atenção", "Busque um paciente primeiro.")
        return

    #obtém os novos valores
    novo_paciente = {
        'nome': entry_nome.get().strip(),
        'nascimento': entry_nascimento.get().strip(),
        'sexo': entry_sexo.get().strip(),
        'telefone': entry_telefone.get().strip(),
        'endereco': entry_endereco.get().strip(),
        'email': entry_email.get().strip(),
        'tipo_sanguineo': entry_sangue.get().strip(),
        'alergias': entry_alergias.get().strip()
    }

    if not novo_paciente['nome']:
        messagebox.showwarning("Validação", "Nome não pode estar vazio.")
        return False
    
    try:
        datetime.strptime(novo_paciente['nascimento'], "%d/%m/%Y")

    except ValueError:
        messagebox.showwarning("Validação", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
        return False
    
    if novo_paciente['email'] and not re.match(r"[^@]+@[^@]+\.[^@]+", novo_paciente['email']):
        messagebox.showwarning("Validação", "Email inválido.")
        return False
    
    if novo_paciente['telefone'] and not re.match(r"\d{10,11}", novo_paciente['telefone']):
        messagebox.showwarning("Validação", "Telefone deve conter 10 ou 11 dígitos numéricos.")
        return False
    

    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()

    try:
        # Primeiro registra as alterações
        for campo in novo_paciente:
            if paciente_original.get(campo) != novo_paciente.get(campo):
                registrar_alteracao(
                    cpf=paciente_original['cpf'],
                    campo_alterado=campo,
                    valor_antigo=paciente_original.get(campo, ''),
                    valor_novo=novo_paciente.get(campo, '')
                )
        c.execute("""
            UPDATE pacientes SET 
                nome_completo = ?, 
                data_nascimento = ?, 
                sexo = ?, 
                telefone = ?, 
                endereco = ?, 
                email = ?, 
                tipo_sanguineo = ?, 
                alergias = ?
            WHERE cpf = ?
        """, (
            novo_paciente['nome'],
            novo_paciente['nascimento'],
            novo_paciente['sexo'],
            novo_paciente['telefone'],
            novo_paciente['endereco'],
            novo_paciente['email'],
            novo_paciente['tipo_sanguineo'],
            novo_paciente['alergias'],
            paciente_original['cpf']
        ))

        if c.rowcount == 0:
            messagebox.showerror("Erro", "Paciente não encontrado para atualização.")
        else:
            conexao.commit()
            messagebox.showinfo("Sucesso", "Dados do paciente atualizados com sucesso!")
        paciente_original.update(novo_paciente)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar:\n{e}")

    finally:
        conexao.close()


Label(janela, text="Buscar por CPF:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
entry_busca_cpf = Entry(janela, width=15)
entry_busca_cpf.grid(row=0, column=1, padx=10, pady=5)

Button(janela, text="Buscar", command=buscar_paciente).grid(row=0, column=2, padx=5, pady=5)

Label(janela, text="Nome Completo").grid(row=1, column=0, padx=10, pady=5, sticky=W)
entry_nome = Entry(janela, width=40)
entry_nome.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Data Nascimento (DD/MM/AAAA)").grid(row=2, column=0, padx=10, pady=5, sticky=W)
entry_nascimento = Entry(janela, width=40)
entry_nascimento.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="CPF").grid(row=3, column=0, padx=10, pady=5, sticky=W)
entry_cpf = Entry(janela, width=40, state='readonly')  # CPF não pode ser alterado
entry_cpf.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Sexo").grid(row=4, column=0, padx=10, pady=5, sticky=W)
entry_sexo = Entry(janela, width=40)
entry_sexo.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Telefone").grid(row=5, column=0, padx=10, pady=5, sticky=W)
entry_telefone = Entry(janela, width=40)
entry_telefone.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Endereço").grid(row=6, column=0, padx=10, pady=5, sticky=W)
entry_endereco = Entry(janela, width=40)
entry_endereco.grid(row=6, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Email").grid(row=7, column=0, padx=10, pady=5, sticky=W)
entry_email = Entry(janela, width=40)
entry_email.grid(row=7, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Tipo Sanguíneo").grid(row=8, column=0, padx=10, pady=5, sticky=W)
entry_sangue = Entry(janela, width=40)
entry_sangue.grid(row=8, column=1, columnspan=2, padx=10, pady=5)

Label(janela, text="Alergias").grid(row=9, column=0, padx=10, pady=5, sticky=W)
entry_alergias = Entry(janela, width=40)
entry_alergias.grid(row=9, column=1, columnspan=2, padx=10, pady=5)


Button(janela, text="Atualizar Dados", command=atualizar_paciente, bg="lightblue").grid(row=10, column=0, columnspan=3, padx=10, pady=20, ipadx=100)


janela.mainloop()