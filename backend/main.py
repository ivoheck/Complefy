from flask import Flask

app = Flask(__name__) 

@app.route('/')  
def home():
    return "TODO welcome page"


if __name__ == '__main__':
    print('test')
    app.run(debug=True)