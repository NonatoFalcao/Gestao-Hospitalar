import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date, datetime
from medico import criar_tabela_medicos

criar_tabela_medicos()

conn = sqlite3.connect("Pacientes/pacientes.db")
cursor = conn.cursor()

id_paciente = None
nome_paciente = ""
cpf_paciente = ""

def paciente_ativo(cpf):
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()

    c.execute("""
        SELECT 1 FROM pacientes p
        LEFT JOIN pacientes_inativados i ON p.ID_Paciente = i.id_paciente
        WHERE p.cpf = ? AND i.id_paciente IS NULL
    """, (cpf,))

    resultado = c.fetchone()
    conexao.close()
    return resultado is not None 

def buscar_paciente():
    global id_paciente, nome_paciente, cpf_paciente

    cpf = entry_cpf.get().strip()
    cursor.execute("SELECT id_Paciente, nome_completo FROM pacientes WHERE cpf = ?", (cpf,))
    resultado = cursor.fetchone()

    if resultado:
        id_paciente, nome_paciente = resultado
        cpf_paciente = cpf
        messagebox.showinfo("Paciente encontrado", f"Nome: {nome_paciente}")
        listar_consultas()
    else:
        messagebox.showerror("Erro", "Paciente não encontrado.")

def carregar_medicos():
    cursor.execute("SELECT id, nome FROM medicos")
    medicos = cursor.fetchall()
    nomes = [f"{id_} - {nome}" for id_, nome in medicos]
    combobox_medico["values"] = nomes

def agendar_consulta():
    if not id_paciente:
        messagebox.showerror("Erro", "Busque um paciente antes de agendar.")
        return

    data = entry_data.get().strip()
    horario = entry_horario.get().strip()
    medico_info = combobox_medico.get()

    if not data or not horario or not medico_info:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    id_medico = int(medico_info.split(" - ")[0])
    cursor.execute("SELECT nome FROM medicos WHERE id = ?", (id_medico,))
    medico_nome = cursor.fetchone()[0]

    #verificar se a data escolhida é no passado
    try:
        data = datetime.strptime(data, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
        return
    
    if data < date.today():
        messagebox.showwarning("Aviso", "Preencha uma data válida")
        return

    #verificar conflito
    cursor.execute("""
        SELECT 1 FROM consultas
        WHERE medico = ? AND data_consulta = ? AND horario = ? AND status = 'Agendada'
    """, (medico_nome, data, horario))
    if cursor.fetchone():
        messagebox.showerror("Erro", "Este horário já está ocupado para este médico.")
        return

    cursor.execute("""
        INSERT INTO consultas (id_paciente, nome_paciente, cpf_paciente, medico, data_consulta, horario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_paciente, nome_paciente, cpf_paciente, medico_nome, data, horario))
    conn.commit()

    messagebox.showinfo("Sucesso", "Consulta agendada com sucesso.")
    entry_data.delete(0, END)
    entry_horario.delete(0, END)
    combobox_medico.set("")
    listar_consultas()

def listar_consultas():
    for item in tabela.get_children():
        tabela.delete(item)

    cursor.execute("""
        SELECT data_consulta, horario, medico, status
        FROM consultas
        WHERE id_paciente = ?
        ORDER BY data_consulta DESC
    """, (id_paciente,))
    for row in cursor.fetchall():
        tabela.insert("", "end", values=row)

# Janela principal
janela = Tk()
janela.title("Agendamento de Consulta")
janela.geometry("700x500")

# Frame de formulário
frame_form = LabelFrame(janela, text="Agendar Nova Consulta", padx=10, pady=10)
frame_form.pack(padx=10, pady=10, fill="x")

Label(frame_form, text="CPF do Paciente:").grid(row=0, column=0, sticky=W)
entry_cpf = Entry(frame_form)
entry_cpf.grid(row=0, column=1, padx=5)
Button(frame_form, text="Buscar", command=buscar_paciente).grid(row=0, column=2, padx=5)

Label(frame_form, text="Data (DD-MM-AAAA):").grid(row=1, column=0, sticky=W, pady=5)
entry_data = Entry(frame_form)
entry_data.grid(row=1, column=1, padx=5, pady=5)

Label(frame_form, text="Horário (HH:MM):").grid(row=2, column=0, sticky=W)
entry_horario = Entry(frame_form)
entry_horario.grid(row=2, column=1, padx=5)

Label(frame_form, text="Médico:").grid(row=3, column=0, sticky=W)
combobox_medico = ttk.Combobox(frame_form, state="readonly")
combobox_medico.grid(row=3, column=1, padx=5, pady=5)

Button(frame_form, text="Agendar Consulta", command=agendar_consulta, bg="#4CAF50", fg="white").grid(
    row=4, column=0, columnspan=3, pady=10
)

# Tabela de consultas
tabela = ttk.Treeview(janela, columns=("data", "horario", "medico", "status"), show="headings")
tabela.heading("data", text="Data")
tabela.heading("horario", text="Horário")
tabela.heading("medico", text="Médico")
tabela.heading("status", text="Status")
tabela.pack(padx=10, pady=10, fill="both", expand=True)

if __name__ == "__main__":
    carregar_medicos()
    janela.mainloop()

