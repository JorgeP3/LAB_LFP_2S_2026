
print("-------------------------------")
nombre = "Jorge"

print("Hola,",nombre, "!")
print(f"Hola, {nombre}!")

print("------------Pedir datos al usuario-------------------")

#nombre = input("Ingrese su nombre: ")
"""
Esto es un comentario
comentario de varias
lineas
"""

print("Hola,",nombre, "!")

print("------------Operaciones matematicas-------------------")

a = 10
b = 5
print("Suma:", a + b)
print("Resta:", a - b)
print("Multiplicacion:", a * b)
print("Division:", a / b)

print("------------condicional-------------------")
#edad = int(input("Ingrese su edad: "))
edad = 20
if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")

print("------------Ciclo for-------------------")

for i in range(10,0,-1):
    print(i)
