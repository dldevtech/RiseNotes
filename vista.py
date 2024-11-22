import tkinter as tk
from tkinter import ttk, messagebox
from modelo import GestorTareas

class IGRiseNotes:
    def __init__(self, window, modelo):
        """Inicializa la interfaz gráfica"""
        self.window = window
        self.modelo = GestorTareas
        self.window.title("Rise Notes - Gestor de Tareas")

        #-----------------------------COMPOSICIÓN GRÁFICA-----------------------

        self.label = ttk.Label()