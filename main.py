import sys
import os

# Füge das Projektverzeichnis zu sys.path hinzu
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, render_template, session, request
import pandas as pd
from io import BytesIO
from backend.time_slot_input.extract_syllabus_info import GetSallybusInfo
from backend.tor_input.pdf_to_text import GetCompSubsFromInput

app = Flask(__name__) 
#TODO change to secret key
app.secret_key = 'your_secret_key'

@app.route('/')  
def home():
    #Reset all previus stored data
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
        #sallybus = GetSallybusInfo().from_myStudy_exel_export(syllabus_data_df)
        #session['sallybus'] = sallybus    
    except Exception as e:
        print(f'extracting information from sallybus was not possible {e}')

    try:
        tor_pdf_data = BytesIO(tor_file.read())
        finished_comps = GetCompSubsFromInput().getCompSubsFromTOR(tor_pdf_data)
        session['finished_comps'] = finished_comps

    except Exception as e:
        print(f'extracting information from TOR was not possible {e}')

    return render_template('select_interests_page.html')

if __name__ == '__main__':
    app.run(debug=True)