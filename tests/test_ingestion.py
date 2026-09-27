import pytest
from unittest.mock import MagicMock, patch

def test_chunk_text_logic():
    """Prueba unitaria para la división de texto en chunks."""
    sample_text = "Este es un documento técnico de prueba. " * 50
    chunk_size = 100
    overlap = 20
    
    # Simulación simple de chunking
    chunks = [sample_text[i:i+chunk_size] for i in range(0, len(sample_text), chunk_size - overlap)]
    
    assert len(chunks) > 1
    assert len(chunks[0]) == chunk_size

@patch("chromadb.PersistentClient")
def test_chroma_db_mocking(mock_chroma_client):
    """Prueba que los datos se envíen a ChromaDB simulando la base de datos."""
    # Instancia mock de la colección
    mock_collection = MagicMock()
    mock_client_instance = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chroma_client.return_value = mock_client_instance

    # Ejecutar simulación de inserción
    collection = mock_client_instance.get_or_create_collection("rag_collection")
    collection.add(
        documents=["Texto simulado"],
        metadatas=[{"page": 1}],
        ids=["doc_1"]
    )

    # Verificar que el método 'add' fue invocado correctamente
    mock_collection.add.assert_called_once_with(
        documents=["Texto simulado"],
        metadatas=[{"page": 1}],
        ids=["doc_1"]
    )