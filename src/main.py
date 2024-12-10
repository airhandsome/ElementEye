# coding = utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from PyQt6.QtWidgets import QApplication

from src.utils.settings import SettingsManager
from ui.main_window import MainWindow
from utils.logger import setup_logger


def main():
    # 设置日志
    setup_logger()

    # 加载配置
    settings_manager = SettingsManager()
    settings = settings_manager.load_settings()

    # 创建应用
    app = QApplication(sys.argv)

    # 创建主窗口
    window = MainWindow(settings)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
