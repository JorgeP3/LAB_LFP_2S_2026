from models.Token import Token
from models.Error import Error


class Analyzer():
    """
    Analizador léxico (AFD implementado a mano) para el PRIMER FRAGMENTO
    de HorarioScript: el bloque HORARIO { CURSOS { curso: "..." [codigo: "...",
    creditos: N], ... }; };

    Está basado en la estructura del analizador que Lester usó en su propio
    proyecto de 2024 (recorrido carácter a carácter, con "reentrada" al
    estado 0 cuando un lexema termina). Se adaptó para:
      1) Reconocer ENTEROS (dígitos) -> no existía en el analizador original.
      2) Clasificar las palabras reservadas por CATEGORÍA (bloque / elemento /
         atributo) en vez de un simple True/False.
      3) Vaciar el último lexema pendiente al llegar a EOF (el analizador
         original de 2024 podía perder el último token si el archivo
         terminaba justo en un símbolo, una palabra o una cadena).

    ----------------------------------------------------------------------
    Automata (nomenclatura de la herramienta usada para dibujarlo):
        L = letra          D = dígito         Q = comilla ( " )
        O = cualquier cosa EXCEPTO salto de línea (dentro de una cadena)
        C = caracter especial / símbolo ( { } [ ] : , ; )

        S0 --L--> S1(letra, self-loop L)                  [aceptación]
        S0 --D--> S2(digito, self-loop D)                  [aceptación]
        S0 --Q--> S3(dentro de cadena, self-loop O)        [NO aceptación]
        S3 --Q--> S4(cierre de cadena)                     [aceptación]
        S0 --C--> S4(símbolo)                              [aceptación]

    S4 es un estado de aceptación "compartido": se llega desde dos caminos
    distintos (cerrar una cadena, o reconocer un símbolo suelto). Por eso,
    dentro del código, en vez de fijarnos en qué estado estamos, nos fijamos
    en 'previousState' para saber CUÁL de los dos caminos se usó, y así
    decidir si el token es CADENA o SIMBOLO.
    ----------------------------------------------------------------------
    """

    # --- Palabras reservadas del lenguaje, agrupadas por categoría -------
    # (Aquí solo dejamos las que aparecen en el fragmento HORARIO/CURSOS.
    #  Cuando avancen a CATEDRATICOS, AULAS y CLASES, van a tener que
    #  agregar: catedratico, aula, clase (elemento); con, en (relación);
    #  dia, capacidad, edificio, categoria, inicio, fin, seccion (atributo);
    #  y CATEDRATICOS, AULAS, CLASES (bloque).)

    PALABRAS_BLOQUE = ["HORARIO", "CURSOS"]

    PALABRAS_ELEMENTO = ["curso"]

    PALABRAS_ATRIBUTO = ["codigo", "creditos"]

    # Símbolos válidos de un solo carácter. Nota: ';' se agregó porque el
    # fragmento de ejemplo termina en "};" y el analizador original de 2024
    # no la incluía.
    SIMBOLOS_VALIDOS = ["{", "}", "[", "]", ":", ",", ";"]

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.errors = []

    def borrarListas(self):
        self.tokens.clear()
        self.errors.clear()

    # ------------------------------------------------------------------
    # Clasifica una palabra ya acumulada (solo letras) contra las listas
    # de reservadas. Si no pertenece a ninguna, HorarioScript NO tiene
    # identificadores libres, así que se reporta como error léxico.
    # ------------------------------------------------------------------
    def clasificarPalabra(self, palabra):
        if palabra in self.PALABRAS_BLOQUE:
            return "Palabra reservada (bloque)"
        elif palabra in self.PALABRAS_ELEMENTO:
            return "Palabra reservada (elemento)"
        elif palabra in self.PALABRAS_ATRIBUTO:
            return "Palabra reservada (atributo)"
        else:
            return None  # no es ninguna reservada conocida -> error

    def isValidSymbol(self, char):
        return char in self.SIMBOLOS_VALIDOS

    # ------------------------------------------------------------------
    # state0: es el "dispatcher". Mira UN carácter y decide a qué estado
    # saltar. Se usa tanto al inicio del análisis como cada vez que un
    # token termina y hay que reprocesar el carácter que lo cortó (la
    # "reentrada" que ya usaba el analizador original).
    # ------------------------------------------------------------------
    def state0(self, char, line, column):
        if char.isalpha():
            return 1
        elif char.isdigit():
            return 2
        elif char == '"':
            return 3
        elif self.isValidSymbol(char):
            return 4
        else:
            # Espacios, tabulaciones y saltos de línea se ignoran (son
            # delimitadores silenciosos, no generan token ni error).
            if ord(char) in (10, 32, 9):
                pass
            else:
                self.errors.append(
                    Error(char, char, "CARACTER_NO_RECONOCIDO", line, column)
                )
            return 0

    # ------------------------------------------------------------------
    # Recorrido principal del AFD, carácter a carácter.
    # ------------------------------------------------------------------
    def analyze(self):
        indice = 0
        line = 1
        column = 1
        lexema = ""

        state = 0
        previousState = -1  
        self.borrarListas()

        for char in self.text:

            # ---------------- ESTADO 0: dispatcher ----------------
            if state == 0:
                state = self.state0(char, line, column)
                if state == 0: 
                    lexema = ""
                    previousState = -1
                else:
                    # 1 (letra), 2 (digito), 3 (comilla abre), 4 (simbolo)
                    lexema += char
                    previousState = 0

            # ---------------- ESTADO 1: acumulando letras (S1) ----------------
            elif state == 1:
                if char.isalpha():
                    lexema += char
                    state = 1
                else:
                    # La palabra terminó: se decide su tipo con lo acumulado.
                    tipo = self.clasificarPalabra(lexema)
                    if tipo is not None:
                        self.tokens.append(
                            Token(tipo, lexema, line, column - len(lexema), indice)
                        )
                        indice += 1
                    else:
                        self.errors.append(
                            Error(lexema, lexema, "PALABRA_NO_RECONOCIDA",
                                  line, column - len(lexema))
                        )

                    lexema = ""
                    # Reentrada: el carácter que cortó la palabra puede ser
                    # el inicio de un nuevo token (o un espacio, o un error).
                    state = self.state0(char, line, column)
                    if state == 0:
                        lexema = ""
                        previousState = -1
                    else:
                        lexema += char
                        previousState = 0

            # ---------------- ESTADO 2: acumulando dígitos (S2) ----------------
            elif state == 2:
                if char.isdigit():
                    lexema += char
                    state = 2
                else:
                    self.tokens.append(
                        Token("ENTERO", lexema, line, column - len(lexema), indice)
                    )
                    indice += 1

                    lexema = ""
                    state = self.state0(char, line, column)
                    if state == 0:
                        lexema = ""
                        previousState = -1
                    else:
                        lexema += char
                        previousState = 0

            # ---------------- ESTADO 3: dentro de una cadena (S3) ----------------
            elif state == 3:
                if char == '"':
                    # comilla de cierre -> pasamos al estado de aceptación
                    lexema += char
                    state = 4
                    previousState = 3
                elif char != "\n":
                    lexema += char
                    state = 3
                else:
                    # Llegó un salto de línea y la cadena nunca cerró.
                    self.errors.append(
                        Error(lexema, char, "CADENA_SIN_CERRAR",
                              line, column - len(lexema))
                    )
                    lexema = ""
                    state = 0

            # ---------------- ESTADO 4: aceptación (S4) ----------------
            # Se llega aquí desde dos caminos distintos:
            #   previousState == 0 -> era un SIMBOLO suelto ({ } [ ] : , ;)
            #   previousState == 3 -> se acaba de cerrar una CADENA
            elif state == 4:
                if previousState == 0:
                    self.tokens.append(
                        Token("SIMBOLO", lexema, line, column - len(lexema), indice)
                    )
                    indice += 1
                elif previousState == 3:
                    self.tokens.append(
                        Token("CADENA", lexema, line, column - len(lexema), indice)
                    )
                    indice += 1

                lexema = ""
                # Reentrada de nuevo: el carácter actual todavía no se ha
                # procesado, puede ser el inicio de otro token.
                state = self.state0(char, line, column)
                if state == 0:
                    lexema = ""
                    previousState = -1
                else:
                    lexema += char
                    previousState = 0

            # ---------------- Control de línea / columna ----------------
            # (Igual que en el analizador original: se actualiza SIEMPRE,
            # sin importar en qué estado estemos, porque es un problema
            # independiente del reconocimiento de tokens.)
            if ord(char) == 10:      # salto de línea
                line += 1
                column = 1
            elif ord(char) == 9:     # tabulación
                column += 4
            elif ord(char) == 32:    # espacio
                column += 1
            else:
                column += 1

        # ------------------------------------------------------------
        # FIN DEL ARCHIVO (EOF): si el texto termina justo en medio de
        # un token (una palabra, un número, un símbolo o una cadena),
        # ese último lexema nunca se procesa dentro del 'for' porque ya
        # no queda un carácter siguiente que dispare la reentrada.
        # Este bloque es el que el analizador de 2024 NO tenía, y por
        # eso podía "perder" el último token del archivo.
        # ------------------------------------------------------------
        if state == 1:
            tipo = self.clasificarPalabra(lexema)
            if tipo is not None:
                self.tokens.append(
                    Token(tipo, lexema, line, column - len(lexema), indice)
                )
            else:
                self.errors.append(
                    Error(lexema, lexema, "PALABRA_NO_RECONOCIDA",
                          line, column - len(lexema))
                )
        elif state == 2:
            self.tokens.append(
                Token("ENTERO", lexema, line, column - len(lexema), indice)
            )
        elif state == 3:
            # El archivo terminó y la cadena nunca se cerró.
            self.errors.append(
                Error(lexema, "EOF", "CADENA_SIN_CERRAR",
                      line, column - len(lexema))
            )
        elif state == 4:
            if previousState == 0:
                self.tokens.append(
                    Token("SIMBOLO", lexema, line, column - len(lexema), indice)
                )
            elif previousState == 3:
                self.tokens.append(
                    Token("CADENA", lexema, line, column - len(lexema), indice)
                )
