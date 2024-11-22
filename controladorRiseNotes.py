from modeloRiseNotes import GestionTareas  # Importa el modelo
from vistaRiseNotes import InterfazRiseNotes  # Importa la vista
from datetime import datetime

class ControladorRiseNotes:
    def __init__(self, vista: InterfazRiseNotes, modelo: GestionTareas):
        """Inicializa el controlador"""
        self.vista = vista
        self.modelo = modelo
        self.vista.controlador = self
        self.actualizarVista()

    def actualizarVista(self):
        """Carga todas las tareas del modelo y las muestra en la vista"""
        today = datetime.now().strftime('%Y-%m-%d')
        tasks = self.modelo.getTasksByDate(today)
        print("Tareas enviadas a la vista:", tasks)
        self.vista.showTasks(tasks)

    def addTask(self, task, category, date):
        """Agrega una nueva tarea al modelo y actualiza la vista"""
        self.modelo.addTask(task, category, date)
        self.actualizarVista()

    def delete(self, task_id):
        """Elimina una tarea del modelo y actualiza la vista"""
        self.modelo.delTask(task_id)
        self.actualizarVista()

    #FUNCIÓN PARA OBTENER EL TASKID DE UNA TAREA
 
    #FUNCIÓN PARA EDITAR TAREA A TRAVÉS DEL MODELO
    def editar(self, task_id, task, category):
        """Edita una tarea existente en el modelo y actualiza la vista"""
        self.modelo.editTask(task_id, task, category)
        self.actualizarVista()

    #FUNCIÓN PARA COMPLETAR TAREA EN EL CONTROLADOR
    def completeTask(self, task_id):
        """Marca una tarea como completada y actualiza la vista"""
        self.modelo.completeTask(task_id)
        self.actualizarVista()

    #FUNCIÓN PARA OBTENER LA TAREA DE X FECHA
    def getTasksByDate(self, date):
        """Devuelve las tareas de una fecha específica"""
        return self.modelo.getTasksByDate(date)

    def filtrarTareas(self, estado):
        """Muestra solo tareas con un estado específico"""
        tasks = self.modelo.getTasksByState(estado)
        self.vista.showTasks(tasks)


