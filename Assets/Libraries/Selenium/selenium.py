    
import os

import requests
from selenium.webdriver.common.by import By
from Assets.Libraries.Data.data import Count_ocurrences, Verify_money_in_text
from Assets.Libraries.cfg import Settings



def Get_News_Atributtes(news, news_parts, news_data):

    title = news_parts[1]  # Junta as duas primeiras partes com um espaço
    description = news_parts[2]
    
    try:
        page_identifier = ' '.join(title.split(' ')[3:6])
    except:
        page_identifier = ' '.join(title.split(' ')[0:3])
    #getting image
    filepath = Download_news_Image(news, page_identifier)
    money_in_text = Verify_money_in_text(title, description)
    ocurrences = Count_ocurrences(title, description)

    news_data.append({
        "Title": title,
        "Description": description,
        "Filepath": filepath,
        "Money_in_text": money_in_text,
        "Occurrences": ocurrences
    })

    return news_data


def Download_news_Image(news, page_identifier):
    try:
        img_element = news.find_element(By.TAG_NAME, 'img')
        img_url = img_element.get_attribute('src')

        # Fazer o download da imagem usando requests
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            # Verificar se o diretório existe, caso contrário, criar
            if not os.path.exists(Settings.Images_path):
                os.makedirs(Settings.Images_path)

            # Caminho completo para salvar a imagem
            filepath = os.path.join(Settings.Images_path, f"{page_identifier}.png")

            # Salvar a imagem
            with open(filepath, 'wb') as f:
                f.write(response.content)

            return filepath
    
        else:
            print(f"Não foi possível baixar a imagem. Código de status: {response.status_code}")

    except Exception as e:
        print(f"Erro ao baixar a imagem: {str(e)}")