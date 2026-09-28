Python
# make_readme.py
readme_content = """# 🚀 Sistema RAG Multimodal - Procesamiento de Documentos Técnicos

Un sistema de **Generación Aumentada por Recuperación (RAG Multimodal)** diseñado para ingerir, indexar y consultar manuales y documentos técnicos en formato PDF que contienen texto, esquemas, tablas e imágenes. La solución utiliza una arquitectura limpia desacoplada, procesamiento en segundo plano, almacenamiento vectorial persistente e inferencia multimodal con **Google Gemini**.

---

## 📐 Arquitectura del Sistema

El sistema implementa una **Arquitectura en Capas / Hexagonal**, separando la capa de transporte (API REST), la lógica de negocio (motor RAG e ingesta) y las integraciones con servicios externos (LLM y Vector Database).

+-----------------------------------------------------------------------+
|                             CAPA DE USUARIO                           |
|                  Streamlit UI (Puerto 8501)                           |
+-----------------------------------------------------------------------+
|
| HTTP / REST
v
+-----------------------------------------------------------------------+
|                             CAPA DE API                               |
|                  FastAPI Backend (Puerto 8000)                        |
|   Endpoints: POST /upload | GET /status/{job_id} | POST /query       |
+-----------------------------------------------------------------------+
|                                      |
(Procesamiento Asíncrono)              (Recuperación & Inferencia)
v                                      v
+-------------------------------+      +--------------------------------+
|    CAPA DE LÓGICA DE NEGO    |      |         MOTOR RAG CORE         |
|  - Extraedor PyMuPDF          |      |  - Búsqueda Semántica / Híbrida|
|  - Layout & Spatial Mapping   |      |  - Prompting Defensivo          |
|  - Chunking Inteligente       |      |  - Retry & Backoff (Tenacity) |
+-------------------------------+      +--------------------------------+
|                                      |
v                                      v
+-----------------------------------------------------------------------+
|                           CAPA DE DATOS E IA                          |
|   ChromaDB (Vector Store)   |   Google Gemini API (Inferencia LLM) |
+-----------------------------------------------------------------------+


---

## 📑 Registro de Decisiones Técnicas (ADR)

| Componente | Tecnología Elegida | Justificación Técnica |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI** | Soporte nativo para asincronía (`async/await`), velocidad de ejecución superior en Python, generación automática de documentación OpenAPI y fácil integración con tareas en segundo plano (`BackgroundTasks`). |
| **Frontend UI** | **Streamlit** | Desarrollo agilizado de interfaces conversacionales interactivas con soporte nativo para renderizado de Markdown, imágenes interactivas e historial de chat. |
| **Vector Database** | **ChromaDB** | Módulo liviano, persistencia en disco o almacenamiento compartible mediante volúmenes de Docker, y soporte optimizado para embeddings sin requerir clusters complejos. |
| **Procesamiento de PDF**| **PyMuPDF (Fitz)** | Alta velocidad de procesamiento de PDFs pesados, capacidad de extraer coordenadas de trazado (*bounding boxes*), fragmentación por páginas e imágenes vectoriales/rasterizadas sin perder resolución. |
| **Inferencia LLM** | **Gemini (gemini-3.8-flash)**| Inferencia multimodal nativa capaz de comprender relaciones contexto-imagen, alto límite de ventana de contexto y excelente relación de latencia/costo. |
| **Resiliencia** | **Tenacity** | Implementación del patrón *Exponential Backoff* para reintentos automáticos ante *rate limits* (HTTP 429) o micro-caídas de red de las APIs de IA. |

---

## 🛠️ Estructura del Proyecto

```text
rag-multimodal/
├── .github/
│   └── workflows/
│       └── docker-ci.yml          # Pipeline de Integración Continua (CI)
├── backend/
│   ├── __init__.py
│   ├── main.py                    # API FastAPI y Endpoints
│   ├── rag_engine.py              # Motor RAG, embeddings e integración con Gemini
│   └── ingestion.py               # Extracción de PDF, mapeo espacial y chunking
├── frontend/
│   └── app.py                     # Interfaz gráfica conversacional en Streamlit
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py          # Pruebas unitarias de procesamiento de datos
│   └── test_api.py                # Pruebas de integración con Mocks (Pytest)
├── docker-compose.yml             # Orquestación de contenedores Backend + Frontend
├── Dockerfile.backend             # Dockerfile optimizado para la API
├── Dockerfile.frontend            # Dockerfile optimizado para la UI
├── requirements.txt               # Dependencias del proyecto
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore                     # Archivos excluidos de Git
└── README.md                      # Documentación del proyecto
⚙️ Configuración e Instalación
Requisitos Previos
Git

Docker Desktop (con WSL 2 habilitado en Windows)

Clave de API de Google Gemini AI Studio

1. Clonar el Repositorio
Bash
git clone [https://github.com/Juandatorres3005/rag-multimodal.git](https://github.com/Juandatorres3005/rag-multimodal.git)
cd rag-multimodal
2. Configurar Variables de Entorno
Crea un archivo .env en la raíz del proyecto tomando como base el archivo .env.example:

Bash
GEMINI_API_KEY=tu_api_key_aqui
🐳 Ejecución con Docker (Recomendado)
Inicia todos los servicios con un solo comando gracias a Docker Compose:

Bash
docker compose up --build
Una vez iniciados los contenedores:

Interfaz de usuario (Streamlit): http://localhost:8501

Documentación interactiva de la API (Swagger UI): http://localhost:8000/docs

Para detener la aplicación:

Bash
docker compose down
🧪 Pruebas Unitarias e Integración (pytest)
El proyecto cuenta con una suite de pruebas que aísla las APIs de terceros mediante Mocks (unittest.mock), garantizando la ejecución de pruebas sin costo ni dependencia de conexión a internet.

Para ejecutar las pruebas localmente:

Bash
pytest -v
El pipeline de GitHub Actions (.github/workflows/docker-ci.yml) ejecuta automáticamente estos tests en cada push o pull_request a la rama principal.

🔌 API Reference
1. Ingesta Asíncrona de PDF
POST /upload

Response:

JSON
{
  "job_id": "a1b2c3d4-e5f6-7890",
  "status": "Pending",
  "message": "El documento se está procesando en segundo plano."
}
2. Estado de Procesamiento
GET /status/{job_id}

Response:

JSON
{
  "job_id": "a1b2c3d4-e5f6-7890",
  "status": "Completed",
  "chunks_processed": 42,
  "images_extracted": 5
}
3. Consulta RAG Multimodal
POST /query

Request Body:

JSON
{
  "question": "¿Cuál es la tolerancia de torque de la bomba hidráulica?"
}
Response:

JSON
{
  "answer": "Según el manual técnico, la tolerancia de torque es de 25 Nm ± 2. [Fuente: Manual_Motor.pdf, Página 14]",
  "sources": [
    {
      "page": 14,
      "source": "Manual_Motor.pdf",
      "image_path": "extracted_images/page_14_img1.png"
    }
  ]
}
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("¡README.md generado con éxito!")

---

## 🌐 Demostración en la Nube (Deployment)

El sistema se encuentra desplegado y funcional en Render:
* **Aplicación Web (Streamlit UI):** https://rag-frontend-5v5h.onrender.com
* **Documentación interactiva de la API (FastAPI Docs):** https://rag-backend-5v5h.onrender.com/docs
