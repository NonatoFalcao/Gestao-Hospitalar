import sqlite3
import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

janela = tk.Tk()
janela.title('Cadastro Paciente')
janela. geometry("330x350")

def cadastrar_paciente():
    try:
        conexao = sqlite3.connect('Pacientes/pacientes.db')


        c = conexao.cursor()

        nome = entry_nome.get().strip()
        nascimento = entry_nascimento.get().strip()
        cpf = entry_cpf.get().strip()
        sexo = entry_sexo.get().strip()
        telefone = entry_telefone.get().strip()
        endereco = entry_endereco.get().strip()

        #validacao dos formatos e dados

        if not all([nome, nascimento, cpf, sexo, telefone, endereco]):
          messagebox.showerror("Atenção!", "Preencha todos os campos.")
          return 
        
        try:
            data_convertida = datetime.strptime(nascimento, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Erro", "A data de nascimento deve estar no formato DD/MM/AAAA")
            return
        
        if not (cpf.isdigit() and len(cpf) == 11):
            messagebox.showerror("Erro", "O CPF deve conter 11 números.")
            return

        if sexo.lower() not in['masculino', 'feminino', 'outro']:
            messagebox.showerror("Erro", "Sexo deve ser Feminino, Masculino ou Outro")
            return
        
        if not (telefone.isdigit() and len(telefone) in [10, 11]):
            messagebox.showerror("Erro", "Telefone Inválido! Use DDD + número.")
            return

        #inserção na tabela
        c.execute("INSERT INTO pacientes(" \
                    "nome_completo, data_nascimento, cpf, sexo, telefone, endereco" \
                    ") VALUES(:nome_completo, :data_nascimento, :cpf, :sexo, :telefone, :endereco)",
                  {
                      'nome_completo': nome,
                      'data_nascimento': nascimento,
                      'cpf': cpf,
                      'sexo': sexo,
                      'telefone': telefone,
                      'endereco': endereco
                  })
        

        conexao.commit()
        conexao.close()

        #limpa os campos
        entry_nome.delete(0, "end")
        entry_nascimento.delete(0, "end")
        entry_cpf.delete(0, "end")
        entry_sexo.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_endereco.delete(0, "end")

        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar paciente:\n{e}")
                             
def exporta_paciente():
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()

    c.execute("SELECT *, oid FROM pacientes")
    pacientes_cadastrados = c.fetchall()
    # print(clientes_cadastrados)
    pacientes_cadastrados = pd.DataFrame(pacientes_cadastrados, columns = ['nome_completo', 'data_nascimento', 'cpf', 'sexo', 'telefone', 'endereco', 'Id_banco'])
    pacientes_cadastrados.to_excel('Pacientes/pacientes.xlsx')
    
    conexao.commit()
    conexao.close()

label_nome = tk.Label(janela, text='Nome Completo')
label_nome.grid(row=0, column=0, padx=10, pady=10)

entry_nome = tk.Entry(janela, width=35)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_nascimento = tk.Label(janela, text='Data Nascimento')
label_nascimento.grid(row=1, column=0, padx=10, pady=10)

entry_nascimento = tk.Entry(janela, width=35)
entry_nascimento.grid(row=1, column=1, padx=10, pady=10)

label_cpf = tk.Label(janela, text='CPF')
label_cpf.grid(row=2, column=0, padx=10, pady=10)

entry_cpf = tk.Entry(janela, width=35)
entry_cpf.grid(row=2, column=1, padx=10, pady=10)

label_sexo = tk.Label(janela, text='Sexo')
label_sexo.grid(row=3, column=0, padx=10, pady=10)

entry_sexo = tk.Entry(janela, width=35)
entry_sexo.grid(row=3, column=1, padx=10, pady=10)

label_telefone = tk.Label(janela, text='Telefone')
label_telefone.grid(row=4, column=0, padx=10, pady=10)

entry_telefone = tk.Entry(janela, width=35)
entry_telefone.grid(row=4, column=1, padx=10, pady=10)

label_endereco = tk.Label(janela, text='Endereço')
label_endereco.grid(row=5, column=0, padx=10, pady=10)

entry_endereco = tk.Entry(janela, width=35)
entry_endereco.grid(row=5, column=1, padx=10, pady=10)

botao_cadastrar = tk.Button(text='Cadastrar Paciente', command=cadastrar_paciente)
botao_cadastrar.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=80)

botao_exportar = tk.Button(text='Exportar para Excel', command=exporta_paciente)
botao_exportar.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=80)



janela.mainloop()