import requests
from bs4 import BeautifulSoup
from src.utils.logger import get_logger

logger = get_logger(__name__)

class HTMLParser:
    def __init__(self):
        self.soup = None
        
    def parse_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
            return True
        except Exception as e:
            logger.error(f"解析URL失败: {str(e)}")
            return False
            
    def get_element_tree(self):
        if not self.soup:
            return None
        return self._build_element_tree(self.soup)
        
    def _build_element_tree(self, element):
        if element.name is None:
            return None
            
        node = {
            'name': element.name,
            'attrs': element.attrs,
            'text': str(element),
            'children': []
        }
        
        for child in element.children:
            if child.name is not None:
                child_node = self._build_element_tree(child)
                if child_node:
                    node['children'].append(child_node)
                    
        return node
