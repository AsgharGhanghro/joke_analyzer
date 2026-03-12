import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))

    # Google Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # Model
    MODEL_PATH = os.getenv('MODEL_PATH')
    TOKENIZER_PATH = os.getenv('TOKENIZER_PATH')
    DEVICE = os.getenv('DEVICE', 'cpu')
    MAX_LENGTH = int(os.getenv('MAX_LENGTH', '128'))

    # Voice Processing
    ENABLE_VOICE = os.getenv('ENABLE_VOICE', 'True').lower() == 'true'
    MAX_AUDIO_SIZE = int(os.getenv('MAX_AUDIO_SIZE', '10485760'))

    # Battery System
    BATTERY_DECAY_RATE = float(os.getenv('BATTERY_DECAY_RATE', '0.1'))
    BATTERY_RECHARGE_TIME = int(os.getenv('BATTERY_RECHARGE_TIME', '300'))

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')