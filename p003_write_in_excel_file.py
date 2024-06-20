from Assets.Libraries.RPA.control import Result
from Assets.Libraries.RPA.logger import RPAProcess
from Assets.Libraries.cfg import Settings

@RPAProcess
class P003_Write_In_Excel_File():
    """Register the news information in an excel"""
    
    def __new__(self, news_data):
       
        self.T01_Create_Excel_File(news_data)
        

    def T01_Create_Excel_File(news_data):
        """Cria um novo arquivo json com as issues obtidas do jira"""
        
        return Result(success = True, logOutput = "", data = None)
