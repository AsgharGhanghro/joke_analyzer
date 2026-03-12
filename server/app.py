# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS # type: ignore
# import random
# import logging
# import re
# import os
# from config import Config


# from google import genai 
# from google.genai import types # type: ignore


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# app = Flask(__name__, static_folder='../client')
# CORS(app)

# client = genai.Client(api_key=Config.GEMINI_API_KEY)

# def analyze_joke_features(joke):
#     features = {
#         'has_question': '?' in joke,
#         'has_exclamation': '!' in joke,
#         'has_because': 'because' in joke.lower(),
#         'has_why': 'why' in joke.lower(),
#         'word_count': len(joke.split()),
#         'has_punctuation': bool(re.search(r'[.,;:!?]', joke)),
#         'has_ellipsis': '...' in joke,
#         'has_setup_punchline': len(joke.split()) > 6 and ('?' in joke or 'because' in joke.lower())
#     }
#     return features

# def evaluate_joke_score(joke):
#     features = analyze_joke_features(joke)
#     score = 50
    
#     if features['has_setup_punchline']: score += 20
#     if features['has_question'] and features['has_exclamation']: score += 15
#     if features['has_question']: score += 10
#     if features['has_exclamation']: score += 8
#     if features['has_because']: score += 12
#     if features['has_why']: score += 10
#     if features['has_ellipsis']: score += 5
    
#     word_count = features['word_count']
#     if 10 <= word_count <= 30: score += 10
#     elif 5 <= word_count < 10 or 30 < word_count <= 50: score += 5
#     elif word_count < 5: score -= 10
#     else: score -= 5
    
#     pun_words = ['bear', 'bare', 'son', 'sun', 'flower', 'flour', 'see', 'sea', 'write', 'right', 'knight', 'night']
#     if any(word in joke.lower() for word in pun_words): score += 15
    
#     score += random.randint(-8, 8)
#     return max(0, min(100, round(score)))

# def get_feedback_and_rating(score):
#     if score >= 90: return "🤯 LEGENDARY! This joke is pure comedy gold!", "LEGENDARY"
#     elif score >= 80: return "😂 HILARIOUS! You should be on stage with that one!", "EXCELLENT"
#     elif score >= 70: return "😆 EXCELLENT! That would get big laughs anywhere!", "GREAT"
#     elif score >= 60: return "😄 VERY GOOD! Solid joke structure and timing!", "GOOD"
#     elif score >= 50: return "🙂 GOOD JOKE! Not bad at all.", "AVERAGE"
#     elif score >= 40: return "😐 AVERAGE. Could use some polishing.", "BELOW AVERAGE"
#     elif score >= 30: return "😕 BELOW AVERAGE. The punchline needs work.", "POOR"
#     elif score >= 20: return "😬 POOR JOKE. Try a different approach.", "BAD"
#     else: return "💀 TERRIBLE! My circuits are crying...", "TERRIBLE"

# @app.route('/')
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/health')
# def health_check():
#     return jsonify({"status": "online", "message": "JokeBot API v2.0"})

# @app.route('/evaluate', methods=['POST'])
# def evaluate_joke():
#     try:
#         data = request.json
#         joke = data.get('joke', '').strip()
        
#         if not joke: return jsonify({"error": "No joke provided"}), 400
#         if len(joke.split()) < 3: return jsonify({"error": "Joke too short", "suggestion": "Add more words"}), 400
        
#         logger.info(f"Evaluating joke: {joke[:50]}...")
#         score = evaluate_joke_score(joke)
#         feedback, rating = get_feedback_and_rating(score)
        
#         return jsonify({
#             "quality_score": score,
#             "rating": rating,
#             "feedback": feedback,
#             "model_used": True
#         })
#     except Exception as e:
#         logger.error(f"Error: {str(e)}")
#         return jsonify({"error": "Evaluation failed", "quality_score": 50, "feedback": "Error in evaluation", "rating": "ERROR"}), 500

# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided in request"}), 400

#     audio_file = request.files['audio']
    
    
#     raw_mime_type = request.form.get('mimeType', 'audio/webm')
    
    
#     base_mime_type = raw_mime_type.split(';')[0]

#     try:
        
#         audio_bytes = audio_file.read()
        
#         file_size = len(audio_bytes)
#         logger.info(f"Received audio size: {file_size} bytes, Format: {base_mime_type}")
        
#         if file_size < 100:
#             logger.error("The audio file is empty or corrupted!")
#             return jsonify({"error": "Microphone didn't capture audio. File is empty."}), 400
            
#         logger.info("Sending inline audio to Gemini...")
        
#         response = client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=[
#                 "You are an expert transcriptionist. Listen to the following audio and transcribe it EXACTLY as spoken. Do not add formatting, do not guess words, and do not provide commentary. Return ONLY the text.",
#                 types.Part.from_bytes(
#                     data=audio_bytes,
#                     mime_type=base_mime_type
#                 )
#             ]
#         )
            
      
#         if response.text:
#             transcript = response.text.strip()
#             logger.info(f"Transcription successful: {transcript}")
#             return jsonify({"transcript": transcript})
#         else:
#             logger.warning("Gemini returned an empty response (no speech detected).")
#             return jsonify({"error": "No clear speech detected. Please speak louder!"}), 400
            
#     except Exception as e:
#         logger.error(f"Transcription error: {str(e)}")
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/<path:path>')
# def serve_static(path):
#     return send_from_directory(app.static_folder, path)

# if __name__ == '__main__':
#     logger.info("🚀 Starting JokeBot Server v2.0...")
#     logger.info("🌐 Server running at: http://127.0.0.1:5000")
#     app.run(host='0.0.0.0', port=5000, debug=True)



from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # type: ignore
import random
import logging
import re
from config import Config
from google import genai
from google.genai import types  # type: ignore
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../client')
CORS(app)

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def analyze_joke_features(joke):
    features = {
        'has_question': '?' in joke,
        'has_exclamation': '!' in joke,
        'has_because': 'because' in joke.lower(),
        'has_why': 'why' in joke.lower(),
        'word_count': len(joke.split()),
        'has_punctuation': bool(re.search(r'[.,;:!?]', joke)),
        'has_ellipsis': '...' in joke,
        'has_setup_punchline': len(joke.split()) > 6 and ('?' in joke or 'because' in joke.lower())
    }
    return features


def evaluate_joke_score(joke):
    features = analyze_joke_features(joke)
    score = 50

    if features['has_setup_punchline']:
        score += 20
    if features['has_question'] and features['has_exclamation']:
        score += 15
    if features['has_question']:
        score += 10
    if features['has_exclamation']:
        score += 8
    if features['has_because']:
        score += 12
    if features['has_why']:
        score += 10
    if features['has_ellipsis']:
        score += 5

    word_count = features['word_count']
    if 10 <= word_count <= 30:
        score += 10
    elif 5 <= word_count < 10 or 30 < word_count <= 50:
        score += 5
    elif word_count < 5:
        score -= 10
    else:
        score -= 5

    pun_words = [
        'bear','bare','son','sun','flower','flour',
        'see','sea','write','right','knight','night'
    ]

    if any(word in joke.lower() for word in pun_words):
        score += 15

    score += random.randint(-8, 8)

    return max(0, min(100, round(score)))


def get_feedback_and_rating(score):

    if score >= 90:
        return "🤯 LEGENDARY! This joke is pure comedy gold!", "LEGENDARY"

    elif score >= 80:
        return "😂 HILARIOUS! You should be on stage with that one!", "EXCELLENT"

    elif score >= 70:
        return "😆 EXCELLENT! That would get big laughs anywhere!", "GREAT"

    elif score >= 60:
        return "😄 VERY GOOD! Solid joke structure and timing!", "GOOD"

    elif score >= 50:
        return "🙂 GOOD JOKE! Not bad at all.", "AVERAGE"

    elif score >= 40:
        return "😐 AVERAGE. Could use some polishing.", "BELOW AVERAGE"

    elif score >= 30:
        return "😕 BELOW AVERAGE. The punchline needs work.", "POOR"

    elif score >= 20:
        return "😬 POOR JOKE. Try a different approach.", "BAD"

    else:
        return "💀 TERRIBLE! My circuits are crying...", "TERRIBLE"


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/health')
def health_check():
    return jsonify({
        "status": "online",
        "message": "JokeBot API v2.0"
    })



@app.route('/evaluate', methods=['POST'])
def evaluate_joke():

    try:
        data = request.json
        joke = data.get('joke', '').strip()

        if not joke:
            return jsonify({"error": "No joke provided"}), 400

        if len(joke.split()) < 3:
            return jsonify({
                "error": "Joke too short",
                "suggestion": "Add more words"
            }), 400

        logger.info(f"Evaluating joke: {joke[:60]}")

        score = evaluate_joke_score(joke)
        feedback, rating = get_feedback_and_rating(score)

        return jsonify({
            "quality_score": score,
            "rating": rating,
            "feedback": feedback,
            "model_used": True
        })

    except Exception as e:

        logger.error(f"Evaluation error: {str(e)}")

        return jsonify({
            "error": "Evaluation failed",
            "quality_score": 50,
            "feedback": "Error in evaluation",
            "rating": "ERROR"
        }), 500


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    audio_bytes = audio_file.read()

    if len(audio_bytes) < 100:
        return jsonify({
            "error": "Audio too small. Speak louder."
        }), 400

    try:

        logger.info(f"Audio received: {len(audio_bytes)} bytes")

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=[

                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type="audio/webm"
                ),

                "Transcribe this speech to text. Return only spoken words."
            ]
        )

        transcript = ""

        if hasattr(response, "text") and response.text:
            transcript = response.text.strip()

        elif response.candidates:
            transcript = response.candidates[0].content.parts[0].text.strip()

        if transcript:

            logger.info(f"Transcript: {transcript}")

            return jsonify({
                "transcript": transcript
            })

        else:

            return jsonify({
                "error": "No clear speech detected"
            }), 400

    except Exception as e:

        logger.error(f"Transcription error: {str(e)}")

        return jsonify({
            "error": str(e)
        }), 500


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':

    logger.info("🚀 Starting JokeBot Server v2.0...")
    logger.info("🌐 Server running at: http://127.0.0.1:5000")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )