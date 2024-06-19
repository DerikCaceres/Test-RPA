
from RPA.Browser.Selenium import Selenium
from Assets.Libraries.Data.data import Obtain_months
from Assets.Libraries.RPA.control import Result, Retry
from Assets.Libraries.RPA.logger import RPAProcess
from Assets.Libraries.Selenium.selenium import Get_News_Atributtes
from Assets.Libraries.cfg import Settings

@RPAProcess
class P002_Access_Site():
    """ Obtém as informações do Jira """
    
    def __new__(self):
        
        self.browser = Selenium()
        self.T01_Open_Browser(self)
        self.T02_Search_News(self)
        
 
    @Retry(1)  # Em caso de erro, faz 1 nova tentativa  
    def T01_Open_Browser(self): 
        try:
            # Open browser
            self.browser.open_available_browser(Settings.Site_Url, maximized=True)

        except Exception as e:
            print(f"Erro ao abrir o navegador ou encontrar o elemento: {e}")
            raise e

        return Result(success = True, logOutput = f"Site opened", data = None)



    def T02_Search_News(self):

        self.browser.wait_until_page_contains_element(Settings.web_elements['search'], timeout=25)
        self.browser.click_element(Settings.web_elements['search'])

        # Writing the text in the search search bar
        search_input = self.browser.get_webelement(Settings.web_elements['search_bar'])
        self.browser.input_text(search_input, Settings.search_phrase)
        # Pressiona a tecla Enter no campo de busca
        self.browser.press_keys(search_input, 'ENTER')

        news_elements = self.browser.find_elements("xpath://*/ul[@class='search-results-module-results-menu']/li")
        # Itera sobre cada elemento li encontrado
        months = Obtain_months(Settings.date_range)
        for news in news_elements:  # Assumindo que há 10 elementos por página
            news_parts = news.text.split('\n')
            date = news_parts[3]
            if months in date:
                Get_News_Atributtes(news)
        
        return Result(success = True, logOutput = "News obtained.", data = None)


