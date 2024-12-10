import json
from datetime import datetime
from pathlib import Path

class HistoryManager:
    def __init__(self):
        self.history_file = Path.home() / '.html_parser' / 'history.json'
        self.history_file.parent.mkdir(exist_ok=True)
        self.history = self.load_history()
        self.max_history = 100  # 默认最大历史记录数
        
    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
        
    def add_entry(self, url):
        entry = {
            'url': url,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(entry)
        self.trim_history()  # 确保历史记录不超过最大条数
        self.save_history()
        
    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
            
    def set_max_history(self, max_history):
        self.max_history = max_history
        self.trim_history()  # 立即修剪历史记录
        
    def trim_history(self):
        """修剪历史记录以符合最大条数限制"""
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.save_history()
