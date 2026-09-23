class Token():
    """
    Representa un token reconocido por el AFD.

    name    -> tipo de token (ej: "Palabra reservada (bloque)", "ENTERO", "CADENA", "SIMBOLO")
    value   -> el lexema tal cual apareció en el texto (ej: "HORARIO", "4", "\"LFP-0796\"")
    line    -> línea donde INICIA el lexema
    column  -> columna donde INICIA el lexema
    indice  -> número consecutivo del token dentro de la tabla de tokens (para el reporte)
    """
    def __init__(self, name, value, line, column, indice):
        self.name = name
        self.value = value
        self.line = line
        self.column = column
        self.indice = indice

    def __str__(self):
        return f"Token({self.indice}, {self.value}, {self.name}, {self.line}, {self.column})"
