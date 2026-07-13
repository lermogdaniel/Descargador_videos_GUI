import customtkinter as ctk
import threading
import io
import requests
from PIL import Image
from src.motor_video import extraer_metadatos, descargar_video

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class DescargadorYoutube(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1280x720')
        self.title('Youtube Downloader')

        self.video_actual_url = None

        # --- PANEL DE BUSQUEDA --- #
        self.frame_busqueda = ctk.CTkFrame(self, corner_radius=10)
        self.frame_busqueda.pack(pady=20, padx=20, fill='x')

        self.input_url = ctk.CTkEntry(
            self.frame_busqueda, 
            placeholder_text='Pega el enlace del video aquí (Youtube, Vimeo etc...)', width=450)
        self.input_url.pack(side='left', padx=15, pady=15, fill='x', expand=True)

        self.boton_buscar = ctk.CTkButton(
            self.frame_busqueda, 
            text='Buscar',
            command=self.busqueda_asincrona
        )
        self.boton_buscar.pack(side='left', padx=15, pady=15)

        # --- PANEL DE METADATOS (Oculto al inicio) --- #
        self.frame_info = ctk.CTkFrame(self, corner_radius=10, fg_color='transparent')

        self.label_miniatura = ctk.CTkLabel(self.frame_info, text='') # Contenedor de la imagen
        self.label_miniatura.pack(pady=10)

        self.label_titulo = ctk.CTkLabel(self.frame_info, text='', font=ctk.CTkFont(size=14, weight='bold'), wraplength=600)
        self.label_titulo.pack(pady=5)

        self.label_detalles = ctk.CTkLabel(self.frame_info, text='', font=ctk.CTkFont(size=12), text_color='gray')
        self.label_detalles.pack(pady=5)

        self.boton_descargar = ctk.CTkButton(
            self.frame_info, 
            text='Descargar', 
            fg_color='#10B981', 
            hover_color='#059669',
            command=self.iniciar_descarga
        )
        self.boton_descargar.pack(pady=15)

        # --- SELECTOR DE RESOLUCION --- #
        self.frame_calidad = ctk.CTkFrame(self.frame_info, fg_color='transparent')
        self.frame_calidad.pack(pady=10)

        self.lbl_calidad = ctk.CTkLabel(self.frame_calidad, text="Selecciona la resolución:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_calidad.pack(side="left", padx=10)

        # Menu desplegable inicializado vacío
        self.menu_calidad = ctk.CTkOptionMenu(self.frame_calidad, values=["Seleccionar"])
        self.menu_calidad.pack(side="left", padx=10)

        # --- ESTADO/CARGA --- #
        self.label_estado = ctk.CTkLabel(self, text='Listo para escanear', font=ctk.CTkFont(size=12))
        self.label_estado.pack(side='bottom', pady=10)

    # --- ASINCRONIA CON THREADS --- #
    def busqueda_asincrona(self):
        url = self.input_url.get().strip()
        if not url: return

        url_limpia = url.split('&')[0]

        self.label_estado.configure(text='Analizando video...')
        self.boton_buscar.configure(state='disabled')
        self.frame_info.pack_forget()

        threading.Thread(target=self._hilo_buscar, args=(url_limpia,), daemon=True).start()

    def _hilo_buscar(self, url):
        meta = extraer_metadatos(url)
        self.after(0, self._finalizar_busqueda, meta)

    def _finalizar_busqueda(self, meta):
        self.boton_buscar.configure(state='normal')
        if not meta:
            self.label_estado.configure(text='Error: No se pudo obtener información del enlace.')

        self.video_actual_url = meta['url']
        self.label_titulo.configure(text=meta['titulo'])
        self.label_detalles.configure(text=f'Canal: {meta['autor']} | Duración: {meta['duracion']}')

        self.menu_calidad.configure(values=meta['resoluciones'])
        self.menu_calidad.set(meta['resoluciones'][0])

        try:
            res = requests.get(meta['thumb_url'], timeout=5)
            img_data = Image.open(io.BytesIO(res.content))
            img_ctk = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(320, 100))
            self.label_miniatura.configure(image=img_ctk)
        except Exception:
            self.label_miniatura.configure(image=None, text='[Miniatura no disponible]')

        self.frame_info.pack(pady=10, padx=20, fill='both', expand=True)
        self.label_estado.configure(text='Metadatos cargados con éxito.')

    def iniciar_descarga(self):
        if not self.video_actual_url: return

        resolucion_seleccionada = self.menu_calidad.get()
        self.boton_descargar.configure(state='disabled', text='Descargando...')
        self.label_estado.configure(text = 'Descargando archivos a tu pc...')

        threading.Thread(target=self._hilo_descargar, args=(resolucion_seleccionada,), daemon=True).start()

    def _hilo_descargar(self, calidad):
        """Este método se ejecuta en el hilo secundario y calcula el éxito localmente."""
        # Ejecutamos la descarga física (Esta función de motor_video devuelve True o False)
        resultado_exito = descargar_video(self.video_actual_url, calidad)
        
        # Volvemos de forma segura al hilo principal (GUI) para mostrar el resultado visual
        self.after(0, self._finalizar_descarga, resultado_exito)

    def _finalizar_descarga(self, exito):
        """Este método sí recibe el parámetro 'exito' desde el after."""
        self.boton_descargar.configure(state="normal", text="📥 Descargar Video")
        if exito:
            self.label_estado.configure(text="🎉 ¡Descarga Completada con éxito! Revisa tu carpeta de Descargas.")
        else:
            self.label_estado.configure(text="❌ Error: La descarga no pudo completarse.")