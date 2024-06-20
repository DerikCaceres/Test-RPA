from Assets.Libraries.Data.pandas import DataFramePrettier
from Assets.Libraries.RPA.control import Result
from Assets.Libraries.RPA.logger import RPAProcess
from Assets.Libraries.Windows.file import CreateFile
from Assets.Libraries.cfg import Settings
import pandas as pd

@RPAProcess
class P003_Write_In_Excel_File():
    """Register the news information in an excel"""
    
    def __new__(self, news_data):
       
        self.T01_Create_Excel_File(news_data)
        

    def T01_Create_Excel_File(news_data):
        """Cria um novo arquivo json com as issues obtidas do jira"""

        news_df = pd.DataFrame(news_data)

        # Dataframe to excel
        news_df.to_excel(Settings.worksheet_news_path, index=False)
        #Save Log
        CreateFile(Settings.log_worksheet, DataFramePrettier(news_df))

        return Result(success = True, logOutput = "", data = None)
