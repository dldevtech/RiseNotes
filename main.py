#parte principal que va lanzar la aplicación
from apariencia import InterfazRiseNotes
import tkinter as tk #Añadimos tkinter ocn nombre mas pequeño para eficiencia en el código

#Punto de entrada de la aplicación
if __name__ == "__main__":
#Creamos una ventana raíz de Tkinter donde se va a almacenar lo diseñado en apariencia
    root = tk.Tk()

    #Creamos una instancia para la interfaz
    app = InterfazRiseNotes(root)

    #Ejecutamos el bucle principal de Tkinter
    root.mainloop()
    ###ME HE QUEDADO EN LA PARTE EN LA QUE HE AÑADIDO EL MENU DE CATEGORIA PERO QUE NO SE PUEDE EDITAR, ESE ES EL SIGUIENTE PASO
    