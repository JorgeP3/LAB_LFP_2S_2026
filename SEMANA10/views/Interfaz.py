import tkinter
from tkinter import filedialog, messagebox
import webbrowser
import os

from controllers.Analyzer import Analyzer


class Interfaz:
    """
    Interfaz gráfica (misma estructura que el ejemplo de 'Contador de
    palabras y caracteres'): una clase Interfaz que recibe la ventana
    principal y arma los widgets, y un main.py que solo la invoca.

    Botones:
      - Cargar archivo -> igual que en el ejemplo, abre un .txt/.hor y lo
        mete al Text de entrada.
      - Analizar        -> corre el AnalizadorLexico sobre el texto y
        genera la tabla de tokens (o de errores) como un HTML aparte,
        que se abre automáticamente en el navegador.
      - Borrar          -> limpia el área de texto.
    """

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("HorarioScript - Analizador Lexico (fragmento HORARIO/CURSOS)")
        self.ventana.geometry("650x520")
        self.crear_interfaz()

    def crear_interfaz(self):
        lbl_entrada = tkinter.Label(self.ventana, text="Texto HorarioScript a analizar:")
        lbl_entrada.place(x=10, y=10)

        # Campo de texto donde el usuario puede escribir directamente
        # o donde se carga el contenido de un archivo.
        self.txt_entrada = tkinter.Text(self.ventana, width=78, height=22)
        self.txt_entrada.place(x=10, y=35)

        btn_cargar = tkinter.Button(
            self.ventana, text="Cargar archivo", command=self.cargar_archivo
        )
        btn_cargar.place(x=10, y=440)

        btn_analizar = tkinter.Button(
            self.ventana, text="Analizar", command=self.analizar
        )
        btn_analizar.place(x=140, y=440)

        btn_borrar = tkinter.Button(
            self.ventana, text="Borrar", command=self.borrar
        )
        btn_borrar.place(x=230, y=440)

        self.lbl_resultado = tkinter.Label(
            self.ventana, text="Tokens: 0 | Errores: 0"
        )
        self.lbl_resultado.place(x=10, y=475)

    # ------------------------------------------------------------------
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo HorarioScript",
            filetypes=(("Archivos .hor / .txt", "*.hor *.txt"),
                       ("Todos los archivos", "*.*"))
        )
        if not ruta:
            return

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()

            self.txt_entrada.delete("1.0", tkinter.END)
            self.txt_entrada.insert(tkinter.END, contenido)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se pudo abrir el archivo.")

    def borrar(self):
        self.txt_entrada.delete("1.0", tkinter.END)
        self.lbl_resultado.config(text="Tokens: 0 | Errores: 0")

    # ------------------------------------------------------------------
    def analizar(self):
        contenido = self.txt_entrada.get("1.0", "end-1c")  # sin el \n final que agrega Tk

        analyzer = Analyzer(contenido)
        analyzer.analyze()

        n_tokens = len(analyzer.tokens)
        n_errores = len(analyzer.errors)
        self.lbl_resultado.config(text=f"Tokens: {n_tokens} | Errores: {n_errores}")

        # Siempre generamos la tabla de tokens (aunque haya errores, para
        # que el estudiante vea qué SÍ se logró reconocer antes del error).
        ruta_tokens = self.reporte_tokens_html(analyzer.tokens)
        webbrowser.open("file://" + os.path.abspath(ruta_tokens))

        if n_errores > 0:
            ruta_errores = self.reporte_errores_html(analyzer.errors)
            webbrowser.open("file://" + os.path.abspath(ruta_errores))
            texto_error = "Error" if n_errores == 1 else "Errores"
            messagebox.showwarning(
                "Analisis con errores",
                f"El texto contiene {n_errores} {texto_error} lexico(s).\n"
                f"Revisa la tabla de errores que se abrio en el navegador."
            )

    # ------------------------------------------------------------------
    # Genera la tabla de tokens en HTML (numero, lexema, tipo, linea, columna)
    # ------------------------------------------------------------------
    def reporte_tokens_html(self, lista_tokens):
        ruta = "ReporteTokens.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n")
            f.write("<meta charset='UTF-8'>\n<title>Tabla de Tokens - HorarioScript</title>\n")
            f.write(self._estilos())
            f.write("</head>\n<body>\n<div class='container'>\n")
            f.write("<h1>Tabla de Tokens</h1>\n")
            f.write(f"<p class='subtitle'>{len(lista_tokens)} token(s) reconocido(s)</p>\n")
            f.write("<table>\n<thead><tr>")
            f.write("<th>#</th><th>Lexema</th><th>Tipo de Token</th><th>Linea</th><th>Columna</th>")
            f.write("</tr></thead>\n<tbody>\n")

            for token in lista_tokens:
                f.write("<tr>")
                f.write(f"<td class='num'>{token.indice + 1}</td>")
                f.write(f"<td class='lexema'>{self._escapar(token.value)}</td>")
                f.write(f"<td class='{self._clase_tipo(token.name)}'>{token.name}</td>")
                f.write(f"<td class='centro'>{token.line}</td>")
                f.write(f"<td class='centro'>{token.column}</td>")
                f.write("</tr>\n")

            f.write("</tbody>\n</table>\n</div>\n</body>\n</html>")
        return ruta

    # ------------------------------------------------------------------
    # Genera la tabla de errores en HTML (numero, lexema, tipo, linea, columna)
    # ------------------------------------------------------------------
    def reporte_errores_html(self, lista_errores):
        ruta = "ReporteErrores.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n")
            f.write("<meta charset='UTF-8'>\n<title>Tabla de Errores - HorarioScript</title>\n")
            f.write(self._estilos())
            f.write("</head>\n<body>\n<div class='container'>\n")
            f.write("<h1>Tabla de Errores Lexicos</h1>\n")
            f.write(f"<p class='subtitle'>{len(lista_errores)} error(es) detectado(s)</p>\n")
            f.write("<table>\n<thead><tr>")
            f.write("<th>#</th><th>Lexema</th><th>Tipo de Error</th><th>Linea</th><th>Columna</th>")
            f.write("</tr></thead>\n<tbody>\n")

            for i, error in enumerate(lista_errores, start=1):
                f.write("<tr>")
                f.write(f"<td class='num'>{i}</td>")
                f.write(f"<td class='lexema'>{self._escapar(error.lexema)}</td>")
                f.write(f"<td class='tipo-error'>{error.tipo}</td>")
                f.write(f"<td class='centro'>{error.line}</td>")
                f.write(f"<td class='centro'>{error.column}</td>")
                f.write("</tr>\n")

            f.write("</tbody>\n</table>\n</div>\n</body>\n</html>")
        return ruta

    # ------------------------------------------------------------------
    def _clase_tipo(self, nombre_tipo):
        if "bloque" in nombre_tipo:
            return "tipo-bloque"
        elif "elemento" in nombre_tipo:
            return "tipo-elemento"
        elif "atributo" in nombre_tipo:
            return "tipo-atributo"
        elif nombre_tipo == "SIMBOLO":
            return "tipo-simbolo"
        elif nombre_tipo == "CADENA":
            return "tipo-cadena"
        elif nombre_tipo == "ENTERO":
            return "tipo-entero"
        return ""

    def _escapar(self, texto):
        return (texto.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;"))

    def _estilos(self):
        return """
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; background:#f4f6f8; color:#1f2937; margin:0; padding:40px 20px; }
  .container { max-width:950px; margin:0 auto; background:#fff; border-radius:10px;
               box-shadow:0 2px 10px rgba(0,0,0,0.08); padding:30px 35px 40px; }
  h1 { font-size:22px; margin-bottom:4px; color:#111827; }
  .subtitle { margin-top:0; color:#6b7280; font-size:14px; margin-bottom:25px; }
  table { border-collapse:collapse; width:100%; font-size:14px; }
  th { background:#1f2937; color:#fff; text-align:left; padding:10px 12px; }
  td { padding:8px 12px; border-bottom:1px solid #e5e7eb; }
  tr:nth-child(even) td { background:#f9fafb; }
  .lexema { font-family:Consolas,'Courier New',monospace; color:#1e3a8a; }
  .centro { text-align:center; }
  .num { text-align:center; color:#374151; }
  .tipo-bloque { color:#7c2d12; font-weight:600; }
  .tipo-elemento { color:#92400e; font-weight:600; }
  .tipo-atributo { color:#065f46; font-weight:600; }
  .tipo-simbolo { color:#6b7280; }
  .tipo-cadena { color:#1d4ed8; }
  .tipo-entero { color:#b91c1c; }
  .tipo-error { color:#b91c1c; font-weight:600; }
</style>
"""
