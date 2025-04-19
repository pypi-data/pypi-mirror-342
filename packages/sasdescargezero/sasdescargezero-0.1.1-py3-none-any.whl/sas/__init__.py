from .downloader import SASDownloader

__version__ = "0.1.0"

# Crear una instancia global de SASDownloader al importar el módulo
_downloader = SASDownloader()

def download(urls):
    """Función principal para iniciar la descarga de archivos."""
    _downloader.process_urls(urls)

# Mostrar mensaje para ingresar el enlace al importar
print(" • >> ", end="")
urls = input()
if urls.strip():
    download(urls)
