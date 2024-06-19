from datetime import datetime
from Assets.Libraries.RPA.inputs import GetParameter
from selenium import webdriver


class Options():

    # Indica se será acessado o Jira de Homologação
    Search_phrase = GetParameter("search_phrase") 
 
       
class Global():
    
    begin_time = datetime.now()
    
    log_directory = begin_time.strftime('./History/%Y/%m/%d/%Y-%m-%d %Hh%Mm%Ss')
    
    errors = list()
    
    browser: webdriver.Chrome
    browser_started = False
 

class Settings():

    Site_Url = 'https://www.latimes.com/'
    search_phrase = 'economy'
    date_range = 2
    Images_path = "Assets\\Libraries\\Images"
    web_elements = {
        "search":"xpath://button[@data-element='search-button']",
        "search_bar":"xpath://input[@data-element='search-form-input']",
        "confirm_search":"/html/body/div[2]/ps-search-results-module/form",
        "news":"/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/ul",
        "news_tittle":"xpath://h1[@class='headline']",
        "news_date":"xpath://time[@class='published-date']",
        "news_description":"/html/body/div[2]/div[2]/main/article/div[4]",
        "news_image":".//picture/img"

    }
