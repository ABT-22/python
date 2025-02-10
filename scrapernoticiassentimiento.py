import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import csv

def obtener_noticias():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    noticias = []
    for item in soup.find_all("h3"):  # Extraer titulares
        titulo = item.get_text().strip()
        if titulo:
            noticias.append(titulo)
    return noticias

def analizar_sentimiento(texto):
    analisis = TextBlob(texto)
    polaridad = analisis.sentiment.polarity
    if polaridad > 0:
        return "Positivo"
    elif polaridad < 0:
        return "Negativo"
    else:
        return "Neutral"

def guardar_resultados(noticias):
    with open("noticias_sentimiento.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Titular", "Sentimiento"])
        for noticia in noticias:
            escritor.writerow([noticia, analizar_sentimiento(noticia)])

def main():
    print("Obteniendo noticias...")
    noticias = obtener_noticias()
    guardar_resultados(noticias)
    print("Análisis de sentimiento completado. Resultados guardados en 'noticias_sentimiento.csv'")

if __name__ == "__main__":
    main()