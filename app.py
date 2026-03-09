import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from utils.pdf_extractor import extract_text_from_pdf
from utils.youtube_extractor import extract_transcript_from_url
from utils.gemini_engine import process_content
from utils.audio_gen import generate_audio
from utils.video_gen import generate_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'
app.config['VIDEO_FOLDER'] = 'static/video'

# Ensure directories exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['AUDIO_FOLDER'], app.config['VIDEO_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    content_type = request.form.get('type')
    text = ""
    
    if content_type == 'pdf':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        
    elif content_type == 'url':
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        text = extract_transcript_from_url(url)
    
    if not text:
        print(f"DEBUG: Extraction failed for {content_type}")
        return jsonify({'error': f'Failed to extract text from {content_type}'}), 500
    
    print(f"DEBUG: Extracted text length: {len(text)}")
    
    # Process with Gemini
    ai_data, error_msg = process_content(text)
    if not ai_data:
        print(f"DEBUG: AI Processing failed: {error_msg}")
        return jsonify({'error': f'AI processing failed: {error_msg}'}), 500
    
    # Generate Media
    audio_file = generate_audio(ai_data['summary'])
    # Video generation is expensive, might want to trigger it separately or handle async
    # For now, let's just return the data and offer a button to generate video
    
    return jsonify({
        'summary': ai_data['summary'],
        'concepts': ai_data['concepts'],
        'quiz': ai_data['quiz'],
        'keywords': ai_data['keywords'],
        'audio_url': f'/static/audio/{audio_file}'
    })

@app.route('/generate_video', methods=['POST'])
def video_gen():
    summary = request.json.get('summary')
    keywords = request.json.get('keywords')
    video_file = generate_video(summary, keywords)
    return jsonify({'video_url': f'/static/video/{video_file}'})

if __name__ == '__main__':
    app.run(debug=True)
