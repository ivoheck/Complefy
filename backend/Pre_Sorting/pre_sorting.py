import os
import json

def filter_unfinished_events(modules_file, criteria_file, events_dir, output_file):
    # Load module data
    with open(modules_file, 'r', encoding='utf-8') as f:
        modules = json.load(f)["module"]
    
    # Create a mapping of module names to IDs
    module_name_to_id = {module["name"]: module["id"] for module in modules}
    
    # Load filter criteria
    with open(criteria_file, 'r', encoding='utf-8') as f:
        criteria = json.load(f)
    
    # Get finished module IDs based on names in criteria
    finished_module_ids = {module_name_to_id[name] for name in criteria["finished_comps"] if name in module_name_to_id}
    
    # Initialize a list to store events from unfinished modules
    unfinished_events = []
    
    # Iterate over files in the events directory
    for filename in os.listdir(events_dir):
        if filename.startswith("parsed_events_module_") and filename.endswith(".json"):
            # Extract module ID from the filename
            mod_id = int(filename.replace("parsed_events_module_", "").replace(".json", ""))
            
            # Skip finished modules
            if mod_id in finished_module_ids:
                continue
            
            # Load events from the file
            with open(os.path.join(events_dir, filename), 'r', encoding='utf-8') as f:
                events = json.load(f)
            
            # Add events to the result list
            unfinished_events.extend(events)
    
    # Write the result to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unfinished_events, f, ensure_ascii=False, indent=4)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the script directory
modules_file = os.path.join(script_dir, "modules.json")
criteria_file = os.path.join(script_dir, "filter_criteria.json")
events_dir = os.path.join(script_dir, "parsed_events")
output_file = os.path.join(script_dir, "unfinished_events.json")

filter_unfinished_events(modules_file, criteria_file, events_dir, output_file)
