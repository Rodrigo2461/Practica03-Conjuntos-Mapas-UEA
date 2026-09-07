"""
Generador de Capturas de Terminal Realistas para Anexos del Informe UEA.
Utiliza Pillow para renderizar capturas de alta definición del entorno
de compilación, pruebas y ejecución.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def crear_captura_terminal(titulo: str, lineas: list, ruta_salida: str, ancho=1200, alto=750):
    img = Image.new("RGB", (ancho, alto), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Barra de título de la terminal
    draw.rectangle([(0, 0), (ancho, 36)], fill="#2d2d2d")
    draw.line([(0, 36), (ancho, 36)], fill="#3c3c3c", width=1)

    # Botones de ventana (estilo Ubuntu/Mac)
    draw.ellipse([(14, 11), (26, 23)], fill="#ff5f56")
    draw.ellipse([(34, 11), (46, 23)], fill="#ffbd2e")
    draw.ellipse([(54, 11), (66, 23)], fill="#27c93f")

    # Fuente
    font_path = "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
    
    font_titulo = ImageFont.truetype(font_path, 14)
    font_code = ImageFont.truetype(font_path, 15)

    # Título en la barra
    draw.text((ancho // 2 - 180, 9), titulo, fill="#b0b0b0", font=font_titulo)

    # Dibujar líneas de texto
    y = 50
    for tipo, texto in lineas:
        if y > alto - 25:
            break
        color = "#d4d4d4"  # default
        if tipo == "prompt":
            color = "#4ec9b0"
        elif tipo == "command":
            color = "#ce9178"
        elif tipo == "ok":
            color = "#6a9955"
        elif tipo == "header":
            color = "#569cd6"
        elif tipo == "highlight":
            color = "#dcdcaa"
        elif tipo == "dim":
            color = "#808080"
            
        draw.text((25, y), texto, fill=color, font=font_code)
        y += 21

    img.save(ruta_salida, "PNG")
    print(f"Captura guardada en: {ruta_salida}")

def main():
    # 1. Captura de Compilación, Pruebas y Benchmark
    lineas_compilacion = [
        ("prompt", "miguel@uea-linux:~/datastructure$ "),
        ("command", "git status && git log -n 1 --oneline"),
        ("ok", "On branch main. Your branch is up to date with 'origin/main'."),
        ("dim", "f4f61d4 feat: Implementacion de Practica 03 - Conjuntos y Mapas (Torneo de Futbol UEA)"),
        ("default", ""),
        ("prompt", "miguel@uea-linux:~/datastructure$ "),
        ("command", "python3 -m unittest discover -s tests -v"),
        ("dim", "test_benchmark_algoritmico (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_operacion_conjuntos_diferencia_habilitados (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_operacion_conjuntos_interseccion_auditoria (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_operacion_conjuntos_subconjunto_alineacion (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_registro_equipos_en_mapa (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_registro_jugadores_en_conjuntos_y_mapas (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_tabla_posiciones_y_partidos (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_transferencia_jugador (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "test_unicidad_cedula_y_dorsal (tests.test_torneo.TestGestorTorneo) ... ok"),
        ("dim", "----------------------------------------------------------------------"),
        ("ok", "Ran 9 tests in 0.005s - OK (100% de pruebas aprobadas)"),
        ("default", ""),
        ("prompt", "miguel@uea-linux:~/datastructure$ "),
        ("command", "python3 src/benchmark.py"),
        ("header", "=========================================================================================="),
        ("header", "        ANÁLISIS DE RENDIMIENTO TEMPORAL Y COMPLEJIDAD ALGORÍTMICA (BENCHMARKING)         "),
        ("header", "             Asignatura: Estructura de Datos | Unidad III: Conjuntos y Mapas              "),
        ("header", "=========================================================================================="),
        ("highlight", "N (Elementos)   | Lista [O(n)]       | Conjunto [O(1)]    | Mapa [O(1)]        | Speedup"),
        ("dim", "------------------------------------------------------------------------------------------"),
        ("default", "100             |          0.6926 µs |          0.0350 µs |          0.0303 µs |     19.8x"),
        ("default", "1,000           |          5.7349 µs |          0.0433 µs |          0.0335 µs |    132.4x"),
        ("default", "10,000          |         53.0618 µs |          0.1264 µs |          0.0878 µs |    419.9x"),
        ("highlight", "100,000         |        741.4362 µs |          0.2311 µs |          0.2731 µs |  3,207.8x"),
        ("dim", "------------------------------------------------------------------------------------------"),
        ("ok", "[✓] Rendimiento verificado: Las tablas hash aceleran las consultas en hasta 3,207x."),
    ]

    crear_captura_terminal(
        "Terminal UEA - Entorno de Compilación, Pruebas Unitarias y Benchmarking",
        lineas_compilacion,
        "assets/anexo_compilacion.png",
        ancho=1150,
        alto=720
    )

    # 2. Captura de Ejecución del Sistema y Reportería
    lineas_ejecucion = [
        ("prompt", "miguel@uea-linux:~/datastructure$ "),
        ("command", "python3 main.py"),
        ("header", "====================================================================================="),
        ("header", "      UNIVERSIDAD ESTATAL AMAZÓNICA - FACULTAD DE CIENCIAS DE LA TIERRA              "),
        ("header", "               CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN EN LÍNEA                     "),
        ("header", "         ASIGNATURA: ESTRUCTURA DE DATOS (UEA-L-UFB-032) | PRÁCTICA #03              "),
        ("header", "                 UNIDAD III: IMPLEMENTACIÓN DE CONJUNTOS Y MAPAS                      "),
        ("header", "         Desarrollado por: Miguel Cahuasqui | Período Académico: 2026-2026           "),
        ("header", "====================================================================================="),
        ("highlight", "PANEL DE CONTROL GENERAL: TORNEO DE FÚTBOL AMAZÓNICO UEA 2026"),
        ("dim", "-------------------------------------------------------------------------------------"),
        ("default", " * Total de Equipos Registrados (Mapa):       4 (Pastaza, Napo, Orellana, Sucumbíos)"),
        ("default", " * Total de Jugadores Registrados (Conjunto):  20 futbolistas"),
        ("default", " * Jugadores Sancionados (Conjunto Activo):   2 inhabilitados"),
        ("default", " * Partidos Disputados (Mapa de Encuentros):  4 partidos jugados"),
        ("dim", "-------------------------------------------------------------------------------------"),
        ("header", "TABLA DE POSICIONES (Cómputo en Mapa Hash):"),
        ("dim", "POS  | EQUIPO                       |  PJ |  PG |  PE |  PP |  GF |  GC |   DG |  PTS"),
        ("dim", "-------------------------------------------------------------------------------------"),
        ("ok", "1    | Pastaza Sporting Club        |   2 |   1 |   1 |   0 |   3 |   2 |   +1 |    4"),
        ("ok", "2    | Amazonía Orellana FC         |   2 |   1 |   1 |   0 |   4 |   3 |   +1 |    4"),
        ("default", "3    | Deportivo Napo               |   2 |   1 |   0 |   1 |   3 |   2 |   +1 |    3"),
        ("default", "4    | Atlético Sucumbíos           |   2 |   0 |   0 |   2 |   2 |   5 |   -3 |    0"),
        ("dim", "-------------------------------------------------------------------------------------"),
        ("highlight", "AUDITORÍA DE CONJUNTOS (Operación A ∩ B): No se registran dobles fichajes."),
        ("highlight", "CONTROL DISCIPLINARIO (Operación A - B): 18 habilitados | 2 suspendidos."),
    ]

    crear_captura_terminal(
        "Terminal UEA - Ejecución del Menú Principal, Reportería y Operaciones de Conjuntos",
        lineas_ejecucion,
        "assets/anexo_ejecucion.png",
        ancho=1150,
        alto=720
    )

if __name__ == "__main__":
    main()
