from yt_dlp import YoutubeDL
from pathlib import Path

def extraer_metadatos(url: str) -> dict | None:
    '''
    Extrae la información técnica, título y miniatura
    de un vídeo sin descargarlo
    '''
    # Opciones de busqueda
    ydl_opts = {
        'skip_download' : True,
        'quiet' : True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            formatos = info.get('formats', [])
            resoluciones = set()

            for f in formatos:
                alto = f.get('height')
                if alto and f.get('vcodec') != 'none':
                    resoluciones.add(f'{alto}p')

            formatos_ordenados = sorted(list(resoluciones), key=lambda x: int(x.replace('p', '')), reverse=True)

            if not formatos_ordenados:
                formatos_ordenados = ['best']

            return {
                'titulo' : info.get('title', 'No Title'),
                'duracion' : f'{info.get("duration", 0) // 60}m {info.get("duration", 0) % 60}s',
                'autor' : info.get('uploader', 'Desconocido'),
                'thumb_url' : info.get('thumbnail'),
                'url' : url,
                'resoluciones' : formatos_ordenados
            }
    except Exception as e:
        print(f'Error al extraer datos con yt-dlp: {e}')
        return None
    
def descargar_video(url: str, calidad: str) -> bool:
    '''
    Descarga el video en la mejor calidad disponible
    en la carpeta descargas del usuario
    '''
    # Rutas de la carpeta descargas del usuario y destino de el archivo descargado
    ruta_descarga = Path.home() / 'Downloads'
    ruta_salida = str(ruta_descarga / '%(title)s.mp4')

    resolucion = calidad.replace('p', '')
    resolucion_formato = f'bestvideo[height<={resolucion}]+bestaudio/best[height<={resolucion}]'

    # Opciones de descarga
    ydl_opts = {
        'format' : resolucion_formato,
        'merge_output_format' : 'mp4',
        'remux_video' : 'mp4',
        'outtmpl' : ruta_salida,
        'quiet' : True,
    }

    try:
        print(f'Descargando en {resolucion_formato} a {ruta_descarga}')
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
            return True
    except Exception as e:
        print(f'Error durante la descarga: {e}')
        return False