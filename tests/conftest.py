import sys
import os

# Registrar el directorio raíz del proyecto en el PYTHONPATH de pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
