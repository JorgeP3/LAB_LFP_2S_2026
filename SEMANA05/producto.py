class Producto:
    def __init__(self, id, nombre, precio, id_categoria):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.id_categoria = id_categoria

    def imprimir(self):
        print(f"ID: {self.id}, Nombre: {self.nombre}, Precio: {self.precio}, ID Categoría: {self.id_categoria}  ")

    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_precio(self):
        return self.precio
    
    def get_precio(self):
        return self.precio

    def get_id_categoria(self):
        return self.id_categoria