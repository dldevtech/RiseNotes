from baseDatos import BaseDatos

class GestionTareas:
    def __init__(self, dbName="RiseNotes.db"):
        """Inicializa el listado de tareas personales (Diccionario) e inicialización en el modelo de la base de datos"""
        self.db = BaseDatos(dbName) #Conexión con la base de datos
        self.taskList = {} #Cache de tareas en memoria que va a ser sincronizado con la base de datos
        ##self.taskCounter = 0 #Agregamos contador de tareas para que cada una tenga una ID DESPUÉS DE AGREGAR BASE DE DATOS NO ES NECESARIO
        
        #Definicion diccionario de categorias para asignar id a cada categoria y enlazarlo a la base de datos
        self.CATEGORIAS ={
            "Mente": 1,
            "Cuerpo": 2,
            "Espíritu":3
        }
        
        self.syncDB() #Sincronización con la base de datos y el diccionario de tareas

    #FUNCION PARA SINCRONIZAR DICCIONARIO Y BASE DE DATOS
    def syncDB(self):
        """Sincroniza el diccionario con las tareas almacenadas en la base de datos"""
        query = "SELECT * FROM Tareas"
        rows = self.db.ejecutarComando(query)

        #Para obtener de forma inversa el id y transformarlo en una categoría:
        idToCategory = {v: k for k, v in self.CATEGORIAS.items()}

        self.taskList = {
            str(row[0]): {
                "task": row[3], 
                "category": idToCategory.get(row[2], "Desconocido"), 
                "date": row[4], 
                "estado": row[5]
            }

            for row in rows
        }
        print("Sincronizado taskList:", self.taskList)  # Imprime las tareas cargadas desde la base de datos


    #FUNCIÓN QUE AÑADE TAREAS A LA BASE DE DATOS
    def addTask(self, task, category, date):
        """Registra una tarea nueva en la base de datos"""
        query = """
            INSERT INTO Tareas (ID_Usuario, ID_Categoria, Descripcion, Fecha, Estado)
            VALUES (?,?,?,?,?)
        """
        categoryID = self.CATEGORIAS.get(category, None)
        if categoryID is not None:

            parametros = (1, categoryID, task, date, "pendiente")
            self.db.ejecutarComando(query, parametros)
            self.syncDB()
        else:
            print(f"Categoría inválida: {category}")

    #FUNCIÓN PARA ELIMINAR TAREA DE LA BASE DE DATOS
    def delTask(self, task_id):
        """Elimina una tarea de la Base de Datos"""
        query = "DELETE FROM Tareas WHERE ID_Tarea = ?"
        parametros = (task_id,)
        self.db.ejecutarComando(query, parametros)
        self.syncDB()

    #FUNCIÓN PARA OBTENER LISTA DE TAREAS
    def getTask(self, task_id):
        """Devuelve la lista de tareas"""
        return self.taskList.get(task_id, None)
    
    #FUNCIÓN PARA CAMBIAR EL ESTADO DE UNA TAREA COMO COMPLETADA
    def completeTask (self, task_id):
        """Marca como completada una tarea y cambia su estado en la base de datos"""
        query = "UPDATE Tareas SET Estado = 'completada' WHERE ID_Tarea = ?"
        parametros = (task_id,)
        self.db.ejecutarComando(query, parametros)
        self.syncDB()

    #FUNCIÓN PARA DEVOLVER TODAS LAS TAREAS
    def getAllTasks(self):
        """Devuelve todas las tareas"""
        print("Contenido de taskList en getAllTasks:", self.taskList) #DEPURACION!!
        return self.taskList
    
    #FUNCIÓN PARA FILTRAR TAREAS POR ESTADO
    def getTasksByState(self, estado):
        """Filtra las tareas por estado ('pendiente' o 'completada')"""
        return {task_id: task for task_id, task in self.taskList.items() if task["estado"] == estado}
    
    #FUNCIÓN PARA EDITAR TAREAS CONECTADA CON LA BASE DE DATOS
    def editTask(self, task_id, task, category):
        """Edita una tarea existente en la base de datos"""
        query = """
            UPDATE Tareas
            SET Descripcion = ?, ID_Categoria = ?
            WHERE ID_Tarea = ?
        """
        categoryID = self.CATEGORIAS.get(category, None)

        if categoryID is not None:
            parametros = (task, categoryID, task_id)
            self.db.ejecutarComando(query, parametros)
            self.syncDB()  # Sincronizar después de actualizar

    
    #Función para contar la cantidad de tareas
    #def totalNumTask(self):
        #"""Cuenta el numero total de tareas"""
        #return len(self.taskList)
    