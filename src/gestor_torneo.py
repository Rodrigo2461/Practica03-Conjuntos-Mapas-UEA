"""
Lógica central del Sistema de Gestión del Torneo de Fútbol.
Implementa el uso exhaustivo de Conjuntos (set), Mapas/Diccionarios (dict)
y operaciones fundamentales de la Teoría de Conjuntos.
"""

from typing import Dict, Set, Tuple, List, Optional
from src.models import Equipo, Jugador, Partido, Posicion


class GestorTorneo:
    """
    Controlador principal del torneo que administra los Tipos Abstractos de Datos (TAD):
    - MAPAS / DICCIONARIOS (dict):
        * mapa_equipos: dict[str, Equipo] -> Mapeo O(1) de ID a objeto Equipo.
        * mapa_jugadores: dict[str, Jugador] -> Mapeo O(1) de cédula a objeto Jugador.
        * mapa_categorias: dict[str, set[str]] -> Mapeo de categoría a conjunto de IDs de equipos.
        * mapa_partidos: dict[str, Partido] -> Mapeo de ID de partido a registro del encuentro.
    - CONJUNTOS (set):
        * conjunto_todos_jugadores: set[str] -> Registro universal de cédulas de jugadores.
        * conjunto_sancionados: set[str] -> Conjunto dinámico de jugadores inhabilitados para jugar.
        * equipo.jugadores_ids: set[str] -> Conjunto de jugadores pertenecientes a cada club.
    """

    def __init__(self, nombre_torneo: str = "Torneo Interfacultades UEA 2026"):
        self.nombre_torneo: str = nombre_torneo
        
        # --- MAPAS / DICCIONARIOS (Tablas Hash) ---
        self.mapa_equipos: Dict[str, Equipo] = {}
        self.mapa_jugadores: Dict[str, Jugador] = {}
        self.mapa_categorias: Dict[str, Set[str]] = {}
        self.mapa_partidos: Dict[str, Partido] = {}
        
        # --- CONJUNTOS (Sets) ---
        self.conjunto_todos_jugadores: Set[str] = set()
        self.conjunto_sancionados: Set[str] = set()

    # =========================================================================
    # GESTIÓN DE EQUIPOS (Operaciones en Mapas O(1))
    # =========================================================================

    def registrar_equipo(self, id_equipo: str, nombre: str, ciudad: str,
                         director_tecnico: str, categoria: str = "Grupo A") -> Tuple[bool, str]:
        """
        Registra un equipo en el mapa de equipos O(1).
        Evita duplicidad de identificadores mediante verificación en hash table.
        """
        id_limpio = id_equipo.strip().upper()
        if id_limpio in self.mapa_equipos:
            return False, f"El equipo con código '{id_limpio}' ya se encuentra registrado."

        nuevo_equipo = Equipo(
            id_equipo=id_limpio,
            nombre=nombre.strip(),
            ciudad=ciudad.strip(),
            director_tecnico=director_tecnico.strip(),
            categoria=categoria.strip(),
            jugadores_ids=set()
        )
        self.mapa_equipos[id_limpio] = nuevo_equipo

        # Actualizar mapa de categorías (asociación categoría -> conjunto de equipos)
        if categoria not in self.mapa_categorias:
            self.mapa_categorias[categoria] = set()
        self.mapa_categorias[categoria].add(id_limpio)

        return True, f"Equipo '{nombre}' registrado con éxito en la categoría '{categoria}'."

    def consultar_equipo(self, id_equipo: str) -> Optional[Equipo]:
        """Búsqueda de equipo por ID en tiempo constante O(1)."""
        return self.mapa_equipos.get(id_equipo.strip().upper())

    # =========================================================================
    # GESTIÓN DE JUGADORES (Conjuntos y Mapas O(1))
    # =========================================================================

    def registrar_jugador(self, cedula: str, nombre: str, edad: int,
                          posicion: Posicion, dorsal: int,
                          equipo_id: Optional[str] = None) -> Tuple[bool, str]:
        """
        Registra un jugador en el mapa global y en el conjunto universal de jugadores.
        Verifica unicidad en O(1) con conjuntos.
        """
        cedula_limpia = cedula.strip()
        if cedula_limpia in self.conjunto_todos_jugadores:
            return False, f"Error: La cédula '{cedula_limpia}' ya pertenece a un jugador registrado en el torneo."

        # Validar equipo si se especificó
        equipo_obj = None
        if equipo_id:
            equipo_id_limpio = equipo_id.strip().upper()
            equipo_obj = self.consultar_equipo(equipo_id_limpio)
            if not equipo_obj:
                return False, f"Error: El equipo '{equipo_id_limpio}' no existe en el sistema."

            # Validar que no exista dorsal duplicado en el mismo equipo usando generadores sobre mapa
            dorsales_equipo = {
                self.mapa_jugadores[cid].dorsal
                for cid in equipo_obj.jugadores_ids
                if cid in self.mapa_jugadores
            }
            if dorsal in dorsales_equipo:
                return False, f"Error reglamentario: El dorsal #{dorsal} ya está asignado a otro jugador de '{equipo_obj.nombre}'."

        nuevo_jugador = Jugador(
            cedula=cedula_limpia,
            nombre=nombre.strip(),
            edad=edad,
            posicion=posicion,
            dorsal=dorsal,
            equipo_id=equipo_obj.id_equipo if equipo_obj else None
        )

        # Inserción en Mapas y Conjuntos en O(1)
        self.mapa_jugadores[cedula_limpia] = nuevo_jugador
        self.conjunto_todos_jugadores.add(cedula_limpia)

        if equipo_obj:
            equipo_obj.jugadores_ids.add(cedula_limpia)

        return True, f"Jugador '{nombre}' (Cédula: {cedula_limpia}) registrado correctamente."

    def consultar_jugador(self, cedula: str) -> Optional[Jugador]:
        """Búsqueda directa de jugador por clave primaria (cédula) en O(1)."""
        return self.mapa_jugadores.get(cedula.strip())

    def transferir_jugador(self, cedula: str, nuevo_equipo_id: str) -> Tuple[bool, str]:
        """
        Transfiere un jugador de un equipo a otro.
        Actualiza los conjuntos de jugadores de ambos equipos en O(1).
        """
        jugador = self.consultar_jugador(cedula)
        if not jugador:
            return False, f"No existe el jugador con cédula '{cedula}'."

        nuevo_equipo = self.consultar_equipo(nuevo_equipo_id)
        if not nuevo_equipo:
            return False, f"No existe el equipo de destino '{nuevo_equipo_id}'."

        # Retirar del equipo anterior si tenía
        if jugador.equipo_id and jugador.equipo_id in self.mapa_equipos:
            self.mapa_equipos[jugador.equipo_id].jugadores_ids.discard(cedula)

        # Agregar al nuevo equipo
        nuevo_equipo.jugadores_ids.add(cedula)
        jugador.equipo_id = nuevo_equipo.id_equipo

        return True, f"Jugador '{jugador.nombre}' transferido exitosamente a '{nuevo_equipo.nombre}'."

    # =========================================================================
    # GESTIÓN DE DISCIPLINAS Y SANCIONES (Conjuntos Dinámicos)
    # =========================================================================

    def aplicar_tarjeta(self, cedula: str, tipo: str = "amarilla") -> Tuple[bool, str]:
        """
        Registra tarjeta a un jugador y si amerita sanción, lo agrega
        al conjunto de sancionados en O(1).
        """
        jugador = self.consultar_jugador(cedula)
        if not jugador:
            return False, f"Jugador con cédula '{cedula}' no encontrado."

        if tipo.lower() in ("roja", "red"):
            jugador.tarjetas_rojas += 1
            self.conjunto_sancionados.add(cedula)
            return True, f"Tarjeta ROJA registrada a '{jugador.nombre}'. Jugador añadido a sancionados."
        elif tipo.lower() in ("amarilla", "yellow"):
            jugador.tarjetas_amarillas += 1
            if jugador.tarjetas_amarillas >= 3:
                self.conjunto_sancionados.add(cedula)
                return True, f"3ra Tarjeta AMARILLA para '{jugador.nombre}'. Sanción automática aplicada."
            return True, f"Tarjeta amarilla registrada a '{jugador.nombre}' ({jugador.tarjetas_amarillas} acumuladas)."
        else:
            return False, "Tipo de tarjeta no válido. Use 'amarilla' o 'roja'."

    def levantar_sancion(self, cedula: str) -> Tuple[bool, str]:
        """
        Levanta la sanción de un jugador y reinicia tarjetas rojas/amarillas.
        Elimina la cédula del conjunto de sancionados en O(1).
        """
        jugador = self.consultar_jugador(cedula)
        if not jugador:
            return False, f"Jugador con cédula '{cedula}' no encontrado."

        if cedula in self.conjunto_sancionados:
            self.conjunto_sancionados.discard(cedula)
            jugador.tarjetas_rojas = 0
            jugador.tarjetas_amarillas = 0
            return True, f"Sanción levantada para '{jugador.nombre}'. Habilitado para jugar."
        return False, f"El jugador '{jugador.nombre}' no tiene sanciones vigentes."

    # =========================================================================
    # OPERACIONES FORMALES DE TEORÍA DE CONJUNTOS
    # =========================================================================

    def obtener_jugadores_habilitados(self, id_equipo: str) -> Set[str]:
        """
        OPERACIÓN DE CONJUNTOS: DIFERENCIA (A - B)
        Habilitados = Nómina del Equipo - Jugadores Sancionados
        Retorna el conjunto de cédulas de jugadores que tienen permiso reglamentario
        para disputar el siguiente encuentro.
        """
        equipo = self.consultar_equipo(id_equipo)
        if not equipo:
            return set()
        
        # Diferencia de conjuntos en Python: A - B
        return equipo.jugadores_ids - self.conjunto_sancionados

    def obtener_jugadores_inhabilitados_equipo(self, id_equipo: str) -> Set[str]:
        """
        OPERACIÓN DE CONJUNTOS: INTERSECCIÓN (A ∩ B)
        Inhabilitados = Nómina del Equipo ∩ Jugadores Sancionados
        """
        equipo = self.consultar_equipo(id_equipo)
        if not equipo:
            return set()
        return equipo.jugadores_ids & self.conjunto_sancionados

    def auditoria_doble_inscripcion(self) -> Dict[Tuple[str, str], Set[str]]:
        """
        OPERACIÓN DE CONJUNTOS: INTERSECCIÓN MULTIPAR (A ∩ B)
        Auditoría reglamentaria: Detecta si algún jugador ha sido inscrito
        simultáneamente en dos equipos distintos (fraude o conflicto de fichaje).
        Retorna un mapa con los pares de equipos en conflicto y el conjunto de cédulas duplicadas.
        """
        conflictos: Dict[Tuple[str, str], Set[str]] = {}
        equipos = list(self.mapa_equipos.values())

        for i in range(len(equipos)):
            for j in range(i + 1, len(equipos)):
                equipo_a = equipos[i]
                equipo_b = equipos[j]
                
                # Intersección de plantillas
                duplicados = equipo_a.jugadores_ids & equipo_b.jugadores_ids
                if duplicados:
                    conflictos[(equipo_a.id_equipo, equipo_b.id_equipo)] = duplicados

        return conflictos

    def obtener_nomina_consolidada(self, ids_equipos: List[str]) -> Set[str]:
        """
        OPERACIÓN DE CONJUNTOS: UNIÓN (A ∪ B ∪ C ...)
        Calcula el conjunto total de jugadores participantes de un grupo, categoría
        o selección combinada sin elementos duplicados.
        """
        conjunto_unificado: Set[str] = set()
        for eid in ids_equipos:
            equipo = self.consultar_equipo(eid)
            if equipo:
                conjunto_unificado = conjunto_unificado | equipo.jugadores_ids
        return conjunto_unificado

    def comparar_plantillas(self, id_equipo_a: str, id_equipo_b: str) -> Dict[str, Set[str]]:
        """
        OPERACIONES DE CONJUNTOS COMPLETAS ENTRE DOS EQUIPOS:
        - Unión (A ∪ B)
        - Intersección (A ∩ B)
        - Exclusivos de A (A - B)
        - Exclusivos de B (B - A)
        - Diferencia Simétrica (A △ B o A ^ B): jugadores que están en un equipo pero no en ambos.
        """
        equipo_a = self.consultar_equipo(id_equipo_a)
        equipo_b = self.consultar_equipo(id_equipo_b)

        set_a = equipo_a.jugadores_ids if equipo_a else set()
        set_b = equipo_b.jugadores_ids if equipo_b else set()

        return {
            "union": set_a | set_b,
            "interseccion": set_a & set_b,
            "exclusivos_a": set_a - set_b,
            "exclusivos_b": set_b - set_a,
            "diferencia_simetrica": set_a ^ set_b
        }

    def validar_alineacion(self, id_equipo: str, alineacion_cedulas: Set[str]) -> Tuple[bool, List[str]]:
        """
        OPERACIONES DE CONJUNTOS: SUBCONJUNTOS (⊆) Y CONJUNTOS DISJUNTOS
        Valida si una alineación (titulares y suplentes presentados para un partido):
        1. Es subconjunto estricto de la nómina oficial del equipo (alineacion ⊆ equipo.jugadores_ids).
        2. Es disjunta con el conjunto de sancionados (alineacion ∩ sancionados == ∅).
        """
        errores: List[str] = []
        equipo = self.consultar_equipo(id_equipo)
        if not equipo:
            return False, [f"El equipo '{id_equipo}' no existe."]

        # 1. Comprobación de Subconjunto: alineacion_cedulas <= equipo.jugadores_ids
        no_inscritos = alineacion_cedulas - equipo.jugadores_ids
        if no_inscritos:
            nombres = [
                self.mapa_jugadores[c].nombre if c in self.mapa_jugadores else c
                for c in no_inscritos
            ]
            errores.append(f"Los siguientes jugadores NO están inscritos en el equipo: {', '.join(nombres)}")

        # 2. Comprobación de Disyunción con Sancionados:
        sancionados_incluidos = alineacion_cedulas & self.conjunto_sancionados
        if sancionados_incluidos:
            nombres = [
                self.mapa_jugadores[c].nombre if c in self.mapa_jugadores else c
                for c in sancionados_incluidos
            ]
            errores.append(f"Infracción reglamentaria: Se incluyeron jugadores suspendidos/sancionados: {', '.join(nombres)}")

        valido = len(errores) == 0
        return valido, errores

    # =========================================================================
    # GESTIÓN DE PARTIDOS Y TABLA DE POSICIONES (Mapas Dinámicos)
    # =========================================================================

    def registrar_partido(self, id_partido: str, local_id: str, visitante_id: str,
                          goles_local: int, goles_visitante: int, jornada: int = 1) -> Tuple[bool, str]:
        """
        Registra el marcador de un encuentro y actualiza las métricas en los mapas de equipos.
        """
        local = self.consultar_equipo(local_id)
        visitante = self.consultar_equipo(visitante_id)

        if not local or not visitante:
            return False, "Uno o ambos equipos no existen en el torneo."

        if local_id == visitante_id:
            return False, "Un equipo no puede disputar un partido contra sí mismo."

        partido = Partido(
            id_partido=id_partido,
            equipo_local_id=local_id,
            equipo_visitante_id=visitante_id,
            goles_local=goles_local,
            goles_visitante=goles_visitante,
            fecha_jornada=jornada,
            jugado=True
        )
        self.mapa_partidos[id_partido] = partido

        # Actualizar estadísticas del local
        local.partidos_jugados += 1
        local.goles_favor += goles_local
        local.goles_contra += goles_visitante

        # Actualizar estadísticas del visitante
        visitante.partidos_jugados += 1
        visitante.goles_favor += goles_visitante
        visitante.goles_contra += goles_local

        if goles_local > goles_visitante:
            local.partidos_ganados += 1
            visitante.partidos_perdidos += 1
        elif goles_visitante > goles_local:
            visitante.partidos_ganados += 1
            local.partidos_perdidos += 1
        else:
            local.partidos_empatados += 1
            visitante.partidos_empatados += 1

        return True, f"Partido registrado: {local.nombre} {goles_local} - {goles_visitante} {visitante.nombre}"

    def obtener_tabla_posiciones(self, categoria: Optional[str] = None) -> List[Equipo]:
        """
        Genera la tabla de posiciones ordenada por Puntos (descendente),
        Diferencia de Goles (descendente) y Goles a Favor (descendente).
        """
        if categoria and categoria in self.mapa_categorias:
            equipos = [
                self.mapa_equipos[eid]
                for eid in self.mapa_categorias[categoria]
                if eid in self.mapa_equipos
            ]
        else:
            equipos = list(self.mapa_equipos.values())

        # Ordenamiento multifactorial estándar FIFA/FEF
        equipos_ordenados = sorted(
            equipos,
            key=lambda eq: (eq.puntos, eq.diferencia_goles, eq.goles_favor),
            reverse=True
        )
        return equipos_ordenados
