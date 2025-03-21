from tkinter import *
# from PIL import Image, ImageTk
import requests
import datetime
import math
import twilio
from twilio.rest import Client

# Twilio Konto | !pip install twilio
# https://console.twilio.com/?frameUrl=%2Fconsole%3Fx-target-region%3Dus1
account_sid = 'AC82adb38fb9bcd3bb83c26f838b40419e'
auth_token = '585b262e5855179dda4314de73063be2'
client = Client(account_sid, auth_token)

class GUI:
    def __init__(self):
        
        # Definiere Hintergrundfarbe 
        self.hintergrundFarbe = "#000000"
        
        # Fenster
        self.fenster = Tk()
        self.fenster.title("Warn-Wetter-App")
        self.fenster.configure(bg=self.hintergrundFarbe)
        self.fenster.geometry("1000x600")  # Startgröße des Fensters
        self.fenster.minsize(1000, 600)    # Minimum Größe des Fensters

        # Konfiguriere 3 Zeilen und 2 Spalten
        self.fenster.grid_columnconfigure(0, weight=1)      # Linke Spalte (Wetterinfos), Skalierung in X
        self.fenster.grid_columnconfigure(1, minsize=350)   # Rechte Spalte (Wetterwarnungen), Skalierung in X
        self.fenster.grid_rowconfigure(2, weight=1)         # Zeile 2, Skalierung in Y, Linke Spalte und Rechte Spalte


        ###### Überschrift ######
        self.ueberschrift = Label(self.fenster, text="Warn-Wetter-App", font=("Segoe UI Semibold", 35), bg="#002060", fg="white", pady=15)
        self.ueberschrift.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0) # Grid: sticky="ew" (east-west) über die ganze Breite ausdehnen


        ###### Eingabefeld ######
        self.eingabe_frame = Frame(self.fenster, bg=self.hintergrundFarbe)
        self.eingabe_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=40, pady=10) 
        
        self.label_standort = Label(self.eingabe_frame, text="Standort:", font=("Segoe UI Semibold", 24), bg=self.hintergrundFarbe, fg="white")
        self.label_standort.pack(side=LEFT, padx=10)
        
        self.eingabefeld = Entry(self.eingabe_frame, font=("Segoe UI", 20), bg="#002060", fg="white", insertbackground="white",relief="flat") # insertbackground bestimmt die Farbe des Text-Cursors
        self.eingabefeld.pack(side=LEFT, fill=X, expand=True) # Frame: fill=X: über die ganze Breite, expand=True: skaliert ?????
 
 
        ###### Linke Seite (Wetterinfos) ######
        self.linke_seite = Frame(self.fenster, bg=self.hintergrundFarbe)
        self.linke_seite.grid(row=2, column=0, sticky="nsew", padx=(40, 10), pady=20) # Grid: sticky="nsew" in alle Richtungen ausdehnen
        
        self.label_aktuell = Label(self.linke_seite, text="Aktuell:", font=("Segoe UI Semibold", 24), bg=self.hintergrundFarbe, fg="white")
        self.label_aktuell.pack(anchor="nw")

        # self.foto = PhotoImage(file="wolke.png")
        # self.label_bild = Label(self.linke_seite, image=self.foto, bg="#595959")
        # self.label_bild.pack(side=LEFT, expand=True)
       
        self.label_bild = Label(self.linke_seite, text="🌤", font=("Segoe UI Semibold", 100), bg=self.hintergrundFarbe, fg="white")
        self.label_bild.pack(side=LEFT, expand=True)
        
        self.label_temperatur = Label(self.linke_seite, text="0°C", font=("Segoe UI Semibold", 50), bg=self.hintergrundFarbe, fg="white")
        self.label_temperatur.pack(side=RIGHT, expand=True)

        ###### Rechte Seite (Wetterwarnungen) ######
        self.rechte_seite = Frame(self.fenster, bg="#404040")
        self.rechte_seite.grid(row=2, column=1, sticky="nsew", padx=(10, 40), pady=20)
        
        self.label_warnung = Label(self.rechte_seite, text="Info:", font=("Segoe UI Semibold", 24), bg="#404040", fg="white")
        self.label_warnung.pack(anchor="nw", padx=10)
        
        self.label_warnMeldung = Label(self.rechte_seite, text="Text", font=("Segoe UI Semibold", 18), bg="#404040", fg="white")
        self.label_warnMeldung.pack(anchor="nw", padx=10, pady=10)

        ###### WetterApp ######
        self.wetterApp = WetterApp(self) # Objekt von WetterApp erzeugen und an die GUI (self) übergeben
           
        # Bindet die Funktion an die Eingabetaste
        self.eingabefeld.bind("<Return>", self.wetterApp.standort_geändert)

        # Die Schriftgröße relativ zur Fenstergröße skalieren wenn die Fenstergröße geändert wird
        # Eine Lambda-Funktion wird verwendet, um self.schriftgröße () mit dem event-Parameter aufzurufen
        self.fenster.bind("<Configure>", lambda event: self.schriftgröße())
        
        # after(10, ...) Die Funktion stellt sicher, dass das GUI vollständig geladen ist, bevor die Wetterdaten angezeigt werden.
        self.fenster.after(10, self.wetterApp.hole_wetter)
        
    def schriftgröße (self):
        # Hole die aktuelle Breite des Fensters
        fensterBreite = self.fenster.winfo_width()
        
        # Berechne die Schriftgröße basierend auf der Fensterbreite (z.B. 10% der Fensterbreite)
        bild_fontSize = int(fensterBreite * 0.15)
        temperatur_fontSize = int(fensterBreite * 0.06)

        # Aktualisiere die Schriftgröße des Labels für das Bild
        self.label_bild.config(font=("Segoe UI Semibold", bild_fontSize))
        
        # Aktualisiere die Schriftgröße des Labels für die Temperatur
        self.label_temperatur.config(font=("Segoe UI Semibold", temperatur_fontSize))


class WetterApp:
    
    def __init__(self, gui): # ????
        self.gui = gui  # Referenz zur GUI
        
        # Stadtname eingeben
        self.ort = "berlin"
        self.letzterOrt = self.ort.title()
        self.hole_ort()
        self.gui.eingabefeld.delete(0, END)  # Aktuellen Inhalt löschen
        self.gui.eingabefeld.insert(0, self.ort.title())
        
    def standort_geändert(self, event=None):
        self.ort = self.gui.eingabefeld.get().title()  # Stadtname holen und formatieren
        self.hole_ort()
        self.hole_wetter()

    def hole_ort(self):
        
        # Geocoding-API von Open-Meteo
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={self.ort}&count=1&language=de&format=json"
        geo_antwort = requests.get(geo_url)
        geo_daten = geo_antwort.json()

        if "results" in geo_daten:
            self.breite = geo_daten["results"][0]["latitude"]
            self.laenge = geo_daten["results"][0]["longitude"]
            self.letzterOrt = self.ort.title()
            self.gui.eingabefeld.delete(0, END)  # Aktuellen Inhalt löschen
            self.gui.eingabefeld.insert(0, self. ort)
            print(f"📍 {self.ort}: {self.breite}, {self.laenge}")
            
        else:
            self.gui.eingabefeld.delete(0, END)  # Aktuellen Inhalt löschen
            self.gui.eingabefeld.insert(0, self.letzterOrt)
            print(self.letzterOrt)
        
    def hole_wetter(self):
        
        ###### Wetterdaten von der Open-Meteo API ######
        wetter_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.breite}&longitude={self.laenge}&current_weather=true"  # URL
        wetter_antwort = requests.get(wetter_url)  # Die Daten werden von der API abgerufen und kommen im Json-Format
        wetter_daten = wetter_antwort.json()  # Json Daten in Object konvertieren
        print(wetter_daten["current_weather"])
        
        # Temperatur aus dem Obejekt lesen
        temperaturDaten = wetter_daten["current_weather"]["temperature"]
        # Temperatur in der GUI aktualisieren
        self.gui.label_temperatur.config(text=f"{temperaturDaten}°C")
        
        # Hole Emoji als Bild
        iconDaten = wetter_daten["current_weather"]["weathercode"]
        self.holeEmoji(iconDaten)

        # Hole Warnungen
        self.warnungen(wetter_daten)
        
        # Uhrzeit: Berechne die Farbe basierend auf der Zeit
        self.hintergrundfarbe()
    
    
    def warnungen(self, wetter_daten):

        warnungen = []
        warnungenSMS = []

        temperatur = wetter_daten["current_weather"]["temperature"]
        windGeschwindigkeit = wetter_daten["current_weather"]["windspeed"]
        wetterCode = wetter_daten["current_weather"]["weathercode"]

        # Test extreme Temperaturen
        if temperatur <= 0:
            warnungen.append("Gefrierende Temperaturen!")
            warnungenSMS.append("Achtung: Gefrierende Temperaturen! Bitte vorsichtig sein.")
        elif temperatur >= 30:  # 30
            warnungen.append("Hitzewelle-Warnung!")
            warnungenSMS.append("Achtung: Hitzewelle-Warnung! Trinke ausreichend Wasser und vermeide die Sonne.")

        # Test starke Winde
        if windGeschwindigkeit >= 50:
            warnungen.append("Starke Windwarnung!")
            warnungenSMS.append("Achtung: Starke Windwarnung! Sei vorsichtig bei Outdoor-Aktivitäten.")
        elif windGeschwindigkeit >= 30:  # 30
            warnungen.append("Moderater Wind, Vorsicht geboten.")
            warnungenSMS.append("Achtung: Moderater Wind, Vorsicht geboten! Schütze empfindliche Gegenstände.")

        # Wettercodes (Beispielcodes, Meteo.com)
        wetterDaten = {
            0: "Klarer Himmel.",
            1: "Überwiegend klar.",
            2: "Teilweise bewölkt.",
            3: "Bedeckt.",
            45: "Nebel.",
            48: "Gefrierender Nebel.",
            51: "Leichter Nieselregen.",
            53: "Mäßiger Nieselregen.",
            55: "Starker Nieselregen.",
            61: "Leichter Regen.",
            63: "Mäßiger Regen.",
            65: "Starker Regen.",
            66: "Gefrierender leichter Regen.",
            67: "Gefrierender starker Regen.",
            71: "Leichter Schneefall.",
            73: "Mäßiger Schneefall.",
            75: "Starker Schneefall.",
            77: "Schneekörner.",
            80: "Leichte Regenschauer.",
            81: "Mäßige Regenschauer.",
            82: "Starke Regenschauer.",
            85: "Leichte Schneeschauer.",
            86: "Starke Schneeschauer.",
            95: "Gewitter.",
            96: "Gewitter mit leichtem Hagel.",
            99: "Gewitter mit starkem Hagel."
        }

        # Die Wettercode Warnungen dem Array hinzufügen und eine SMS bei extremen Codes sammeln
        extreme_wetter_codes = [55, 65, 67, 75, 82, 86, 95, 96, 99]
        if wetterCode in extreme_wetter_codes:
            warnungen.append(wetterDaten.get(wetterCode))  # Warnung hinzufügen
            warnungenSMS.append(f"Achtung: {wetterDaten.get(wetterCode)}")

        # Die Wettercode Warnungen dem Array hinzufügen
        warnungen.append(wetterDaten.get(wetterCode))  # Falls der Code nicht vorhanden ist, wird None zurückgegeben

        # Verbinde die Liste der Warnungen zu einem einzigen String (Zeilenumbrüchen = \n)
        warnungen_text = '\n'.join(warnungen)

        # Aktualisiere das Label mit den Warnungen
        self.gui.label_warnMeldung.config(text=warnungen_text, wraplength=350, justify="left")

        # Ausgabe der Warnungen (zum Testen)
        print(warnungen_text)

        # Wenn es Nachrichten gibt, sende diese als eine einzelne Nachricht
        if warnungenSMS:
            # Meine Twilio-Nummer
            tel_von = '+16516152417'
            # Meine Telefonnummer
            tel_an = '+491754163411'
            # Alle Nachrichten in einer einzigen Nachricht kombinieren
            warnungen_SMS = "\n".join(warnungenSMS)

            print(f"Von: {tel_von}\nAn: {tel_an}\n\nSMS Nachricht:\n{warnungen_SMS}")
            
            # SMS über Twilio verschicken
            # client.messages.create(
            #     body=warnungen_SMS,
            #     from=tel_von,  
            #     to=tel_an
            # )


    def holeEmoji(self, iconDaten):
        
        if iconDaten == 0:
            emoji = "☀"  
        elif iconDaten == 1:
            emoji = "🌤"
        elif iconDaten == 2:
            emoji = "⛅"
        elif iconDaten == 3:
            emoji = "☁"
        elif iconDaten in [45, 48]:
            emoji = "🌫"
        elif iconDaten in [51, 53, 55]:
            emoji = "🌦"
        elif iconDaten in [61, 63, 65, 80, 81, 82]:
            emoji = "🌧"
        elif iconDaten in [71, 73, 75, 85, 86]:
            emoji = "❄"
        elif iconDaten in [95, 96, 99]:
            emoji = "⛈"
        else:
            emoji = "❓"

        self.gui.label_bild.config(text=f"{emoji}")
        # print(emoji)

    def hintergrundfarbe(self):

        self.aktuelle_zeit = datetime.datetime.now()
        # self.aktuelle_zeit = datetime.datetime(2025, 3, 12, 2, 0, 0, 0)
        # print (self.aktuelle_zeit)

        # Rechne Stunden und Minuten in eine Float um (15:30 = 15,5) 
        self.stunde = self.aktuelle_zeit.hour + self.aktuelle_zeit.minute / 60 
        # print (self.stunde)

        # https://www.geogebra.org/calculator
        # f(x)=255 (1-(((x-12)/(12)))^(2))
        self.rot = max(0, int( 100 * (1 - math.pow((self.stunde - 12) / 12, 2)) + 25))
        self.grün = max(0, int( 125 * (1 - math.pow((self.stunde - 12) / 12, 2)) + 25))
        self.blau = max (0, min(255, int( 255 * (1 - math.pow((self.stunde - 12) / 12, 2)) + 25)))
        
        # Konvertiere RGB in Hexadezimal (:02x)
        self.hexFarbe = f"#{self.rot:02x}{self.grün:02x}{self.blau:02x}"
        # print(self.hexFarbe)  # Debugging: print color

        # Aktualisiere die Hintergrundfarbe der Fenster
        self.gui.fenster.configure(bg=self.hexFarbe)
        self.gui.label_standort.configure(bg=self.hexFarbe, fg="white")
        self.gui.linke_seite.configure(bg=self.hexFarbe)
        self.gui.label_temperatur.configure(bg=self.hexFarbe, fg="white")
        self.gui.label_bild.configure(bg=self.hexFarbe, fg="white")
        self.gui.label_aktuell.configure(bg=self.hexFarbe, fg="white")
        self.gui.eingabe_frame.configure(bg=self.hexFarbe)
   
# GUI erstellen und starten
wetterApp = GUI()
wetterApp.fenster.mainloop()







