import os
from producto import Producto
from categoria import Categoria

def main():
    productos = [] #lista para almacenar los productos
    categorias = [] #lista para almacenar las categorias

    carpeta_actual = os.path.dirname(__file__) #obtener la ruta del archivo actual
    ruta_productos=os.path.join(carpeta_actual, "productos.txt") #unir la ruta del archivo actual con el nombre del archivo
    ruta_categorias=os.path.join(carpeta_actual, "categorias.txt") #unir la ruta del archivo actual con el nombre del archivo
    ruta_html= os.path.join(carpeta_actual, "productos.html") #unir la ruta del archivo actual con el nombre del archivo

    #print(carpeta_actual)
    #print(ruta_productos)

    while True:
        print("\n======MENU======")
        print("1. Cargar productos")
        print("2. Cargar categorias")
        print("3. Mostrar productos")
        print("4. Mostrar productos con sucategoria")
        print("5. Mostrar productos por categoria")
        print("6. mostrar producto mas caro")
        print("7. salir")
        opcion = int(input("\nIngrese una opcion: "))

        if opcion==1:
            productos.clear() #limpiar la lista de productos antes de cargar nuevos datos

            try:
                with open(ruta_productos,"r") as archivo:
                    for linea in archivo:
                        linea=linea.strip() #eliminar espacios en blanco al inicio y al final de la linea
                                              #0      1        2
                        # "1,Mouse,25.50,idCategoria" -> ["1", "Mouse", "25.50",idCategoria]
                        partes=linea.split(",") #separar la linea en partes usando la coma como separador

                        if len(partes)==4:
                            id=int(partes[0]) #convertir el primer elemento a entero
                            nombre=partes[1] #el segundo elemento es el nombre
                            precio=float(partes[2]) #convertir el tercer elemento a flotante
                            id_categoria=int(partes[3]) #convertir el cuarto elemento a entero

                            producto=Producto(id, nombre, precio, id_categoria) #crear un objeto Producto
                            productos.append(producto) #agregar el producto a la lista
                print("\nArchivo cargado correctamente.")
            except FileNotFoundError:
                print("No se pudo abrir el archivo.")

        elif opcion==2:
            categorias.clear() #limpiar la lista de categorias antes de cargar nuevos datos

            try:
                with open(ruta_categorias,"r") as archivo:
                    for linea in archivo:
                        linea=linea.strip() #eliminar espacios en blanco al inicio y al final de la linea
                        partes=linea.split(",") #separar la linea en partes usando la coma como separador

                        if len(partes)==2:
                            id=int(partes[0]) #convertir el primer elemento a entero
                            nombre=partes[1] #el segundo elemento es el nombre

                            categoria=Categoria(id, nombre) #crear un objeto Categoria
                            categorias.append(categoria) #agregar la categoria a la lista
                print("\nArchivo cargado correctamente.")
            except FileNotFoundError:
                print("No se pudo abrir el archivo.")
                
        elif opcion==3:
            if not productos:
                print("\nNo hay productos cargados.")
            else:
                for producto in productos:
                    producto.imprimir() #llamar al metodo imprimir de la clase Producto

                with open(ruta_html, "w", encoding="utf-8") as html:
                    html.write("<!DOCTYPE html>\n")
                    html.write("<html>\n")
                    html.write("<head>\n")
                    html.write("<meta charset='UTF-8'>\n")
                    html.write("<title>Lista de Productos</title>\n")
                    html.write("<style>\n")
                    html.write("table { border-collapse: collapse; width: 60%; }\n")
                    html.write("th, td { border: 1px solid black; padding: 8px; text-align: center; }\n")
                    html.write("th { background-color: #f2f2f2; }\n")
                    html.write("</style>\n")
                    html.write("</head>\n")
                    html.write("<body>\n")

                    html.write("<h2>Lista de Productos</h2>\n")
                    html.write("<table>\n")
                    html.write("<tr><th>ID</th><th>Nombre</th><th>Precio</th></tr>\n")

                    # una fila <tr> por cada producto
                    for producto in productos:
                        html.write(
                            f"<tr><td>{producto.get_id()}</td>"
                            f"<td>{producto.get_nombre()}</td>"
                            f"<td>Q{producto.get_precio()}</td></tr>\n"
                        )

                    html.write("</table>\n")
                    html.write("</body>\n")
                    html.write("</html>\n")

                print("Archivo productos.html generado correctamente.")
        #PRODUCTOS CON SU CATEGORIA
        elif opcion==4:
            if not productos or not categorias:
                print("\nNo hay productos o categorias cargados.")
            else:
                print("\nCategorias productos con su categoria:")
            for producto in productos:
                nombre_categoria = "Desconocida" #valor por defecto si no se encuentra la categoria

                for categoria in categorias:
                    if producto.get_id_categoria() == categoria.get_id():
                        nombre_categoria = categoria.get_nombre()
                        break

                print(f"ID: {producto.get_id()}, Nombre: {producto.get_nombre()}, Precio: {producto.get_precio()}, Categoria: {nombre_categoria}")

        elif opcion==5:
            if not productos or not categorias:
                print("Debe cargar productos y categorias primero.")
            else:
                print("\n===== PRODUCTOS AGRUPADOS POR CATEGORIA =====")

                for c in categorias:
                    print(f"\nCategoria: {c.get_nombre()}")
                    print("--------------------------")

                    tiene_productos = False

                    for p in productos:
                        if p.get_id_categoria() == c.get_id():
                            print(f"- {p.get_nombre()} (Q{p.get_precio()})")
                            tiene_productos = True

                    if not tiene_productos:
                        print("No hay productos en esta categoria.")

        elif opcion==6:
            if not productos:
                print("\nNo hay productos cargados.")
            else:
                mas_caro = productos[0] #asumir que el primer producto es el mas caro

                for producto in productos:
                    if producto.get_precio() > mas_caro.get_precio(): #comparar el precio del producto actual con el mas caro
                        mas_caro = producto #actualizar el producto mas caro

                print("\nProducto más caro:")
                mas_caro.imprimir() #llamar al metodo imprimir del producto mas caro
        elif opcion==7:
            print("Saliendo del programa...")
            break
        else:
            print("Opcion invalida, intente nuevamente.")
if __name__ == "__main__":
    main()