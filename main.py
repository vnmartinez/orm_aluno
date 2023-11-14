import tkinter as tk
from tkinter import ttk, filedialog
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from supabase_py import create_client, Client
import const
import requests 
import httpx

supabase: Client = create_client(const.SUPABASE_URL, const.SUPABASE_KEY)
Base = declarative_base()
engine = create_engine(const.DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    idade = Column(Integer)
    turma = Column(String)
    url_foto = Column(String)

def salvar_aluno():
    nome = entry_nome.get()
    idade = entry_idade.get()
    turma = entry_turma.get()
    foto_path = entry_foto.get()

    with open(foto_path, 'rb') as f:
        data = supabase.storage.from_("imagens").upload(file=f, file_options={"content-type": "image/jpeg"})

    url_foto = data['publicURL']
    
    aluno = Aluno(nome=nome, idade=idade, turma=turma, url_foto=url_foto)
    session.add(aluno)
    session.commit()

    atualizar_grid()

def selecionar_foto():
    foto_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    entry_foto.delete(0, tk.END)
    entry_foto.insert(0, foto_path)

def atualizar_grid():
    for row in tree.get_children():
        tree.delete(row)

    alunos = session.query(Aluno).all()

    for aluno in alunos:
        tree.insert('', 'end', values=(aluno.nome, aluno.idade, aluno.turma, aluno.url_foto))

root = tk.Tk()
root.title("Cadastro de Alunos")

label_nome = tk.Label(root, text="Nome:")
entry_nome = tk.Entry(root)

label_idade = tk.Label(root, text="Idade:")
entry_idade = tk.Entry(root)

label_turma = tk.Label(root, text="Turma:")
entry_turma = tk.Entry(root)

label_foto = tk.Label(root, text="Caminho da Foto:")
entry_foto = tk.Entry(root)

btn_selecionar_foto = tk.Button(root, text="Selecionar Foto", command=selecionar_foto)
btn_salvar = tk.Button(root, text="Salvar Aluno", command=salvar_aluno)

tree = ttk.Treeview(root, columns=("Nome", "Idade", "Turma", "Foto URL"))
tree.heading("#0", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Idade", text="Idade")
tree.heading("Turma", text="Turma")
tree.heading("Foto URL", text="Foto URL")

label_nome.grid(row=0, column=0)
entry_nome.grid(row=0, column=1)

label_idade.grid(row=1, column=0)
entry_idade.grid(row=1, column=1)

label_turma.grid(row=2, column=0)
entry_turma.grid(row=2, column=1)

label_foto.grid(row=3, column=0)
entry_foto.grid(row=3, column=1)
btn_selecionar_foto.grid(row=3, column=2)

btn_salvar.grid(row=4, column=0, columnspan=2)

tree.grid(row=5, column=0, columnspan=2)

atualizar_grid()

root.mainloop()
