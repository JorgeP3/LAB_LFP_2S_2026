def main():
    # 1. Lista

    numeros = [1, 2, 3, 4, 5]

    print(numeros) #imprimir la lista completa
    #acceder a un elemento de la lista
    print("acceso a un elemento de la lista")
    print("Elemento en la posición 2:", numeros[2]) #acceder al elemento en la posición 2 (índice 2)

    #modificar un elemento de la lista
    numeros[2] = 10
    print("Elemento modificado en la posición 2:", numeros[2])

    print(numeros)

    # 2. Matriz (lista de listas)

    matriz = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    # acceder a un elemento
    print("\nAcceso a un elemento en matriz:")
    print("Elemento en la fila 1, columna 2:", matriz[1][2])

    # modificar un elemento
    matriz[1][2] = 20
    print("Elemento en la fila 1, columna 2 (modificado):", matriz[1][2])

    print(matriz)

    # 3. ITERACION CON FOR POR ELEMENTO

    valores = [10, 20, 30, 40, 50]
    print("\nIteración con for por elemento:")

    for valor in valores:
        print(valor)

    # 4. Metodos de listas
    numeros_lista = []
    print(numeros_lista)

    # Agregar elementos a la lista
    numeros_lista.append(5)
    numeros_lista.append(10)
    numeros_lista.append(15)

    print(numeros_lista)

    # Eliminar elementos de la lista
    numeros_lista.pop()
    numeros_lista.pop()

    print(numeros_lista)

    # 6. ESCRITURA DE ARCHIVO
    # "w" abre el archivo en modo escritura (lo crea si no existe)
    # "with" cierra el archivo automaticamente al salir del bloque,
    # incluso si ocurre un error, por eso no hace falta un close() manual.
    with open("archivo.txt", "w") as salida:
        salida.write("Hola, este es un archivo de texto.\n")
        salida.write("Escrito desde Python.\n")
    print("\nArchivo creado y escrito exitosamente.")

    # 7. LECTURA DE ARCHIVO
    # "r" abre el archivo en modo lectura (falla si el archivo no existe)
    try:
        with open("archivo.txt", "r") as entrada:
            print("\nContenido del archivo:")
            for linea in entrada:  # leer el archivo linea por linea
                print(linea.rstrip("\n"))
        print("\nArchivo leido exitosamente.")
    except FileNotFoundError:
        print("Error al abrir el archivo.")


if __name__ == "__main__":
    main()