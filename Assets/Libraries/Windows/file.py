
import io
import json

def ReadJson(file):
    """Lê arquivo json e transforma em dicionário"""
    content = io.open(file, mode="r", encoding="utf-8-sig").read()
    dict = json.loads(content)
    return dict
 
