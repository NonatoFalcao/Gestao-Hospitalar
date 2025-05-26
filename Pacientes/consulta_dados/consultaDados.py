import sqlite3
import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

janela = tk.Tk()
janela.title('Consulta dos dados ')
janela. geometry("330x350")

def consulta_dados_paciente():
    try:
        conexao = sqlite3.connect("Pacientes/pacientes.db")

        c = conexao.cursor()

        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        id_paciente = entry_id.get()

        if nome:
            c.execute("SELECT * FROM pacientes WHERE nome_completo = ?", (nome,))
        elif cpf:
            c.execute("SELECT * FROM pacientes WHERE cpf = ?", (cpf,))
        elif id_paciente:
            c.execute("SELECT * FROM pacientes WHERE ID_Paciente = ?", (id_paciente,))
        else:
            messagebox.showwarning("Erro", "Preencha pelo menos um dos campos!")
            return
        resultado = c.fetchone()

        if resultado:
            messagebox.showinfo("Resultado", f"Paciente:\n\nNome: {resultado[1]}\nNascimento: {resultado[2]}\nCPF: {resultado[3]}\
                                \nSexo: {resultado[4]}\nTelefone: {resultado[5]}\nEndereço: {resultado[6]}\nEmail: {resultado[7]}\
                                \nTipo Sanguíneo: {resultado[8]}\nAlergias Conhecidas: {resultado[9]}")
        else:
            messagebox.showwarning("Não encontrado", "Paciente não encontrado! Tente novamente.")
            return
    
        conexao.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar paciente:\n{e}")

label_nome = tk.Label(janela, text='Nome Completo')
label_nome.grid(row=0, column=0, padx=10, pady=10)

entry_nome = tk.Entry(janela, width=35)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_cpf = tk.Label(janela, text='CPF')
label_cpf.grid(row=2, column=0, padx=10, pady=10)

entry_cpf = tk.Entry(janela, width=35)
entry_cpf.grid(row=2, column=1, padx=10, pady=10)

label_id = tk.Label(janela, text='ID')
label_id.grid(row=3, column=0, padx=10, pady=10)

entry_id = tk.Entry(janela, width=35)
entry_id.grid(row=3, column=1, padx=10, pady=10)


botao_consultar = tk.Button(janela, text='Consultar Pacientes', command=consulta_dados_paciente)
botao_consultar.grid(row=4, column=0, columnspan=2, padx=10, pady=20, ipadx=80)



janela.mainloop()
    
