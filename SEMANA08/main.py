import tkinter
from views.interfaz import Interfaz

def main():
    #Creamos la ventana principal de la aplicacion
    ventana = tkinter.Tk()

    #llamamos a interfaz: le pasamos la ventana para que la clase interfaz
    #construya adentro los elementos (botones, texto)
    Interfaz(ventana) 

    ventana.mainloop() #mantenemos la ventana abierta hasta que el usuario la cierre

if __name__ == "__main__":
    main()