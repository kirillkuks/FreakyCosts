from typing import override, Dict

from html.parser import HTMLParser as HtmlParser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from characters_list import characters_list, CharacterCost
from excel_saver import ExcelSaver


class GentorHtmlParser(HtmlParser):
    class _ParsingContext:
        character_name = ''
        constelation_index = 0
        constelation_tag: bool = False

        result: Dict[str, CharacterCost] = {}
    
    _parsing_context : _ParsingContext = None

    def __init__(self):
        self._parsing_context = GentorHtmlParser._ParsingContext()
        super().__init__(convert_charrefs=True)

    def get_result(self) -> Dict[str, CharacterCost]:
        assert self._parsing_context is not None
        return self._parsing_context.result

    @override
    def feed(self, html_data: str):
        start_index = html_data.find('<planilhas-detalhamento-personagens')
        html_data = html_data[start_index:]

        end_tag = '</planilhas-detalhamento-personagens'
        end_index = html_data.find(end_tag)
        html_data = html_data[:end_index + (len(end_tag)) + 1]

        super().feed(html_data)

    @override
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self._parsing_context.constelation_index = 0
        elif tag == 'td':
            self._parsing_context.constelation_tag = True

    @override
    def handle_endtag(self, tag):
        if tag == 'tr' and len(self._parsing_context.character_name) > 0:
            self._parsing_context.character_name = ''
        if tag == 'td':
            self._parsing_context.constelation_tag = False
    
    @override
    def handle_data(self, data):
        if not self._parsing_context.constelation_tag:
            return

        prepared_text = data.strip()

        if prepared_text in characters_list:
            self._parsing_context.character_name = prepared_text
            self._parsing_context.result[self._parsing_context.character_name] = CharacterCost()
            
        try:
            cost_value = int(prepared_text)

            self._parsing_context.result[self._parsing_context.character_name].set_constelation_value_by_index(
                self._parsing_context.constelation_index,
                cost_value
            )

            self._parsing_context.constelation_index += 1
        except ValueError as _:
            _


def load_gentor_html_as_str() -> str:
    gentor_url = 'https://gentor.vercel.app/planilhas/3'

    chrome_service = Service(executable_path=ChromeDriverManager().install())
    chrome_startup_options = Options()
    chrome_startup_options.add_argument('--headless')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_startup_options)

    driver.get(gentor_url)
    
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, 'planilhas-detalhamento-personagens'))
            )
    except Exception as _:
        print('Unable to load Getor url')

    return str(driver.page_source)


if __name__ == '__main__':
    gentor_html = load_gentor_html_as_str()
    
    gentor_html_parser = GentorHtmlParser()
    gentor_html_parser.feed(gentor_html)
    constelation_data = gentor_html_parser.get_result()

    saver = ExcelSaver()
    saver.save('costs', constelation_data)
