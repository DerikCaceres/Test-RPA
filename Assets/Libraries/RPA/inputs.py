import os
from Assets.Libraries.Windows.file import ReadJson

json_inputs = False
inputs_path = f".\\Assets\\input.json"

if os.path.isfile(inputs_path):
    json_inputs = True
    inputs = ReadJson(inputs_path)


def GetParameter(parameter_name: str) -> str:
    """Obtém o valor de um parâmetro do arquivo de entradas ou das variáveis de ambiente

    Args:
        parameter_name (str): O identificador do parâmetro.

    Returns:
        str: parâmetro obtido
    """
    
    return inputs[parameter_name] if json_inputs else os.getenv(parameter_name)

