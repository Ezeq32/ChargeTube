import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
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

        self.lista_opcion_formato.bind("<<ComboboxSelected>>",self.seleccionar_opcion)

        
        self.calidad_video_label = tk.Label(master, text="Calidad de Video:")
        #self.calidad_video_label.pack()
        
        self.opciones_calidad_video = ['360p', '720p']
        self.lista_opcion_calidad_video = ttk.Combobox(root, values=self.opciones_calidad_video)

        self.descargar_button = tk.Button(master, text="Descargar", command=self.obtener_directorio)
        self.descargar_button.pack()

    def seleccionar_opcion(self, event):
        opcion_seleccionada = self.lista_opcion_formato.get()
        if opcion_seleccionada == 'Video/mp4':
            self.calidad_video_label.pack()
            self.lista_opcion_calidad_video.pack()
        elif opcion_seleccionada == 'Audio/mp3':
            self.calidad_video_label.pack_forget()
            self.lista_opcion_calidad_video.pack_forget()
            
    def obtener_directorio(self):
        
        self.directorio_entry.insert(0, filedialog.askdirectory()) 
    
    def descargar(self):
        url = self.url_entry.get()
        directorio = self.directorio_entry.get()
        opcion = self.opcion_var.get()

if __name__ == '__main__':
    root = tk.Tk()
    app = DescargadorApp(root)
    root.mainloop()
