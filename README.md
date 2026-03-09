Turbolearn ai is a Flask-based AI learning assistant that converts long educational content into quick and engaging learning material.
The system accepts PDF documents or YouTube lecture URLs and automatically generates:



📄 Concise summaries
🧠 Key concepts
❓ Quiz questions
🔊 Audio explanations
🎬 Short learning videos
This helps students understand long content in minutes instead of hours.



🚀 Features


📄 PDF Processing
Upload a PDF document and the system extracts text using PyPDF2, then sends it to AI for analysis.
🎥 YouTube Video Processing
Paste a YouTube video URL and the system:
Extracts transcripts using youtube-transcript-api / pytube
Cleans and merges transcript text
Sends it to AI for structured learning content


🧠 AI Content Generation
Using Gemini AI, the system generates:
summary
key concepts
Quiz questions with answers
Subject keywords
🔊 Audio Generation
The generated summary is converted into speech using gTTS, allowing users to listen to explanations.
🎬 Video Generation
The system automatically creates short educational videos:
For Math / Science / Physics
Animated formula explanations
For General Subjects
Animated slides with key points
Videos are generated using MoviePy.
🏗 System Architecture
Frontend


Bootstrap Dashboard
Backend



Flask (Python)
AI Engine
Gemini API
Content Processing
PyPDF2
youtube-transcript-api
pytube
Media Generation
gTTS (Audio)
MoviePy (Video)
📂 Project Structure




AI-Knowledge-Helper
│
├── app.py
│
├── utils
│   ├── pdf_extractor.py
│   ├── youtube_extractor.py
│   ├── gemini_engine.py
│   ├── audio_gen.py
│   └── video_gen.py
│
├── templates
│   └── index.html
│
├── static
│   ├── uploads
│   ├── audio
│   └── video
│
└── README.md
⚙️ Installation
Clone the repository:
Bash

git clone https://github.com/your-username/ai-knowledge-helper.git
Navigate to the project folder:
Bash

cd ai-knowledge-helper
Install dependencies:
Bash

pip install -r requirements.txt
Run the Flask server:
Bash

python app.py
Open in browser:

http://127.0.0.1:5000
🧠 How It Works
1️⃣ User uploads a PDF or pastes a YouTube URL
2️⃣ The system extracts content
3️⃣ AI analyzes the content using Gemini
4️⃣ The system generates:
Summary
Concepts
Quiz
5️⃣ Audio explanation is generated
6️⃣ A short learning video is created
7️⃣ Results appear in the dashboard.
🎯 Use Cases
Students summarizing lectures
Quick revision before exams
Converting long videos into quick learning
AI-assisted learning platforms
📸 Interface
The dashboard provides:
PDF Upload
YouTube URL input
Process Content button
Summary card
Concepts card
Quiz section
Audio player
Video player
⚡ Performance Optimization
To handle long YouTube videos:
Transcripts are chunked
AI summarizes segments
Final result is condensed into 1–2 minute learning content
🔒 Security
API keys are stored using environment variables and not pushed to GitHub.
Example:

.env
GEMINI_API_KEY=your_api_key


🛠 Technologies Used


Python
Flask
PyPDF2
youtube-transcript-api
pytube
Gemini API
gTTS
MoviePy
Bootstrap


📌 Future Improvements
Multi-language support
AI flashcards generation
AI note-taking assistant
Mobile-friendly UI
Real-time lecture summarization
