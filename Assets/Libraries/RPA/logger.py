import cgitb
import coloredlogs
import inspect
import logging
import os
import sys
from time import perf_counter
from Assets.Libraries.cfg import Global

execution_start = perf_counter() # início da contagem do tempo de execuçao

class RPALogging:
    
    def __init__(self) -> None:
        
        #Configura o padrao de formataçao do logger
        formatterStr = '''%(asctime)s,%(msecs)d %(name)s %(levelname)s => %(message)s

* params: %(params)-8s
* function duration: %(runningTime)-15s | * time elapsed: %(totalRunningTime)-15s
* success:%(success)-8s
* output: %(output)-8s

'''
        #Cria a pasta onde será armazenado o log
        logPath = Global.begin_time.strftime('./History/%Y/%m/%d/%Y-%m-%d %Hh%Mm%Ss')
        os.makedirs(logPath, exist_ok=True)
        
        cgitb.enable(display=1, logdir=logPath, context=5, format='text')
        
        #Cria um file handler que será reponsável pela escrita dos logs em um arquivo
        fh = logging.FileHandler( filename=logPath + "/logger.log", encoding='UTF-8')
        
        #Determina que logs a partir do nível DEBUG devem ser logados no arquivo de saída
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt=formatterStr,
                                    datefmt='%Y-%m-%d %H:%M:%S',
                                    defaults={
                                        'totalRunningTime': None,
                                        'name': os.getlogin(),
                                        'description': None,
                                        'runningTime': None,
                                        'params': None,
                                        'success': None,
                                        'output': None
                                    }
                                    )
        fh.setFormatter(formatter)
        
        # loggin config
        logging.basicConfig(format=formatterStr,
                            datefmt='%d-%m-%Y %H:%M:%S',
                            level=logging.INFO,
                            encoding='UTF-8',
                            handlers=[fh]
                            ),
        
        coloredlogs.install(level='INFO')
        
        self.StartLogger()
    
    def StartLogger(self):
    
        # Loga a inicialização do processo
        logger = logging.getLogger("[START]")
        logger.info(f"Process started by {os.getlogin()}. Args: {sys.argv}")

    def TerminateLogger(code):
        
        #Loga a finalização do processo
        logger = logging.getLogger("[END]")
        
        
        end = perf_counter()  # fim da contagem do tempo de execuçao
        total_runningTime = "{0:.6f}s".format(end - execution_start)  # calcula o tempo de execuçao
        logger.info(f"Process finished with code {code}. Duration: {total_runningTime} s")
    
                 
    def Task(f):
               
        def inner(*args, **kwargs):
            
            error = None
            logger = logging.getLogger("[" + str(f.__qualname__.split('.')[0]).upper() + "] [" + str(f.__name__.split('.')[0]).upper() + "] ")  #define o nome do logger como TASK
            start = perf_counter()  # início da contagem do tempo de execuçao

            try:
                f_result = f(*args, **kwargs)  # tenta executar a chamada da funçao
                result = f_result
                
                

                if(result == None or ( 'success' not in result or 'logOutput' not in result or 'data' not in result)):
                    if result == None:
                        result = { }             
                    result['success'] = False
                    excpt = f'{f.__name__} não retorna um dos seguintes atributos obrigatórios: success, logOutput or data.'
                    raise Exception(excpt)

            except Exception as e:  # em caso de exceçao, adiciona os dados da exceçao no log
                
                error_output = cgitb.text(sys.exc_info(), context=1) #"".join(traceback.format_exception(type(e), e, e.__traceback__, 3))
                
                
                result = {
                    'logOutput': error_output,
                    'success': False
                }
                
                error = e
                
                
            end = perf_counter()   # fim da contagem do tempo de execuçao
            runningTime = "{0:.6f}s".format(end - start)  # calcula o tempo de execuçao
            total_runningTime = "{0:.6f}s".format(end - execution_start)  # calcula o tempo de execuçao
            
            arguments = [str(a)[:8000] for a in args]  # cria uma lista de todos os argumentos posicionais passados para a funçao
            kwarguments = ["{0}:{1}".format(k, v) for (k, v) in kwargs.items()]  # cria uma lista de todos os argumentos nomeados passados para a funçao

        
            # monta o objeto de log
            logData = {
                'description': f.__doc__,  # usa a docstring da funçao como descriçao do log
                'runningTime': runningTime,  #tempo de execuçao,
                'totalRunningTime': total_runningTime,  #tempo de execuçao
                'params': arguments + kwarguments,  #parâmetros de execuçao
                'output': result['logOutput'],  #saída de log da funçao
                'success': " " + str(result['success']).lower()  #status da execuçao
            }
            
        
            #Caso a funçao tenha sido executada com sucesso, log um debug, caso nao, loga um warning
            if  error != None:
                
                #loga a exceçao
                logger.exception( f.__doc__, extra=logData)
                
                #propaga a exceçao
                raise error 
            else:
                #loga a execuçao
                logger.info(f.__doc__, extra=logData) if result['success'] else logger.warning(
                f.__doc__, extra=logData)
                
                #retorna o resultado da funçao
                return result
        
        return inner
    
def RPAProcess(cls):

    for name, fn in inspect.getmembers(cls, inspect.isfunction):
        if name != "__new__":
            setattr(cls, name, RPALogging.Task(fn))
    return cls
