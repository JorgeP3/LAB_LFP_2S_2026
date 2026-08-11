def sumar():
    a = int(input("Ingrese el primer número: "))
    b = int(input("Ingrese el segundo número: "))
    print(f"La suma de {a} y {b} es: {a + b}")

def restar():
    a = int(input("Ingrese el primer número: "))
    b = int(input("Ingrese el segundo número: "))
    print(f"La resta de {a} y {b} es: {a - b}")

def main():

    while True:
        print("===== MENU =====")
        print("1. sumar")
        print("2. restar")
        print("3. salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            sumar()
        elif opcion == 2:
            restar()
        elif opcion == 3:
            print("Saliendo del programa...")
            break #palabra reservada para salir de un bucle
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()