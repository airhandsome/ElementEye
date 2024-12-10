from PyQt6.QtWidgets import QTabWidget
from src.ui.parser_widget import ParserWidget

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        
        # 创建第一个标签页
        self.add_tab()
        
    def add_tab(self):
        parser_widget = ParserWidget()
        index = self.addTab(parser_widget, "新标签页")
        self.setCurrentIndex(index)
        
    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
