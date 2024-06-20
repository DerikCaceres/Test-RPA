
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
        news_data = self.T03_Get_NewsInfo(self)['data']
        return news_data
 
    @Retry(1)  # Em caso de erro, faz 1 nova tentativa  
    def T01_Open_Browser(self): 
        try:
            # Open browser
            self.browser.open_available_browser(Settings.Site_Url, maximized=True)

        except Exception as e:
            raise Exception ("Failure to open browser: ", e)

        return Result(success = True, logOutput = f"Site opened", data = None)


    @Retry(1)
    def T02_Search_News(self):
        """Search the news on the portal"""

        #failure to open browser
        self.browser.wait_until_page_contains_element(Settings.web_elements['search'], timeout=25)
        self.browser.click_element(Settings.web_elements['search'])

        # Writing the text in the search search bar
        search_input = self.browser.get_webelement(Settings.web_elements['search_bar'])
        self.browser.input_text(search_input, Settings.search_phrase)
        # Pressiona a tecla Enter no campo de busca
        self.browser.press_keys(search_input, 'ENTER')
        
        return Result(success = True, logOutput = "News obtained.", data = None)


    def T03_Get_NewsInfo(self):
        """Get information from the news found"""

        page_number = 1
        all_news_collected = False
        news_data = []
        #Get valid search months
        months = Obtain_months(Settings.date_range)
        current_url = self.browser.get_location()

        while not all_news_collected:

            self.browser.wait_until_page_contains_element(Settings.web_elements['news'], timeout=25)
            news_elements = self.browser.find_elements(Settings.web_elements['news'])

            if not news_elements:
                # If there are no more news elements, exit the loop
                all_news_collected = True
                break

            for news in news_elements:
                news_parts = news.text.split('\n')
                date = news_parts[3]
                if any(month in date for month in months):
                    news_data = Get_News_Atributtes(news, news_parts, news_data)
                else:
                    # If the date is not in range, end the loop
                    all_news_collected = True
                    break

            if not all_news_collected:
                #Advance to the next page
                page_number += 1
                next_page_url = f"{current_url}&p={page_number}"
                self.browser.go_to(next_page_url)

        
        return Result(success = True, logOutput = "News information obtained.", data = news_data)


