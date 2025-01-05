import json
import re
import os
import sys

# Verzeichnis des Projekts (Root-Verzeichnis) ermitteln
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # Passe die Anzahl der '..' an

# Projekt-Root zu sys.path hinzufügen, falls noch nicht enthalten
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Assuming MyStudyWebService is already implemented and available
from backend.Service.WebService import MyStudyWebService

# Initialize the web service client
wsdl_url = "https://mystudy.leuphana.de/mystudy_webservice.wsdl"
service = MyStudyWebService(wsdl_url)

# Step 1: Fetch modules for the specified gebiet_id
def fetch_modules_for_gebiet(gebiet_id):
    try:
        #print(f"Fetching modules for gebiet_id: {gebiet_id}")  # Debugging output
        modules = service.get_module_from_gebiet(gebiet_id)  # Corrected function
        #print(f"Raw Modules fetched: {modules}")  # Debugging output
        # Save raw data directly after fetching
        with open("raw_modules.json", "w", encoding="utf-8") as f:
            f.write(str(modules))
        return modules
    except Exception as e:
        print(f"Error fetching modules for gebiet_id {gebiet_id}: {e}")
        return None

# Step 2: Manually parse and extract relevant data from raw module data
def manual_parse_modules(raw_data):
    try:
        if not isinstance(raw_data, str):
            raw_data = str(raw_data)

        print("Starting manual parsing of raw data...")
        modules = []
        # Split data by module blocks
        module_blocks = re.findall(r"\(modul\)\{.*?\}", raw_data, re.DOTALL)

        for block in module_blocks:
            module = {}
            # Extract ID
            id_match = re.search(r"id = (\d+)", block)
            if id_match:
                module["id"] = int(id_match.group(1))

            # Extract Name
            name_match = re.search(r"name = \"(.*?)\"", block)
            if name_match:
                module["name"] = name_match.group(1)

            # Add more fields as necessary...

            if module:
                modules.append(module)

        #print(f"Manually parsed modules: {modules}")
        return {"module": modules}
    except Exception as e:
        print(f"Error during manual parsing: {e}")
        return None

# Step 3: Extract module IDs from the manually parsed modules
def extract_module_ids(parsed_modules):
    if not parsed_modules or "module" not in parsed_modules:
        print("No valid modules to extract IDs from.")
        return []

    module_ids = []
    try:
        for mod in parsed_modules.get("module", []):
            if "id" in mod:
                module_ids.append(mod["id"])
            else:
                print(f"Module missing 'id': {mod}")
    except Exception as e:
        print(f"Error while extracting module IDs: {e}")
    #print(f"Extracted Module IDs: {module_ids}")  # Debugging output
    return module_ids

# Step 4: Save modules to a JSON file for inspection
def save_modules_to_json(modules, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(modules, f, indent=4, ensure_ascii=False)
        print(f"Modules successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving modules to JSON: {e}")

# Step 5: Fetch events for each module and save to a text file
def fetch_events_for_modules(module_ids):
    if not module_ids:
        print("No module IDs to fetch events for.")
        return []

    events_data = []
    for module_id in module_ids:
        try:
            #print(f"Fetching events for module ID: {module_id}")
            events = service.get_veranstaltungen_from_modul(module_id)
            #print(f"Events for Module {module_id}: {events}")  # Debugging output
            for event in events:
                events_data.append({
                    "id": event.id,
                    "name": event.name,
                    "content": event.inhalt,
                    "goals": event.ziel,
                    "semester_id": event.semester_id,
                    "veranstaltungsart": {
                        "id": event.veranstaltungsart.id,
                        "name": event.veranstaltungsart.langtext,
                    } if hasattr(event, 'veranstaltungsart') else None,
                    "persons": [
                        {
                            "id": person.id,
                            "firstname": person.vorname,
                            "lastname": person.nachname,
                            "title": person.titel,
                        }
                        for person in getattr(event, 'personen', [])
                    ],
                    "termine": [
                        {
                            "id": termin.id,
                            "raum": termin.raum.langtext if hasattr(termin, 'raum') else None,
                            "time": termin.string if hasattr(termin, 'string') else None,
                        }
                        for termin in getattr(event, 'termine', [])
                    ],
                })
        except Exception as e:
            print(f"Error fetching events for module_id {module_id}: {e}")
    return events_data

# Step 6: Save events data to a text file
def save_to_txt(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            if data:
                for item in data:
                    f.write(f"{json.dumps(item, indent=4, ensure_ascii=False)}\n\n")
            else:
                f.write("No events to save.")
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to text file: {e}")

def get_module_ids():
    gebiet_id = 10641
    raw_modules = fetch_modules_for_gebiet(gebiet_id)
    parsed_modules = manual_parse_modules(raw_modules)
    return extract_module_ids(parsed_modules)

# Main function to coordinate the workflow
def main():
    gebiet_id = 10641
    raw_modules = fetch_modules_for_gebiet(gebiet_id)
    parsed_modules = manual_parse_modules(raw_modules)  # Manually parse raw data
    save_modules_to_json(parsed_modules, "modules.json")  # Save modules for inspection
    module_ids = extract_module_ids(parsed_modules)
    events_data = fetch_events_for_modules(module_ids)
    save_to_txt(events_data, "veranstaltungen.txt")

if __name__ == "__main__":
    main()
