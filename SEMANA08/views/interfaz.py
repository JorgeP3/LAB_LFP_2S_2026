import tkinter
from tkinter import messagebox, filedialog

class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Contador de palabras y caracteres")

        self.ventana.geometry("500x450")
        self.crear_interfaz()

    def crear_interfaz(self):
        lbl_entrada = tkinter.Label(self.ventana, text="Texto a analizar:")
        # x=10 -> 10 pixeles desde el borde izquierdo
        # y=10 -> 10 pixeles desde el borde superior
        lbl_entrada.place(x=10,y=10)

        #campo de texto para ingresar el texto a analizar

        self.txt_entrada = tkinter.Text(self.ventana, width=58, height=18)
        self.txt_entrada.place(x=10,y=35)

        #Boton cargar archivo
        btn_cargar = tkinter.Button(
            self.ventana, text="Cargar archivo", command=self.cargar_archivo
            )
        btn_cargar.place(x=10,y=340)

        #boton contar
        btn_contar = tkinter.Button(
            self.ventana, text="Contar", command=self.contar
            )
        btn_contar.place(x=140,y=340)
        #boton borrar
        btn_borrar = tkinter.Button(
            self.ventana, text="Borrar", command=self.borrar
            )
        btn_borrar.place(x=220,y=340)

        #ETIQUETA DE RESULTADOS
        self.lbl_resultados = tkinter.Label(self.ventana, text="Palabras: 0 | Caracteres: 0")
        self.lbl_resultados.place(x=10,y=380)

    def cargar_archivo(self):
        ruta= filedialog.askopenfilename(
            title="Seleccionar un archivo de texto", 
            filetypes=(("Archivos de texto","*.txt"),("Todos los archivos","*.*"))
        )

        #el usuario cierra la ventana sin elegir archvio
        if not ruta:
            return

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()

            # "1.0" significa "linea 1, columna 0", es decir, el inicio del texto.
            # tkinter.END significa "hasta el final de todo el contenido".
            # Borramos primero lo que ya hubiera escrito, para no mezclarlo
            # con el contenido del archivo que se va a cargar.
            self.txt_entrada.delete("1.0", tkinter.END) #limpiar el campo de texto
            self.txt_entrada.insert(tkinter.END, contenido) #insertar el contenido del archivo en el campo de texto

        except FileNotFoundError:
            messagebox.showerror("Error", "No se pudo abrir el archivo.")

    def contar(self):


        contenido = self.txt_entrada.get("1.0", tkinter.END) #obtenemos el contenido del campo de texto
        palabras = contenido.split() #separamos el contenido en palabras
        cantidad_palabras = len(palabras) #contamos la cantidad de palabras

        cantidad_caracteres = len(contenido.strip()) #contamos la cantidad de caracteres, eliminando los espacios al inicio y al final

        self.lbl_resultados.config(text=f"Palabras: {cantidad_palabras} | Caracteres: {cantidad_caracteres}")

    def borrar(self):
        self.txt_entrada.delete("1.0", tkinter.END) #limpiar el campo de texto
        self.lbl_resultados.config(text="Palabras: 0 | Caracteres: 0") #limpiar la etiqueta de resultados