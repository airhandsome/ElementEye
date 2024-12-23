# ElementEye - HTML元素分析器

ElementEye 是一个用于解析和分析HTML元素的可视化工具，它提供了直观的界面来查看和过滤网页中的HTML标签结构。

## 功能特点

- 🔍 **HTML解析**: 输入URL即可解析网页结构
- 🌲 **树形视图**: 以树形结构展示HTML元素的层级关系
- 🏷️ **快捷标签**: 常用HTML标签的快速过滤按钮
- 🔎 **实时过滤**: 支持按标签名、class、id或属性进行过滤
- 📋 **标签预览**: 查看选中元素的完整HTML代码
- 📝 **复制功能**: 一键复制选中元素的HTML代码
- 📜 **历史记录**: 保存已访问的URL记录

## 安装要求

- Python 3.8+
- PyQt6
- BeautifulSoup4
- aiohttp

## 安装步骤

1. 克隆仓库：
bash
git clone https://github.com/airhandsome/ElementEye.git
cd ElementEye


2. 安装依赖：
bash
pip install -r requirements.txt

3. 运行程序：
bash
python main.py
2. 在URL输入框中输入要解析的网页地址

3. 点击"解析"按钮开始解析

4. 使用过滤框或快捷标签按钮筛选特定元素

5. 在树形视图中选择元素可以：
   - 预览元素的HTML代码
   - 右键复制元素代码
   - 查看元素的属性信息

## 项目结构

```bash
ElementEye/
├── src/
│ ├── core/
│ │ └── parser.py # HTML解析核心
│ ├── ui/
│ │ ├── main_window.py # 主窗口
│ │ └── parser_widget.py # 解析器界面
│ ├── utils/
│ │ ├── history.py # 历史记录管理
│ │ └── logger.py # 日志工具
│ └── main.py # 程序入口
├── requirements.txt # 依赖列表
└── README.md # 项目说明
```

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 作者

- airhandsome

## 致谢

感谢以下开源项目：
- PyQt6
- BeautifulSoup4
- aiohttp
