class GestionTareas:
    def __init__(self):
        """Inicializa el listado de tareas personales (Diccionario)"""
        self.taskList = {}
        self.taskCounter = 0 #Agregamos contador de tareas para que cada una tenga una ID

    #Función que añade las distintas tareas
    def addTask(self, task, category, date):
        """Registra una tarea nueva en taskList"""
        self.taskCounter += 1
        task_id = f"tarea_{self.taskCounter}"
        self.taskList[task_id] = {
            "task": task,
            "category": category,
            "date": date,
            "estado": "pendiente"
        }
        return task_id

    #FUNCIÓN PARA ELIMINAR TAREA
    def delTask(self, task_id):
        """Elimina una tarea de la taskList"""
        if task_id in self.taskList:
            del self.taskList[task_id]

    #FUNCIÓN PARA OBTENER LISTA DE TAREAS
    def getTask(self, task_id):
        """Devuelve la lista de tareas"""
        return self.taskList.get(task_id, None)
    
    #FUNCIÓN PARA CAMBIAR EL ESTADO DE UNA TAREA COMO COMPLETADA
    def completeTask (self, task_id):
        """Marca como completada una tarea"""
        if task_id in self.taskList:
            self.taskList[task_id]["estado"] = "completada"

    #FUNCIÓN PARA DEVOLVER TODAS LAS TAREAS
    def getAllTasks(self):
        """Devuelve todas las tareas"""
        return self.taskList
    
    #FUNCIÓN PARA FILTRAR TAREAS POR ESTADO
    def getTasksByState(self, estado):
        """Filtra las tareas por estado ('pendiente' o 'completada')"""
        return {task_id: task for task_id, task in self.taskList.items() if task["estado"] == estado}
    
    #Función para contar la cantidad de tareas
    #def totalNumTask(self):
        #"""Cuenta el numero total de tareas"""
        #return len(self.taskList)
    