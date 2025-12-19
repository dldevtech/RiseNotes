import sqlite3 #Importamos la libreria para conectar a la base de datos

class BaseDatos:
    def __init__(self, dbName="RiseNotes.db"):
        """Inicializa la conexión a la base de datos y crea las tablas si no existen"""
        self.connection = sqlite3.connect(dbName) #Conexión a SQLite
        self.cursor = self.connection.cursor() #Variable para ejecutar los comandos SQL
        self.crearTablas() #Crear tablas al iniciar

    #FUNCIÓN PARA CREAR TABLAS
    def crearTablas (self):
        """Crea las tablas en la base de datos si no existen"""
        
        #Tabla Usuario
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT NOT NULL
            )
        """)

        #Tabla Categorias
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categorias (
                ID_Categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                catNombre TEXT NOT NULL
            )
        """)

        # Insertar categorías iniciales si no existen
        Categorias = [
            (1, "Mente"),
            (2, "Cuerpo"),
            (3, "Espiritu")
        ]
        
        self.cursor.executemany("""
            INSERT OR IGNORE INTO Categorias (ID_Categoria, catNombre) 
            VALUES (?, ?)
        """, Categorias)

        
        self.cursor.execute("""
            INSERT OR IGNORE INTO Usuarios (ID_Usuario, Nombre) 
            VALUES (1, 'UsuarioLocal')
        """)
        self.connection.commit()

        #Tabla Tareas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tareas (
                ID_Tarea INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Usuario INTEGER NOT NULL,
                ID_Categoria INTEGER NOT NULL,
                Descripcion TEXT NOT NULL,
                Fecha TEXT NOT NULL,
                Estado TEXT NOT NULL,
                FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
                FOREIGN KEY (ID_Categoria) REFERENCES Categorias (ID_Categoria)
            )
        """)
        self.connection.commit()

    #FUNCIÓN PARA EJECUTAR COMANDOS
    def ejecutarComando(self, query, parametros=()):
        """Ejecuta un comando SQL genérico"""
        self.cursor.execute(query, parametros)
        self.connection.commit()
        return self.cursor.fetchall()
    
    #FUNCIÓN PARA CERRAR LA CONEXIÓN CON LA BASE DE DATOS
    def dbClose(self):
        """Cierra la conexión con la base de datos"""
        self.connection.close()