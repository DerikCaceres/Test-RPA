
from RPA.Browser.Selenium import Selenium
from Assets.Libraries.Data.data import Obtain_months
from Assets.Libraries.RPA.control import Result, Retry
from Assets.Libraries.RPA.logger import RPAProcess
from Assets.Libraries.Selenium.selenium import Get_News_Atributtes
from Assets.Libraries.cfg import Settings

@RPAProcess
class P002_Access_Site():
    """ Obtém as informações das News """
    
    def __new__(self):
        
        self.browser = Selenium()
        self.T01_Open_Browser(self)
        self.T02_Search_News(self)
        news_data = self.T03_Get_NewsInfo(self)
        return news_data
 
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

        return Result(success = True, logOutput = "News obtained.", data = None)


    def T03_Get_NewsInfo(self):


        page_number = 1
        all_news_collected = False
        news_data = []
        months = Obtain_months(Settings.date_range)
        current_url = self.browser.get_location()

        while not all_news_collected:

            self.browser.wait_until_page_contains_element(Settings.web_elements['news'], timeout=25)
            news_elements = self.browser.find_elements(Settings.web_elements['news'])

            if not news_elements:
                # Se não houver mais elementos de notícias, saia do loop
                all_news_collected = True
                break

            for news in news_elements:
                news_parts = news.text.split('\n')
                date = news_parts[3]
                if any(month in date for month in months):
                    news_data = Get_News_Atributtes(news, news_parts, news_data)
                else:
                    # Se a data não estiver no intervalo, finalize o loop
                    all_news_collected = True
                    break

            if not all_news_collected:
                # Avança para a próxima página
                page_number += 1
                next_page_url = f"{current_url}&p={page_number}"
                self.browser.go_to(next_page_url)

        
        return Result(success = True, logOutput = "News obtained.", data = news_data)


