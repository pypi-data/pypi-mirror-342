""" 简单的解析工具 """
from lxml import html
from bs4 import BeautifulSoup

class HtmlXPathTree():
    """用于检索HTMl信息"""
    def __init__(self,html_content:str) -> None:
        self.tree = html.fromstring(html_content)
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def xpath(self,xpath_word:str)->str:
        """使用xpath引导

        Args:
            xpath_word (str): xpath语法

        Returns:
            str: tree
        """
        return self.tree.xpath(xpath_word)
