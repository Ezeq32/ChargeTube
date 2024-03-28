from pytube import YouTube
from pytube import Playlist

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
        
        
        
if __name__ == '__main__':
    
    while True:
        print('--------------------------------------------')
        print('''▄▄▄█████▓ █    ██  ▄▄▄▄   ▓█████     ▄████▄   ██░ ██  ▄▄▄       ██▀███    ▄████ ▓█████     ██▒   █▓      ██▓ ██▓
▓  ██▒ ▓▒ ██  ▓██▒▓█████▄ ▓█   ▀    ▒██▀ ▀█  ▓██░ ██▒▒████▄    ▓██ ▒ ██▒ ██▒ ▀█▒▓█   ▀    ▓██░   █▒     ▓██▒▓██▒
▒ ▓██░ ▒░▓██  ▒██░▒██▒ ▄██▒███      ▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄  ▓██ ░▄█ ▒▒██░▄▄▄░▒███       ▓██  █▒░     ▒██▒▒██▒
░ ▓██▓ ░ ▓▓█  ░██░▒██░█▀  ▒▓█  ▄    ▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██ ▒██▀▀█▄  ░▓█  ██▓▒▓█  ▄      ▒██ █░░     ░██░░██░
  ▒██▒ ░ ▒▒█████▓ ░▓█  ▀█▓░▒████▒   ▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒░██▓ ▒██▒░▒▓███▀▒░▒████▒      ▒▀█░   ██▓ ░██░░██░
  ▒ ░░   ░▒▓▒ ▒ ▒ ░▒▓███▀▒░░ ▒░ ░   ░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒▓ ░▒▓░ ░▒   ▒ ░░ ▒░ ░      ░ ▐░   ▒▓▒ ░▓  ░▓  
    ░    ░░▒░ ░ ░ ▒░▒   ░  ░ ░  ░     ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░   ░  ░ ░  ░      ░ ░░   ░▒   ▒ ░ ▒ ░
  ░       ░░░ ░ ░  ░    ░    ░      ░         ░  ░░ ░  ░   ▒     ░░   ░ ░ ░   ░    ░           ░░   ░    ▒ ░ ▒ ░
            ░      ░         ░  ░   ░ ░       ░  ░  ░      ░  ░   ░           ░    ░  ░         ░    ░   ░  ''')
        print('--------------------------------------------')
        print('-by Eze32q')
        
        print('''Elegi el formato que quieras
                0-Salir
                1-Audio
                2-Video''')
        entrada_opcion = int(input('$--> '))
        if entrada_opcion == 1:
            url = input('Pega la url:')
            directorio_almacen = input('Pega el directorio usando el formato: C:\\carpeta\\carpeta-plonks: ')
            if 'playlist' in url:
                puntero_playlist = ListaReproduccion(url, directorio_almacen, None)
                puntero_playlist.descargar_audio()
            else:
                puntero_audio = ArchivoAudio(url, directorio_almacen)
                puntero_audio.descargar()
        elif entrada_opcion == 2:
            url = input('Pega la url:')
            directorio_almacen = input('Pega el directorio usando el formato C:\\carpeta\\carpeta-plonks:')
            print('Escribi la calidad de video fighter.')
            calidad_video = input('360p | 720p  (pone el p al final del numero): ')
            if 'playlist' in url:
                puntero_playlist = ListaReproduccion(url, directorio_almacen, calidad_video)
                puntero_playlist.descargar_video()
            else:
                puntero_video = ArchivoVideo(url, directorio_almacen, calidad_video)
                puntero_video.descargar()
        elif entrada_opcion == 0:
            break
                
    
    '''musica = ListaReproduccion('https://www.youtube.com/playlist?list=PL4Fe1aP1msIAz-PsGgm998lfkMKwaoIWZ','C:\\Users\\ezece\\Desktop\\Carpeta codigos\\10-Python\\POO\\pytube\\musica_prueba','1080p')
    musica.descargar_video()'''
