from baseDatos import BaseDatos

class GestionTareas:
    def __init__(self, dbName="RiseNotes.db"):
        """Inicializa el listado de tareas personales (Diccionario) e inicialización en el modelo de la base de datos"""
        self.db = BaseDatos(dbName) #Conexión con la base de datos
        self.taskList = {} #Cache de tareas en memoria que va a ser sincronizado con la base de datos
        ##self.taskCounter = 0 #Agregamos contador de tareas para que cada una tenga una ID DESPUÉS DE AGREGAR BASE DE DATOS NO ES NECESARIO
        
        
        self.syncDB() #Sincronización con la base de datos y el diccionario de tareas

    #FUNCION PARA SINCRONIZAR DICCIONARIO Y BASE DE DATOS
    def syncDB(self):
        """Sincroniza el diccionario con las tareas almacenadas en la base de datos"""
        query = """SELECT Tareas.ID_Tarea, 
                        Tareas.Descripcion, 
                        Categorias.catNombre,
                        Tareas.Fecha,
                        Tareas.Estado
                        FROM Tareas JOIN Categorias 
                        WHERE Tareas.ID_Categoria = Categorias.ID_Categoria
                    """
        rows = self.db.ejecutarComando(query)



        self.taskList = {
            str(row[0]): {
                "task": row[1], 
                "category": row[2], 
                "date": row[3], 
                "estado": row[4]
            }

            for row in rows
        }

    #FUNCIÓN PARA MAPEAR IDCATEGORIA Y USARLO EN LA LOGICA
    def getCategoryID(self, catNombre):
        """Devuelve el ID de una categoría a partir de su nombre"""
        query = "SELECT ID_Categoria FROM Categorias WHERE catNombre = ?"
        result = self.db.ejecutarComando(query, (catNombre,))
        return result[0][0] if result else None

    #FUNCIÓN QUE AÑADE TAREAS A LA BASE DE DATOS
    def addTask(self, task, category, date):
        """Registra una tarea nueva en la base de datos."""
        categoryID = self.getCategoryID(category)
        if categoryID is not None:
            query = """
                INSERT INTO Tareas (ID_Usuario, ID_Categoria, Descripcion, Fecha, Estado)
                VALUES (?,?,?,?,?)
            """
            parametros = (1, categoryID, task, date, "pendiente")
            self.db.ejecutarComando(query, parametros)
            self.syncDB()
        else:
            raise ValueError(f"Categoría inválida: {category}")



    #FUNCIÓN PARA ELIMINAR TAREA DE LA BASE DE DATOS
    def delTask(self, task_id):
        """Elimina una tarea de la Base de Datos"""
        query = "DELETE FROM Tareas WHERE ID_Tarea = ?"
        self.db.ejecutarComando(query, (task_id,))
        self.syncDB()

    #FUNCIÓN PARA OBTENER LISTA DE TAREAS
    def getTask(self, task_id):
        """Devuelve la lista de tareas"""
        return self.taskList.get(task_id, None)
    
    #FUNCIÓN PARA CAMBIAR EL ESTADO DE UNA TAREA COMO COMPLETADA
    def completeTask (self, task_id):
        """Marca como completada una tarea y cambia su estado en la base de datos"""
        query = "UPDATE Tareas SET Estado = 'completada' WHERE ID_Tarea = ?"
        self.db.ejecutarComando(query, (task_id,))
        self.syncDB()

    #FUNCIÓN PARA DEVOLVER TODAS LAS TAREAS
    def getAllTasks(self):
        """Devuelve todas las tareas"""
        return self.taskList
    
    #FUNCIÓN PARA FILTRAR TAREAS POR ESTADO
    def getTasksByState(self, estado):
        """Filtra las tareas por estado ('pendiente' o 'completada')"""
        return {task_id: task for task_id, task in self.taskList.items() if task["estado"] == estado}
    
    #FUNCIÓN PARA EDITAR TAREAS CONECTADA CON LA BASE DE DATOS
    def editTask(self, task_id, task, category):
        """Edita una tarea existente en la base de datos"""
        categoryID = self.getCategoryID(category)
        if categoryID:
            query = "UPDATE Tareas SET Descripcion = ?, ID_Categoria = ? WHERE ID_Tarea = ?"
            self.db.ejecutarComando(query, (task, categoryID, task_id))
            self.syncDB()

    #FUNCIÓN PARA OBTENER TAREA DE UN DIA ESPECIFICO
    def getTasksByDate(self, date):
        """Devuelve las tareas de una fecha específica"""
        query = """SELECT Tareas.ID_Tarea, 
                        Tareas.Descripcion, 
                        Categorias.catNombre,
                        Tareas.Fecha,
                        Tareas.Estado
                        FROM Tareas JOIN Categorias 
                        WHERE Tareas.ID_Categoria = Categorias.ID_Categoria
                        AND Tareas.Fecha = ?
                    """
        rows = self.db.ejecutarComando(query, (date,))
    
    
        return {
            str(row[0]): {
                "task": row[1],
                "category": row[2],
                "date": row[3],
                "estado": row[4]
            }
            for row in rows
        }

    
    #Función para contar la cantidad de tareas
    #def totalNumTask(self):
        #"""Cuenta el numero total de tareas"""
        #return len(self.taskList)
    