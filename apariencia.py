import tkinter as tk
from tkinter import ttk, messagebox
from funcionalidades import GestionTareas

class InterfazRiseNotes:
    def __init__(self, window):
        """Inicializa la interfaz gráfica""" #Usamos estas marcas de cara al documentar el propio código
        self.window = window
        self.window.title("RiseNotes - Gestor de Tareas")

        """Inicialización de la clase GestorTareas"""
        self.taskManager = GestionTareas()

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
        self.delButton = ttk.Button(self.window, text="Editar Tarea", command = self.editTask)
        self.delButton.pack(pady=5)


    #A continuación añadimos las funcionalidades de los elementos
    
    #Función para que taskField reconozca la tecla Enter
    def enterPress(self, event):
        """Función para agregar tarea al presionar Enter en taskField"""
        self.addTask()

    #Función para agregar tarea
    def addTask(self):
        """Función para agregar una tarea nueva (vacía por ahora)"""
        task = self.taskField.get()
        category = self.categoryVar.get() #Ampliación con la categoria

        if task and category:
            #Agregar tarea al gestor
            self.taskManager.addTask(f"[{category}]{task}")
            #Mostrar tarea en la lista gráfica
            self.taskListbox.insert(tk.END, f"[{category}]{task}")
            #Limpiar el campo de texto para añadir nueva tarea
            self.taskField.delete(0, tk.END)
            self.categoryVar.set("")
            print(f"Tarea agregada correctamente: {task}") #De momento solo muestra por consolan NO NECESARIO
        
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar una tarea y seleccionar una categoría")

    #Función para eliminar una tarea
    def delTask(self):
        """Función para eliminar una tarea seleccionada"""
        try:
            #Obtener la tarea seleccionada
            indexTask = self.taskListbox.curselection()[0]
            selectedTask = self.taskListbox.get(indexTask)

            #Eliminar tarea de la lista interna y de la interfaz gráfica
            self.taskManager.delTask(selectedTask)
            self.taskListbox.delete(indexTask)
        except IndexError:
            print("No se ha seleccionado ninguna tarea.")


    #Función para editar tarea junto con opción de boton cambiante a guardar
    def editTask(self):
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

                #Borrar la tarea original (con categoria) del gestor y agregar la editada
                    self.taskManager.delTask(selectedTask) #borramos la tarea original
                    self.taskManager.addTask(f"[{editedCategory}] {editedTask}")

                #Actualizamos la lista visual: eliminamos la tarea original y añadimos la editada
                self.taskListbox.delete(selectedTaskIndex)
                self.taskListbox.insert(selectedTaskIndex, f"[{editedCategory}] {editedTask}")

                #Limpiamos la entrada de texto y la categoria
                self.taskField.delete(0, tk.END) #Borramos el campo de tareas
                self.categoryVar.set("") #Cuando guardamos cambios vuelve la categoryVar blanca

                #Restauramos el boton a su funcionalidad original
                self.addButtom.config(text="Agregar tarea", command=self.addTask)
                self.taskField.bind("<Return>", self.enterPress)

            #cambiar el botón "Agregar tarea" por "Guardar cambios"
            self.addButtom.config(text="Guardar cambios", command=saveChange) #ese addTask tendra que ser sustituido cuando conectemos a db
            self.taskField.bind("<Return>",saveChange)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para editar.")