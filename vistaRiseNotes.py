import tkinter as tk
from tkinter import ttk, messagebox
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
    
    #Función para que taskField reconozca la tecla Enter
    def enterPress(self, event):
        """Función para agregar tarea al presionar Enter en taskField"""
        self.addTask()

    #Función para agregar tarea
    def addTask(self):
        """Función para agregar una tarea nueva"""
        task = self.taskField.get()
        category = self.categoryVar.get() #Ampliación con la categoria
        date = "2024-11-11" #De momento agregamos esto de forma manual hasta implementar funcionalidad

        if task and category:
            #Agregar tarea a través de controlador
            self.controlador.addTask(task, category, date)
            self.taskField.delete(0, tk.END) #Limpiar el campo de texto para añadir nueva tarea
            self.categoryVar.set("")
            print(f"Tarea agregada correctamente: {task}") #Solo muestra por consolan NO NECESARIO
        
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar una tarea y seleccionar una categoría")

    #FUNCIÓN PARA MOSTRAR TAREAS
    def showTasks(self, tasks):
        """Actualiza la lista de tareas mostrada con formato"""
        self.taskListbox.delete(0, tk.END)

        for task_id, task in tasks.items():

            # Formatear la fecha, categoría, descripción y estado
            estado = "[✔]" if task["estado"] == "completada" else "[ ]"
            formattedTask = f"{task_id}: [{task['category']}] {task['task']} {estado}"

            # Insertar la tarea formateada en la lista
            self.taskListbox.insert(tk.END, formattedTask)


    #Función para eliminar una tarea
    def delTask(self):
        """Función para eliminar una tarea seleccionada"""
        #Obtener la tarea seleccionada
        selectedIndex = self.taskListbox.curselection()

        if selectedIndex:
            selectedTask = self.taskListbox.get(selectedIndex)
            task_id = selectedTask.split(":")[0]
            self.controlador.delete(task_id)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar")



    #Función para editar tarea junto con opción de boton cambiante a guardar
    def editTask(self):
        """Función para editar la tarea seleccionada"""
        indexTask = self.taskListbox.curselection()
        if indexTask:
            selectedTaskIndex = indexTask[0]
            selectedTask = self.taskListbox.get(selectedTaskIndex)

            #Separar la categoria de la tarea
            category, task = selectedTask.split("]", 1) #Este task es el que separamos de selected Task para obtener lo que selecciona el usuario en tarea y categoria
            category = category[1:] #Quitamos el primer "]" para obtener la categoria 

            #Insertar la tarea en el cuadro de texto para que el usuario la edite y la categoria
            self.taskField.delete(0, tk.END)
            self.taskField.insert(0, task)
            self.categoryVar.set(category) #Aqui seteamos categoryVar para que coincida con lo que se seleccionó

            def saveChange(event=None):
                editedTask = self.taskField.get()
                editedCategory = self.categoryVar.get()

                if editedTask and editedCategory:
                #Llamamos al controlador para actualizar la tarea
                    self.controlador.editar(selectedTaskIndex, editedTask, editedCategory)
                    self.addButtom.config(text="Agregar Tarea", command=self.addTask)
                    self.taskField.delete(0, tk.END)
                    self.categoryVar.set("")

            #cambiar el botón "Agregar tarea" por "Guardar cambios"
            self.addButtom.config(text="Guardar cambios", command=saveChange) #ese addTask tendra que ser sustituido cuando conectemos a db
            self.taskField.bind("<Return>",saveChange)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para editar.")

    #FUNCIÓN PARA MARCAR TAREA COMPLETADA
    def completeTask(self):
        """Función para establecer una tarea como completada"""
        selected_index = self.taskListbox.curselection()
        if selected_index:
            selected_task = self.taskListbox.get(selected_index)
            task_id = selected_task.split(":")[0]
            self.controlador.completeTask(task_id)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para marcar como completada")
