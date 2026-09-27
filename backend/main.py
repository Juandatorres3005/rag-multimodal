import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ports.llm_provider import GeminiProvider
from backend.services.rag import query_rag_system
from backend.services.vector_db import store_chunks_in_db
from backend.services.ingestion import process_pdf

app = FastAPI(
    title="RAG Multimodal API",
    description="Backend para procesamiento de PDFs e inferencia con RAG y Gemini",
    version="1.0.0"
)

# Habilitar CORS para integración segura con el cliente Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia única del proveedor de lenguaje (Gemini)
llm_service = GeminiProvider()

# Esquema para la consulta
class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Servidor RAG Multimodal en ejecución."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Recibe un archivo PDF, extrae texto e imágenes e indexa los vectores en ChromaDB."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo enviado debe ser de formato PDF.")

    temp_file_path = f"temp_{file.filename}"
    try:
        # Guardar temporalmente el PDF recibido
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Extraer fragmentos e imágenes asociadas
        chunks = process_pdf(temp_file_path)

        # 2. Guardar vectores en ChromaDB limpiando la colección previa
        store_chunks_in_db(chunks, clear_previous=True)

        return {
            "status": "success",
            "message": f"Archivo '{file.filename}' procesado e indexado con éxito.",
            "chunks_count": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el PDF: {str(e)}")

    finally:
        # Eliminación del archivo temporal
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/query")
async def query_index(request: QueryRequest):
    """Atiende preguntas del usuario buscando en ChromaDB e infiriendo con Gemini."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta ingresada no puede estar vacía.")

    try:
        response = query_rag_system(
            query=request.question,
            llm_provider=llm_service
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el flujo RAG: {str(e)}")