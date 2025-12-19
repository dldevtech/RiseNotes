import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import Calendar

class InterfazRiseNotes:
    def __init__(self, window, controlador):
        """Inicializa la interfaz gráfica""" #Usamos estas marcas de cara al documentar el propio código
        self.window = window
        self.controlador = controlador #Referencia al controlador para poder manejar los eventos
        self.window.configure(bg="gray10")
        self.window.title("RiseNotes")

        # ESTILOS PARA MEJORAR INTERFAZ
        self.style = ttk.Style()
        self.style.theme_use("clam")

        #TLABEL
        self.style.configure("TLabel", 
                             background="gray10", 
                             foreground="#f0f0f0", 
                             font=("Arial", 12)
                             )
        
        #TBUTTON
        self.style.configure("TButton", 
                             background="gray10", 
                             foreground="deep sky blue",
                             font=("Arial", 12, "bold"), 
                             padding=5
                             )
        
        #TBUTTON ACCENT
        self.style.configure("Accent.TButton", 
                             background="#0078D7", 
                             foreground="#ffffff", 
                             font=("Arial", 10)
                             )
        
        #TBUTTON MAP
        self.style.map("TButton", 
                       background=[("active", "DeepPink2")], 
                       foreground=[("active", "deep sky blue")]
                       )
        
        #TCOMBOBOX
        self.style.configure("TCombobox", 
                             fieldbackground="#2b2b2b", 
                             foreground="#gray10", 
                             arrowcolor="#f0f0f0"
                             )
        
        #TPROGRESSBAR
        self.style.configure("TProgressbar", 
                             troughcolor="#444444", 
                             background="deep sky blue"
                             )
#========================================================================================================================
#COMPONENTES VISUALES PARA LA VENTANA

        #FRAME CREADO PARA QUE LA VENTANA NO ESTE PEGADA A LOS COMPONENTES
        self.mainFrame = tk.Frame(self.window,
                                  bg="gray10",
                                  highlightbackground="deep sky blue",
                                  highlightthickness=5,
                                  highlightcolor="deep sky blue"
                                  )        
        self.mainFrame.pack(padx=10,
                            pady=10,
                            fill="both",
                            expand=True
                            )
        
        #LABEL BIENVENIDA
        self.label = ttk.Label(self.mainFrame, 
                               text="Bienvenido a Rise Notes", 
                               style="TLabel"
                               )
        self.label.pack(pady=10)

        #FECHA TODAY PREDETERMINADA
        self.selectedDate = datetime.date.today()

        #LABEL FECHA SELECCIONADA
        self.dateEtiqueta = ttk.Label(self.mainFrame, 
                                      text=f"{self.formatDate(self.selectedDate)}",
                                      style="TLabel"
                                      )
        self.dateEtiqueta.pack(pady=5)

        #MARCO PARA BOTONES NAVEGACIÓN DÍA
        btnDia = ttk.Frame(self.mainFrame, 
                           style="TButton",
                           relief="flat"
                           )        
        btnDia.pack(pady=5)

        #BOTON DÍA ANTERIOR
        self.prevDayButton = ttk.Button(btnDia, 
                                        text="←",  
                                        style="TButton", 
                                        command=self.prevDay,
                                        )
        self.prevDayButton.pack(side=tk.LEFT, padx=10)

        #WIDGET DIA ESPECIFICO
        #BOTON IR A FECHA
        self.selectDateButton = ttk.Button(
            btnDia,  
            style="TButton",
            text="Ir a Fecha", 
            command=self.openDateSelector
        )
        self.selectDateButton.pack(side=tk.LEFT, padx=10)

        #BOTON DIA POSTERIOR
        self.nextDayButton = ttk.Button(btnDia, 
                                        text="→", 
                                        style="TButton", 
                                        command=self.nextDay
                                        )
        self.nextDayButton.pack(side=tk.LEFT, padx=10)

        #LABEL SELECCIÓN CATEGORÍA
        self.categoryLabel = ttk.Label(self.mainFrame, 
                                       text="Seleccione una categoría:", 
                                       style="TLabel"
                                       )
        self.categoryLabel.pack(pady=5)

        #COMBOBOX CATEGORIA
        self.categoryVar = tk.StringVar(value="Selecciona Categoria")
        self.categoryMenu = ttk.Combobox(self.mainFrame, 
                                         textvariable = self.categoryVar, 
                                         state="readonly", 
                                         style="TCombobox"
                                         )
        #Opciones de Categorías
        self.categoryMenu['values'] = ("Mente", 
                                       "Cuerpo", 
                                       "Espíritu"
                                       )
        self.categoryMenu.pack(pady=5)

        #LABEL PARA ENTRADA DE TEXTO
        self.entryLabel = ttk.Label(self.mainFrame, 
                                       text="Describe tu tarea:", 
                                       style="TLabel"
                                       )
        self.entryLabel.pack(pady=5)

        #ENTRY PARA ACTIVIDAD
        self.taskField = ttk.Entry(self.mainFrame,
                                   font=("San Francisco", 10)
                                   )
        self.taskField.pack(pady=5)
        #ASIGNAR ENTER EN ENTRY
        self.taskField.bind("<Return>", self.enterPress)

        #BOTÓN AGREGAR TAREA
        self.addButtom = ttk.Button(self.mainFrame, 
                                    text="Agregar Tarea", 
                                    command = self.addTask
                                    )
        self.addButtom.pack(pady=5)

        #LISTBOX QUE MUESTRA TAREAS
        self.taskListbox = tk.Listbox(self.mainFrame, 
                                      width=50, 
                                      height=10, 
                                      bg="gray13", 
                                      fg="#f0f0f0", 
                                      font=("Comic Sans MS", 12), 
                                      highlightbackground="DeepPink2", 
                                      highlightthickness=5)
        self.taskListbox.pack(pady=10, padx=10)

        #LABEL CRITERIOS PROGRESO
        self.categoryLabel = ttk.Label(self.mainFrame, 
                                       text="Completa 2 tareas de cada 'CATEGORIA' para completar", 
                                       style="TLabel"
                                       )
        self.categoryLabel.pack(pady=5)
        
        #BARRA DE PROGRESO
        self.progress = ttk.Progressbar(self.mainFrame, 
                                        orient="horizontal", 
                                        length=400, 
                                        mode="determinate", 
                                        style="TProgressbar"
                                        )
        self.progress.pack(pady=10)

        #LABEL PORCENTAJE PROGRESO
        self.progressLabel = ttk.Label(self.mainFrame, 
                                       text="Progreso Diario: 0%", 
                                       style="TLabel"
                                       )
        self.progressLabel.pack(pady=5)

        #BOTÓN ELIMINAR TAREA
        self.delButton = ttk.Button(self.mainFrame, 
                                    text="Eliminar Tarea", 
                                    style="TButton", 
                                    command = self.delTask
                                    )
        self.delButton.pack(pady=5)

        #BOTÓN EDITAR TAREA
        self.editButton = ttk.Button(self.mainFrame, 
                                     text="Editar Tarea", 
                                     style="TButton", 
                                     command = self.editTask
                                     )
        self.editButton.pack(pady=5)

        #BOTÓN COMPLETAR TAREA
        self.completeButton = ttk.Button(self.mainFrame, 
                                         text="Marcar como Completada", 
                                         style="TButton", 
                                         command=self.completeTask
                                         )
        self.completeButton.pack(pady=5)

#=======================================================================================================
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

        #VENTANA EMERGENTE
        top = tk.Toplevel(self.window)
        top.configure(bg="gray10")
        top.title("Seleccionar Fecha")
        top.geometry("300x350")
        top.resizable(False, False)
        dateFrame = tk.Frame(top,
                            bg="gray10",
                            highlightbackground="deep sky blue",
                            highlightthickness=5,
                            highlightcolor="deep sky blue"
                            )
        dateFrame.pack(fill="both", 
                       expand=True, 
                       padx=10, 
                       pady=10)   

        # Calendario en la ventana emergente
        cal = Calendar(
            dateFrame,
            selectmode="day",
            year=self.selectedDate.year,
            month=self.selectedDate.month,
            day=self.selectedDate.day,
            date_pattern="yyyy-MM-dd",
            locale = "es"
        )
        cal.pack(pady=20)

        # Botón para confirmar la selección de fecha
        selectButton = ttk.Button(dateFrame, text="Seleccionar", command=selectDate)
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

    #FUNCIÓN PARA EL RECONOCIMIENTO DE EL BOTÓN ENTER
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

    #FUNCIÓN PARA MOSTRAR TAREAS EN LISTBOX
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


    #FUNCIÓN EDITAR TAREA Y BOTÓN CAMBIANTE A GUARDAR CAMBIOS
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
    
    #FUNCIÓN PARA FORMATO EN ESPAÑOL POR INCOMPATIBILIDAD CON LOCALE
    def formatDate (self, date):
        """Devuelve la fecha en formato 'Lunes, 30-11-2024' con el día traducido al español
        para cada día de la semana"""

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
