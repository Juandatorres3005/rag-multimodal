import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

@patch("google.generativeai.GenerativeModel")
@patch("backend.main.collection")  # Reemplaza con la referencia exacta a tu variable 'collection' en backend/main.py
def test_query_endpoint_success(mock_collection, mock_gemini_model):
    """Prueba el endpoint /query simulando respuestas de Gemini y ChromaDB."""
    
    # 1. Mock de ChromaDB (Respuesta de recuperación)
    mock_collection.query.return_value = {
        "documents": [["El sistema de frenos requiere mantenimiento cada 10,000 km."]],
        "metadatas": [[{"page": 12, "image_path": "extracted_images/page_12_img1.png"}]]
    }

    # 2. Mock de Gemini API (Respuesta generada)
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Según el manual, el mantenimiento debe realizarse cada 10,000 km."
    mock_model_instance.generate_content.return_value = mock_response
    mock_gemini_model.return_value = mock_model_instance

    # 3. Realizar la petición HTTP al endpoint de la API
    payload = {"question": "¿Cada cuánto se hace el mantenimiento de frenos?"}
    response = client.post("/query", json=payload)

    # 4. Validaciones
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "Según el manual" in data["answer"]
    assert len(data.get("sources", [])) > 0


def test_query_empty_question():
    """Prueba la validación ante una pregunta vacía."""
    response = client.post("/query", json={"question": ""})
    assert response.status_code in [400, 422]  # Unprocessable Entity o Bad Request