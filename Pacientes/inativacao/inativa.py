import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

def criar_tabela_inativados():

    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()
    conexao.commit()
    conexao.close()

def verificar_consultas_pendentes(cpf):
    conexao = sqlite3.connect('Pacientes/pacientes.db')
    c = conexao.cursor()
    
    c.execute("""
    SELECT COUNT(*) FROM consultas 
    WHERE cpf_paciente = ? AND data_consulta > datetime('now') AND status = 'Agendada'
    """, (cpf,))
    
    count = c.fetchone()[0]
    conexao.close()
    return count > 0

def inativar_paciente():
    janela = tk.Tk()
    janela.title("Inativar Cadastro de Paciente")
    janela.geometry("500x400")
    
    #variáveis para armazenar os dados do paciente
    paciente_info = {
        'id': None,
        'cpf': None,
        'nome': None,
        'status': None
    }
    
    tk.Label(janela, text="CPF do Paciente:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_cpf = tk.Entry(janela, width=20)
    entry_cpf.grid(row=0, column=1, padx=10, pady=10)
    
    btn_buscar = tk.Button(janela, text="Buscar", command=lambda: buscar_paciente(entry_cpf.get()))
    btn_buscar.grid(row=0, column=2, padx=10, pady=10)

    frame_info = tk.LabelFrame(janela, text="Informações do Paciente")
    frame_info.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')
    
    lbl_info = tk.Label(frame_info, text="Nenhum paciente selecionado", justify='left')
    lbl_info.pack(padx=10, pady=10)
    
    tk.Label(janela, text="Motivo da Inativação:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    text_motivo = tk.Text(janela, width=40, height=5)
    text_motivo.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
    

    btn_inativar = tk.Button(janela, text="Confirmar Inativação", state='disabled',  command=lambda: confirmar_inativacao(text_motivo.get("1.0", tk.END)))
    btn_inativar.grid(row=3, column=1, pady=20)
    
    def buscar_paciente(cpf):
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            messagebox.showwarning("Aviso", "CPF inválido! Deve conter 11 dígitos.")
            return
        
        conexao = sqlite3.connect('Pacientes/pacientes.db')
        c = conexao.cursor()
        
        try:
            #verifica se o paciente existe e está ativo
            c.execute("""
            SELECT ID_Paciente, nome_completo, cpf FROM pacientes 
            WHERE cpf = ? AND ID_Paciente NOT IN (SELECT id_paciente FROM pacientes_inativados)
            """, (cpf,))
            
            resultado = c.fetchone()
            
            if resultado:
                paciente_info['id'] = resultado[0]
                paciente_info['nome'] = resultado[1]
                paciente_info['cpf'] = resultado[2]
                paciente_info['status'] = 'Ativo'
                
                #verifica consultas pendentes
                if verificar_consultas_pendentes(cpf):
                    lbl_info.config(text=f"Paciente: {resultado[1]}\nCPF: {cpf}\nStatus: Ativo\n\nATENÇÃO: Paciente tem consultas agendadas!")
                    btn_inativar.config(state='disabled')
                else:
                    lbl_info.config(text=f"Paciente: {resultado[1]}\nCPF: {cpf}\nStatus: Ativo")
                    btn_inativar.config(state='normal')
            else:
                #verifica se já está inativado
                c.execute("""
                SELECT p.nome_completo, p.cpf, i.data_inativacao 
                FROM pacientes p JOIN pacientes_inativados i ON p.ID_Paciente = i.id_paciente 
                WHERE p.cpf = ?
                """, (cpf,))
                
                resultado = c.fetchone()
                if resultado:
                    lbl_info.config(text=f"Paciente: {resultado[0]}\nCPF: {resultado[1]}\nStatus: Inativo desde {resultado[2]}")
                    paciente_info['status'] = 'Inativo'
                else:
                    messagebox.showwarning("Não encontrado", "Paciente não encontrado no sistema.")
                    lbl_info.config(text="Nenhum paciente selecionado")
                
                btn_inativar.config(state='disabled')
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar paciente:\n{e}")
        finally:
            conexao.close()
    
    def confirmar_inativacao(motivo):
        motivo = motivo.strip()
        if not motivo:
            messagebox.showwarning("Aviso", "Por favor, informe o motivo da inativação.")
            return
        
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja inativar este paciente?"):
            return
        
        conexao = sqlite3.connect('Pacientes/pacientes.db')
        c = conexao.cursor()
        
        try:
            #registra na tabela de inativados
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("""
            INSERT INTO pacientes_inativados 
            (id_paciente, cpf, data_inativacao, motivo, responsavel)
            VALUES (?, ?, ?, ?, ?)
            """, (paciente_info['id'], paciente_info['cpf'], data_atual, motivo, "admin"))  # Substituir pelo usuário logado
            
            conexao.commit()
            messagebox.showinfo("Sucesso", f"Paciente inativado com sucesso em {data_atual}")
            
            #atualiza a interface
            lbl_info.config(text=f"Paciente: {paciente_info['nome']}\nCPF: {paciente_info['cpf']}\nStatus: Inativo desde {data_atual}")
            paciente_info['status'] = 'Inativo'
            btn_inativar.config(state='disabled')
            text_motivo.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inativar paciente:\n{e}")
            conexao.rollback()
        finally:
            conexao.close()
    
    criar_tabela_inativados()
    
    janela.mainloop()

if __name__ == "__main__":
    inativar_paciente()