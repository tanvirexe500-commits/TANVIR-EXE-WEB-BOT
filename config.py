import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///free_uids.db'
    
    # Discord Configuration
    DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    DISCORD_CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID')
    
    # External API
    UID_API_URL = os.environ.get('UID_API_URL') or 'http://46.250.239.109:6020'
    
    # Pastebin Configuration
    PASTEBIN_URL = os.environ.get('PASTEBIN_URL') or 'https://pastebin.com/raw/jj1pZfNu'
    
    # Server Configuration
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5001)
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
