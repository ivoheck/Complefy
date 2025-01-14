import json
import os
import sys
import re
from datetime import datetime
import html
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Service.WebService import MyStudyWebService

# Initialisierung des Webservice-Clients
wsdl_url = "https://mystudy.leuphana.de/mystudy_webservice.wsdl"
service = MyStudyWebService(wsdl_url)

def fetch_modules_for_gebiet(gebiet_id):
    try:
        print(f"Fetching modules for gebiet_id: {gebiet_id}")
        modules = service.get_module_from_gebiet(gebiet_id)
        print("Modules fetched successfully.")
        return modules.module
    except Exception as e:
        print(f"Error fetching modules for gebiet_id {gebiet_id}: {e}")
        return []

def parse_module_data(raw_modules):
    parsed_modules = []
    for modul in raw_modules:
        parsed_modules.append({
            "id": modul.id,
            "name": modul.name,
            "nummer": modul.nummer,
            "angebot": modul.angebot,
            "credits": modul.credits,
            "semester_id": modul.semester_id
        })
    return parsed_modules

def convert_timestamp_to_date(timestamp):
    if timestamp:
        return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
    return None

def convert_seconds_to_time(seconds):
    if seconds:
        hours, remainder = divmod(int(seconds), 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}"
    return None

def parse_raw_event_data(raw_data_str):
    # Verwende reguläre Ausdrücke, um Veranstaltungsblöcke zu extrahieren
    event_blocks = re.findall(r"\(veranstaltung\)\{(.*?)\}\s*(?=\(veranstaltung\)|$)", raw_data_str, re.DOTALL)
    events_dict = defaultdict(lambda: {"termine": [], "inhalt": "Kein Inhalt"})

    for block in event_blocks:
        try:
            event_id_match = re.search(r"id\s*=\s*(\d+)", block)
            name_match = re.search(r"name\s*=\s*\"(.*?)\"", block)
            semester_id_match = re.search(r"semester_id\s*=\s*(\d+)", block)
            inhalt_match = re.search(r"inhalt\s*=\s*\"(.*?)\"", block, re.DOTALL)

            event_id = event_id_match.group(1) if event_id_match else None
            name = html.unescape(name_match.group(1)) if name_match else "Unbekannt"
            semester_id = semester_id_match.group(1) if semester_id_match else None
            inhalt = html.unescape(inhalt_match.group(1)) if inhalt_match else "Kein Inhalt"

            termine_matches = re.findall(r"\(termin\)\{(.*?)\}", block, re.DOTALL)
            for termin in termine_matches:
                datum_match = re.search(r"beginn_datum\s*=\s*(\d+)", termin)
                beginn_zeit_match = re.search(r"beginn_zeit\s*=\s*(\d+)", termin)
                ende_zeit_match = re.search(r"ende_zeit\s*=\s*(\d+)", termin)

                datum = convert_timestamp_to_date(datum_match.group(1)) if datum_match else None
                beginn_zeit = convert_seconds_to_time(beginn_zeit_match.group(1)) if beginn_zeit_match else None
                ende_zeit = convert_seconds_to_time(ende_zeit_match.group(1)) if ende_zeit_match else None

                events_dict[event_id]["termine"].append({
                    "datum": datum,
                    "beginn_zeit": beginn_zeit,
                    "ende_zeit": ende_zeit
                })

            events_dict[event_id].update({
                "id": event_id,
                "name": name,
                "semester_id": semester_id,
                "inhalt": inhalt
            })
        except Exception as e:
            print(f"Error parsing block: {block[:100]}... \nError: {e}")

    parsed_events = list(events_dict.values())
    return parsed_events

def fetch_events_for_modules(module_ids):
    all_events = []
    for module_id in module_ids:
        try:
            print(f"Fetching events for module_id: {module_id}")
            events_response = service.get_veranstaltungen_from_modul(module_id)
            
            # Konvertiere Rohdaten in String und speichere zur Analyse
            raw_data_str = str(events_response)
            with open(f"raw_events4_module_{module_id}.txt", "w", encoding="utf-8") as raw_file:
                raw_file.write(raw_data_str)
            print(f"Raw data for module_id {module_id} saved successfully.")

            # Parsing der Rohdaten
            parsed_events = parse_raw_event_data(raw_data_str)
            all_events.extend(parsed_events)
        except Exception as e:
            print(f"Error fetching events for module_id {module_id}: {e}")
    return all_events

def save_to_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")

def main():
    gebiet_id = 10641
    raw_modules = fetch_modules_for_gebiet(gebiet_id)
    parsed_modules = parse_module_data(raw_modules)
    save_to_json(parsed_modules, "parsed_modules4.json")

    module_ids = [modul["id"] for modul in parsed_modules]
    events_data = fetch_events_for_modules(module_ids)
    save_to_json(events_data, "parsed_events4.json")

if __name__ == "__main__":
    main()
