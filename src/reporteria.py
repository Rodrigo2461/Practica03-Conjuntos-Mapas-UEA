"""
Módulo de Reportería y Visualización del Torneo.
Permite consultar, filtrar y presentar de forma estética y estructurada
los elementos que conforman los mapas y conjuntos del sistema.
"""

from typing import List, Optional
from src.gestor_torneo import GestorTorneo
from src.models import Equipo, Jugador


class ReporteriaTorneo:
    """
    Genera reportes legibles en consola con formato de tablas,
    resaltando el uso de mapas y conjuntos.
    """

    def __init__(self, gestor: GestorTorneo):
        self.gestor = gestor

    @staticmethod
    def _linea_separadora(ancho: int = 80, char: str = "=") -> str:
        return char * ancho

    def mostrar_tabla_posiciones(self, categoria: Optional[str] = None) -> None:
        """Visualiza la tabla de posiciones calculada a partir de los mapas."""
        equipos = self.gestor.obtener_tabla_posiciones(categoria)
        titulo = f"TABLA DE POSICIONES - {categoria if categoria else 'GENERAL'}"

        print("\n" + self._linea_separadora(85))
        print(f"{titulo.center(85)}")
        print(self._linea_separadora(85))
        print(f"{'POS':<4} | {'EQUIPO':<28} | {'PJ':>3} | {'PG':>3} | {'PE':>3} | {'PP':>3} | {'GF':>3} | {'GC':>3} | {'DG':>4} | {'PTS':>4}")
        print("-" * 85)

        for pos, eq in enumerate(equipos, start=1):
            print(f"{pos:<4} | {eq.nombre[:28]:<28} | {eq.partidos_jugados:>3} | {eq.partidos_ganados:>3} | "
                  f"{eq.partidos_empatados:>3} | {eq.partidos_perdidos:>3} | {eq.goles_favor:>3} | "
                  f"{eq.goles_contra:>3} | {eq.diferencia_goles:>+4} | {eq.puntos:>4}")

        print(self._linea_separadora(85))
        print(f"Total de equipos en contienda: {len(equipos)}")

    def mostrar_nomina_equipo(self, id_equipo: str) -> None:
        """
        Muestra la plantilla completa de un club, contrastando
        su conjunto de jugadores con el conjunto de sancionados.
        """
        equipo = self.gestor.consultar_equipo(id_equipo)
        if not equipo:
            print(f"\n[!] Error: Equipo con código '{id_equipo}' no encontrado.")
            return

        habilitados = self.gestor.obtener_jugadores_habilitados(id_equipo)
        inhabilitados = self.gestor.obtener_jugadores_inhabilitados_equipo(id_equipo)

        print("\n" + self._linea_separadora(85))
        print(f"NÓMINA OFICIAL: {equipo.nombre.upper()} ({equipo.ciudad})".center(85))
        print(f"Director Técnico: {equipo.director_tecnico} | Categoría: {equipo.categoria}".center(85))
        print(self._linea_separadora(85))
        print(f"{'DORSAL':<8} | {'CÉDULA':<12} | {'NOMBRE':<28} | {'EDAD':<5} | {'POSICIÓN':<14} | {'ESTADO':<15}")
        print("-" * 85)

        # Ordenar por dorsal para presentación prolija
        jugadores = [
            self.gestor.mapa_jugadores[cid]
            for cid in equipo.jugadores_ids
            if cid in self.gestor.mapa_jugadores
        ]
        jugadores_ordenados = sorted(jugadores, key=lambda j: j.dorsal)

        for j in jugadores_ordenados:
            estado = "HABILITADO" if j.cedula in habilitados else "SUSPENDIDO"
            print(f"#{j.dorsal:<7} | {j.cedula:<12} | {j.nombre[:28]:<28} | {j.edad:<5} | {j.posicion.value:<14} | {estado:<15}")

        print(self._linea_separadora(85))
        print(f"Total en nómina: {len(equipo.jugadores_ids)} | "
              f"Habilitados: {len(habilitados)} | "
              f"Suspendidos: {len(inhabilitados)}")

    def mostrar_reporte_disciplinario(self) -> None:
        """
        Presenta el reporte disciplinario global basado en el conjunto
        universal de sancionados.
        """
        sancionados_ids = self.gestor.conjunto_sancionados
        print("\n" + self._linea_separadora(85))
        print("REPORTE DISCIPLINAR GLOBAL: JUGADORES SANCIONADOS / INHABILITADOS".center(85))
        print("(Gestionado mediante Tipo Abstracto de Datos: CONJUNTO - set)".center(85))
        print(self._linea_separadora(85))

        if not sancionados_ids:
            print("  [OK] No existen jugadores sancionados actualmente en el torneo.")
            print(self._linea_separadora(85))
            return

        print(f"{'CÉDULA':<12} | {'NOMBRE':<26} | {'EQUIPO':<22} | {'T. AMARILLAS':<12} | {'T. ROJAS':<8}")
        print("-" * 85)

        for cid in sancionados_ids:
            j = self.gestor.mapa_jugadores.get(cid)
            if j:
                nombre_eq = "Sin Equipo"
                if j.equipo_id and j.equipo_id in self.gestor.mapa_equipos:
                    nombre_eq = self.gestor.mapa_equipos[j.equipo_id].nombre
                print(f"{j.cedula:<12} | {j.nombre[:26]:<26} | {nombre_eq[:22]:<22} | {j.tarjetas_amarillas:>12} | {j.tarjetas_rojas:>8}")

        print(self._linea_separadora(85))
        print(f"Total de futbolistas suspendidos en el torneo: {len(sancionados_ids)}")

    def mostrar_auditoria_torneo(self) -> None:
        """
        Realiza auditoría mediante intersección de conjuntos para alertar
        posibles irregularidades reglamentarias (doble fichaje o inconsistencias).
        """
        conflictos = self.gestor.auditoria_doble_inscripcion()
        print("\n" + self._linea_separadora(85))
        print("AUDITORÍA REGLAMENTARIA DEL TORNEO (INTERSECCIÓN DE CONJUNTOS)".center(85))
        print(self._linea_separadora(85))

        if not conflictos:
            print("  [CORRECTO] No se detectaron anomalías reglamentarias.")
            print("  Todos los conjuntos de jugadores por equipo son mutuamente disjuntos.")
        else:
            print("  [ALERTA DE IRREGULARIDAD] Se detectó doble fichaje en los siguientes casos:")
            for (eq_a_id, eq_b_id), cedulas in conflictos.items():
                eq_a = self.gestor.consultar_equipo(eq_a_id)
                eq_b = self.gestor.consultar_equipo(eq_b_id)
                nom_a = eq_a.nombre if eq_a else eq_a_id
                nom_b = eq_b.nombre if eq_b else eq_b_id
                print(f"\n  * Conflicto entre: '{nom_a}' y '{nom_b}':")
                for cid in cedulas:
                    j = self.gestor.mapa_jugadores.get(cid)
                    nom_jug = j.nombre if j else "Desconocido"
                    print(f"    - Cédula: {cid} | Nombre: {nom_jug}")

        print(self._linea_separadora(85))

    def mostrar_comparacion_plantillas(self, id_equipo_a: str, id_equipo_b: str) -> None:
        """
        Demuestra visualmente las 4 operaciones de teoría de conjuntos
        aplicadas a dos clubes deportivos.
        """
        eq_a = self.gestor.consultar_equipo(id_equipo_a)
        eq_b = self.gestor.consultar_equipo(id_equipo_b)

        if not eq_a or not eq_b:
            print("\n[!] Uno o ambos equipos no existen para la comparación.")
            return

        ops = self.gestor.comparar_plantillas(id_equipo_a, id_equipo_b)

        print("\n" + self._linea_separadora(85))
        print(f"ANÁLISIS DE TEORÍA DE CONJUNTOS: {eq_a.nombre} vs {eq_b.nombre}".center(85))
        print(self._linea_separadora(85))

        print(f"\n1. UNIÓN (A ∪ B) -> Jugadores totales de ambos clubes:")
        print(f"   Total de elementos únicos: {len(ops['union'])}")

        print(f"\n2. INTERSECCIÓN (A ∩ B) -> Jugadores compartidos (debe ser 0 en fair-play):")
        if ops['interseccion']:
            nombres = [self.gestor.mapa_jugadores[c].nombre for c in ops['interseccion'] if c in self.gestor.mapa_jugadores]
            print(f"   [!] Coincidentes ({len(ops['interseccion'])}): {', '.join(nombres)}")
        else:
            print("   [OK] Conjuntos disjuntos (0 jugadores en común).")

        print(f"\n3. DIFERENCIA (A - B) -> Exclusivos de {eq_a.nombre}:")
        print(f"   Total de jugadores exclusivos: {len(ops['exclusivos_a'])}")

        print(f"\n4. DIFERENCIA (B - A) -> Exclusivos de {eq_b.nombre}:")
        print(f"   Total de jugadores exclusivos: {len(ops['exclusivos_b'])}")

        print(f"\n5. DIFERENCIA SIMÉTRICA (A △ B o A ^ B) -> Jugadores que pertenecen a solo uno de ellos:")
        print(f"   Total de elementos en la diferencia simétrica: {len(ops['diferencia_simetrica'])}")

        print(self._linea_separadora(85))

    def mostrar_resumen_general(self) -> None:
        """Resumen estadístico y dimensional de las estructuras de datos."""
        print("\n" + self._linea_separadora(85))
        print(f"PANEL DE CONTROL GENERAL: {self.gestor.nombre_torneo.upper()}".center(85))
        print(self._linea_separadora(85))
        print(f" * Total de Equipos Registrados (Mapa):       {len(self.gestor.mapa_equipos)}")
        print(f" * Total de Jugadores Registrados (Conjunto):  {len(self.gestor.conjunto_todos_jugadores)}")
        print(f" * Jugadores en el Mapa Clave-Valor:          {len(self.gestor.mapa_jugadores)}")
        print(f" * Jugadores Sancionados (Conjunto Activo):   {len(self.gestor.conjunto_sancionados)}")
        print(f" * Partidos Disputados (Mapa de Encuentros):  {len(self.gestor.mapa_partidos)}")
        print(f" * Categorías Registradas:                    {len(self.gestor.mapa_categorias)}")
        print(self._linea_separadora(85))
