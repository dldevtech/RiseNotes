class GestionTareas:
    def __init__(self):
        """Inicializa el listado de tareas personales"""
        self.taskList = []

    #Función que añade las distintas tareas
    def addTask(self, task):
        """Registra una tarea nueva en taskList"""
        self.taskList.append(task)

    #Función para eliminar una tarea de la lista 
    def delTask(self, task):
        """Elimina una tarea de la taskList"""
        self.taskList.remove(task)

    #Función para obtener la lista de tareas
    def getTask(self):
        """Devuelve la lista de tareas"""
        return self.taskList
    
    #Función para contar la cantidad de tareas
    def totalNumTask(self):
        """Cuenta el numero total de tareas"""
        return len(self.taskList)
    