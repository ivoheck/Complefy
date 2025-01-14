import json
import os
import sys

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

            # Überprüfung und Extraktion der Veranstaltungen
            if isinstance(events_response, tuple):
                events_response = events_response[0] if len(events_response) > 0 else None
            
            if events_response and hasattr(events_response, 'veranstaltungen'):
                events_list = events_response.veranstaltungen
                if not isinstance(events_list, list):
                    events_list = [events_list]

                for event in events_list:
                    event_dict = {
                        "id": event.id,
                        "name": event.name,
                        "semester_id": event.semester_id,
                        "veranstaltungsart": {
                            "id": event.veranstaltungsart.id,
                            "name": event.veranstaltungsart.langtext
                        },
                        "termine": [
                            {
                                "id": termin.id,
                                "datum": termin.beginn_datum,
                                "beginn_zeit": termin.beginn_zeit,
                                "ende_zeit": termin.ende_zeit,
                                "raum": termin.raum.kurztext if termin.raum else None
                            }
                            for termin in event.termine
                        ],
                        "dozenten": [
                            {
                                "id": person.id,
                                "name": f"{person.vorname} {person.nachname}"
                            }
                            for person in event.personen
                        ]
                    }
                    all_events.append(event_dict)
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
