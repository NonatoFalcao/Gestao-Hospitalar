
import sqlite3
import pandas as pd
import tkinter as tk

janela = tk.Tk()
janela.title('Cadastro Paciente')
janela. geometry("330x350")

def cadastrar_paciente():
    conexao = sqlite3.connect('Pacientes/pacientes.db')

    c = conexao.cursor()

    c.execute("INSERT INTO paciente VALUES(:nome_completo, :data_nascimento, :cpf, :sexo, :telefone, :endereco)",
              {
                  'nome_completo': tk.entry_nome.get(),
                  'data_nascimento': tk.entry_nascimento.get(),
                  'cpf': tk.entry_cpf.get(),
                  'sexo': tk.entry_sexo.get(),
                  'telefone': tk.entry_telefone.get(),
                  'endereco': tk.entry_endereco.get()
              })
    
    conexao.commit()
    conexao.close()

    tk.entry_nome_completo.delete(0, "end")
    tk.entry_data_nascimento.delete(0, "end")
    tk.entry_cpf.delete(0, "end")
    tk.entry_sexo.delete(0, "end")
    tk.entry_telefone.delete(0, "end")
    tk.entry_endereco.delete(0, "end")
def exporta_paciente():
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()

    c.execute("SELECT *, oid FROM pacientes")
    pacientes_cadastrados = c.fetchall()
    # print(clientes_cadastrados)
    pacientes_cadastrados = pd.Dataframe(pacientes_cadastrados, columns = ['nome_completo', 'data_nascimento', 'cpf', 'sexo', 'telefone', 'endereco', 'Id_banco'])
    pacientes_cadastrados.to_excel('pacientes.xlsx')
    
    conexao.commit()
    conexao.close()

label_nome = tk.Label(janela, text='Nome Completo')
label_nome.grid(row=0,column=0, padx=10, pady=10)

label_nascimento = tk.Label(janela, text='Data Nascimento')
label_nascimento.grid(row=1, column=0, padx=10, pady=10)

label_cpf = tk.Label(janela, text='CPF')
label_cpf.grid(row=2, column=0 , padx=10, pady=10)

label_sexo = tk.Label(janela, text='Sexo')
label_sexo.grid(row=3, column=0, padx=10, pady=10)

label_telefone = tk.Label(janela, text='Telefone')
label_telefone.grid(row=3, column=0, padx=10, pady=10)

label_endereco = tk.Label(janela, text='Endereço')
label_endereco.grid(row=3, column=0, padx=10, pady=10)

entry_nome = tk.Entry(janela , width =35)
entry_nome.grid(row=0,column=1, padx=10, pady=10)

entry_nascimento = tk.Entry(janela, width =35)
entry_nascimento.grid(row=1, column=1, padx=10, pady=10)

entry_cpf = tk.Entry(janela, width =35)
entry_cpf.grid(row=2, column=1 , padx=10, pady=10)

entry_sexo = tk.Entry(janela, width =35)
entry_sexo.grid(row=3, column=1, padx=10, pady=10)

entry_sexo = tk.Entry(janela, width =35)
entry_sexo.grid(row=3, column=1, padx=10, pady=10)

botao_cadastrar = tk.Button(text='Cadastrar Cliente', command=cadastrar_paciente)
botao_cadastrar.grid(row=4, column=0,columnspan=2, padx=10, pady=10 , ipadx = 80)

botao_exportar = tk.Button(text='Exportar para Excel', command=exporta_paciente)
botao_exportar.grid(row=5, column=0,columnspan=2, padx=10, pady=10 , ipadx = 80)


janela.mainloop()