from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QTableWidget, QMessageBox, QDialog, \
    QMenu, QFileDialog

from src.ui.settings_dialog import SettingsDialog
from src.ui.tab_widget import TabWidget
from src.utils.history import HistoryManager
from src.utils.settings import SettingsManager

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.history_manager = HistoryManager()
        self.settings_manager = SettingsManager()
        
        self.init_ui()
        self.setup_menu()
        
    def init_ui(self):
        self.setWindowTitle("HTML标签解析器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 创建标签页管理器
        self.tab_widget = TabWidget(self)
        layout.addWidget(self.tab_widget)
        
    def setup_menu(self):
        # 创建菜单栏
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        file_menu.addAction('新建标签页', self.tab_widget.add_tab)
        file_menu.addAction('打开', self.open_file)
        file_menu.addAction('保存', self.save_file)
        file_menu.addSeparator()
        file_menu.addAction('退出', self.close)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑')
        edit_menu.addAction('设置', self.open_settings)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图')
        view_menu.addAction('历史记录', self.show_history)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        help_menu.addAction('关于', self.show_about)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            "",
            "HTML Files (*.html);;All Files (*)"
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 创建新标签页并设置内容
                current_tab = self.tab_widget.currentWidget()
                if current_tab:
                    current_tab.set_html_content(content)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开文件失败: {str(e)}")

    def save_file(self):
        current_tab = self.tab_widget.currentWidget()
        if not current_tab:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            "",
            "HTML Files (*.html);;All Files (*)"
        )
        if file_name:
            try:
                content = current_tab.get_current_content()
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(content)
                QMessageBox.information(self, "成功", "文件保存成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")

    def open_settings(self):
        try:
            dialog = SettingsDialog(self.settings, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # 更新设置
                self.settings_manager.save_settings(self.settings)
                # 应用设置
                self.apply_settings()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开设置失败: {str(e)}")

    def apply_settings(self):
        try:
            # 应用主题
            theme = self.settings.get('theme', '浅色')
            if theme == '浅色':
                self.setStyleSheet(f"""
                    QMainWindow, QDialog {{
                        background-color: #f5f5f5;
                    }}
                    QWidget {{
                        background-color: #ffffff;
                        color: #2c3e50;
                        font-size: {self.settings.get('font_size', 12)}pt;
                    }}
                    QMenuBar {{
                        background-color: #ffffff;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    QMenuBar::item:selected {{
                        background-color: #e0e0e0;
                        border-radius: 4px;
                    }}
                    QMenu {{
                        background-color: #ffffff;
                        border: 1px solid #e0e0e0;
                        padding: 5px;
                    }}
                    QMenu::item:selected {{
                        background-color: #e0e0e0;
                        border-radius: 4px;
                    }}
                    QPushButton {{
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 4px;
                    }}
                    QPushButton:hover {{
                        background-color: #2980b9;
                    }}
                    QPushButton:pressed {{
                        background-color: #2472a4;
                    }}
                    QLineEdit {{
                        padding: 8px;
                        border: 1px solid #e0e0e0;
                        border-radius: 4px;
                        background-color: #ffffff;
                    }}
                    QLineEdit:focus {{
                        border: 1px solid #3498db;
                    }}
                    QTreeWidget {{
                        border: 1px solid #e0e0e0;
                        border-radius: 4px;
                    }}
                    QTreeWidget::item {{
                        padding: 5px;
                    }}
                    QTreeWidget::item:selected {{
                        background-color: #3498db;
                        color: white;
                    }}
                    QScrollBar:vertical {{
                        border: none;
                        background: #f0f0f0;
                        width: 10px;
                        border-radius: 5px;
                    }}
                    QScrollBar::handle:vertical {{
                        background: #c0c0c0;
                        border-radius: 5px;
                    }}
                    QScrollBar::handle:vertical:hover {{
                        background: #a0a0a0;
                    }}
                """)
            else:
                self.setStyleSheet(f"""
                    QMainWindow, QDialog {{
                        background-color: #1e1e1e;
                    }}
                    QWidget {{
                        background-color: #2d2d2d;
                        color: #ffffff;
                        font-size: {self.settings.get('font_size', 12)}pt;
                    }}
                    QMenuBar {{
                        background-color: #2d2d2d;
                        border-bottom: 1px solid #3d3d3d;
                    }}
                    QMenuBar::item:selected {{
                        background-color: #3d3d3d;
                        border-radius: 4px;
                    }}
                    QMenu {{
                        background-color: #2d2d2d;
                        border: 1px solid #3d3d3d;
                        padding: 5px;
                    }}
                    QMenu::item:selected {{
                        background-color: #3d3d3d;
                        border-radius: 4px;
                    }}
                    QPushButton {{
                        background-color: #0d47a1;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 4px;
                    }}
                    QPushButton:hover {{
                        background-color: #1565c0;
                    }}
                    QPushButton:pressed {{
                        background-color: #0a3d87;
                    }}
                    QLineEdit {{
                        padding: 8px;
                        border: 1px solid #3d3d3d;
                        border-radius: 4px;
                        background-color: #2d2d2d;
                        color: white;
                    }}
                    QLineEdit:focus {{
                        border: 1px solid #0d47a1;
                    }}
                    QTreeWidget {{
                        border: 1px solid #3d3d3d;
                        border-radius: 4px;
                        background-color: #2d2d2d;
                    }}
                    QTreeWidget::item {{
                        padding: 5px;
                    }}
                    QTreeWidget::item:selected {{
                        background-color: #0d47a1;
                        color: white;
                    }}
                    QScrollBar:vertical {{
                        border: none;
                        background: #2d2d2d;
                        width: 10px;
                        border-radius: 5px;
                    }}
                    QScrollBar::handle:vertical {{
                        background: #4d4d4d;
                        border-radius: 5px;
                    }}
                    QScrollBar::handle:vertical:hover {{
                        background: #5d5d5d;
                    }}
                """)
            
            # 更新字体大小
            self.update_font_size()
            
            # 更新网络超时设置
            timeout = self.settings.get('timeout', 10)
            # 这里可以更新网络请求的超时设置
            
            # 更新历史记录限制
            max_history = self.settings.get('max_history', 100)
            self.history_manager.set_max_history(max_history)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"应用设置失败: {str(e)}")

    def update_font_size(self):
        """更新所有控件的字体大小"""
        try:
            font_size = self.settings.get('font_size', 12)
            
            # 更新主窗口字体
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)
            
            # 更新标签页中的控件字体
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if tab:
                    # 更新树形视图字体
                    tree_font = tab.tree.font()
                    tree_font.setPointSize(font_size)
                    tab.tree.setFont(tree_font)
                    
                    # 更新预览区域字体
                    preview_font = tab.preview.font()
                    preview_font.setPointSize(font_size)
                    tab.preview.setFont(preview_font)
                    
                    # 更新其他输入框字体
                    url_font = tab.url_input.font()
                    url_font.setPointSize(font_size)
                    tab.url_input.setFont(url_font)
                    
                    filter_font = tab.filter_input.font()
                    filter_font.setPointSize(font_size)
                    tab.filter_input.setFont(filter_font)
                    
            # 更新菜单字体
            menu_font = self.menuBar().font()
            menu_font.setPointSize(font_size)
            self.menuBar().setFont(menu_font)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新字体大小失败: {str(e)}")

    def show_history(self):
        class HistoryDialog(QDialog):
            def __init__(self, history, parent=None):
                super().__init__(parent)
                self.history = history
                self.init_ui()
                
            def init_ui(self):
                self.setWindowTitle("历史记录")
                self.setGeometry(100, 100, 600, 400)
                
                layout = QVBoxLayout()
                
                # 创建表格
                table = QTableWidget()
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["URL", "时间"])
                
                # 填充历史记录
                table.setRowCount(len(self.history))
                for i, entry in enumerate(self.history):
                    url_item = QTableWidgetItem(entry['url'])
                    time_item = QTableWidgetItem(
                        datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    )
                    table.setItem(i, 0, url_item)
                    table.setItem(i, 1, time_item)
                
                table.resizeColumnsToContents()
                layout.addWidget(table)
                
                self.setLayout(layout)
        
        dialog = HistoryDialog(self.history_manager.history, self)
        dialog.exec()

    def show_about(self):
        """显示关于对话框"""
        about_text = """
        ElementEye HTML元素分析器
        版本: 1.0.0
        
        这是一个用于解析和分析HTML元素的专业工具。
        
        功能特点:
        - HTML解析和可视化
        - 标签过滤和搜索
        - 标签属性查看
        - 历史记录管理
        
        作者: airhandsome
        """
        QMessageBox.about(
            self,
            "关于 ElementEye",
            about_text
        )

    def update_texts(self):
        """更新所有UI文本"""
        self.setWindowTitle(self.lang_manager.get_text("window_title"))
        # 更新菜单
        self.update_menu_texts()
        # 更新其他控件文本
        # ...
        
    def update_menu_texts(self):
        """更新菜单文本"""
        menus = self.menuBar().findChildren(QMenu)
        for menu in menus:
            if menu.title() == "文件" or menu.title() == "File":
                menu.setTitle(self.lang_manager.get_text("menu_file"))
            # ... 更新其他菜单 ...
