import io
import pandas as pd

def DataFramePrettier(df: pd.DataFrame, tablefmt = 'grid', index = None):
    """ Transforma o DataFrame em uma tabela melhor visível """
    return df.to_markdown(headers='keys', tablefmt=tablefmt, index=index)

def DictListToDataFrame(data: list[dict]):
    """ Transforma uma lista de dicionários em um DataFrame"""
    return pd.json_normalize(data)

def DictListPrettier(data: list[dict], tablefmt = 'grid'):
    """ Converte uma lista de dicionários em formato visual mais apresentável
    
    Args:
        data (list): Lista de dicionários para ser convertida
        tablefmt (str): Formato da tabela de saída conforme a biblioteca tabulate (Ver https://github.com/astanin/python-tabulate para outros detalhes e tipos de formatação)

    Returns:
        markdown (str): Lista formatada como tabela
    """

    df = DictListToDataFrame(data) # Cria um DataFrame
    markdown = DataFramePrettier(df, tablefmt, index = range(1, len(data)+1))  # Estiliza como tabela
    return markdown

def DictListToHTMLTable(data: list[dict], custom = ''):
    """ Converte uma lista de dicionários em formato HTML
    
    Args:
        data (list): Lista de dicionários para ser convertida
        custom (str): Script css com os estilos da tabela

    Returns:
        html (str): Lista formatada como tabela HTML juntamente com os estilos selecionados
    """

    html = DictListPrettier(data, tablefmt='html')  # Estiliza como tabela HTML

    # Por padrão utiliza o estilo CSS apresentado
    if custom != '':
        css = custom
    else:
        css = """<head>
<meta charset="UTF-8">
<style>
    .dataframe {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10px;
        border-collapse: collapse;
    }
    
    .dataframe td,
    .dataframe th {
        border: 1px solid #ddd;
        padding: 8px;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    
    .dataframe tr:hover {
        background-color: #ddd;
    }
    
    .dataframe th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #6f0ca8;
        color: white;
    }
</style>
</head>
<table class='dataframe'>"""

    return css + html.replace('<table>', '')

def FindTextInDataFrame(df: pd.DataFrame, text: str) -> list[tuple]:
    """ Procura um texto no dataframe
    
    Args:
        df: Dataframe onde o texto deve ser procurado
        text (str): Texto que deve ser procurado

    Returns:
        Lista de tuplas com os valores de linha e coluna em que o texto foi encontrado no dataframe. Exemplo: [(1,0), (2,0)]
    """

    return [(df[col][df[col].eq(text)].index[i], df.columns.get_loc(col)) for col in df.columns for i in range(len(df[col][df[col].eq(text)].index))]

def ReadJsonPandas(file: str):
    """Lê arquivo json e transforma em dataframe"""
    content = io.open(file, mode="r", encoding="utf-8").read()
    df = pd.read_json(content, encoding='utf-8', typ='series')
    return df
