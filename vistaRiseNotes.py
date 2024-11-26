import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import Calendar
from modeloRiseNotes import GestionTareas

class InterfazRiseNotes:
    def __init__(self, window, controlador):
        """Inicializa la interfaz gráfica""" #Usamos estas marcas de cara al documentar el propio código
        self.window = window
        self.controlador = controlador #Referencia al controlador para poder manejar los eventos
        self.window.title("RiseNotes - Gestor de Tareas")

        #"""Inicialización de la clase GestorTareas""" LO HEMOS QUITADO AL PASAR A MVC
        #self.taskManager = GestionTareas()

        #Creamos una etiqueta de bienvenida
        self.label = ttk.Label(self.window, text="Bienvenido a Rise Notes", font= ("Times New Roman", 16))
        self.label.pack(pady=10)

        # Fecha actual seleccionada
        self.selectedDate = datetime.date.today()

        # Mostrar la fecha seleccionada
        self.dateEtiqueta = ttk.Label(self.window, text=f"{self.formatDate(self.selectedDate)}", font=("Arial", 12))
        self.dateEtiqueta.pack(pady=5)

        # Botones para cambiar de día
        btnDia = ttk.Frame(self.window)
        btnDia.pack(pady=5)

        self.prevDayButton = ttk.Button(btnDia, text="←", command=self.prevDay)
        self.prevDayButton.pack(side=tk.LEFT, padx=5)

        #WIDGET DIA ESPECIFICO
        # Botón para abrir el selector de fecha
        self.selectDateButton = ttk.Button(
            btnDia, 
            text="Ir a Fecha", 
            command=self.openDateSelector
        )
        self.selectDateButton.pack(side=tk.LEFT, padx=5)

        self.nextDayButton = ttk.Button(btnDia, text="→", command=self.nextDay)
        self.nextDayButton.pack(side=tk.LEFT, padx=5)

        #Selección de categoría
        self.categoryLabel = ttk.Label(self.window, text="Seleccione una categoría:")
        self.categoryLabel.pack(pady=5)
        #Menú desplegable para seleccionar la categoría
        self.categoryVar = tk.StringVar()
        self.categoryMenu = ttk.Combobox(self.window, textvariable = self.categoryVar)
        self.categoryMenu['values'] = ("Mente", "Cuerpo", "Espíritu") #Categorías principales en RiseNotes
        self.categoryMenu.pack(pady=5)

        #Entrada para la nueva actividad
        self.taskField = ttk.Entry(self.window, width=50)
        self.taskField.pack(pady=5)
        #Funcion para que la tecla Enter registre la tarea
        self.taskField.bind("<Return>", self.enterPress)

        #botón para registrar una nueva tarea o modificar
        self.addButtom = ttk.Button(self.window, text="Agregar Tarea", command = self.addTask)
        self.addButtom.pack(pady=5)

        #Lista para mostrar las tareas agregadas
        self.taskListbox = tk.Listbox(self.window, width=50)
        self.taskListbox.pack(pady=10)

        #Etiquetas de la Barra de progreso
        #BARRA DE PROGRESO
        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Etiqueta para mostrar el porcentaje
        self.progressLabel = ttk.Label(self.window, text="Progreso Diario: 0%")
        self.progressLabel.pack(pady=5)

        #Botón para eliminar la tarea
        self.delButton = ttk.Button(self.window, text="Eliminar Tarea", command = self.delTask)
        self.delButton.pack(pady=5)

        #Botón para eliminar la tarea
        self.editButton = ttk.Button(self.window, text="Editar Tarea", command = self.editTask)
        self.editButton.pack(pady=5)

        #Botón para completar tarea
        self.completeButton = ttk.Button(self.window, text="Marcar como Completada", command=self.completeTask)
        self.completeButton.pack(pady=5)



    #FUNCIONALIDADES DE LOS ELEMENTOS VISUALES

    #FUNCIÓN PARA WIDGET DE DIA ESPECÍFICO
    def openDateSelector(self):
        """Abre una ventana emergente para seleccionar una fecha"""
        def selectDate():
            """Toma la fecha seleccionada del calendario y actualiza la fecha principal"""
            selectedDateStr = cal.get_date()  # Esto devuelve un string
            self.selectedDate = datetime.datetime.strptime(selectedDateStr, "%Y-%m-%d").date()
            self.dateEtiqueta.config(text=f"{self.formatDate(self.selectedDate)}")
            self.updateListbox()  # Actualiza la lista de tareas
            top.destroy()  # Cierra la ventana emergente

        # Crear una ventana emergente
        top = tk.Toplevel(self.window)
        top.title("Seleccionar Fecha")
        top.geometry("300x300")
        top.resizable(False, False)

        # Calendario en la ventana emergente
        cal = Calendar(
            top,
            selectmode="day",
            year=self.selectedDate.year,
            month=self.selectedDate.month,
            day=self.selectedDate.day,
            date_pattern="yyyy-MM-dd",
            locale = "es"
        )
        cal.pack(pady=20)

        # Botón para confirmar la selección de fecha
        selectButton = ttk.Button(top, text="Seleccionar", command=selectDate)
        selectButton.pack(pady=10)

    #FUNCIÓN DIA ANTERIOR PREVDAY
    def prevDay(self):
        """Retrocede un día y actualiza la vista"""
        self.selectedDate -= datetime.timedelta(days=1)
        self.dateEtiqueta.config(text=f"{self.formatDate(self.selectedDate)}")
        self.updateListbox()

    #FUNCIÓN DÍA SIGUIENTE NEXTDAY
    def nextDay(self):
        """Avanza un día y actualiza la vista"""
        self.selectedDate += datetime.timedelta(days=1)
        self.dateEtiqueta.config(text=f"{self.formatDate(self.selectedDate)}")
        self.updateListbox()
    
    #FUNCIÓN PARA ACTUALIZAR LISTBOX POR DIA
    def updateListbox(self):
        """Actualiza el Listbox con las tareas del día seleccionado"""
        tasks = self.controlador.getTasksByDate(self.selectedDate.strftime("%Y-%m-%d"))
        self.taskListbox.delete(0, tk.END)
        self.taskOfListbox = list(tasks.keys()) #Guardamos los IDs de las tareas del Listbox

        for task_id, task in tasks.items():
            estado = "[✔]" if task["estado"] == "completada" else "[ ]"
            formattedTask = f"[{task['category']}] {task['task']} {estado}"
            self.taskListbox.insert(tk.END, formattedTask)
        
        self.showTasks(tasks)
        self.updateProgressBar() #Refrescar barra progreso cada vez que actualizamos el Listbox
    
    #Función para que taskField reconozca la tecla Enter
    def enterPress(self, event):
        """Función para agregar tarea al presionar Enter en taskField"""
        self.addTask()

    #FUNCIÓN PARA OBTENER EL TASK ID DE LISTBOX
    def getSelectedTaskID (self):
        """Obtiene el ID de la tarea seleccionada en el Listbox"""
        selectedIndex = self.taskListbox.curselection()
        print(selectedIndex) #DEPURACION
        print(self.taskOfListbox)
        if selectedIndex:
            return self.taskOfListbox[selectedIndex[0]]
        
        else:
            return None

    #FUNCIÓN PARA AGREGAR UNA TAREA
    def addTask(self):
        """Función para agregar una tarea nueva"""
        task = self.taskField.get()
        category = self.categoryVar.get() #Ampliación con la categoria
        date = self.selectedDate.strftime("%Y-%m-%d")  # Fecha seleccionada

        if task and category:
            #Agregar tarea a través de controlador
            self.controlador.addTask(task, category, date)
            self.taskField.delete(0, tk.END) #Limpiar el campo de texto para añadir nueva tarea
            self.categoryVar.set("")
            self.updateListbox()  # Actualizar el Listbox con la nueva tarea
        
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar una tarea y seleccionar una categoría")

    #FUNCIÓN PARA MOSTRAR TAREAS
    def showTasks(self, tasks):
        """Actualiza la lista de tareas mostrada con formato"""
        self.taskListbox.delete(0, tk.END)

        for task_id, task in tasks.items():

            # Formatear la fecha, categoría, descripción y estado
            estado = "[✔]" if task["estado"] == "completada" else "[ ]"
            formattedTask = f"[{task['category']}] {task['task']} {estado}"

            # Insertar la tarea formateada en la lista
            self.taskListbox.insert(tk.END, formattedTask)

    #FUNCIÓN PARA ELIMINAR UNA TAREA
    def delTask(self):
        """Elimina la tarea seleccionada"""
        task_id = self.getSelectedTaskID()
        if task_id:
            self.controlador.delete(task_id)
            self.updateListbox()
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")


    #Función para editar tarea junto con opción de boton cambiante a guardar
    def editTask(self):
        """Función para editar la tarea seleccionada"""
        task_id = self.getSelectedTaskID()
        if task_id:
            task = self.controlador.modelo.getTask(task_id)

            #Insertar la tarea en el cuadro de texto para que el usuario la edite y la categoria
            self.taskField.delete(0, tk.END)
            self.taskField.insert(0, task["task"])
            self.categoryVar.set(task["category"]) #Aqui seteamos categoryVar para que coincida con lo que se seleccionó

            #Función interna para guardar los cambios
            def saveChange(event=None):
                editedTask = self.taskField.get()
                editedCategory = self.categoryVar.get()

                if editedTask and editedCategory:
                #Llamamos al controlador para actualizar la tarea
                    self.controlador.editar(task_id, editedTask, editedCategory)
                    self.addButtom.config(text="Agregar Tarea", command=self.addTask)
                    self.taskField.delete(0, tk.END)
                    self.categoryVar.set("")
                    self.updateListbox()

            #cambiar el botón "Agregar tarea" por "Guardar cambios"
            self.addButtom.config(text="Guardar cambios", command=saveChange) #ese addTask tendra que ser sustituido cuando conectemos a db
            self.taskField.bind("<Return>",saveChange)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para editar.")

    #FUNCIÓN PARA MARCAR TAREA COMPLETADA
    def completeTask(self):
        """Marca una tarea como completada"""
        task_id = self.getSelectedTaskID()
        if task_id:
            self.controlador.completeTask(task_id)
            self.updateListbox()
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para marcar como completada.")

    #FUNCIÓN BARRA DE PROGRESO
    def updateProgressBar(self):
        """Calcula y actualiza la barra de progreso diaria"""

        if not self.controlador: #Depuración para comprobar si se inicializa el controlador
            self.progress ['value'] = 0
            self.progressLabel.config(text="Progreso Diario: 0%")
            return
        
        tasks = self.controlador.getTasksByDate(self.selectedDate.strftime("%Y-%m-%d"))
    
        categories = ["Mente", "Cuerpo", "Espíritu"]
        requirementTasks = 2
        completedTask = 0

        for category in categories:
            # Contar tareas completadas en la categoría
            completed = sum(1 for task in tasks.values() if task["category"] == category and task["estado"] == "completada")
            completedTask += min(completed, requirementTasks)  # Contar hasta el máximo requerido

        totalRequirement = len(categories) * requirementTasks  # Total de tareas necesarias para 100%
        progressDiary = (completedTask / totalRequirement) * 100 if totalRequirement > 0 else 0

        # Actualizar la barra de progreso y la etiqueta
        self.progress['value'] = progressDiary
        self.progressLabel.config(text=f"Progreso Diario: {progressDiary:.0f}%")
    def formatDate (self, date):
        """Devuelve la fecha en formato 'Lunes, 30-11-2024' con el día traducido al español"""
        weekDays = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        
        weekDays = weekDays[date.strftime('%A')]  # Traduce el día de la semana
        return f"{weekDays}, {date.strftime('%d-%m-%Y')}"  # Devuelve el día traducido con la fecha
