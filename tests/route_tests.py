import unittest
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.major_name = "compu"
        self.token = "test+test_secret"
        self.headers = {
            'Authorization' : f"Bearer {self.token}"
        }


    def test_read_major(self):
        response = client.get(f"/major/{self.major_name}")
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response body and data

    def test_update_major(self):
        major_payload = {
            "nombre": f"Major del alumno {self.token.split('+')[0]}",
            "requisitos": {
                "relacion": "AND",
                "subrequisitos": [
                    {
                        "nombre": "Pack 1",
                        "relacion": "AND",
                        "subrequisitos": [
                            "IIC2333",
                            "ICE2164",
                            "AFE4326"
                        ]
                    },
                    {
                        "nombre": "Pack 2",
                        "relacion": "AND",
                        "subrequisitos": [
                            "IIC3257",
                            "IGM6547",
                            "IIC6424"
                        ]
                    },
                    {
                        "nombre": "Track",
                        "relacion": "OR",
                        "subrequisitos": [
                            {
                                "nombre": "Track 1",
                                "relacion": "AND",
                                "subrequisitos": [
                                    "IIC2343",
                                    "IIC2613"
                                ]
                            },
                            {
                                "nombre": "Track 2",
                                "relacion": "AND",
                                "subrequisitos": [
                                    "IIC2713",
                                    "IIC2733"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        response = client.put(f"/major/{self.major_name}", json=major_payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response body and data

    def test_validate_major(self):
        cursos_aprobados = ["course1", "course2"]
        response = client.post(f"/major/{self.major_name}/validate", json={"cursos_aprobados": cursos_aprobados})
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response body and data

    def test_read_major_packages(self):
        response = client.get(f"/major/{self.major_name}/packages")
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response body and data

    def test_delete_major(self):
        response = client.delete(f"/major/{self.major_name}/IIC2333" , headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response body and data

    def test_update_major_invalid_structure(self):
        major_payload = {
            "invalid_key": "value"
        }
        response = client.put(f"/major/{self.major_name}", json=major_payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        # Add assertions to validate the response body and data

    def test_update_major_missing_key(self):
        major_payload = {
            "nombre": "Major del alumno 17640040",
            # Missing the "requisitos" key
        }
        response = client.put(f"/major/{self.major_name}", json=major_payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        # Add assertions to validate the response body and data


if __name__ == "__main__":
    unittest.main()

