import fitz  # PyMuPDF
import os
from typing import List, Dict, Any

IMAGE_OUTPUT_DIR = "./extracted_images"
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

def process_pdf(pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    doc = fitz.open(pdf_path)
    chunks = []
    
    filename = os.path.basename(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. Extraer imágenes de la página
        image_list = page.get_images(full=True)
        page_image_path = ""
        
        if image_list:
            # Tomamos la primera imagen relevante de la página
            xref = image_list[0][0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            img_filename = f"page_{page_num + 1}_img1.{image_ext}"
            page_image_path = os.path.join(IMAGE_OUTPUT_DIR, img_filename)
            
            with open(page_image_path, "wb") as f:
                f.write(image_bytes)

        # 2. Extraer texto y dividirlo en chunks
        text = page.get_text()
        if not text.strip():
            continue

        # Fragmentación simple por tamaño de palabras/caracteres
        words = text.split()
        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunk_text = " ".join(words[i : i + chunk_size])
            chunks.append({
                "type": "text",
                "content": chunk_text,
                "page": page_num + 1,
                "source": filename,
                "associated_image": page_image_path if page_image_path else ""
            })

    doc.close()
    return chunks