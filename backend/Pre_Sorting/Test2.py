import json
import re

# Assuming MyStudyWebService is already implemented and available
from Service.WebService import MyStudyWebService

# Initialize the web service client
wsdl_url = "https://mystudy.leuphana.de/mystudy_webservice.wsdl"
service = MyStudyWebService(wsdl_url)

# Step 1: Fetch modules for the specified gebiet_id
def fetch_modules_for_gebiet(gebiet_id):
    try:
        print(f"Fetching modules for gebiet_id: {gebiet_id}")
        modules = service.get_module_from_gebiet(gebiet_id)
        print("Modules fetched successfully.")
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

        modules = []
        module_blocks = re.findall(r"\(modul\)\{.*?\}", raw_data, re.DOTALL)

        for block in module_blocks:
            module = {}
            id_match = re.search(r"id = (\d+)", block)
            if id_match:
                module["id"] = int(id_match.group(1))

            name_match = re.search(r"name = \"(.*?)\"", block)
            if name_match:
                module["name"] = name_match.group(1)

            if module:
                modules.append(module)

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
    except Exception as e:
        print(f"Error while extracting module IDs: {e}")
    return module_ids

# Step 4: Save modules to a JSON file for inspection
def save_modules_to_json(modules, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(modules, f, indent=4, ensure_ascii=False)
        print(f"Modules successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving modules to JSON: {e}")

# Step 5: Fetch events for each module and save raw data to a file
def fetch_events_for_modules(module_ids):
    if not module_ids:
        print("No module IDs to fetch events for.")
        return []

    events_data = []
    for module_id in module_ids:
        try:
            events = service.get_veranstaltungen_from_modul(module_id)
            event_list = []
            for event in events:
                if len(event) < 6:  # Prüfen, ob das Tupel die erwartete Länge hat
                    print(f"Skipping incomplete event for module_id {module_id}: {event}")
                    continue
                event_dict = {
                    "id": event[0],  # Index 0: ID der Veranstaltung
                    "name": event[1],  # Index 1: Name der Veranstaltung
                    "semester_id": event[4],  # Index 4: Semester-ID
                    "veranstaltungsart": {
                        "id": event[5][0],  # Index 0 im Sub-Tupel: ID der Veranstaltungsart
                        "name": event[5][1]  # Index 1 im Sub-Tupel: Name der Veranstaltungsart
                    } if event[5] else None
                }
                event_list.append(event_dict)
            with open(f"raw_events_module_{module_id}.json", "w", encoding="utf-8") as f:
                json.dump(event_list, f, indent=4, ensure_ascii=False)
            events_data.extend(event_list)
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

# Main function to coordinate the workflow
def main():
    gebiet_id = 10641
    raw_modules = fetch_modules_for_gebiet(gebiet_id)
    parsed_modules = manual_parse_modules(raw_modules)
    save_modules_to_json(parsed_modules, "modules.json")
    module_ids = extract_module_ids(parsed_modules)
    events_data = fetch_events_for_modules(module_ids)
    save_to_txt(events_data, "veranstaltungen.txt")

if __name__ == "__main__":
    main()
