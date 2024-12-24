from flask import Flask, render_template, request
import model_one
import importlib
import os
app = Flask(__name__, template_folder='templates')  # Указываем папку для шаблонов


@app.before_request #ПЕРЕЗАГРУЗКА МОДЕЛИ после обновления страницы
def reload_model():
    global model
    model = importlib.reload(importlib.import_module('model_one'))


@app.route('/',  methods=['GET', 'POST'])
def index():
    return render_template('index.html', tomorrow=model_one.tomorrow, week = model_one.week, month=model_one.month, quater =model_one.quarter)

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    global model #загрузка при первой загрузке 
    model = importlib.import_module('model_one')    
    app.run(host="localhost", port=port, debug=True)
