import tkinter
from views.Interfaz import Interfaz


def main():
    # Creamos la ventana principal de la aplicacion
    ventana = tkinter.Tk()

    # Le pasamos la ventana a Interfaz para que construya adentro
    # los elementos (Text, botones, etiquetas).
    Interfaz(ventana)

    ventana.mainloop()  # mantenemos la ventana abierta hasta que el usuario la cierre


if __name__ == "__main__":
    main()
