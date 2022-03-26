import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader
from wordcloud import WordCloud, STOPWORDS


# Extrae el texto del comunicado de política monetaria (o cualquier otro documento pdf)
def text_extract(pdf_path):

    # Texto
    anuncio = ""
    with open(pdf_path, mode="rb") as f:
        reader = PdfFileReader(f)
        for page in range(len(reader.pages)):
            text = reader.getPage(page)
            anuncio = anuncio + " " + text.extractText()

    # Quitamos puntuación
    ptt = [".", ",", ";", ":", "\n", "(", ")"]
    for t in ptt:
        anuncio = anuncio.replace(t, "")

    # Dejamos máximo 1 espacio
    # Para garantizar lo anterior podemos incrementar el número de ciclos
    for i in range(5):
        anuncio = anuncio.replace("  ", " ")

    # Dejamos en minúsculas el texto
    anuncio = anuncio.lower()

    return anuncio


# Crea la nube de palabras del texto y la guarda
def word_cloud(string, image_name):

    # Usemos las stopwords en inglés en caso de usar un texto en inglés.
    stopwords = set(STOPWORDS)

    # Agregamos stopwords en español del documento adjunto.
    file = open("stopwords_es.txt", "r", encoding="utf-8")
    other_stop = file.readlines()
    for stops in range(len(other_stop)):
        other_stop[stops] = other_stop[stops].replace("\n", "")

    for i in other_stop:
        stopwords.add(i)

    # Generamos la imágen y guardamos
    wc = WordCloud(
        stopwords=stopwords,
        max_words=2000,
        background_color="white",
        width=640,
        height=480,
        contour_color="black",
        colormap="twilight",
    ).generate(string)

    plt.figure(figsize=(8, 6))
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig("WordCloud\\" + image_name + ".png")

    return None


if __name__ == "__main__":
    anuncio = text_extract('Anuncios_Banxico\\' + input('Nombre del PDF (PATH):') + '.pdf')
    word_cloud(anuncio, input('Nombre de la imágen:'))
    
