import locale
import sys
from Assets.Libraries.Windows.screen import SetScreenResolution
from Assets.Libraries.RPA.logger import RPAProcess
from Assets.Libraries.RPA.control import Result


@RPAProcess
class P001_Project_Setup():
    """Leitura e tratamento do json de configuração"""
    
    def __new__(self):
        
        self.T01_Project_Setup()


    def T01_Project_Setup():
        """Configurações do projeto"""
           
        locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8') # Desconsidera avisos
        
        try: sys.stdout.reconfigure(encoding='utf-8') # Configura a saída no console com codificação UTF8
        except: pass
        
        SetScreenResolution()  # Configura a resolução da tela (width=1920, heigth=1080) 

        return Result(success = True, logOutput = "COnfiguração realizda." , data = None)
    

        