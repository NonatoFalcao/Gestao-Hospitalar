import tkinter as tk
from tkinter import messagebox
import subprocess

usuarios = {
    'recepcionista': {'senha': '123', 'perfil': 'recepcionista'},
    'medico': {'senha': 'abc', 'perfil': 'medico'},
    'admin': {'senha': 'admin', 'perfil': 'administrador'}
}

def abrir_menu(perfil):
    janela_menu = tk.Tk()
    janela_menu.title('Menu Principal')
    janela_menu.geometry("330x400")

    def abrir_consulta():
        subprocess.Popen(["python", r"Pacientes\consulta_dados\consultaDados.py"])

    def abrir_cadastro():
        subprocess.Popen(["python", r"Pacientes\cadastro\cadastro_paciente.py"])

    def abrir_agendamento():
        subprocess.Popen(["python", r"Pacientes\agendamento\agendamento_consulta.py"])

    def abrir_atualizacao():
        subprocess.Popen(["python", r"Pacientes\atualizar_dados\atualizaDados.py"])

    def abrir_inativacao():
        subprocess.Popen(["python", r"Pacientes\inativacao\inativa.py"])

    if perfil in ['recepcionista', 'administrador']:
        tk.Button(janela_menu, text='Cadastrar Paciente', command=abrir_cadastro).pack(pady=5, ipadx=20)
        tk.Button(janela_menu, text='Consultar Paciente', command=abrir_consulta).pack(pady=5, ipadx=20)
        tk.Button(janela_menu, text='Atualizar Paciente', command=abrir_atualizacao).pack(pady=5, ipadx=20)
        tk.Button(janela_menu, text='Agendar Consulta', command=abrir_agendamento).pack(pady=5, ipadx=20)

    if perfil == 'administrador':
        tk.Button(janela_menu, text='Inativar Paciente', command=abrir_inativacao).pack(pady=5, ipadx=20)

    if perfil == 'medico':
        tk.Button(janela_menu, text='Consultar Paciente', command=abrir_consulta).pack(pady=5, ipadx=20)

    janela_menu.mainloop()

def realizar_login():
    usuario = entry_user.get().strip()
    senha = entry_senha.get().strip()

    if usuario in usuarios and usuarios[usuario]['senha'] == senha:
        perfil = usuarios[usuario]['perfil']
        messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario} ({perfil})")
        janela_login.destroy()
        abrir_menu(perfil)
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos")

#tela de login
janela_login = tk.Tk()
janela_login.title("Login - Sistema Hospital CESUPA")
janela_login.geometry("300x200")

tk.Label(janela_login, text="Usuário:").pack(pady=5)
entry_user = tk.Entry(janela_login)
entry_user.pack()

tk.Label(janela_login, text="Senha:").pack(pady=5)
entry_senha = tk.Entry(janela_login, show="*")
entry_senha.pack()

tk.Button(janela_login, text="Entrar", command=realizar_login).pack(pady=15)

janela_login.mainloop()
