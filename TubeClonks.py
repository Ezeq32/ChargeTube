from pytube import YouTube
from pytube import Playlist
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class ArchivoAudio:
    def __init__(self, url, directorio_almacen):
        self.url = url
        #la direccion para guardar los archivos, el r'' sirve para crear una string 'raw' o cruda, esta cadena no le hace caso a los caracteres especiales.
        #si pones \n en una cadena normal, en lugar de imprimir \n hace un salto de linea, pero en una cadena cruda imprime literalmente el '\n'.
        #esta cadena sirve en strings que almacenan directorios ya que los directorios representan las carpetas con \\
        self.directorio_almacen = r'' + directorio_almacen
        #le digo puntero url porque Youtube crea un objeto que contiene el video, pero no es el video descargado, simplemente apunta a la url.
        self.puntero_stream = YouTube(url)
    
    def purificar_nombre(self, titulo):
        if '(' in titulo or ')' in titulo or '|' in titulo or '[' in titulo or ']' in titulo or '/' in titulo or '\\' in titulo:
            titulo = titulo.replace('|', ' ').replace('(', ' ').replace(')', ' ').replace('[', ' ').replace(']', ' ').replace('/', ' ').replace('\\', ' ')
        return titulo
    
    def descargar(self):
        audio = self.puntero_stream.streams.filter(only_audio=True).order_by('abr').asc().first()
        # esto era para filtrar los archivos de audio por mp3 y wav pero la mayoria de archivos estan en audio/webm
        audio_mp3 = self.puntero_stream.streams.filter(only_audio=True, file_extension='mp3').order_by('abr').asc().first()
        audio_wav = self.puntero_stream.streams.filter(only_audio=True, file_extension='wav').order_by('abr').asc().first()
        
        if audio_mp3:
            audio = audio_mp3
        elif audio_wav:
            audio = audio_wav
        
        titulo_audio = self.purificar_nombre(audio.title)

        try:
            audio.download(self.directorio_almacen, f'{titulo_audio}.mp3')
            print(f"Se descargo {titulo_audio} en: {self.directorio_almacen}")
        except Exception as e:
            print(f"Error al descargar {self.puntero_stream.title}: {str(e)}")

        
class ArchivoVideo(ArchivoAudio):
    def __init__(self, url, directorio_almacen, calidad_video):
        super().__init__(url, directorio_almacen)
        self.calidad_video = calidad_video

    def descargar(self):
        '''streams = self.puntero_url.streams

        # Mostrar información de cada stream
        for stream in streams:
            print(stream)'''
        
        video_inmutable = self.puntero_stream.streams.filter(res=self.calidad_video).first()
        video_mutable = self.puntero_stream.streams.filter(progressive=True).get_by_resolution(self.calidad_video)
        
        if video_mutable != None:
            video = video_mutable
        else:
            video = video_inmutable
        try:
            video_titulo = self.purificar_nombre(video.title)
        except AttributeError:
            print(f'No se encontro la resolucion {self.calidad_video} en las descargas de {self.puntero_stream.title}, intente con otra.')
            return AttributeError
        try:
            video.download(self.directorio_almacen, f'{video_titulo}.mp4')
            print(f"Se descargo {video_titulo} en: {self.directorio_almacen}")
        except Exception as e:
            print(f"Error al descargar {self.puntero_stream.title}: {str(e)}")
            return Exception
        

class ListaReproduccion:
    def __init__(self, url, directorio_almacen, calidad_video):
        self.directorio_almacen = directorio_almacen
        self.calidad_video = calidad_video
        self.puntero_playlist = Playlist(url)
    
    def descargar_audio(self):
        for url_audio in self.puntero_playlist.video_urls:
            archivo = ArchivoAudio(url_audio, self.directorio_almacen)
            archivo.descargar()
            
    def descargar_video(self):
        for url_video in self.puntero_playlist.video_urls:
            archivo = ArchivoVideo(url_video, self.directorio_almacen, self.calidad_video)
            archivo.descargar()
        

class DescargadorApp:
    def __init__(self, master):
        self.master = master
        master.title("Descargador de YouTube")

        self.label = tk.Label(master, text="Bienvenido al Descargador de YouTube")
        self.label.pack()

        self.url_label = tk.Label(master, text="URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master)
        self.url_entry.pack()

        #self.directorio_label = tk.Label(master, text="Directorio:")
        #self.directorio_label.pack()

        #self.directorio_entry = tk.Entry(master)
        #self.directorio_entry.pack()
        
        self.opcion_formato_label = tk.Label(master, text='Elegi el formato')
        self.opcion_formato_label.pack()

        self.opciones_formato = ["Audio/mp3", "Video/mp4"]
        self.lista_opcion_formato = ttk.Combobox(root, values=self.opciones_formato)
        self.lista_opcion_formato.pack()

        self.lista_opcion_formato.bind("<<ComboboxSelected>>",self.seleccionar_opcion_formato)

        
        self.calidad_video_label = tk.Label(master, text="Calidad de Video:")
        #self.calidad_video_label.pack()
        
        self.opciones_calidad_video = ['360p', '720p']
        self.lista_opcion_calidad_video = ttk.Combobox(root, values=self.opciones_calidad_video)

        self.descargar_button = tk.Button(master, text="Descargar", command=self.descargar)
        self.descargar_button.pack(side='bottom')

    def seleccionar_opcion_formato(self, event):
        opcion_seleccionada = self.lista_opcion_formato.get()
        if opcion_seleccionada == 'Audio/mp3':
            self.calidad_video_label.pack_forget()
            self.lista_opcion_calidad_video.pack_forget()
        elif opcion_seleccionada == 'Video/mp4':
            self.calidad_video_label.pack()
            self.lista_opcion_calidad_video.pack()
    
    def descargar(self):
        url = self.url_entry.get()
        directorio = filedialog.askdirectory()
    
        if self.lista_opcion_formato.get() == 'Audio/mp3':
            if 'playlist' in url:
                puntero_playlist = ListaReproduccion(url, directorio, None)
                puntero_playlist.descargar_audio()
            else:    
                audio = ArchivoAudio(url, directorio)
                audio.descargar()
        elif self.lista_opcion_formato.get() == 'Video/mp4':
            calidad_video = self.lista_opcion_calidad_video.get()
            if 'playlist' in url:
                puntero_playlist = ListaReproduccion(url, directorio, calidad_video)
                puntero_playlist.descargar_video()
            else:
                video = ArchivoVideo(url, directorio, calidad_video)
                video.descargar() 
            
if __name__ == '__main__':
    root = tk.Tk()
    app = DescargadorApp(root)
    root.mainloop()