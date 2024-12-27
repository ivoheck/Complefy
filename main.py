import sys
import os
from flask import Flask, render_template, session, request
import pandas as pd
from io import BytesIO
from backend.time_slot_input.extract_syllabus_info import GetSallybusInfo
from backend.tor_input.pdf_to_text import GetCompSubsFromInput

# Füge das Projektverzeichnis zu sys.path hinzu
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

app = Flask(__name__)
# TODO: Ändere den secret key
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    # Reset all previously stored data
    session = None
    return render_template('landing_page.html')

@app.route('/upload_data_page')
def upload_data_page():
    return render_template('upload_data_page.html')

@app.route('/select_interests_page', methods=['POST'])
def upload_data():
    syllabus_file = request.files.get('syllabus')
    tor_file = request.files.get('tor')

    try:
        syllabus_data_df = pd.read_excel(BytesIO(syllabus_file.read()))
        sallybus = GetSallybusInfo().from_myStudy_exel_export(syllabus_data_df)
        session['sallybus'] = sallybus
    except Exception as e:
        print(f'extracting information from syllabus was not possible: {e}')

    try:
        tor_pdf_data = BytesIO(tor_file.read())
        finished_comps = GetCompSubsFromInput().getCompSubsFromTOR(tor_pdf_data)
        session['finished_comps'] = finished_comps
    except Exception as e:
        print(f'extracting information from TOR was not possible: {e}')

    return render_template('select_interests_page.html')

@app.route('/complefy_chat', methods=['POST','GET'])
def complefy_chat():

    essay_preference = request.form.get('essay') == 'true'
    exam_preference = request.form.get('exam') == 'true'
    additional_prompt = request.form.get('additionalUserPrompt')

    session['preferences'] = {
        'essay': essay_preference,
        'exam': exam_preference,
        'additionalUserPrompt': additional_prompt,
    }
    
    print(session)
    return render_template('complefy_chat.html')

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