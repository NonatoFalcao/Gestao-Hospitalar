import tkinter as tk
import subprocess

def abrir_consulta():
    subprocess.Popen(["python", r"Pacientes\consulta_dados\consultaDados.py"])

def abrir_cadastro():
    subprocess.Popen(["python", r"Pacientes\cadastro\cadastro_paciente.py"])

janela = tk.Tk()
janela.title('Menu')
janela.geometry("330x350")

botao_consultar = tk.Button(janela, text='Consultar Paciente', command=abrir_consulta)
botao_consultar.grid(row=0, column=0, columnspan=2, padx=100, pady=10, ipadx=10)

botao_cadastrar = tk.Button(janela, text='Cadastrar Paciente', command=abrir_cadastro)
botao_cadastrar.grid(row=1, column=0, columnspan=2, padx=100, pady=10, ipadx=10)

janela.mainloop()