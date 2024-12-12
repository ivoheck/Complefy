from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')  
def home():
    return render_template('landing_page.html')

@app.route('/upload_data_page')
def upload_data_page():
    return render_template('upload_data_page.html')


if __name__ == '__main__':
    app.run(debug=True)