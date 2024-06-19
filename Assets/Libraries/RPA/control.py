import cgitb
from functools import wraps
import sys
import time
import traceback
from Assets.Libraries.RPA.logger import RPALogging


def OnErrorRaise(error): 
    """ Exceção mais informativa, que deve ser lançada caso ocorra uma exceção ao chamar a função """
    
    def dec(f):
            @wraps(f)
            def inner(*args, **kwargs):
                
                    try:
                        return f(*args, **kwargs)
                    except Exception as e:     
                        raise Exception(f"{error}.")
            return inner
    return dec
    
def TerminateAll(e):
    """Chama o evento de erro e finaliza a execução"""  
    RPALogging.TerminateLogger(1)
    sys.exit(1)  # Stop execution with error result
    

def Terminate():
    """Finaliza a execução """
    RPALogging.TerminateLogger(0)
    sys.exit(0)  # Stop execution
      
def Result(success: bool, logOutput, data):
    """Retorna o resultado da task"""
    
    result = {
        'success' : success,
        'logOutput' : logOutput,
        'data' : data
    }
   
    return result
    
def Retry(times : float, onErrorFunction = None): 
    """ Tenta chamar a função dado número de vezes antes de lançar uma exceção"""
    
    def dec(f):
        @wraps(f)
        def inner(*args, **kwargs):
            for i in range(times):
                try:
                    return f(*args, **kwargs)
                except Exception as e:     
                    if(i == (times-1)):
                        raise e
                    else:
                        if(onErrorFunction != None):
                            onErrorFunction()
                        time.sleep(0.100)
        return inner
    return dec
