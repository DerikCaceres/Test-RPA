import traceback

class Error():
    
    def __init__(self, error_message, e, critical=False, filename=None) -> None:
        """Representa um erro ocorrido durante a execução

        Args:
            error_message (_type_): O erro ocorrido
            e (_type_): A exceção
            critical (bool, optional): Informa se o erro ocorrido é critico. Erros que afetam o registro da issue no Jira devem ser considerados críticos. Defaults to "False".
        """
        
        self.filename = filename
        self.error = error_message
        self.details = e.__repr__()
        self.error_message = str(e)
        self.cause = e.__cause__
        self.stacktrace = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        self.level = "critical" if critical else "minor" 
       
    
    def as_report_data(self):
        """Retorna o HTML desse erro para que seja usado na composição do relatório"""
        
        return f"""
    
    <span id='{self.level}'>
       <strong>Erro:</strong> {self.error}
    </span>"""
    
    def __hash__(self):
        return hash((self.error, self.details))
    
    def __eq__(self, other=None):
        
        if other != None:
            return self.error == other.error and self.details == other.details
        return True
    

    def as_dict(self):
            
            issue_dict = {}
            keys = self.__dict__.keys()
            
            for key in keys:
                value = self.__dict__[key]
                
                if type(value) == list:
                    value_dict = [item.__dict__ for item in value]
                    value = value_dict
                    
                if type(value) == Error:
                    value = value.__dict__
                
                issue_dict[key] = str(value) if (type(value) != dict and type(value) != list and value != None ) else value           
            
            return issue_dict    