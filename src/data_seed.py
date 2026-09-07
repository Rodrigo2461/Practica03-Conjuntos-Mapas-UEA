"""
Generador de Datos Iniciales (Seed Data).
Carga equipos, futbolistas y encuentros deportivos representativos
de la región amazónica ecuatoriana para demostración del sistema.
"""

from src.gestor_torneo import GestorTorneo
from src.models import Posicion


def cargar_datos_demostracion(gestor: GestorTorneo) -> None:
    """
    Inicializa el torneo con equipos, plantillas y partidos
    que permiten evidenciar de inmediato todas las operaciones
    de conjuntos, mapas y reportería.
    """
    # 1. Registro de Equipos (Mapas de Equipos)
    equipos_iniciales = [
        ("PAS", "Pastaza Sporting Club", "Puyo", "Prof. Carlos Mera", "Grupo Amazónico"),
        ("NAP", "Deportivo Napo", "Tena", "Prof. Edwin Rivadeneyra", "Grupo Amazónico"),
        ("ORE", "Amazonía Orellana FC", "El Coca", "Prof. Marcelo Gaibor", "Grupo Amazónico"),
        ("SUC", "Atlético Sucumbíos", "Nueva Loja", "Prof. Washington Guevara", "Grupo Amazónico"),
    ]

    for id_eq, nom, ciu, dt, cat in equipos_iniciales:
        gestor.registrar_equipo(id_eq, nom, ciu, dt, cat)

    # 2. Registro de Jugadores por Equipo
    # Pastaza Sporting Club (PAS)
    jugadores_pastaza = [
        ("1600112233", "Mateo Cahuasqui", 22, Posicion.PORTERO, 1),
        ("1600223344", "Andrés Villamarín", 24, Posicion.DEFENSA, 2),
        ("1600334455", "Christian Palacios", 21, Posicion.DEFENSA, 4),
        ("1600445566", "Javier Chimbo", 25, Posicion.MEDIOCAMPISTA, 8),
        ("1600556677", "David Quishpe", 20, Posicion.DELANTERO, 9),
        ("1600667788", "Luis Curipallo", 23, Posicion.DELANTERO, 11),
    ]
    for ced, nom, ed, pos, dor in jugadores_pastaza:
        gestor.registrar_jugador(ced, nom, ed, pos, dor, "PAS")

    # Deportivo Napo (NAP)
    jugadores_napo = [
        ("1500112233", "Carlos Shiguango", 23, Posicion.PORTERO, 1),
        ("1500223344", "Gabriel Tapuy", 22, Posicion.DEFENSA, 3),
        ("1500334455", "Wilson Cerda", 26, Posicion.MEDIOCAMPISTA, 10),
        ("1500445566", "Holger Grefa", 24, Posicion.MEDIOCAMPISTA, 7),
        ("1500556677", "Santiago Andi", 20, Posicion.DELANTERO, 9),
    ]
    for ced, nom, ed, pos, dor in jugadores_napo:
        gestor.registrar_jugador(ced, nom, ed, pos, dor, "NAP")

    # Amazonía Orellana FC (ORE)
    jugadores_orellana = [
        ("2200112233", "Bryan Vaca", 21, Posicion.PORTERO, 1),
        ("2200223344", "Nelson Tanguila", 25, Posicion.DEFENSA, 4),
        ("2200334455", "Kevin Coquinche", 22, Posicion.MEDIOCAMPISTA, 6),
        ("2200445566", "Jhonatan Alvarado", 23, Posicion.DELANTERO, 9),
        ("2200556677", "Mauricio Jumbo", 27, Posicion.DELANTERO, 18),
    ]
    for ced, nom, ed, pos, dor in jugadores_orellana:
        gestor.registrar_jugador(ced, nom, ed, pos, dor, "ORE")

    # Atlético Sucumbíos (SUC)
    jugadores_sucumbios = [
        ("2100112233", "Darwin Castillo", 24, Posicion.PORTERO, 12),
        ("2100223344", "Anthony Bone", 23, Posicion.DEFENSA, 2),
        ("2100334455", "Jefferson Nazareno", 22, Posicion.MEDIOCAMPISTA, 8),
        ("2100445566", "Miller Bolaños Jr", 21, Posicion.DELANTERO, 11),
    ]
    for ced, nom, ed, pos, dor in jugadores_sucumbios:
        gestor.registrar_jugador(ced, nom, ed, pos, dor, "SUC")

    # 3. Aplicación de Sanciones para Demostración de Conjuntos
    # Tarjeta roja directa a Christian Palacios (Pastaza)
    gestor.aplicar_tarjeta("1600334455", tipo="roja")
    # 3 amarillas acumuladas a Wilson Cerda (Napo)
    gestor.aplicar_tarjeta("1500334455", tipo="amarilla")
    gestor.aplicar_tarjeta("1500334455", tipo="amarilla")
    gestor.aplicar_tarjeta("1500334455", tipo="amarilla")

    # 4. Registro de Partidos Disputados (Actualiza Tabla de Posiciones)
    gestor.registrar_partido("PAR_01", "PAS", "NAP", 2, 1, jornada=1)
    gestor.registrar_partido("PAR_02", "ORE", "SUC", 3, 2, jornada=1)
    gestor.registrar_partido("PAR_03", "PAS", "ORE", 1, 1, jornada=2)
    gestor.registrar_partido("PAR_04", "NAP", "SUC", 2, 0, jornada=2)
