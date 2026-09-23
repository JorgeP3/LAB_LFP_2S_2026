class Error():
    """
    Representa un error léxico detectado durante el recorrido del AFD.

    lexema     -> el texto que se venía acumulando cuando se detectó el error
                  (puede ser el carácter suelto, o una cadena sin cerrar, etc.)
    errorChar  -> el carácter puntual que disparó el error
    tipo       -> tipo de error (ej: "CARACTER_NO_RECONOCIDO", "CADENA_SIN_CERRAR")
    line       -> línea donde ocurrió el error
    column     -> columna donde ocurrió el error (columna de INICIO del lexema con error)
    """
    def __init__(self, lexema, errorChar, tipo, line, column):
        self.lexema = lexema
        self.errorChar = errorChar
        self.tipo = tipo
        self.line = line
        self.column = column

    def __str__(self):
        return f"Error({self.tipo}, '{self.errorChar}', linea {self.line}, columna {self.column})"
