class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def imprimir(self):
        print(f"ID: {self.id}, Nombre: {self.nombre}, Precio: {self.precio}")

    def get_precio(self):
        return self.precio