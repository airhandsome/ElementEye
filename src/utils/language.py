from src.config.translations import TRANSLATIONS

class LanguageManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_language = "中文"
        return cls._instance
    
    def set_language(self, language):
        if language in TRANSLATIONS:
            self.current_language = language
            
    def get_text(self, key):
        return TRANSLATIONS[self.current_language].get(key, key) 