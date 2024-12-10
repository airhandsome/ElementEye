import json
from pathlib import Path

from src.core.parser import logger


class SettingsManager:
    def __init__(self):
        self.settings_file = Path.home() / '.html_parser' / 'settings.json'
        self.settings_file.parent.mkdir(exist_ok=True)
        self.settings = self.load_settings()

    def load_settings(self):
        if self.settings_file.exists():
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_settings()

    def save_settings(self, settings):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"保存设置失败: {str(e)}")
            raise

    def get_default_settings(self):
        return {
            'theme': 'light',
            'language': 'zh_CN',
            'max_history': 100,
            'export_format': 'html'
        }
