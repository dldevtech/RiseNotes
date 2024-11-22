
import tkinter as tk
from tkinter import ttk

def crearEstilos():
    """Define varios estilos para etiquetas ttk.Label"""
    style = ttk.Style()

    # Estilo 1: Básico con fondo blanco y texto negro
    style.configure("Basic.TLabel", background="white", foreground="black", font=("Arial", 12))

    # Estilo 2: Fondo azul claro y texto blanco
    style.configure("Blue.TLabel", background="#ADD8E6", foreground="white", font=("Helvetica", 14, "bold"))

    # Estilo 3: Fondo gris y texto azul
    style.configure("Gray.TLabel", background="#D3D3D3", foreground="blue", font=("Verdana", 12, "italic"))

    # Estilo 4: Fondo negro y texto amarillo
    style.configure("Dark.TLabel", background="black", foreground="yellow", font=("Courier", 12, "bold"))

    # Estilo 5: Fondo verde y texto blanco con fuente más grande
    style.configure("Green.TLabel", background="green", foreground="white", font=("Times New Roman", 16, "bold"))

    # Estilo 6: Fondo degradado (aunque ttk no soporta degradado, se puede usar un color claro)
    style.configure("Gradient.TLabel", background="#FFDDC1", foreground="#4B0082", font=("Comic Sans MS", 12))

def mostrarEstilos(root):
    """Muestra etiquetas con los distintos estilos"""
    estilos = [
        ("Basic.TLabel", "Estilo Básico"),
        ("Blue.TLabel", "Estilo Azul Claro"),
        ("Gray.TLabel", "Estilo Gris con Azul"),
        ("Dark.TLabel", "Estilo Oscuro"),
        ("Green.TLabel", "Estilo Verde"),
        ("Gradient.TLabel", "Estilo Degradado")
    ]

    for estilo, texto in estilos:
        etiqueta = ttk.Label(root, text=texto, style=estilo)
        etiqueta.pack(pady=10, padx=10, fill=tk.X)

# Crear ventana principal
root = tk.Tk()
root.title("Pruebas de Estilos para TTK.Label")
root.geometry("400x300")

# Crear y mostrar estilos
crearEstilos()
mostrarEstilos(root)

# Ejecutar la aplicación
root.mainloop()
