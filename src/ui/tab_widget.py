from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import Qt
from src.ui.parser_widget import ParserWidget

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        
        # 设置样式表
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444444;
                background: #2b2b2b;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #353535;
                color: #ffffff;
                padding: 8px 12px;
                margin-right: 2px;
                border: 1px solid #444444;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2b2b2b;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background: #404040;
            }
            QTabBar::close-button {
                image: url(resources/close.png);
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background: #ff4444;
                border-radius: 2px;
            }
        """)
        
        # 创建第一个标签页
        self.add_tab()
        
    def add_tab(self):
        parser_widget = ParserWidget()
        index = self.addTab(parser_widget, "新标签页")
        self.setCurrentIndex(index)
        
    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
