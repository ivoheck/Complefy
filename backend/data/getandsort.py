import zeep
import json
import os
from zeep.exceptions import Fault
from requests import Session
from zeep.transports import Transport
import warnings
import urllib3
from datetime import datetime, timedelta

# Warnungen deaktivieren
warnings.filterwarnings("ignore", category=UserWarning, module="zeep")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# WSDL URL des Webservices
wsdl_url = "https://mystudy.leuphana.de/mystudy_webservice.wsdl"

# Verzeichnisse und Dateien
base_dir = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.join(base_dir, "module.json")
output_dir = os.path.join(base_dir, "veranstaltungen_json")
criteria_file = os.path.join(base_dir, "filter_criteria.json")
selected_events_file = os.path.join(base_dir, "selected_events.json")
os.makedirs(output_dir, exist_ok=True)

# Funktion zum Laden der Filterkriterien
def load_filter_criteria():
    with open(criteria_file, "r", encoding="utf-8") as file:
        return json.load(file)

# Funktion zum Überprüfen, ob eine Veranstaltung in den Zeitrahmen passt
def is_event_in_timeframe(event, sallybus):
    def convert_to_minutes_since_midnight(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return dt.hour * 60 + dt.minute

    termine_list = event.get("termine")
    if not termine_list:
        return True
    for termine in termine_list.get("termine", []):
        start_minutes = convert_to_minutes_since_midnight(termine["beginn_datum"] + termine["beginn_zeit"])
        end_minutes = convert_to_minutes_since_midnight(termine["ende_datum"] + termine["ende_zeit"])

        day_of_week = datetime.fromtimestamp(termine["beginn_datum"]).strftime("%A").lower()
        if day_of_week in sallybus:
            for period in sallybus[day_of_week]:
                period_start, period_end = period
                if not (end_minutes <= period_start or start_minutes >= period_end):
                    return False
    return True

# Funktion zum Abrufen und Speichern der Module
def fetch_and_log_modules():
    gebiet_id = 10641

    # Benutzerdefinierter Transport für SSL
    session = Session()
    session.verify = False  # SSL-Validierung deaktivieren
    transport = Transport(session=session)

    try:
        client = zeep.Client(wsdl=wsdl_url, transport=transport)
        modules_response = client.service.getModuleFromGebiet(gebiet_id)
        
        # Serialisierung der SOAP-Antwort in ein lesbares Python-Objekt
        serialized_response = zeep.helpers.serialize_object(modules_response)

        # Daten in eine JSON-Datei schreiben
        with open(module_file, "w", encoding="utf-8") as file:
            json.dump(serialized_response, file, indent=4, ensure_ascii=False)
        
        print(f"Module erfolgreich in {module_file} gespeichert.")

    except Fault as fault:
        print(f"Fehler beim Aufruf des SOAP-Webservices: {fault.message}")

# Funktion zum Abrufen und Speichern der Veranstaltungen
def fetch_and_save_events():
    # SOAP-Client erstellen
    client = zeep.Client(wsdl=wsdl_url)

    # JSON-Datei mit Modulen laden
    with open(module_file, "r", encoding="utf-8") as file:
        module_data = json.load(file)

    # Modul-IDs extrahieren
    module_ids = [module['id'] for module in module_data]

    # Für jede Modul-ID Veranstaltungen abrufen und speichern
    for modul_id in module_ids:
        try:
            # Veranstaltungen abrufen
            events_response = client.service.getVeranstaltungenFromModul(modul_id, 48)
            
            # JSON-Datei für das Modul erstellen
            output_file = os.path.join(output_dir, f"veranstaltungen_{modul_id}.json")
            
            # Veranstaltungen in die Datei schreiben
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(zeep.helpers.serialize_object(events_response), outfile, ensure_ascii=False, indent=4)
            
            print(f"Veranstaltungen für Modul-ID {modul_id} gespeichert.")
        except zeep.exceptions.Fault as fault:
            print(f"Fehler beim Abrufen der Veranstaltungen für Modul-ID {modul_id}: {fault}")
        except Exception as e:
            print(f"Allgemeiner Fehler für Modul-ID {modul_id}: {e}")

# Funktion zum Filtern und Speichern der ausgewählten Veranstaltungen
def filter_and_save_selected_events():
    # Module laden
    with open(module_file, "r", encoding="utf-8") as file:
        module_data = json.load(file)

    # Filterkriterien laden
    criteria = load_filter_criteria()
    finished_comps = criteria.get("finished_comps", [])
    sallybus = criteria.get("sallybus", [])

    selected_events = []

    # Modulnamen zu IDs mappen
    finished_comp_ids = [module["id"] for module in module_data if module["name"] in finished_comps]

    # Veranstaltungen aus den JSON-Dateien filtern
    for modul_file in os.listdir(output_dir):
        modul_id = int(modul_file.split("_")[1].split(".")[0])
        if modul_id in finished_comp_ids:
            continue  # Modul wurde bereits belegt, überspringen

        with open(os.path.join(output_dir, modul_file), "r", encoding="utf-8") as file:
            events = json.load(file)

        for event in events:
            if is_event_in_timeframe(event, sallybus):
                selected_events.append(event)

    # Gefilterte Veranstaltungen in selected_events.json speichern
    with open(selected_events_file, "w", encoding="utf-8") as file:
        json.dump(selected_events, file, ensure_ascii=False, indent=4)

    print(f"Gefilterte Veranstaltungen erfolgreich in {selected_events_file} gespeichert.")

# Funktionen ausführen
fetch_and_log_modules()
fetch_and_save_events()
filter_and_save_selected_events()
