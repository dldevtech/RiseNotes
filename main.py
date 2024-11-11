import tkinter as tk
from modeloRiseNotes import GestionTareas
from vistaRiseNotes import InterfazRiseNotes
from controladorRiseNotes import ControladorRiseNotes

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()

    # Crear las instancias de Modelo y Vista
    modelo = GestionTareas()
    vista = InterfazRiseNotes(root, None)  # Inicialmente sin controlador

    # Crear la instancia del Controlador y vincularlo con la Vista y el Modelo
    controlador = ControladorRiseNotes(vista, modelo)

    # Ejecutar la aplicación
    root.mainloop()