# fix_render.py
render_yaml_content = """services:
  # Servicio 1: Backend API (FastAPI)
  - type: web
    name: rag-backend
    env: docker
    dockerfilePath: Dockerfile.backend
    plan: free
    region: oregon
    envVars:
      - key: GEMINI_API_KEY
        sync: false

  # Servicio 2: Frontend UI (Streamlit)
  - type: web
    name: rag-frontend
    env: docker
    dockerfilePath: Dockerfile.frontend
    plan: free
    region: oregon
    envVars:
      - key: BACKEND_URL
        sync: false
"""

with open("render.yaml", "w", encoding="utf-8") as f:
    f.write(render_yaml_content)

print("¡render.yaml actualizado correctamente!")