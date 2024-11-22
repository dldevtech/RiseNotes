import sqlite3

class RiseNotesDB:
    def __init__ (self, dbName="RiseNotesDB.db"):
        """Inicialización de la conexión con la base de datos y creación de las tablas si no existen"""
        self.connection = sqlite3.connect(dbName)
        self.cursor =self.connection.cursor()
        self.crearTablasdb()

    #FUNCIÓN PARA CREAR LAS TABLAS
    def crearTablasdb (self):
        """Crea las tablas de Usuario (solo uno), Categoria y Tareas"""

        #TABLA USUARIO
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario(
                idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        """)

        #INSERTAMOS USUARIO DE TESTEO
        self.cursor.execute("""
            INSERT OR IGNORE INTO usuario (idUsuario, nombre)
                            VALUES (1, 'HarryPotter')
        """)

        #TABLA CATEGORIAS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias(
                idCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
                catNombre TEXT NOT NULL UNIQUE
            )
        """)

        #INSERTAR VALORES DE CATEGORIAS
        self.cursor.executemany("""
            INSERT OR IGNORE INTO categorias (catNombre)
            VALUES (?)
        """, [
                ("Mente",),
                ("Cuerpo",),
                ("Espíritu",)
            ]
        )
        
        #CREAR TABLA TAREAS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas(
                idTarea INTEGER PRIMARY KEY AUTOINCREMENT,
                idUsuario INTEGER NOT NULL,
                idCategoria INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                FOREIGN KEY (idUsuario) REFERENCES usuario (idUsuario),
                FOREIGN KEY (idCategoria) REFERENCES categorias (idCategoria)
            )
        """)
        self.connection.commit()

    #FUNCIÓN PARA EJECUTAR UN COMANDO GENÉRICO
    def ejecutarComando(self, query, parametros=()):
        """"Ejecuta un comando SQL genérico"""
        self.cursor.execute(query, parametros)
        self.connection.commit()
        return self.cursor.fetchall()
    
    #FUNCIÓN PARA CERRAR LA CONEXIÓN CON LA BASE DE DATOS
    def dbClose(self):
        self.connection.close()
    

class GestorTareas:
    def __init__(self):
        """Inicializa el listado de tareas como un diccionario y se conecta con la base de datos"""
        self.db = RiseNotesDB()
        self.dicTareas = {}
        self.sincroDB()

    #FUNCIÓN PARA TRAER A LA CACHÉ LOS RESULTADOS ALOJADOS EN LA BASE DE DATOS
    def sincroDB(self):
        """Sincroniza el diccionario con las tareas almacenadas en la base de datos para que sean accesibles"""
        query = "SELECT * FROM tareas"
        rows = self.db.ejecutarComando(query)
        
        queryCat = "SELECT idCategoria, catNombre FROM categorias"
        categorias = self.db.ejecutarComando(queryCat)
        catConversion = {row[0]: row [1] for row in categorias}

        self.dicTareas= {
            str(row[0]): {
                "tarea": row[3],
                "idCategoria": catConversion.get(row[2], "Desconocida"),
                "fecha": row [4],
                "estado": row [5],
            }

            for row in rows
        }
        print(f"Tareas sincronizadas con la cache: {self.dicTareas} ") #DEPURACION POR CONSOLA

    def agregarTarea (self, idCategoria, descripcion, fecha, estado="pendiente"):
        """Registra una tarea nueva en la base de datos"""
        query = """INSERT INTO tareas (idUsuario, idCategoria, descripcion, fecha, estado)
                VALUES (?, ?, ?, ?, ?)
            """
        
        parametros = (1, idCategoria, descripcion, fecha, estado)
        self.db.ejecutarComando(query, parametros)

        self.sincroDB()

    def borrarTarea(self, idTarea):
        """Elimina una tarea de la Base de Datos"""
        query= """DELETE FROM tareas WHERE idTarea = ?"""
        self.db.ejecutarComando(query, (idTarea,))
        self.sincroDB()

    