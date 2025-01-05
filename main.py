import sys
import os
from flask import Flask, render_template, session, request, jsonify
import pandas as pd
from io import BytesIO
from backend.time_slot_input.extract_syllabus_info import GetSallybusInfo
from backend.image_recognition.image_recognition import SallybusInfoFromImage
from backend.tor_input.pdf_to_text import GetCompSubsFromInput
from backend.llm_connection.llm_connection import LLMConnection, ChatObject
from PIL import Image
import numpy as np
import json

# Füge das Projektverzeichnis zu sys.path hinzu
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

app = Flask(__name__)
# TODO: Ändere den secret key
app.secret_key = 'your_secret_key'
llm = LLMConnection()

@app.route('/')
def home():
    # Reset all previously stored data
    session['syllabus'] = None
    session['preferences'] = None
    session['chat'] = None
    session['preferences'] = None
    return render_template('landing_page.html')

@app.route('/upload_data_page')
def upload_data_page():
    return render_template('upload_data_page.html')

@app.route('/select_interests_page', methods=['POST'])
def upload_data():
    syllabus_file = request.files.get('syllabus')
    tor_file = request.files.get('tor')

    try:
        if syllabus_file:
            # Dateiendung ermitteln
            syllabus_extension = os.path.splitext(syllabus_file.filename)[1].lower()
            if syllabus_extension == '.xlsx':
                syllabus_data_df = pd.read_excel(BytesIO(syllabus_file.read()))
                syllabus = GetSallybusInfo().from_myStudy_exel_export(syllabus_data_df)
                session['syllabus'] = syllabus
                print(syllabus)
                print("sallybus als xlsx erhallten")

            if syllabus_extension == '.png':
                image = Image.open(BytesIO(syllabus_file.read()))
                image_np = np.array(image)
                syllabus = SallybusInfoFromImage(image_np).get_info()
                session['syllabus'] = syllabus
                print('test')
                print(syllabus)


    except Exception as e:
        print(f'extracting information from syllabus was not possible: {e}')

    try:
        tor_pdf_data = BytesIO(tor_file.read())
        finished_comps = GetCompSubsFromInput().getCompSubsFromTOR(tor_pdf_data)
        session['finished_comps'] = finished_comps
    except Exception as e:
        print(f'extracting information from TOR was not possible: {e}')

    return render_template('select_interests_page.html')

def get_syllabus_frontend(day,time_stamps):
    start_hours = time_stamps[0] // 60
    start_mins = time_stamps[0] % 60

    end_hours = time_stamps[1] // 60
    end_mins = time_stamps[1] % 60

    return {"day": day.capitalize(), "start": f"{start_hours:02}:{start_mins:02}", "end": f"{end_hours:02}:{end_mins:02}"}

@app.route('/api/events')
def get_events():
    syllabus = []

    try:
        syllabus_data = session['syllabus']
        print(syllabus_data)
        for day in syllabus_data:
            for time_stamps in syllabus_data[day]:
                syllabus.append(get_syllabus_frontend(day, time_stamps))

        print(syllabus)

    except Exception as e:
        print(e)

    return jsonify(syllabus)

@app.route('/display_input', methods=['POST'])
def display_input():
    essay_preference = request.form.get('essay') == 'true'
    exam_preference = request.form.get('exam') == 'true'
    additional_prompt = request.form.get('additionalUserPrompt')

    session['preferences'] = {
        'essay': essay_preference,
        'exam': exam_preference,
        'additionalUserPrompt': additional_prompt,
    }
    
    session['chat'] = ChatObject().get_chat()

    return render_template('display_input_data_page.html')

@app.route('/complefy_chat', methods=['POST','GET'])
def complefy_chat():

    with open('backend/Pre_Sorting/modules.json', 'r') as file:
        modules = json.load(file)
        modules = modules['module']

    not_finished_ids = [] #id of modules that are not done yet

    try:
        finished_comps = session['finished_comps']
        for module in modules:
            if module['name'] in finished_comps:
                not_finished_ids.append(module['id'])
    except:
        pass

    print(not_finished_ids)

    return render_template('complefy_chat.html')

@app.route('/api/results')
def get_results():
    pass


@app.route('/chat_message', methods=['POST','GET'])
def handle_chat_message():
    data = request.get_json()  # Empfängt die Nachricht als JSON
    message = data.get('message')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Hier kannst du die Nachricht speichern oder weiterverarbeiten
    print(f"Received message: {message}")
    
    question = {"role":"user","content": message}

    awser = llm.chat_completion(session['chat'],question)
    session['chat'] = ChatObject().add_user_promt(session['chat'],question)
    session['chat'] = ChatObject().add_respones(session['chat'],awser)

    print(awser)
    print(type(awser))
    
    return jsonify({"status": "success", "message": str(awser)}), 200

if __name__ == '__main__':
    # Starte den Flask-Server
    app.run(debug=True)


#Beispiel Session dict
{'finished_comps': ['Medialitätsorientierte Zugänge zu den Naturwissenschaften', 
                    'Methodenorientierte Zugänge zu den Naturwissenschaften', 
                    'Praxisorientierte Zugänge zu den Naturwissenschaften', 
                    'Medialitätsorientierte Zugänge zu den Sozialwissenschaften', 
                    'Methodenorientierte Zugänge zu den Sozialwissenschaften', 
                    'Praxisorientierte Zugänge zu inter- und transdisziplinären Wissenschaften'], 

 'preferences': {'essay': True, 
                 'exam': False, 
                 'additionalUserPrompt': ''}, #Nutzer Promt für die LLM um weitergehende suche zu realisieren

 'sallybus': {'friday': [(855, 1020), (855, 1065), (855, 1065), (855, 1065)], 
              'monday': [], 
              'saturday': [], 
              'sunday': [], 
              'thursday': [(615, 705), (735, 825), (735, 825), (830, 965), (855, 1065)], 
              'tuesday': [(885, 1020), (885, 1020), (975, 1065)], 
              'wednesday': [(855, 1065), (840, 960), (960, 1080)]},

  'additionalUserPrompt': 'Additional Promt'
              }