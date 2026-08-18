class Categoria:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def imprimir(self):
        print(f"ID: {self.id}, Nombre: {self.nombre}")

    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre