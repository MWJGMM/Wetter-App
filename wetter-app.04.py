from tkinter import *
from PIL import Image, ImageTk
import requests

class GUI:
    def __init__(self):
        
        # Fenster
        self.fenster = Tk()
        self.fenster.title("Warn-Wetter-App")
        self.hintergrundFarbe = "#606060"
        self.schriftFarbe = "#FFFFFF"
        self.fenster.configure(bg=self.hintergrundFarbe)
        self.fenster.geometry("1000x600")  # Startgröße des Fensters

        # Konfiguriere 3 Zeilen und 2 Spalten
        self.fenster.grid_columnconfigure(0, weight=1)   # Linke Spalte (Wetterinfos), Skalierung in X
        self.fenster.grid_columnconfigure(1, weight=1)   # Rechte Spalte (Wetterwarnungen), Skalierung in X
        self.fenster.grid_rowconfigure(2, weight=1)      # Zeile 2, Skalierung in Y, Linke Spalte und Rechte Spalte

        ###### Überschrift ######
        self.ueberschrift = Label(self.fenster, text="Warn-Wetter-App", font=("Segoe UI Semibold", 35), bg="#002060", fg=self.schriftFarbe, pady=15)
        self.ueberschrift.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0) # Grid: sticky="ew" (east-west) über die ganze Breite ausdehnen

        ###### Eingabefeld ######
        self.eingabe_frame = Frame(self.fenster, bg=self.hintergrundFarbe)
        self.eingabe_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=40, pady=10) 
        
        self.label_standort = Label(self.eingabe_frame, text="Standort:", font=("Segoe UI Semibold", 24), bg=self.hintergrundFarbe, fg=self.schriftFarbe)
        self.label_standort.pack(side=LEFT, padx=10)
        
        self.eingabefeld = Entry(self.eingabe_frame, font=("Segoe UI", 20), bg="#002060", fg=self.schriftFarbe)
        self.eingabefeld.pack(side=LEFT, fill=X, expand=True) # Frame: fill=X: über die ganze Breite, expand=True: skaliert ?????
        self.eingabefeld.insert(0, "Berlin") # Am Anfang einfügen, Index 

        ###### Linke Seite (Wetterinfos) ######
        self.linke_seite = Frame(self.fenster, bg=self.hintergrundFarbe)
        self.linke_seite.grid(row=2, column=0, sticky="nsew", padx=(40, 5), pady=20) # Grid: sticky="nsew" in alle Richtungen ausdehnen
        
        self.label_aktuell = Label(self.linke_seite, text="Aktuell:", font=("Segoe UI Semibold", 18), bg=self.hintergrundFarbe, fg=self.schriftFarbe)
        self.label_aktuell.pack(anchor="nw")

        # self.foto = PhotoImage(file="wolke.png")
        # self.label_bild = Label(self.linke_seite, image=self.foto, bg="#595959")
        # self.label_bild.pack(side=LEFT, expand=True)
       
        self.label_bild = Label(self.linke_seite, text="🌤", font=("Segoe UI Semibold", 130), bg=self.hintergrundFarbe, fg=self.schriftFarbe)
        self.label_bild.pack(side=LEFT, expand=True)
        
        self.label_temperatur = Label(self.linke_seite, text="0°C", font=("Segoe UI Semibold", 80), bg=self.hintergrundFarbe, fg=self.schriftFarbe)
        self.label_temperatur.pack(side=RIGHT, expand=True)

        ###### Rechte Seite (Wetterwarnungen) ######
        self.rechte_seite = Frame(self.fenster, bg="#404040")
        self.rechte_seite.grid(row=2, column=1, sticky="nsew", padx=(5, 40), pady=20)
        
        self.label_aktuell = Label(self.rechte_seite, text="Warnung:", font=("Segoe UI Semibold", 18), bg="#404040", fg=self.schriftFarbe)
        self.label_aktuell.pack(anchor="nw", padx=10)

        ###### WetterApp ######
        self.wetterApp = WetterApp(self) # Objekt von WetterApp erzeugen und an die GUI (self) übergeben

        # Die after(1000, ...) Funktion stellt sicher, dass das GUI vollständig geladen ist, bevor die Wetterdaten angezeigt werden.
        self.fenster.after(1000, self.wetterApp.hole_wetter)
        
    def temperatur(self, temperatur):
        # Aktualisiert das Temperatur-Label mit dem neuen Wert
        self.label_temperatur.config(text=f"{temperatur}°C")


class WetterApp:
    
    def __init__(self, gui): # ????
        self.stadt = "Berlin"
        self.breite = 52.5200  # Breitengrad von Berlin
        self.laenge = 13.4050  # Längengrad von Berlin
        self.gui = gui  # Referenz zur GUI

    def hole_wetter(self):
        ###### Wetterdaten von der Open-Meteo API ######
        wetter_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.breite}&longitude={self.laenge}&current_weather=true"  # URL
        wetter_antwort = requests.get(wetter_url)  # Die Daten werden von der API abgerufen und kommen im Json-Format
        wetter_daten = wetter_antwort.json()  # Json Daten in Object konvertieren
        print(wetter_daten["current_weather"])
        
        # Temperatur aus dem Obejekt lesen
        temperatur = wetter_daten["current_weather"]["temperature"]
        #print(f"Temperatur: {temperatur}°C")
        
        # Temperatur in der GUI aktualisieren
        self.gui.temperatur(temperatur)

# GUI erstellen und starten
wetterApp = GUI()
wetterApp.fenster.mainloop()


