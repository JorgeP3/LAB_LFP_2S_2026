def sumar(a, b):
    return a + b

def circulo_area(radio):
    pi = 3.1416
    return pi * radio ** 2


def main():
    #print("Hello, World!")
    # Comentario de una sola linea

    """
    Esto es un comentario
    de varias lineas
    """

    print("--------------Fundamentos de python-----------------")

    #Tipod de datos
    print("---Tipos de datos en Python:--")
    edad = 20 #int
    poblacion = 1000000 # python no distingue entre int y long
    estatura = 1.75 #float
    promedio = 8.57885 # no distingue entre float y double
    caracter = "a" #no existe el tipo char en python, se usa str
    es_estudiante = True #tipo booleano

    print("Edad:", edad)
    print("Poblacion:", poblacion)
    print("Estatura:", estatura)
    print("Promedio:", promedio)
    print("Caracter:", caracter)
    print("Es estudiante:", es_estudiante)

    #2. Entrada y salida
    """
    print("----Entrada y salida de datos en Python:---")

    user= input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad: ")) #input () siempre devuelve un string
    print("Hola", user, "tienes", edad, "años")
    """

    #3. CONDICIONALES (IF, ELSE, ELIF)

    print("----Condicionales en Python:---")
    """
    numero = int(input("Ingrese un numero entero: "))
    
    if numero > 0:
        print("El numero es positivo")
    elif numero < 0:
        print("El numero es negativo")
    else:
        print("El numero es cero")
    """

    #pyhton no tiene no tiene switch case, se puede usar diccionarios para simularlo, o usar if, elif, else 

    #4. CICLOS (FOR, WHILE)
    print("----Ciclos en Python:---")
    """
    print("--ciclo for--")
    for i in range(1, 11):
        print("Iteracion:", i)

    print("--ciclo while--")

    n = int(input("Ingrese n: "))

    contador = 1
    while contador <= n:
        print("Iteracion:", contador)
        contador += 1
    """

    #5. FUNCIONES
    print("----Funciones en Python:---")
    """
    # Llamada a la función
    a = int(input("Ingrese el primer numero: "))
    b = int(input("Ingrese el segundo numero: "))

    resultado = sumar(a,b)

    print("La suma de", a, "y", b, "es:", resultado)
    """

    # Llamada a la función para calcular el área de un círculo
    radio = float(input("Ingrese el radio del círculo: "))
    area = circulo_area(radio)
    print("El área del círculo con radio", radio, "es:", area)


if __name__ == "__main__":
    main()