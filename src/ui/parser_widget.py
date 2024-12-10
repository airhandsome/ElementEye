from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QLabel, QTreeWidget, QTreeWidgetItem,
                             QTextEdit, QMessageBox, QMenu, QFileDialog, QApplication, QProgressDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction
from src.core.parser import HTMLParser
from src.utils.history import HistoryManager
from src.utils.logger import get_logger
import asyncio
import aiohttp
from urllib.parse import urlparse
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
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
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    return await response.text()
        except Exception as e:
            self.error.emit(str(e))
            return None

    def run(self):
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 执行异步请求
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
        self.thread_pool = ThreadPoolExecutor(max_workers=4)  # 线程池
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
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
        self.filter_input.textChanged.connect(self.apply_filter)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        
        # 树形视图
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["标签", "属性"])
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.itemClicked.connect(self.preview_tag)
        
        # 预览区域
        preview_label = QLabel("标签预览:")
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        self.export_button = QPushButton("导出")
        self.export_button.clicked.connect(self.export_to_file)
        self.copy_button = QPushButton("复制")
        self.copy_button.clicked.connect(self.copy_current_tag)
        
        toolbar_layout.addWidget(self.export_button)
        toolbar_layout.addWidget(self.copy_button)
        toolbar_layout.addStretch()
        
        # 添加所有组件到主布局
        layout.addLayout(url_layout)
        layout.addLayout(filter_layout)
        layout.addWidget(self.tree)
        layout.addWidget(preview_label)
        layout.addWidget(self.preview)
        layout.addLayout(toolbar_layout)
        
    def normalize_url(self, url):
        """规范化URL，添加协议头如果没有的话"""
        url = url.strip()
        if not url:
            return url
            
        if not re.match(r'^https?://', url):
            # 如果URL包含www.，默认使用https
            if url.startswith('www.'):
                return f'https://{url}'
            # 否则尝试http
            return f'http://{url}'
        return url

    def parse_url(self):
        url = self.normalize_url(self.url_input.text())
        if not url:
            QMessageBox.warning(self, "警告", "请输入有效的URL")
            return

        # 显示进度对话框
        self.progress_dialog = QProgressDialog("正在解析...", "取消", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.show()

        # 创建并启动解析线程
        self.parser_thread = ParserThread(url)
        self.parser_thread.finished.connect(self.handle_parsing_finished)
        self.parser_thread.error.connect(self.handle_parsing_error)
        self.parser_thread.progress.connect(self.progress_dialog.setValue)
        self.parser_thread.start()

    def handle_parsing_finished(self, soup):
        self.progress_dialog.close()
        if soup:
            self.history_manager.add_entry(self.url_input.text())
            self.update_tree(soup)

    def handle_parsing_error(self, error_msg):
        self.progress_dialog.close()
        QMessageBox.critical(self, "错误", f"解析失败: {error_msg}")

    def update_tree(self, soup):
        """更新树形结构"""
        self.tree.clear()
        self.build_tree_items(soup, self.tree)
            
    def build_tree_items(self, element, parent):
        """递归构建树形结构"""
        if element.name is None:
            return
            
        # 创建树节点
        attrs = ' '.join([f'{k}="{v}"' for k, v in element.attrs.items()])
        item = QTreeWidgetItem(parent)
        item.setText(0, element.name)
        item.setText(1, attrs)
        item.setData(0, Qt.ItemDataRole.UserRole, str(element))
        
        # 递归处理子元素
        for child in element.children:
            if child.name is not None:
                self.build_tree_items(child, item)
            
    def apply_filter(self):
        filter_text = self.filter_input.text().lower()
        self.filter_tree_items(self.tree.invisibleRootItem(), filter_text)
        
    def filter_tree_items(self, item, filter_text):
        for i in range(item.childCount()):
            child = item.child(i)
            
            tag_text = child.text(0).lower()
            attrs_text = child.text(1).lower()
            
            matches = filter_text in tag_text or filter_text in attrs_text
            
            # 检查子项
            has_visible_children = False
            for j in range(child.childCount()):
                if not child.child(j).isHidden():
                    has_visible_children = True
                    break
                    
            child.setHidden(not (matches or has_visible_children))
            
            # 如果当前项可见，确保所有父节点可见
            if not child.isHidden():
                parent = child.parent()
                while parent:
                    parent.setHidden(False)
                    parent = parent.parent()
                    
            # 递归处理子项
            self.filter_tree_items(child, filter_text)
            
    def show_context_menu(self, position):
        menu = QMenu()
        copy_action = QAction("复制标签", self)
        copy_action.triggered.connect(self.copy_current_tag)
        menu.addAction(copy_action)
        
        preview_action = QAction("预览标签", self)
        preview_action.triggered.connect(lambda: self.preview_tag(self.tree.currentItem()))
        menu.addAction(preview_action)
        
        menu.exec(self.tree.viewport().mapToGlobal(position))
        
    def copy_current_tag(self):
        item = self.tree.currentItem()
        if item:
            tag_html = item.data(0, Qt.ItemDataRole.UserRole)
            QApplication.clipboard().setText(tag_html)
            
    def preview_tag(self, item):
        if item:
            tag_html = item.data(0, Qt.ItemDataRole.UserRole)
            self.preview.setText(tag_html)
            
    def export_to_file(self):
        if not self.preview.toPlainText():
            QMessageBox.warning(self, "警告", "没有可导出的内容")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "导出文件",
            "",
            "HTML Files (*.html);;All Files (*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.preview.toPlainText())
                QMessageBox.information(self, "成功", "文件导出成功")
            except Exception as e:
                logger.error(f"导出文件时发生错误: {str(e)}")
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def set_html_content(self, content):
        """设置HTML内容"""
        self.preview.setText(content)
        # 可以添加解析逻辑

    def get_current_content(self):
        """获取当前内容"""
        return self.preview.toPlainText()
