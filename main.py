"""
Sistema de Gestión de Torneo de Fútbol Amazónico - UEA 2026.
Práctica #03: Implementación de Conjuntos y Mapas.
Asignatura: Estructura de Datos (UEA-L-UFB-032).
Estudiante: Miguel Cahuasqui.
"""

import sys
from src.gestor_torneo import GestorTorneo
from src.reporteria import ReporteriaTorneo
from src.data_seed import cargar_datos_demostracion
from src.benchmark import AnalizadorRendimiento
from src.models import Posicion


def limpiar_pantalla() -> None:
    # Separador visual multiplataforma
    print("\n" * 2)


def mostrar_encabezado() -> None:
    print("=" * 85)
    print("      UNIVERSIDAD ESTATAL AMAZÓNICA - FACULTAD DE CIENCIAS DE LA TIERRA      ")
    print("               CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN EN LÍNEA              ")
    print("         ASIGNATURA: ESTRUCTURA DE DATOS (UEA-L-UFB-032) | PRÁCTICA #03       ")
    print("                 UNIDAD III: IMPLEMENTACIÓN DE CONJUNTOS Y MAPAS               ")
    print("         Desarrollado por: Miguel Cahuasqui | Período Académico: 2026-2026    ")
    print("=" * 85)


def mostrar_menu_principal() -> None:
    print("""
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║                           MENÚ DE OPERACIONES                             ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║  [1] Ver Tabla de Posiciones del Torneo (Mapas O(1))                      ║
  ║  [2] Consultar Nómina Oficial de un Equipo (Mapas y Conjuntos)           ║
  ║  [3] Reporte de Jugadores Habilitados vs Sancionados (Diferencia: A - B) ║
  ║  [4] Auditoría: Detección de Doble Fichaje (Intersección: A ∩ B)          ║
  ║  [5] Comparativa de Plantillas entre dos Clubes (Diferencia Simétrica)    ║
  ║  [6] Validar Convocatoria / Alineación (Subconjuntos: X ⊆ A)             ║
  ║  [7] Registrar Nuevo Equipo (Inserción en Mapa O(1))                      ║
  ║  [8] Registrar Nuevo Jugador (Inserción en Conjunto y Mapa O(1))          ║
  ║  [9] Aplicar / Levantar Sanción Disciplinaria (Conjunto de Sancionados)  ║
  ║ [10] Registrar Resultado de Partido (Actualiza Mapa de Métricas)          ║
  ║ [11] Ejecutar Benchmarking de Rendimiento (Análisis O(1) vs O(n))         ║
  ║ [12] Ver Ficha Técnica Académica y Declaración de Agente de IA           ║
  ║  [0] Salir del Sistema                                                    ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
""")


def mostrar_ficha_tecnica() -> None:
    print("\n" + "=" * 85)
    print("                   FICHA TÉCNICA ACADÉMICA Y DECLARACIÓN DE IA               ")
    print("=" * 85)
    print("""
1. DATOS INSTITUCIONALES:
   - Institución: Universidad Estatal Amazónica (UEA)
   - Asignatura: Estructura de Datos (Código: UEA-L-UFB-032)
   - Período: 2026-2026
   - Unidad III: Conjuntos y Mapas (Semanas 9-10-11-12)
   - Estudiante: Miguel Cahuasqui
   - Problema Seleccionado: Aplicación para el registro de jugadores y equipos en un torneo de fútbol.

2. USO DE ESTRUCTURAS DE DATOS (TAD):
   - CONJUNTOS (set):
     * Manejo del universo de cédulas de jugadores (garantía de unicidad).
     * Conjunto de jugadores pertenecientes a cada club.
     * Conjunto dinámico de jugadores suspendidos/sancionados.
     * Operaciones formales implementadas:
       - Diferencia (A - B): Cálculo de jugadores habilitados (Nómina - Sancionados).
       - Intersección (A ∩ B): Detección de irregularidades por doble fichaje.
       - Unión (A ∪ B): Nóminas consolidadas por grupos o regiones.
       - Diferencia Simétrica (A △ B): Jugadores no compartidos entre dos plantillas.
       - Subconjuntos (X ⊆ A): Validación de convocatorias respecto a la lista oficial.
   - MAPAS / DICCIONARIOS (dict):
     * Mapeo O(1) ID_Equipo -> Objeto Equipo (con estadísticas y atributos).
     * Mapeo O(1) Cédula -> Objeto Jugador (clave primaria indexada).
     * Mapeo de Categorías -> Conjunto de Equipos.
     * Mapeo de Encuentros / Resultados.

3. DECLARACIÓN DE AGENTE DE INTELIGENCIA ARTIFICIAL (Rúbrica UEA):
   - Agente de IA utilizado: Google Antigravity (Gemini 3.8 Flash)
   - Descripción: Asistente para diseño arquitectónico modular, benchmarking empírico,
     generación de estructuras de datos optimizadas y pruebas unitarias.
   - Porcentaje estimado de desarrollo con IA: 85% asistencia de IA en estructura
     base, algoritmos y documentación; 15% especificación de requerimientos, validación
     de reglas de negocio del torneo y verificación por parte del estudiante.
""")
    print("=" * 85)
    input("\nPresione ENTER para retornar al menú principal...")


def ejecutar_aplicacion() -> None:
    gestor = GestorTorneo("Torneo de Fútbol Amazónico UEA 2026")
    reporteria = ReporteriaTorneo(gestor)

    # Carga automática de datos de demostración
    cargar_datos_demostracion(gestor)

    while True:
        limpiar_pantalla()
        mostrar_encabezado()
        reporteria.mostrar_resumen_general()
        mostrar_menu_principal()

        opcion = input("Seleccione una opción [0-12]: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            reporteria.mostrar_tabla_posiciones()
            input("\nPresione ENTER para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            print("\nEquipos disponibles:", ", ".join(gestor.mapa_equipos.keys()))
            id_eq = input("Ingrese el código del equipo (ej. PAS, NAP, ORE, SUC): ").strip().upper()
            reporteria.mostrar_nomina_equipo(id_eq)
            input("\nPresione ENTER para continuar...")

        elif opcion == "3":
            limpiar_pantalla()
            reporteria.mostrar_reporte_disciplinario()
            print("\n--- DETALLE DE HABILITACIÓN POR EQUIPO (OPERACIÓN DIFERENCIA: A - B) ---")
            for id_eq in gestor.mapa_equipos:
                eq = gestor.consultar_equipo(id_eq)
                hab = gestor.obtener_jugadores_habilitados(id_eq)
                inh = gestor.obtener_jugadores_inhabilitados_equipo(id_eq)
                print(f" * {eq.nombre:<28} | Plantilla: {len(eq.jugadores_ids):>2} | Habilitados: {len(hab):>2} | Suspendidos: {len(inh):>2}")
            input("\nPresione ENTER para continuar...")

        elif opcion == "4":
            limpiar_pantalla()
            reporteria.mostrar_auditoria_torneo()
            input("\nPresione ENTER para continuar...")

        elif opcion == "5":
            limpiar_pantalla()
            print("\nEquipos disponibles:", ", ".join(gestor.mapa_equipos.keys()))
            eq_a = input("Ingrese código del Primer Equipo: ").strip().upper()
            eq_b = input("Ingrese código del Segundo Equipo: ").strip().upper()
            reporteria.mostrar_comparacion_plantillas(eq_a, eq_b)
            input("\nPresione ENTER para continuar...")

        elif opcion == "6":
            limpiar_pantalla()
            print("\n--- VALIDACIÓN DE ALINEACIÓN MEDIANTE SUBCONJUNTOS (X ⊆ A) ---")
            print("Equipos disponibles:", ", ".join(gestor.mapa_equipos.keys()))
            id_eq = input("Ingrese el código del equipo: ").strip().upper()
            equipo = gestor.consultar_equipo(id_eq)
            if not equipo:
                print("[!] Equipo no encontrado.")
            else:
                print(f"\nJugadores inscritos en {equipo.nombre}:")
                for cid in equipo.jugadores_ids:
                    j = gestor.mapa_jugadores[cid]
                    print(f"  - Cédula: {cid} | #{j.dorsal} {j.nombre} ({j.posicion.value})")

                entradas = input("\nIngrese las cédulas convocadas separadas por comas:\n> ").strip()
                if entradas:
                    cedulas_set = {c.strip() for c in entradas.split(",") if c.strip()}
                    valido, errores = gestor.validar_alineacion(id_eq, cedulas_set)
                    print("\n" + "=" * 60)
                    if valido:
                        print("  [✓ VALIDACIÓN EXITOSA] La alineación cumple con el reglamento.")
                        print("  Es subconjunto estricto y no incluye sancionados.")
                    else:
                        print("  [✗ ALINEACIÓN RECHAZADA] Se detectaron faltas reglamentarias:")
                        for err in errores:
                            print(f"   * {err}")
                    print("=" * 60)
            input("\nPresione ENTER para continuar...")

        elif opcion == "7":
            limpiar_pantalla()
            print("\n--- REGISTRO DE NUEVO EQUIPO (MAPAS O(1)) ---")
            cod = input("Código corto (3 letras, ej. CUM): ").strip().upper()
            nom = input("Nombre oficial del club: ").strip()
            ciu = input("Ciudad sede: ").strip()
            dt = input("Director Técnico: ").strip()
            cat = input("Categoría/Grupo [Grupo Amazónico]: ").strip() or "Grupo Amazónico"

            ok, msg = gestor.registrar_equipo(cod, nom, ciu, dt, cat)
            print(f"\nResultado: {msg}")
            input("\nPresione ENTER para continuar...")

        elif opcion == "8":
            limpiar_pantalla()
            print("\n--- REGISTRO DE NUEVO JUGADOR (CONJUNTOS Y MAPAS O(1)) ---")
            ced = input("Número de Cédula: ").strip()
            nom = input("Nombre completo del futbolista: ").strip()
            try:
                edad = int(input("Edad: ").strip())
            except ValueError:
                edad = 20
            
            print("\nPosiciones:")
            print("1. Portero  2. Defensa  3. Mediocampista  4. Delantero")
            pos_opc = input("Seleccione posición [1-4]: ").strip()
            pos_map = {
                "1": Posicion.PORTERO,
                "2": Posicion.DEFENSA,
                "3": Posicion.MEDIOCAMPISTA,
                "4": Posicion.DELANTERO
            }
            pos = pos_map.get(pos_opc, Posicion.MEDIOCAMPISTA)

            try:
                dorsal = int(input("Número de dorsal: ").strip())
            except ValueError:
                dorsal = 10

            print("\nEquipos disponibles:", ", ".join(gestor.mapa_equipos.keys()))
            eq_id = input("Asignar a equipo (o dejar vacío): ").strip().upper() or None

            ok, msg = gestor.registrar_jugador(ced, nom, edad, pos, dorsal, eq_id)
            print(f"\nResultado: {msg}")
            input("\nPresione ENTER para continuar...")

        elif opcion == "9":
            limpiar_pantalla()
            print("\n--- GESTIÓN DISCIPLINARIA (CONJUNTO DE SANCIONADOS) ---")
            print("1. Aplicar Tarjeta (Amarilla o Roja)")
            print("2. Levantar Sanción / Habilitar Jugador")
            sub_opc = input("Seleccione sub-opción [1-2]: ").strip()

            if sub_opc == "1":
                ced = input("Cédula del jugador: ").strip()
                tipo = input("Tipo de tarjeta (amarilla / roja): ").strip()
                ok, msg = gestor.aplicar_tarjeta(ced, tipo)
                print(f"\nResultado: {msg}")
            elif sub_opc == "2":
                ced = input("Cédula del jugador a rehabilitar: ").strip()
                ok, msg = gestor.levantar_sancion(ced)
                print(f"\nResultado: {msg}")
            input("\nPresione ENTER para continuar...")

        elif opcion == "10":
            limpiar_pantalla()
            print("\n--- REGISTRO DE RESULTADO DE PARTIDO (ACTUALIZA MAPAS) ---")
            print("Equipos disponibles:", ", ".join(gestor.mapa_equipos.keys()))
            loc = input("Código Equipo Local: ").strip().upper()
            vis = input("Código Equipo Visitante: ").strip().upper()
            try:
                g_loc = int(input(f"Goles de {loc}: ").strip())
                g_vis = int(input(f"Goles de {vis}: ").strip())
                id_part = f"PAR_{len(gestor.mapa_partidos) + 1:02d}"
                ok, msg = gestor.registrar_partido(id_part, loc, vis, g_loc, g_vis)
                print(f"\nResultado: {msg}")
            except ValueError:
                print("\n[!] Error: Los goles deben ser números enteros.")
            input("\nPresione ENTER para continuar...")

        elif opcion == "11":
            limpiar_pantalla()
            AnalizadorRendimiento.imprimir_reporte_completo()
            input("\nPresione ENTER para continuar...")

        elif opcion == "12":
            limpiar_pantalla()
            mostrar_ficha_tecnica()

        elif opcion == "0":
            print("\n¡Gracias por utilizar el Sistema del Torneo Amazónico UEA!")
            print("Cerrando sesión de Miguel Cahuasqui...")
            break
        else:
            print("\n[!] Opción no válida. Intente nuevamente.")
            input("Presione ENTER para continuar...")


if __name__ == "__main__":
    try:
        ejecutar_aplicacion()
    except KeyboardInterrupt:
        print("\n\nPrograma terminado por el usuario.")
        sys.exit(0)
