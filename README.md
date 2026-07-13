# 🎬 YT-DLP Selector de Calidad Dinámico (CustomTkinter GUI)

Una aplicación de escritorio de alto rendimiento desarrollada en Python para la gestión y descarga personalizada de flujos multimedia. Cuenta con una interfaz gráfica interactiva construida con `CustomTkinter` y un potente motor de extracción basado en `yt-dlp` que analiza los servidores de origen para ofrecer al usuario un menú desplegable con las resoluciones reales disponibles del video.

El diseño del software implementa de forma estricta el **Principio de Responsabilidad Única (SRP)** y técnicas avanzadas de **Concurrencia mediante Hilos (Multithreading)** para garantizar que la interfaz gráfica permanezca fluida y reactiva en todo momento.

## ⚖️ Descargo de Responsabilidad (Disclaimer)

**IMPORTANTE:** Esta aplicación ha sido desarrollada exclusivamente como un proyecto académico y de demostración técnica para portafolio de ingeniería de software. 

*   El desarrollador **no promueve, fomenta ni facilita** la descarga de material protegido por derechos de autor sin la autorización explícita del titular.
*   El usuario final es el **único y absoluto responsable** de asegurar que el uso de esta herramienta cumpla con los Términos de Servicio de las plataformas consultadas (como YouTube) y las leyes de propiedad intelectual de su jurisdicción. 
*   Se prohíbe el uso de este software para cualquier fin comercial o distribución no autorizada de contenido con *copyright*.

## 🚀 Características Clave

*   **Extracción de Calidades Dinámicas:** Análisis en tiempo real de los manifiestos del video para poblar un componente `CTkOptionMenu` únicamente con las resoluciones físicas existentes (ej. 1080p, 720p, 480p), evitando errores de solicitud por formatos inexistentes.
*   **Saneamiento de Entradas (Sanitization):** Algoritmo automatizado que procesa y limpia la URL del cuadro de texto (`.split('&')`), eliminando parámetros basura de rastreo o listas de reproducción pesadas que congelan los motores de renderizado.
*   **Asincronía en Red (Multithreading):** Uso de la librería nativa `threading` para aislar los procesos pesados de red (análisis de metadatos y descargas en HD) en hilos secundarios, previniendo que la ventana principal de Windows entre en estado "No Responde".
*   **Fusión HD y Remuxing (FFmpeg Portable):** Integración del puente `imageio-ffmpeg` para autogestionar los binarios de codificación desde el entorno virtual de Python. Esto permite fusionar pistas de alta resolución de video y audio en contenedores universales `.mp4` sin instalaciones externas en el sistema operativo.
*   **Portabilidad Dinámica:** Almacenamiento directo mediante `pathlib.Path.home()` hacia la carpeta de *Descargas* del usuario, haciendo el código agnóstico a la estructura de archivos de la máquina donde se ejecute.

## 📁 Estructura del Software

```text
descarga_yt/
│
├── requirements.txt     # Dependencias de producción (customtkinter, yt-dlp, pillow...)
├── README.md            # Documentación técnica e institucional
│
└── src/
    ├── __init__.py
    ├── motor_video.py   # Responsabilidad ÚNICA: Extracción analítica de formatos y descargas
    └── interfaz.py       # Responsabilidad ÚNICA: Gestión de layouts estéticos, widgets y subprocesos
```

## 🛠️ Requisitos e Instalación

### 1. Preparar Entorno Local (Windows)
```bash
git clone https://github.com/lermogdaniel/Descargador_videos_GUI.git
cd descarga_yt

# Configuración del entorno virtual
python -m venv myenv
myenv\Scripts\activate

# Instalación empaquetada de dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la Herramienta
Inicia la interfaz gráfica desde la raíz del proyecto ejecutando:
```bash
python main.py
```

## ⚙️ Notas de Optimización para Producción
Para garantizar el bypass óptimo de los desafíos JavaScript (*n-challenges*) impuestos por los servidores de streaming y asegurar el máximo ancho de banda en la descarga, se recomienda contar con un entorno de ejecución de JavaScript como `Deno` o `Node.js` registrado en el `PATH` del sistema de la máquina local.

---
Desarrollado con un enfoque en Concurrencia y Lógica Defensiva por Daniel Lermo Gutiérrez.
