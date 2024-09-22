from funcoesMEGA import Put_diretorio, Login
from datetime import datetime
from tkinter import Tk, filedialog, messagebox, ttk
from tkinter import *
import tkinter as tk
import os
from tktooltip import ToolTip
import time
from PIL import Image, ImageTk
import secreto
print(secreto.email,secreto.senha)
class TELA():
    def __init__(self):
        super().__init__()
        self.janela = tk.Tk()
        self.janela.title("Escolha Arquivos/Diretórios")
        width = 500
        frm_width = self.janela.winfo_rootx() - self.janela.winfo_x()
        win_width = width + 2 * frm_width

        height = 300
        titlebar_height = self.janela.winfo_rooty() - self.janela.winfo_y()
        win_height = height + titlebar_height + frm_width
        # Obtenha a posição da janela a partir do topo dinamicamente, bem como a posição da esquerda ou direita da seguinte forma
        x = self.janela.winfo_screenwidth() // 2 - win_width // 2
        y = self.janela.winfo_screenheight() // 2 - win_height // 2

        # esta é a linha que centralizará sua janela
        self.janela.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.Tree()
        self.Componentes()
        self.janela.mainloop()
        # Init tela de Aviso
        self.root = Tk()
        self.root.title("Aplicação Principal")

        # Botão para chamar a custom_messagebox
        self.show_msg_button = Button(self.root, text="Mostrar Mensagem", command=self.show_custom_messagebox)
        self.show_msg_button.pack(pady=20)

    # Função para criar a Treeview
    def Tree(self):
        self.tree = ttk.Treeview(self.janela, columns=("Caminho"), show="headings")
        self.tree.heading("Caminho", text="Caminho")
        self.tree.place(x=10, y=10, width=480, height=180)
    # Função para adicionar arquivos
    def Componentes(self):
        ## Imagens
        self.img_del = PhotoImage(file="icones/excluir-pasta-100.png").subsample(3, 3)
        self.imgbkp = PhotoImage(file="icones/backup-100.png").subsample(3, 3)
        self.imgpastas = PhotoImage(file="icones/pastas-100.png").subsample(3, 3)
        self.delLINHA_button = tk.Button(self.janela, text="Del Linha", command=self.delLINHA)
        self.delLINHA_button.configure(image=self.img_del)
        ToolTip(self.delLINHA_button, msg="Excluir Linha")
        self.delLINHA_button.place(x=175, y=190)
        self.dir_button = tk.Button(self.janela, text="Add Dir", command=self.Escolher_Diretorio)
        ToolTip(self.dir_button, msg="Escolha um diretório")
        self.dir_button.configure(image=self.imgpastas)
        self.dir_button.place(x=230, y=190)
        self.backup_button = tk.Button(self.janela, text="Backup", command=self.Backup)
        ToolTip(self.backup_button, msg="Backup dos diretórios da Lista")
        self.backup_button.configure(image=self.imgbkp)
        self.backup_button.place(x=285, y=190)

    # Escolher os  diretórios que serão adicionados ao Backup
    def Escolher_Diretorio(self):
        home= os.path.expanduser("~")
        dir_path = filedialog.askdirectory(initialdir=home)
        if dir_path:  # Verificar se o usuário não cancelou a seleção
            # Verificar se o diretório já existe na Treeview
            if not self.is_duplicate(dir_path):
                self.tree.insert('', 'end', values=(dir_path,))
            else:
                print("Diretório já adicionado!")  # Você pode mostrar uma mensagem de alerta aqui
                messagebox.showwarning("Aviso", "Este diretório já foi adicionado.")

    # Função auxiliar para verificar duplicatas na Treeview
    def is_duplicate(self, dir_path):
        for item in self.tree.get_children():
            existing_value = self.tree.item(item, 'values')[0]  # Pega o primeiro valor (o diretório)
            if existing_value == dir_path:
                return True
        return False
    # Função auxiliar para deletar linhas da Treeview
    def delLINHA(self):
        tamanho = len(self.tree.get_children())
        if tamanho <= 0:
            messagebox.showwarning("Aviso", "Sione a linha para deletar!")
        else:
            for item in self.tree.selection():
                self.tree.delete(item)
    # Função para Backup os diretórios da Treeview
    def Backup(self):
        data = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        base_nome = f"Backup_{data}"
        if (self.Validar_tree()):
            for item in self.tree.get_children():
                diretorio=self.tree.item(item)['values']
                diretorio_filtrado=diretorio[0]
                pasta=diretorio_filtrado.split('/')
                pasta=pasta[-1]
                dir_remoto=os.path.join(base_nome, pasta)
                print("pasta:",dir_remoto)
                Login(secreto.email, secreto.senha)
                Put_diretorio(diretorio_filtrado, dir_remoto)
                # messagebox.showinfo("Backup concluído", "Backup concluído com sucesso!")
                self.lbl_aviso = tk.Label(self.janela, text=f"{diretorio_filtrado} enviado para nuvem com sucesso!!", fg="green",justify="center", background="#FFD700", font=("Arial", 10, "bold"))
                self.lbl_aviso.place(x=10, y=230, width=480)
                self.janela.after(3000, self.janela.update())
            self.show_custom_messagebox(title="Alerta", message="Backup concluído com sucesso!", image_path="icones/joinha.png")
            # time.sleep(3)
            # self.lbl_aviso.configure(text="Backup concluído com sucesso!")
            # self.janela.after(3000, self.janela.update())
        else:
            # comment: 
            messagebox.showwarning("Aviso", "Nenhum diretório foi selecionado.")
        # end if
    def Validar_tree(self):
        tamanho=len(self.tree.get_children())
        if tamanho <= 0:
            return False
        else:
            pass
            return True
    # Função para limpar a Treeview
    def Limpar_treeview(self):
        self.msg_box.destroy()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def show_custom_messagebox(self, title="Alerta", message="Mensagem com Imagem!", image_path="caminho_para_imagem.png"):
        # Criando uma janela Toplevel para o "messagebox"
        self.msg_box = Toplevel(self.janela)
        self.msg_box.overrideredirect(True)
        # 300x200
        width = 300
        frm_width = self.msg_box.winfo_rootx() - self.msg_box.winfo_x()
        win_width = width + 2 * frm_width

        height = 200
        titlebar_height = self.msg_box.winfo_rooty() - self.msg_box.winfo_y()
        win_height = height + titlebar_height + frm_width
        # Obtenha a posição da janela a partir do topo dinamicamente, bem como a posição da esquerda ou direita da seguinte forma
        x = self.msg_box.winfo_screenwidth() // 2 - win_width // 2
        y = self.msg_box.winfo_screenheight() // 2 - win_height // 2

        # esta é a linha que centralizará sua janela
        self.msg_box.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.msg_box.title(title)
        
        
        # Desativando o redimensionamento
        self.msg_box.resizable(False, False)

        # Carregando a imagem
        image = Image.open(image_path)
        image = image.resize((50, 50))  # Ajustando o tamanho da imagem
        self.img = ImageTk.PhotoImage(image)
        
        # Adicionando os widgets
        img_label = Label(self.msg_box, image=self.img)
        img_label.pack(pady=10)
        
        message_label = Label(self.msg_box, text=message, justify="center", font=("Arial", 14, "bold"),fg="green", background="#FFD700")
        message_label.pack(pady=10)
        
        ok_button = Button(self.msg_box, text="OK", command=self.Limpar_treeview)
        ok_button.pack(pady=10)

        # Manter a janela modal
        self.msg_box.grab_set()

TELA()

