# Interview Ready

## Overview
Interview Ready is an AI-powered interview preparation tool designed to simulate real interview experiences. It serves as a clone of Google Interview, helping candidates practice by providing AI-generated questions based on the uploaded job description and submitted resume. 

The platform features a **Google Meet-like** environment where users answer questions verbally, simulating a real interview. AI processes responses, evaluates performance, and dynamically adjusts follow-up questions, making the experience as close to an actual interview as possible.

## Features
- **Job-Specific Questions**: AI generates interview questions based on your resume and job description.
- **Real-Time Voice Processing**: Utilizes Whisper ASR for speech-to-text conversion.
- **AI Evaluation**:
  - Assesses correctness, grammar, and technical accuracy.
  - Adjusts next questions based on previous responses.
  - Provides an overall score and detailed feedback.
- **Multiple Interview Modes**: HR interview, technical interview, and more.
- **Performance Feedback**:
  - Scores for individual questions.
  - Identifies grammatical errors and correctness of responses.
  - Provides recommendations for improvement.

## Future Enhancements
- **Coding Platform**: A whiteboard coding environment for practicing technical interviews.
- **Expanded AI Models**: More specialized interview models for different industries and roles.

## Technologies Used
- **Whisper ASR**: Converts speech to text.
- **AI-Based Evaluation**: Analyzes responses and generates feedback.
- **Real-Time Question Adaptation**: Adjusts difficulty and content based on answers.

## How It Works
1. Upload your **job description** and **resume**.
2. AI generates and asks interview questions in a **video-call-like interface**.
3. You answer verbally, and **Whisper ASR converts speech to text**.
4. AI evaluates your response and **modifies follow-up questions** accordingly.
5. At the end, you receive:
   - **An overall score**.
   - **Detailed feedback on each question**.
   - **Advice on improving your responses**.

## Installation & Usage
### Setting up the Django-based Application
1. **Create a Virtual Environment:**
   - For Unix/macOS:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```
   - For Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Create and Configure Environment Variables:**
   ```sh
   cp example.env .env
   ```
   Edit the `.env` file to match your configuration.
4. **Create a PostgreSQL Database:**
   - Ensure PostgreSQL is installed and running.
   - Create a new database
5. **Apply Migrations:**
   ```sh
   python manage.py migrate
   ```
6. **Create a Superuser:**
   ```sh
   python manage.py createsuperuser
   ```
7. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```

