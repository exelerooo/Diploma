# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from language_exercise_generator import LanguageExerciseGenerator
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
CORS(app)

# Конфигурация
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'csv', 'txt'}

# Инициализация генератора
generator = LanguageExerciseGenerator(
    model_path="path_to_your_model",
    vocabulary_path="default_vocabulary.csv"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/upload_vocabulary', methods=['POST'])
def upload_vocabulary():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Обновляем словарь в генераторе
        generator.update_vocabulary(filepath)
        
        return jsonify({'message': 'Vocabulary uploaded successfully'})
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/generate_exercises', methods=['POST'])
def generate_exercises():
    data = request.json
    vocabulary = data.get('vocabulary', [])
    exercise_types = data.get('types', ['gap_fill', 'paraphrase', 'matching', 'translation'])
    
    try:
        exercises = generator.generate_exercises(vocabulary)
        return jsonify(exercises)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_essay', methods=['POST'])
def analyze_essay():
    data = request.json
    essay_text = data.get('text', '')
    
    try:
        analysis = generator.analyze_essay(essay_text)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
