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
            with open(f"raw_events_module_{module_id}.json", "w", encoding="utf-8") as f:
                json.dump(events, f, indent=4, ensure_ascii=False)

            for event in events:
                termine_data = []
                if isinstance(event[-1], list):
                    for termin in event[-1]:
                        termine_data.append({
                            "id": termin[0],
                            "raum": termin[1]["kurztext"] if termin[1] else None,
                            "beginn_datum": termin[2],
                            "ende_datum": termin[3],
                            "beginn_zeit": termin[4],
                            "ende_zeit": termin[5],
                            "tag": termin[6]
                        })
                else:
                    print(f"No termine found for event ID {event[0]}")

                event_data = {
                    "id": event[0],
                    "name": event[1],
                    "content": event[2],
                    "goals": event[3],
                    "semester_id": event[4],
                    "veranstaltungsart": {
                        "id": event[5][0],
                        "name": event[5][1],
                    } if event[5] else None,
                    "persons": [
                        {
                            "id": person[0],
                            "firstname": person[1],
                            "lastname": person[2],
                            "title": person[3],
                        }
                        for person in event[6]
                    ] if isinstance(event[6], list) else [],
                    "termine": termine_data
                }
                events_data.append(event_data)

        except Exception as e:
            print(f"Error fetching events for module_id {module_id}: {e}")
    return events_data

# Step 6: Parse and transform raw events data to JSON format
def parse_raw_events_to_json(raw_event_file):
    try:
                with open(raw_event_file, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)

                print("Starting parsing of raw events data...")
        events = []
        event_blocks = re.findall(r"\(veranstaltung\)\{.*?\}", raw_data, re.DOTALL)

        for block in event_blocks:
            event = {}
            id_match = re.search(r"id = (\d+)", block)
            if id_match:
                event["id"] = int(id_match.group(1))

            name_match = re.search(r"name = \"(.*?)\"", block)
            if name_match:
                event["name"] = name_match.group(1)

            inhalt_match = re.search(r'inhalt = "(.*?)"', block, re.DOTALL)
            if inhalt_match:
                event["inhalt"] = inhalt_match.group(1).replace("\n", " ")

            ziel_match = re.search(r'ziel = "(.*?)"', block, re.DOTALL)
            if ziel_match:
                event["ziel"] = ziel_match.group(1).replace("\n", " ")

            semester_id_match = re.search(r"semester_id = (\d+)", block)
            if semester_id_match:
                event["semester_id"] = int(semester_id_match.group(1))

            # Extract termine if available
            termine_blocks = re.findall(r"\(termin\)\{.*?\}", block, re.DOTALL)
            termine_list = []
            for termin_block in termine_blocks:
                termin = {}
                termin_id_match = re.search(r"id = (\d+)", termin_block)
                if termin_id_match:
                    termin["id"] = int(termin_id_match.group(1))

                beginn_datum_match = re.search(r"beginn_datum = (\d+)", termin_block)
                if beginn_datum_match:
                    termin["beginn_datum"] = int(beginn_datum_match.group(1))

                ende_datum_match = re.search(r"ende_datum = (\d+)", termin_block)
                if ende_datum_match:
                    termin["ende_datum"] = int(ende_datum_match.group(1))

                beginn_zeit_match = re.search(r"beginn_zeit = (\d+)", termin_block)
                if beginn_zeit_match:
                    termin["beginn_zeit"] = int(beginn_zeit_match.group(1))

                ende_zeit_match = re.search(r"ende_zeit = (\d+)", termin_block)
                if ende_zeit_match:
                    termin["ende_zeit"] = int(ende_zeit_match.group(1))

                tag_match = re.search(r"tag = \"(.*?)\"", termin_block)
                if tag_match:
                    termin["tag"] = tag_match.group(1)

                termine_list.append(termin)

            event["termine"] = termine_list
            events.append(event)

        output_file = raw_event_file.replace("raw_", "parsed_")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4, ensure_ascii=False)

        print(f"Parsed events saved to {output_file}")
    except Exception as e:
        print(f"Error parsing raw events: {e}")

# Step 7: Save events data to a text file
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

    for module_id in module_ids:
        raw_event_file = f"raw_events_module_{module_id}.json"
        parse_raw_events_to_json(raw_event_file)

if __name__ == "__main__":
    main()
