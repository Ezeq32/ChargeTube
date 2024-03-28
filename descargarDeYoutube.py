from pytube import YouTube
from pytube import Playlist

url = input('Pone la url del video o la playlist que queres descargar cloou: ')
opcion_audio_video = input('Elegi el tipo de archivo 1:Video 2:Audio: ')
if '&list' in url or 'playlist' in url:
    playlist_usuario = Playlist(url)
    if opcion_audio_video == '1':
        print('Escribi la calidad de video fighter.')
        calidad_video = input('360p | 720p | 1080p (pone el p al final del numero): ')
        for url_video in playlist_usuario.video_urls:
            youtube = YouTube(url_video)
            video_inmutable = youtube.streams.filter(res=calidad_video).first()
            video_mutable = youtube.streams.filter(progressive=True).get_by_resolution(calidad_video)
            if video_mutable is not None:
                video_mutable.download(r'E:\Users\Eze\Downloads\Musica-videos')
            else:
                video_inmutable.download(r'E:\Users\Eze\Downloads\Musica-videos')
    else:
        for url_video in playlist_usuario.video_urls:
            youtube = YouTube(url_video)
            audio = youtube.streams.filter(only_audio=True).order_by('abr').asc().first()
            nombre_de_archivo = audio.title
            if '/' in nombre_de_archivo:
                nombre_de_archivo = nombre_de_archivo.replace('/',' ')
            audio.download(r'E:\Users\Eze\Downloads\Musica-videos', f'{nombre_de_archivo}.mp3')
else:
    youtube = YouTube(url, on_complete_callback=print('Descarga completada!'))
    
    if opcion_audio_video == '1':
        print('Escribi la calidad de video fighter.')
        calidad_video = input('360p | 720p | 1080p (pone el p al final del numero): ')
        video_inmutable = youtube.streams.filter(res=calidad_video).first()
        video_mutable = youtube.streams.filter(progressive=True).get_by_resolution(calidad_video)
        if video_mutable != None:
            video_mutable.download(r'E:\Users\Eze\Downloads\Musica-videos')
        else:
            video_inmutable.download(r'E:\Users\Eze\Downloads\Musica-videos')
    else:
        audio = youtube.streams.filter(only_audio=True).order_by('abr').asc().first()
        nombre_de_archivo = audio.title
        if '/' in nombre_de_archivo:
            nombre_de_archivo = nombre_de_archivo.replace('/',' ')
        audio.download(r'E:\Users\Eze\Downloads\Musica-videos', f'{nombre_de_archivo}.mp3')




'''
from pytube import YouTube
from pytube import Playlist

url = input('Pone la url del video o la playlist que queres descargar cloou: ')
opcion_audio_video = input('Elegi el tipo de archivo 1:Video 2:Audio: ')
if '&list' in url or 'playlist' in url:
    playlist_usuario = Playlist(url)
    if opcion_audio_video == '1':
        print('Escribi la calidad de video fighter.')
        calidad_video = input('360p | 720p | 1080p (pone el p al final del numero): ')
        for url_video in playlist_usuario.video_urls:
            youtube = YouTube(url_video)
            video_inmutable = youtube.streams.filter(res=calidad_video).first()
            video_mutable = youtube.streams.filter(progressive=True).get_by_resolution(calidad_video)
            if video_mutable is not None:
                video_mutable.download(r'/storage/emulated/0/Music')
            else:
                video_inmutable.download(r'/storage/emulated/0/Music')
    else:
        for url_video in playlist_usuario.video_urls:
            youtube = YouTube(url_video)
            audio = youtube.streams.filter(only_audio=True).order_by('abr').asc().first()
            nombre_de_archivo = audio.title
            if '/' in nombre_de_archivo:
                nombre_de_archivo = nombre_de_archivo.replace('/',' ')
            audio.download(r'/storage/emulated/0/Music', f'{nombre_de_archivo}.mp3')
else:
    youtube = YouTube(url, on_complete_callback=print('Descarga completada!'))
    
    if opcion_audio_video == '1':
        print('Escribi la calidad de video fighter.')
        calidad_video = input('360p | 720p | 1080p (pone el p al final del numero): ')
        video_inmutable = youtube.streams.filter(res=calidad_video).first()
        video_mutable = youtube.streams.filter(progressive=True).get_by_resolution(calidad_video)
        if video_mutable is not None:
            video_mutable.download(r'/storage/emulated/0/Music')
        else:
            video_inmutable.download(r'/storage/emulated/0/Music')
    else:
        audio = youtube.streams.filter(only_audio=True).order_by('abr').asc().first()
        nombre_de_archivo = audio.title
        if '/' in nombre_de_archivo:
            nombre_de_archivo = nombre_de_archivo.replace('/',' ')
        audio.download(r'/storage/emulated/0/Music', f'{nombre_de_archivo}.mp3')'''