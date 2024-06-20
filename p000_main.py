from Assets.Libraries.RPA.control import Terminate, TerminateAll
from Assets.Libraries.RPA.logger import RPALogging
from p001_project_setup import P001_Project_Setup
from p002_yahoo_news import P002_Access_Site
from p003_write_in_excel_file import P003_Write_In_Excel_File

RPALogging()

try:

    P001_Project_Setup()
    news_data = P002_Access_Site()
    P003_Write_In_Excel_File(news_data)
    Terminate()

except Exception as e:
    
    TerminateAll(e)
    
