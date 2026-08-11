import os
from producto import Producto

def main():
    productos = [] #lista para almacenar los productos

    while True:
        print("\n======MENU======")
        print("1. Cargar archivo")
        print("2. Mostrar productos")
        print("3. mostrar producto mas caro")
        print("4. salir")
        opcion = int(input("\nIngrese una opcion: "))

        if opcion==1:
            productos.clear() #limpiar la lista de productos antes de cargar nuevos datos

            carpeta_actual = os.path.dirname(__file__) #obtener la ruta del archivo actual
            ruta=os.path.join(carpeta_actual, "productos.txt") #unir la ruta del archivo actual con el nombre del archivo

            try:
                with open(ruta,"r") as archivo:
                    for linea in archivo:
                        linea=linea.strip() #eliminar espacios en blanco al inicio y al final de la linea
                                              #0      1        2
                        # "1,Mouse,25.50" -> ["1", "Mouse", "25.50"]
                        partes=linea.split(",") #separar la linea en partes usando la coma como separador

                        if len(partes)==3:
                            id=int(partes[0]) #convertir el primer elemento a entero
                            nombre=partes[1] #el segundo elemento es el nombre
                            precio=float(partes[2]) #convertir el tercer elemento a flotante

                            producto=Producto(id, nombre, precio) #crear un objeto Producto
                            productos.append(producto) #agregar el producto a la lista
                print("\nArchivo cargado correctamente.")
            except FileNotFoundError:
                print("No se pudo abrir el archivo.")
                
        elif opcion==2:
            if not productos:
                print("\nNo hay productos cargados.")
            else:
                for producto in productos:
                    producto.imprimir() #llamar al metodo imprimir de la clase Producto
        elif opcion==3:
            if not productos:
                print("\nNo hay productos cargados.")
            else:
                mas_caro = productos[0] #asumir que el primer producto es el mas caro

                for producto in productos:
                    if producto.get_precio() > mas_caro.get_precio(): #comparar el precio del producto actual con el mas caro
                        mas_caro = producto #actualizar el producto mas caro

                print("\nProducto más caro:")
                mas_caro.imprimir() #llamar al metodo imprimir del producto mas caro
        elif opcion==4:
            print("Saliendo del programa...")
            break
        else:
            print("Opcion invalida, intente nuevamente.")
if __name__ == "__main__":
    main()