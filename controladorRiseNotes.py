from modeloRiseNotes import GestionTareas  # Importa el modelo
from vistaRiseNotes import InterfazRiseNotes  # Importa la vista

class ControladorRiseNotes:
    def __init__(self, vista, modelo):
        """Inicializa el controlador"""
        self.vista = vista
        self.modelo = modelo
        self.vista.controlador = self
        self.actualizarVista()

    def addTask(self, task, category, date):
        """Agrega una nueva tarea al modelo y actualiza la vista"""
        self.modelo.addTask(task, category, date)
        self.actualizarVista()

    def delete(self, task_id):
        """Elimina una tarea del modelo y actualiza la vista"""
        self.modelo.delTask(task_id)
        self.actualizarVista()

    def editar(self, task_id, task, category):
        """Edita una tarea existente en el modelo y actualiza la vista"""
        if task_id in self.modelo.taskList:
            self.modelo.taskList[task_id]["task"] = task
            self.modelo.taskList[task_id]["category"] = category
            self.actualizarVista()

    #FUNCIÓN PARA COMPLETAR TAREA EN EL CONTROLADOR
    def completeTask(self, task_id):
        """Marca una tarea como completada y actualiza la vista"""
        self.modelo.completeTask(task_id)
        self.actualizarVista()

    def filtrarTareas(self, estado):
        """Muestra solo tareas con un estado específico"""
        tasks = self.modelo.getTasksByState(estado)
        self.vista.showTasks(tasks)


    def actualizarVista(self):
        """Carga todas las tareas del modelo y las muestra en la vista"""
        tasks = self.modelo.getAllTasks()
        self.vista.showTasks(tasks)