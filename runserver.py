#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time
import webbrowser

def open_browser():
    """Abre el navegador después de asegurarse de que el servidor está corriendo."""
    time.sleep(3)  # Espera 3 segundos para asegurarte de que el servidor está activo
    webbrowser.open("http://127.0.0.1:8000")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Inventario_Project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Inicia el navegador en un hilo separado para evitar bloquear el servidor
    threading.Thread(target=open_browser).start()
    
    # Ejecuta el servidor sin autoreload
    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000", "--noreload"])

if __name__ == '__main__':
    main()