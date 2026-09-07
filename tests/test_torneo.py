"""
Pruebas Unitarias para el Sistema de Gestión de Torneo de Fútbol.
Verifica el correcto funcionamiento de Conjuntos (set) y Mapas (dict),
así como las operaciones de la Teoría de Conjuntos.
"""

import unittest
from src.gestor_torneo import GestorTorneo
from src.models import Posicion
from src.benchmark import AnalizadorRendimiento


class TestGestorTorneo(unittest.TestCase):

    def setUp(self):
        """Inicializa una instancia limpia de GestorTorneo antes de cada prueba."""
        self.gestor = GestorTorneo("Torneo de Prueba UEA")

        # Equipos base para pruebas
        self.gestor.registrar_equipo("PAS", "Pastaza FC", "Puyo", "DT 1", "Grupo A")
        self.gestor.registrar_equipo("NAP", "Deportivo Napo", "Tena", "DT 2", "Grupo A")

    def test_registro_equipos_en_mapa(self):
        """Verifica almacenamiento O(1) e inviolabilidad de claves en el mapa de equipos."""
        equipo = self.gestor.consultar_equipo("PAS")
        self.assertIsNotNone(equipo)
        self.assertEqual(equipo.nombre, "Pastaza FC")
        self.assertEqual(equipo.ciudad, "Puyo")

        # No permitir duplicados de ID de equipo
        ok, msg = self.gestor.registrar_equipo("PAS", "Otro Pastaza", "Puyo", "DT X")
        self.assertFalse(ok)
        self.assertIn("ya se encuentra registrado", msg)

    def test_registro_jugadores_en_conjuntos_y_mapas(self):
        """Verifica que el jugador se registre en el mapa global y en el conjunto del equipo."""
        ok, msg = self.gestor.registrar_jugador(
            cedula="1600112233",
            nombre="Mateo Cahuasqui",
            edad=22,
            posicion=Posicion.PORTERO,
            dorsal=1,
            equipo_id="PAS"
        )
        self.assertTrue(ok)

        # Verificación en Mapa O(1)
        jugador = self.gestor.consultar_jugador("1600112233")
        self.assertIsNotNone(jugador)
        self.assertEqual(jugador.nombre, "Mateo Cahuasqui")

        # Verificación en Conjunto Global O(1)
        self.assertIn("1600112233", self.gestor.conjunto_todos_jugadores)

        # Verificación en Conjunto del Equipo
        equipo_pas = self.gestor.consultar_equipo("PAS")
        self.assertIn("1600112233", equipo_pas.jugadores_ids)

    def test_unicidad_cedula_y_dorsal(self):
        """Valida que no se permitan cédulas duplicadas ni dorsales repetidos en el mismo equipo."""
        self.gestor.registrar_jugador("1600112233", "Mateo", 22, Posicion.PORTERO, 1, "PAS")

        # Cédula duplicada
        ok_ced, msg_ced = self.gestor.registrar_jugador("1600112233", "Clon", 20, Posicion.DEFENSA, 2, "PAS")
        self.assertFalse(ok_ced)
        self.assertIn("ya pertenece a un jugador registrado", msg_ced)

        # Dorsal duplicado en el mismo equipo
        ok_dor, msg_dor = self.gestor.registrar_jugador("1600999999", "Otro", 25, Posicion.DELANTERO, 1, "PAS")
        self.assertFalse(ok_dor)
        self.assertIn("ya está asignado", msg_dor)

    def test_transferencia_jugador(self):
        """Valida la migración de un elemento entre conjuntos de dos clubes."""
        self.gestor.registrar_jugador("1600112233", "Mateo", 22, Posicion.PORTERO, 1, "PAS")
        equipo_pas = self.gestor.consultar_equipo("PAS")
        equipo_nap = self.gestor.consultar_equipo("NAP")

        self.assertIn("1600112233", equipo_pas.jugadores_ids)
        self.assertNotIn("1600112233", equipo_nap.jugadores_ids)

        ok, msg = self.gestor.transferir_jugador("1600112233", "NAP")
        self.assertTrue(ok)
        self.assertNotIn("1600112233", equipo_pas.jugadores_ids)
        self.assertIn("1600112233", equipo_nap.jugadores_ids)

    def test_operacion_conjuntos_diferencia_habilitados(self):
        """
        Prueba la operación de DIFERENCIA (A - B):
        Habilitados = Nómina del Equipo - Jugadores Sancionados.
        """
        self.gestor.registrar_jugador("1600112233", "Mateo", 22, Posicion.PORTERO, 1, "PAS")
        self.gestor.registrar_jugador("1600223344", "Andrés", 24, Posicion.DEFENSA, 2, "PAS")
        self.gestor.registrar_jugador("1600334455", "Christian", 21, Posicion.DEFENSA, 4, "PAS")

        # Inicialmente todos están habilitados
        habilitados = self.gestor.obtener_jugadores_habilitados("PAS")
        self.assertEqual(len(habilitados), 3)

        # Sancionar a Christian con tarjeta roja
        self.gestor.aplicar_tarjeta("1600334455", tipo="roja")
        self.assertIn("1600334455", self.gestor.conjunto_sancionados)

        # Ahora los habilitados deben ser únicamente 2 (A - B)
        habilitados_post = self.gestor.obtener_jugadores_habilitados("PAS")
        self.assertEqual(len(habilitados_post), 2)
        self.assertIn("1600112233", habilitados_post)
        self.assertIn("1600223344", habilitados_post)
        self.assertNotIn("1600334455", habilitados_post)

        # Levantar sanción
        self.gestor.levantar_sancion("1600334455")
        habilitados_restituidos = self.gestor.obtener_jugadores_habilitados("PAS")
        self.assertEqual(len(habilitados_restituidos), 3)

    def test_operacion_conjuntos_interseccion_auditoria(self):
        """
        Prueba la operación de INTERSECCIÓN (A ∩ B) para detectar
        irregularidades de doble fichaje.
        """
        self.gestor.registrar_jugador("1600112233", "Mateo", 22, Posicion.PORTERO, 1, "PAS")
        self.gestor.registrar_jugador("1500112233", "Carlos", 23, Posicion.PORTERO, 1, "NAP")

        # Sin conflicto inicialmente
        conflictos = self.gestor.auditoria_doble_inscripcion()
        self.assertEqual(len(conflictos), 0)

        # Forzar manualmente una doble inscripción en ambos conjuntos
        equipo_nap = self.gestor.consultar_equipo("NAP")
        equipo_nap.jugadores_ids.add("1600112233")

        # Ahora la auditoría debe detectar la intersección no vacía
        conflictos_post = self.gestor.auditoria_doble_inscripcion()
        self.assertEqual(len(conflictos_post), 1)
        self.assertIn(("PAS", "NAP"), conflictos_post)
        self.assertIn("1600112233", conflictos_post[("PAS", "NAP")])

    def test_operacion_conjuntos_subconjunto_alineacion(self):
        """
        Prueba la verificación de SUBCONJUNTO (X ⊆ A) y disyunción con sanciones.
        """
        self.gestor.registrar_jugador("1600112233", "Mateo", 22, Posicion.PORTERO, 1, "PAS")
        self.gestor.registrar_jugador("1600223344", "Andrés", 24, Posicion.DEFENSA, 2, "PAS")

        # Alineación válida (subconjunto propio)
        valido, err = self.gestor.validar_alineacion("PAS", {"1600112233", "1600223344"})
        self.assertTrue(valido)
        self.assertEqual(len(err), 0)

        # Alineación con jugador no inscrito (no es subconjunto)
        invalido, err_no_inscrito = self.gestor.validar_alineacion("PAS", {"1600112233", "9999999999"})
        self.assertFalse(invalido)
        self.assertTrue(any("NO están inscritos" in e for e in err_no_inscrito))

        # Alineación con jugador sancionado
        self.gestor.aplicar_tarjeta("1600223344", tipo="roja")
        invalido_sancionado, err_sancionado = self.gestor.validar_alineacion("PAS", {"1600112233", "1600223344"})
        self.assertFalse(invalido_sancionado)
        self.assertTrue(any("suspendidos/sancionados" in e for e in err_sancionado))

    def test_tabla_posiciones_y_partidos(self):
        """Verifica el cálculo de tabla de posiciones mediante mapas de métricas."""
        self.gestor.registrar_partido("P1", "PAS", "NAP", 3, 1, jornada=1)

        pas = self.gestor.consultar_equipo("PAS")
        nap = self.gestor.consultar_equipo("NAP")

        self.assertEqual(pas.partidos_jugados, 1)
        self.assertEqual(pas.partidos_ganados, 1)
        self.assertEqual(pas.puntos, 3)
        self.assertEqual(pas.diferencia_goles, 2)

        self.assertEqual(nap.partidos_jugados, 1)
        self.assertEqual(nap.partidos_perdidos, 1)
        self.assertEqual(nap.puntos, 0)
        self.assertEqual(nap.diferencia_goles, -2)

        tabla = self.gestor.obtener_tabla_posiciones()
        self.assertEqual(tabla[0].id_equipo, "PAS")
        self.assertEqual(tabla[1].id_equipo, "NAP")

    def test_benchmark_algoritmico(self):
        """Verifica que el analizador de rendimiento ejecute sin excepciones."""
        resultados = AnalizadorRendimiento.medir_busqueda_pertenencia([100, 1000])
        self.assertEqual(len(resultados), 2)
        self.assertGreater(resultados[0]["tiempo_lista_us"], 0)
        self.assertGreater(resultados[0]["tiempo_set_us"], 0)


if __name__ == "__main__":
    unittest.main()
