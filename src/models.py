"""
Modelos de datos para el Sistema de Gestión del Torneo de Fútbol Amazónico (UEA).
Implementa tipos de datos estructurados para Jugadores, Equipos y Partidos.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Set


class Posicion(str, Enum):
    PORTERO = "Portero"
    DEFENSA = "Defensa"
    MEDIOCAMPISTA = "Mediocampista"
    DELANTERO = "Delantero"


@dataclass
class Jugador:
    """
    Representa a un futbolista inscrito en el torneo.
    La 'cedula' actúa como clave primaria única (hasheable) para conjuntos y mapas.
    """
    cedula: str
    nombre: str
    edad: int
    posicion: Posicion
    dorsal: int
    equipo_id: Optional[str] = None
    goles: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0

    def __hash__(self) -> int:
        # Permite usar instancias de Jugador en conjuntos basándose en su cédula única
        return hash(self.cedula)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Jugador):
            return self.cedula == other.cedula
        return False

    @property
    def esta_sancionado(self) -> bool:
        """
        Reglamento deportivo: un jugador está suspendido/sancionado si tiene
        al menos una tarjeta roja directa o acumulación de 3 tarjetas amarillas.
        """
        return self.tarjetas_rojas > 0 or self.tarjetas_amarillas >= 3

    def estado_str(self) -> str:
        if self.tarjetas_rojas > 0:
            return f"SANCIONADO (Tarjeta Roja: {self.tarjetas_rojas})"
        if self.tarjetas_amarillas >= 3:
            return f"SANCIONADO (Acumulación: {self.tarjetas_amarillas} amarillas)"
        return "HABILITADO"


@dataclass
class Equipo:
    """
    Representa un equipo participante en el torneo.
    - 'id_equipo': clave única hasheable.
    - 'jugadores_ids': CONJUNTO (set) de cédulas de los jugadores pertenecientes al club.
      Garantiza que no existan duplicados dentro de la plantilla en O(1).
    """
    id_equipo: str
    nombre: str
    ciudad: str
    director_tecnico: str
    categoria: str = "Primera Categoría"
    jugadores_ids: Set[str] = field(default_factory=set)

    # Estadísticas para tabla de posiciones (almacenadas como mapa conceptual de métricas)
    partidos_jugados: int = 0
    partidos_ganados: int = 0
    partidos_empatados: int = 0
    partidos_perdidos: int = 0
    goles_favor: int = 0
    goles_contra: int = 0

    def __hash__(self) -> int:
        return hash(self.id_equipo)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Equipo):
            return self.id_equipo == other.id_equipo
        return False

    @property
    def puntos(self) -> int:
        return (self.partidos_ganados * 3) + (self.partidos_empatados * 1)

    @property
    def diferencia_goles(self) -> int:
        return self.goles_favor - self.goles_contra

    @property
    def total_jugadores(self) -> int:
        return len(self.jugadores_ids)


@dataclass
class Partido:
    """
    Representa un encuentro deportivo disputado en el torneo.
    """
    id_partido: str
    equipo_local_id: str
    equipo_visitante_id: str
    goles_local: int
    goles_visitante: int
    fecha_jornada: int = 1
    jugado: bool = True
