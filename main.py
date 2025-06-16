import requests
from bs4 import BeautifulSoup
import pandas as pd

def buscar_pagina(url):
    """
    Faz requisição HTTP para a URL e retorna o conteúdo HTML da página.
    
    Parâmetros:
    - url (str): endereço da página web a ser acessada
    
    Retorna:
    - str: conteúdo HTML da página, ou None em caso de erro
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gera erro se status não for 200
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None

def extrair_noticias(html):
    """
    Recebe o HTML da página e extrai os títulos e links das notícias.
    
    Parâmetros:
    - html (str): conteúdo HTML da página
    
    Retorna:
    - list de dicts: cada dicionário tem 'titulo' e 'url' da notícia
    """
    soup = BeautifulSoup(html, 'html.parser')
    noticias = []

    # No site G1, notícias estão em links <a> com classe 'feed-post-link'
    links = soup.find_all('a', class_='feed-post-link')

    for link in links:
        titulo = link.get_text(strip=True)
        url = link['href']
        noticias.append({'titulo': titulo, 'url': url})

    return noticias

def salvar_csv(noticias, nome_arquivo='noticias.csv'):
    """
    Salva a lista de notícias em um arquivo CSV.
    
    Parâmetros:
    - noticias (list): lista de dicionários com título e URL
    - nome_arquivo (str): nome do arquivo CSV (padrão 'noticias.csv')
    """
    df = pd.DataFrame(noticias)
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    print(f"{len(noticias)} notícias salvas em {nome_arquivo}")

def main():
    url = 'https://g1.globo.com/'
    print(f"Buscando notícias em {url} ...")
    html = buscar_pagina(url)

    if html:
        noticias = extrair_noticias(html)
        if noticias:
            salvar_csv(noticias)
        else:
            print("Nenhuma notícia encontrada.")
    else:
        print("Falha ao baixar a página.")

if __name__ == '__main__':
    main()
