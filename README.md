# Wetter-App

Dokumentart: Anforderungsdefinition  
Anforderungsdefinition – Titelblatt  
Projekt: Warn-Wetter-App 
Verfasser: Max Weidner 
Datum: 04.01.2025 / Letzte Überarbeitung: 10.01.2025 
Version: 1.0 

1. Ist-Analyse 
Das vorliegende System beschäftigt sich mit der Bereitstellung und Analyse von Wetterwarnungen.  
Die Warn-Wetter-App soll Wetterlagen, basierend auf den eigenständig angegebenen Standort analysieren. Für den Fall einer 
Extremwetterlage, wie extrem hohe oder niedrige Temperaturen sowie starke Stürme, bis hin zu Tornados, soll der Nutzer eine 
Warn-SMS von der App erhalten, in welcher über die aktuelle, bzw. kurz bevorstehende Wetterlage informiert wird sowie eine 
Verhaltensempfehlung abgegeben wird (Bsp.: Achtung, extreme Hitze – nicht beschattete Orte vermeiden und ausreichend 
trinken.). Der Standortangabe erfolgt per Eingabe des Aufenthaltsortes (z.B. Berlin oder New York) in ein Textfeld. Eingeholt 
werden die Wetterdatenquellen aus einer API eines vertrauenswürdigen Wetterdienstes.

2. Soll-Konzept 
2.1 Produkteinsatz (Systemziele) 
• Warn-Wetter-App soll Nutzer über extreme Wetterereignisse informieren und ihnen rechtzeitig 
Handlungsempfehlungen geben 
Wesentliche Aufgaben und Leistungen: 
• Empfang und Verarbeitung von Wetterdaten 
• Identifikation von Extremwettersituationen 
• Benachrichtigung des Nutzers per SMS 
Anwendungsbereich: 
• Privatpersonen, die sich über lokale Wetterwarnungen informieren möchten 
• Outdoor-Aktivitäten, Veranstaltungsplanungen, Sicherheit 
Zielgruppe: 
• Personen im Besitz eines Endgerätes  
• Personen mit Interesse an einfacher Bedienbarkeit und sicherheitsrelevanter Information. 
Anforderungen an den Benutzer: 
• Fähigkeit zur Eingabe von Standortdaten  
• Zugang zu einem Mobiltelefon, um SMS zu empfangen. 
2.2 Produktumgebung (Basismaschine) 
Hardware: 
• Mobiltelefon oder Computer zur Einrichtung 
• Server für die Datenverarbeitung 
Ein- und Ausgabegeräte: 
• Tastatur oder Touchscreen zur Standorteingabe 
• Bildschirm zur Darstellung von Informationen 
Betriebssystem: 
• Windows, MacOS, Linux (für die Entwicklung) 
• Android/iOS (für die Benachrichtigung) 
Zusatzsoftware: 
• Thonny  
• Zugang zu SMS-Versand-APIs und Wetter-APIs 
2.3 Produktdaten 
Eingabedaten: 
• Standortinformationen  
• aktuelle Wetterdaten von Wetterdiensten 
Ausgabedaten: 
• Benachrichtigungen über Extremwetter (per SMS) 
• Hinweise auf die Wetterlage in der App 
2.4 Benutzerschnittstelle (Oberfläche) 
Bedienung: 
• einfache Eingabe des Standorts über ein Textfeld  
Layout: 
• minimalistisches Design mit klaren Eingabefeldern 
• Übersichtliche Anzeige von Warnmeldungen 
Dialogstruktur: 
• Startseite mit Standortabfrage 
• Anzeige von aktuellen Wetterwarnungen 
2.5 Erweiterungsmöglichkeiten 
• Integration von Push-Benachrichtigungen als Alternative zu SMS 
• Erweiterung auf weitere Naturkatastrophen wie Erdbeben oder Hochwasser

3. Abkürzungen 
Bsp.: Beispiel 
z.B.: zum Beispiel
API: Application Programming Interface 
SMS: Short Message Service 

