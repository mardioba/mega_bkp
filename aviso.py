import tkinter as tk
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk

def custom_messagebox(title, message, image_path):
    # Criando uma janela Toplevel para ser o "messagebox"
    msg_box = Toplevel()
    msg_box.title(title)
    msg_box.geometry("300x200")
    
    # Desativando o redimensionamento
    msg_box.resizable(False, False)
    
    # Carregando a imagem
    image = Image.open(image_path)
    image = image.resize((50, 50))  # Ajustando o tamanho da imagem
    img = ImageTk.PhotoImage(image)
    
    # Adicionando os widgets
    img_label = Label(msg_box, image=img)
    img_label.image = img  # Para evitar que a imagem seja coletada pelo garbage collector
    img_label.pack(pady=10)
    
    message_label = Label(msg_box, text=message)
    message_label.pack(pady=10)
    
    ok_button = Button(msg_box, text="OK", command=msg_box.destroy)
    ok_button.pack(pady=10)
    
    # Manter a janela modal
    msg_box.grab_set()
    msg_box.mainloop()

# Criando a janela principal
root = tk.Tk()

# Botão para mostrar o "messagebox" personalizado
button = Button(root, text="Mostrar Mensagem", command=lambda: custom_messagebox("Alerta", "Mensagem com Imagem!", "icones/joinha.png"))
button.pack(pady=20)

root.mainloop()
