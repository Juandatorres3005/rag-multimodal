from typing import Dict, Any, List
from backend.services.vector_db import collection
from backend.ports.llm_provider import LLMProvider

def query_rag_system(query: str, llm_provider: LLMProvider, top_k: int = 3) -> Dict[str, Any]:
    # 1. Búsqueda vectorial de los chunks más similares
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    
    if not documents:
        return {
            "answer": "No se encontró información Relevante en el documento.",
            "sources": [],
            "images": []
        }
    
    # 2. Construcción del contexto y recolección de metadatos/imágenes
    context = "\n---\n".join(documents)
    sources = []
    associated_images = []
    
    for meta in metadatas:
        source_info = f"Fuente: {meta.get('source', 'Documento')}, Página {meta.get('page', 'N/A')}"
        if source_info not in sources:
            sources.append(source_info)
            
        img_path = meta.get("associated_image")
        if img_path and img_path not in associated_images:
            associated_images.append(img_path)
            
    # 3. Generación de respuesta con Gemini
    answer = llm_provider.generate_response(prompt=query, context=context)
    
    return {
        "answer": answer,
        "sources": sources,
        "images": associated_images
    }