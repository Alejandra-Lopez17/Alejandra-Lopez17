#!/usr/bin/env python
"""
Script para ejecutar la aplicación Streamlit del proyecto.

Uso:
    python run_streamlit.py
    python run_streamlit.py --db-path data/tech_docs_db
"""

import sys
import subprocess
from pathlib import Path


def main():
    # Ruta por defecto a la base de datos
    db_path = "data/tech_docs_db"

    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--db-path":
        if len(sys.argv) > 2:
            db_path = sys.argv[2]

    # Verificar que la base de datos exista
    db_path_obj = Path(db_path)
    if not db_path_obj.exists():
        print(f"⚠️ Advertencia: La base de datos '{db_path}' no existe.")
        print("   Ejecute primero el pipeline de ingestión:")
        print(f"   python -m src.interfaces.cli.main process data/documents")
        print()

    # Construir comando
    app_path = Path(__file__).parent / "src" / "interfaces" / "web" / "streamlit_app.py"

    cmd = [
        sys.executable,  # Usar el mismo Python
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--",
        "--db-path",
        db_path,
    ]

    print("🚀 Iniciando Explorador de Documentos...")
    print(f"   Base de datos: {db_path}")
    print()

    # Ejecutar Streamlit
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
