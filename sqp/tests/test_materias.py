"""
tests/test_materias.py
Pruebas unitarias para el módulo de materias.
Cobertura actual: ~50% — el equipo debe completar hasta ≥85%.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from src.models.database import reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_db():
    reset_db()
    yield
    reset_db()


class TestCrearMateria:

    def test_crear_materia_exitosa(self):
        payload = {"codigo": "CS101", "nombre": "Calidad del Software", "creditos": 3}
        response = client.post("/materias/", json=payload)
        assert response.status_code == 201
        assert response.json()["codigo"] == "CS101"

    def test_crear_materia_creditos_invalidos(self):
        payload = {"codigo": "CS101", "nombre": "Materia", "creditos": 0}
        response = client.post("/materias/", json=payload)
        assert response.status_code == 400

    def test_crear_materia_duplicada(self):
        payload = {"codigo": "CS101", "nombre": "Materia", "creditos": 3}
        client.post("/materias/", json=payload)
        response = client.post("/materias/", json=payload)
        assert response.status_code == 400


class TestObtenerMateria:

    def test_obtener_materia_existente(self):
        client.post("/materias/", json={"codigo": "CS101", "nombre": "Calidad", "creditos": 3})
        response = client.get("/materias/CS101")
        assert response.status_code == 200

    def test_obtener_materia_inexistente(self):
        response = client.get("/materias/XX999")
        assert response.status_code == 404


# ─────────────────────────────────────────────────────────────
#  TODO para el equipo:
#  Agregar tests para:
#  - test_listar_materias_vacio
#  - test_listar_materias_con_datos
#  - test_eliminar_materia_existente
#  - test_eliminar_materia_inexistente
#  - test_crear_materia_con_descripcion
#  - test_creditos_maximo_valido (creditos=6)
#  - test_codigo_se_convierte_a_mayusculas
# ─────────────────────────────────────────────────────────────
class TestListarMaterias:

    def test_listar_materias_vacio(self):
        response = client.get("/materias/")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_materias_con_datos(self):
        client.post("/materias/", json={"codigo": "CS101", "nombre": "Calidad", "creditos": 3})
        client.post("/materias/", json={"codigo": "CS102", "nombre": "Redes", "creditos": 4})
        response = client.get("/materias/")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestEliminarMateria:

    def test_eliminar_materia_existente(self):
        client.post("/materias/", json={"codigo": "CS101", "nombre": "Calidad", "creditos": 3})
        response = client.delete("/materias/CS101")
        assert response.status_code == 204
        assert client.get("/materias/CS101").status_code == 404

    def test_eliminar_materia_inexistente(self):
        response = client.delete("/materias/XX999")
        assert response.status_code == 404


class TestValidacionesMateria:

    def test_crear_materia_con_descripcion(self):
        payload = {
            "codigo": "CS101",
            "nombre": "Calidad del Software",
            "creditos": 3,
            "descripcion": "Fundamentos de calidad y pruebas"
        }
        response = client.post("/materias/", json=payload)
        assert response.status_code == 201
        assert response.json()["descripcion"] == "Fundamentos de calidad y pruebas"

    def test_creditos_maximo_valido(self):
        payload = {"codigo": "CS101", "nombre": "Materia Intensa", "creditos": 6}
        response = client.post("/materias/", json=payload)
        assert response.status_code == 201
        assert response.json()["creditos"] == 6

    def test_codigo_se_convierte_a_mayusculas(self):
        payload = {"codigo": "cs101", "nombre": "Calidad", "creditos": 3}
        response = client.post("/materias/", json=payload)
        assert response.status_code == 201
        assert response.json()["codigo"] == "CS101"