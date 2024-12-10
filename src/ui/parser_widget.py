from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QLabel, QTreeWidget, QTreeWidgetItem,
                            QTextEdit, QMessageBox, QMenu, QFileDialog, QApplication)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction
from src.core.parser import HTMLParser
from src.utils.history import HistoryManager
from src.utils.logger import get_logger
import asyncio
import aiohttp
from bs4 import BeautifulSoup

logger = get_logger(__name__)

class ParserThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, url):
        super().__init__()
        self.url = url

    async def fetch_url(self):
        try:
            timeout = aiohttp.ClientTimeout(total=10)  # 10秒超时
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.url, headers=headers) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        raise Exception(f"HTTP错误: {response.status}")
        except Exception as e:
            self.error.emit(str(e))
            return None

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(self.fetch_url())
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                self.finished.emit(soup)
            loop.close()
        except Exception as e:
            self.error.emit(str(e))

class ParserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parser = HTMLParser()
        self.history_manager = HistoryManager()
        self.common_tags = [
            ('div', '容器'),
            ('p', '段落'),
            ('a', '链接'),
            ('img', '图片'),
            ('span', '行内'),
            ('ul', '列表'),
            ('li', '列表项'),
            ('h1', '标题1'),
            ('input', '输入'),
            ('button', '按钮')
        ]
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # URL输入区域
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入网页地址...")
        self.parse_button = QPushButton("解析")
        self.parse_button.clicked.connect(self.parse_url)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.parse_button)
        
        # 过滤区域
        filter_layout = QHBoxLayout()
        filter_label = QLabel("过滤:")
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("输入标签名、class、id或属性...")
        self.filter_input.textChanged.connect(self.filter_tree)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        
        # 快捷标签按钮区域
        tags_scroll = QWidget()
        tags_layout = QHBoxLayout(tags_scroll)
        tags_layout.setSpacing(5)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        
        for tag, tooltip in self.common_tags:
            tag_btn = QPushButton(tag)
            tag_btn.setToolTip(tooltip)
            tag_btn.setMaximumHeight(25)
            tag_btn.setMinimumWidth(40)
            tag_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e3f2fd;  /* 浅蓝色背景 */
                    border: 1px solid #90caf9;  /* 蓝色边框 */
                    border-radius: 3px;
                    padding: 2px 8px;
                    font-size: 11px;
                    color: #1976d2;  /* 深蓝色文字 */
                }
                QPushButton:hover {
                    background-color: #bbdefb;  /* 鼠标悬停时的颜色 */
                    border-color: #64b5f6;
                }
                QPushButton:pressed {
                    background-color: #90caf9;  /* 按下时的颜色 */
                }
            """)
            tag_btn.clicked.connect(lambda checked, t=tag: self.apply_tag_filter(t))
            tags_layout.addWidget(tag_btn)
        
        tags_layout.addStretch()  # 添加弹性空间
        
        # 树形视图
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["标签", "属性"])
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        
        # 预览区域
        preview_label = QLabel("标签预览:")
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        
        # 添加所有组件到主布局
        main_layout.addLayout(url_layout)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(tags_scroll)
        main_layout.addWidget(self.tree)
        main_layout.addWidget(preview_label)
        main_layout.addWidget(self.preview)

    def parse_url(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入URL")
            return
            
        # 确保URL包含协议
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_input.setText(url)
            
        try:
            self.parser_thread = ParserThread(url)
            self.parser_thread.finished.connect(self.handle_parsing_finished)
            self.parser_thread.error.connect(self.handle_parsing_error)
            self.parser_thread.start()
            
            # 添加到历史记录
            self.history_manager.add_entry(url)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建解析线程失败: {str(e)}")

    def handle_parsing_finished(self, soup):
        self.update_tree(soup)

    def handle_parsing_error(self, error_msg):
        QMessageBox.critical(self, "错误", f"解析失败: {error_msg}")

    def update_tree(self, soup):
        self.tree.clear()
        self.build_tree_items(soup, self.tree)

    def build_tree_items(self, element, parent):
        if element.name is None:
            return
            
        attrs = ' '.join([f'{k}="{v}"' for k, v in element.attrs.items()])
        item = QTreeWidgetItem(parent)
        item.setText(0, element.name)
        item.setText(1, attrs)
        item.setData(0, Qt.ItemDataRole.UserRole, str(element))
        
        for child in element.children:
            if child.name is not None:
                self.build_tree_items(child, item)

    def filter_tree(self, filter_text):
        filter_text = filter_text.lower()
        
        def filter_items(item):
            tag_text = item.text(0).lower()
            attrs_text = item.text(1).lower()
            matches = filter_text in tag_text or filter_text in attrs_text
            
            child_visible = False
            for i in range(item.childCount()):
                if filter_items(item.child(i)):
                    child_visible = True
            
            is_visible = matches or child_visible
            item.setHidden(not is_visible)
            return is_visible
        
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            filter_items(root.child(i))

    def apply_tag_filter(self, tag):
        self.filter_input.setText(tag)

    def show_context_menu(self, position):
        menu = QMenu()
        copy_action = QAction("复制标签", self)
        copy_action.triggered.connect(self.copy_current_tag)
        menu.addAction(copy_action)
        
        preview_action = QAction("预览标签", self)
        preview_action.triggered.connect(self.preview_current_tag)
        menu.addAction(preview_action)
        
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def copy_current_tag(self):
        item = self.tree.currentItem()
        if item:
            tag_html = item.data(0, Qt.ItemDataRole.UserRole)
            QApplication.clipboard().setText(tag_html)

    def preview_current_tag(self):
        item = self.tree.currentItem()
        if item:
            tag_html = item.data(0, Qt.ItemDataRole.UserRole)
            self.preview.setText(tag_html)
