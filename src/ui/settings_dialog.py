#coding=utf-8
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox,
                            QPushButton, QFormLayout, QHBoxLayout, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from src.utils.language import LanguageManager

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.lang_manager = LanguageManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(self.lang_manager.get_text("settings_title"))
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # 主题设置
        theme_label = QLabel(self.lang_manager.get_text("settings_theme"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            self.lang_manager.get_text("settings_theme_light"),
            self.lang_manager.get_text("settings_theme_dark")
        ])
        current_theme = self.settings.get('theme', self.lang_manager.get_text("settings_theme_light"))
        self.theme_combo.setCurrentText(current_theme)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        form_layout.addRow(theme_label, self.theme_combo)
        
        # 语言设置
        language_label = QLabel(self.lang_manager.get_text("settings_language"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["中文", "English"])
        current_language = self.settings.get('language', '中文')
        self.language_combo.setCurrentText(current_language)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        form_layout.addRow(language_label, self.language_combo)
        
        # 网络设置
        timeout_label = QLabel(self.lang_manager.get_text("settings_timeout"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 60)
        self.timeout_spin.setValue(self.settings.get('timeout', 10))
        form_layout.addRow(timeout_label, self.timeout_spin)
        
        # 历史记录设置
        history_label = QLabel(self.lang_manager.get_text("settings_history"))
        self.history_spin = QSpinBox()
        self.history_spin.setRange(10, 1000)
        self.history_spin.setValue(self.settings.get('max_history', 100))
        form_layout.addRow(history_label, self.history_spin)
        
        # 字体大小设置
        font_size_label = QLabel(self.lang_manager.get_text("settings_font_size"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(self.settings.get('font_size', 12))
        self.font_size_spin.valueChanged.connect(self.preview_font_size)
        
        # 字体预览
        self.preview_label = QLabel(self.lang_manager.get_text("settings_font_preview"))
        self.preview_text = QLabel()
        self.preview_text.setText(self.get_preview_text())
        self.preview_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 根据当前主题设置预览样式
        current_theme = self.settings.get('theme', '浅色')
        if current_theme == '浅色':
            self.preview_text.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f5f5f5;
                    color: #333;
                    min-height: 40px;
                    margin: 5px;
                }
            """)
        else:
            self.preview_text.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border: 1px solid #505050;
                    border-radius: 5px;
                    background-color: #2e2e2e;
                    color: #ffffff;
                    min-height: 40px;
                    margin: 5px;
                }
            """)
        
        form_layout.addRow(font_size_label, self.font_size_spin)
        form_layout.addRow(self.preview_label)
        form_layout.addRow(self.preview_text)
        
        layout.addLayout(form_layout)
        
        # 确定和取消按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton(self.lang_manager.get_text("settings_ok"))
        ok_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton(self.lang_manager.get_text("settings_cancel"))
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_preview_text(self):
        """根据当前语言获取预览文本"""
        current_language = self.language_combo.currentText()
        if current_language == "中文":
            return "你好"
        else:
            return "Hello World"
        
    def preview_font_size(self, size):
        """预览字体大小"""
        font = self.preview_text.font()
        font.setPointSize(size)
        self.preview_text.setFont(font)
        
    def on_language_changed(self, language):
        self.lang_manager.set_language(language)
        # 实时更新对话框中的文本
        self.update_texts()
        # 更新字体预览文本
        self.preview_text.setText(self.get_preview_text())
        
    def update_texts(self):
        self.setWindowTitle(self.lang_manager.get_text("settings_title"))
        # 更新其他控件的文本
        # ...
        
    def save_settings(self):
        try:
            # 保存设置
            self.settings['theme'] = self.theme_combo.currentText()
            self.settings['language'] = self.language_combo.currentText()
            self.settings['timeout'] = self.timeout_spin.value()
            self.settings['max_history'] = self.history_spin.value()
            self.settings['font_size'] = self.font_size_spin.value()
            
            # 接受对话框
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                self.lang_manager.get_text("msg_error"),
                f"{self.lang_manager.get_text('msg_save_error')}:{str(e)}"
            )
        
    def on_theme_changed(self, theme):
        """当主题改变时更新预览样式"""
        if theme == '浅色':
            self.preview_text.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f5f5f5;
                    color: #333;
                    min-height: 40px;
                    margin: 5px;
                }
            """)
        else:
            self.preview_text.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border: 1px solid #505050;
                    border-radius: 5px;
                    background-color: #2e2e2e;
                    color: #ffffff;
                    min-height: 40px;
                    margin: 5px;
                }
            """)