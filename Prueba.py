import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar  # Importamos el calendario
import datetime


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas por Día")

        # Fecha actual seleccionada
        self.selectedDate = datetime.date.today()

        # Diccionario simulado para almacenar tareas por día
        self.tasksByDate = {
            "2024-11-12": ["Tarea 1: Leer", "Tarea 2: Escribir"],
            "2024-11-13": ["Tarea 1: Correr", "Tarea 2: Cocinar"],
            "2024-11-14": ["Tarea 1: Pintar"]
        }

        # Etiqueta para mostrar la fecha seleccionada
        self.dateLabel = ttk.Label(self.root, text=f"Día seleccionado: {self.selectedDate}", font=("Arial", 12))
        self.dateLabel.pack(pady=5)

        # Botones de navegación para cambiar de día
        navFrame = ttk.Frame(self.root)
        navFrame.pack(pady=5)

        self.prevDayButton = ttk.Button(navFrame, text="← Día anterior", command=self.prevDay)
        self.prevDayButton.pack(side=tk.LEFT, padx=5)

        self.nextDayButton = ttk.Button(navFrame, text="Día siguiente →", command=self.nextDay)
        self.nextDayButton.pack(side=tk.LEFT, padx=5)

        # Botón para abrir el selector de fechas
        self.selectDateButton = ttk.Button(self.root, text="Seleccionar fecha...", command=self.openCalendar)
        self.selectDateButton.pack(pady=10)

        # Listbox para mostrar tareas del día seleccionado
        self.taskListbox = tk.Listbox(self.root, width=50, height=10)
        self.taskListbox.pack(pady=10)

        # Inicializar el contenido del Listbox
        self.updateListbox()

    def prevDay(self):
        """Retrocede un día y actualiza la vista"""
        self.selectedDate -= datetime.timedelta(days=1)
        self.dateLabel.config(text=f"Día seleccionado: {self.selectedDate}")
        self.updateListbox()

    def nextDay(self):
        """Avanza un día y actualiza la vista"""
        self.selectedDate += datetime.timedelta(days=1)
        self.dateLabel.config(text=f"Día seleccionado: {self.selectedDate}")
        self.updateListbox()

    def updateListbox(self):
        """Actualiza el contenido del Listbox según la fecha seleccionada"""
        # Limpiar el Listbox
        self.taskListbox.delete(0, tk.END)

        # Obtener las tareas de la fecha seleccionada
        dateStr = self.selectedDate.strftime("%Y-%m-%d")
        tasks = self.tasksByDate.get(dateStr, [])  # Obtener tareas o una lista vacía

        # Llenar el Listbox con las tareas del día
        if tasks:
            for task in tasks:
                self.taskListbox.insert(tk.END, task)
        else:
            self.taskListbox.insert(tk.END, "No hay tareas para este día")

    def openCalendar(self):
        """Abre una ventana emergente con un calendario para seleccionar una fecha"""
        calendarWindow = tk.Toplevel(self.root)
        calendarWindow.title("Seleccionar fecha")
        
        # Crear el calendario
        cal = Calendar(calendarWindow, selectmode="day", year=self.selectedDate.year,
                    month=self.selectedDate.month, day=self.selectedDate.day)
        cal.pack(pady=20)

        def setDate():
            """Establece la fecha seleccionada en el calendario"""
            selected_date = cal.get_date()
            self.selectedDate = datetime.datetime.strptime(selected_date, "%m/%d/%y").date()
            self.dateLabel.config(text=f"Día seleccionado: {self.selectedDate}")
            self.updateListbox()
            calendarWindow.destroy()  # Cerrar la ventana del calendario

        # Botón para confirmar la selección
        ttk.Button(calendarWindow, text="Seleccionar", command=setDate).pack(pady=10)

        # Botón para cerrar sin seleccionar
        ttk.Button(calendarWindow, text="Cancelar", command=calendarWindow.destroy).pack(pady=10)


# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
