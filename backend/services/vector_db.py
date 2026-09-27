import chromadb
import uuid
from typing import List, Dict, Any

# Inicializamos ChromaDB de forma local y persistente
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Colección global persistente
collection = chroma_client.get_or_create_collection(name="documentos_tecnicos")

def clear_database():
    """Elimina todos los registros sin destruir el objeto colección."""
    try:
        existing_data = collection.get()
        existing_ids = existing_data.get("ids", [])
        if existing_ids:
            collection.delete(ids=existing_ids)
            print(f"Se limpiaron {len(existing_ids)} registros anteriores de ChromaDB.")
        else:
            print("La base de datos vectorial ya estaba vacía.")
    except Exception as e:
        print(f"Aviso al limpiar la base de datos: {e}")

def store_chunks_in_db(chunks: List[Dict[str, Any]], clear_previous: bool = True):
    """Guarda los fragmentos de texto en la base de datos vectorial con sus metadatos."""
    # 1. Vacía los datos previos sin invalidar la colección importada por otros módulos
    if clear_previous:
        clear_database()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        if chunk["type"] == "text":
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            documents.append(chunk["content"])
            
            # Guardamos metadatos clave
            metadatas.append({
                "page": chunk["page"],
                "source": chunk.get("source", "unknown"),
                "associated_image": chunk.get("associated_image", "")
            })

    # 2. Inserta los nuevos vectores
    if documents:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Indexados {len(documents)} fragmentos en ChromaDB.")