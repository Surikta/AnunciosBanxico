# AnunciosBanxico
Nube de palabras para los anuncios de política monetaria


Utilizando las librerías PyPDF2 y wordcloud generamos una nube de palabras del anuncio de política monetaria de Banxico.
Una vista rápida puede dar a entender el sentido del comunicado y entender los puntos importantes para pre-analizar y enfocar la información sobre algunos temas.

# Modo de uso

Hay dos funciones, una para el tratatmiento de texto y otra para generar la nube de palabras.

# text_extract(pdf_path)

El objetivo es extraer el texto del documento que emite Banxico, como utiliza un español estándar no es necesario crear un diccionario con palabras/emojis como se tendría que hacer con analisis de texto en redes sociales.

La puntuación que se utiliza no es muy extensa ya que es un comunicado y signos como "¡!¿?", entre otros, no son utilizados pero puede agregarse.

```python
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
```

Para el caso del 24 de marzo del 2022 el texto resultante es el siguiente.

```python
anuncio = text_extract('Anuncios_Banxico\\20220324.pdf')
print(anuncio)
 1 anuncio de política monetaria comunicado de prensa 24 de marzo de 2022 la junta de gobierno del banco de méxico decidió incrementar en 50 puntos base el objetivo para la tasa de interés interbancaria a un día a un nivel de 65% con efectos a partir del 25 de marzo de 2022 los indicadores dispon...
```

Los documentos son heterogéneos, en algunos casos puede contener gráfica o tablas mientras que en otros únicamente es texto. La extención del archivo tampoco es homogénea.


# def word_cloud(string, image_name)

Generar la nube de palabras es muy directo utilizando la librería wordcloud en python.

Lo más importante, una vez que se tiene el texto, es remover las "stop words", palabras que no proveen de información relevante (artículos, conjunciones, adverbios, etc.). La librería cuenta con un conjunto de estas stop words, pero en inglés, por lo que habrá que introducir manualmente las palabras que se quieran remover.

Utilizamos el archivo stopwords_es.txt donde podemos agregar nuevas stop words en forma de lista. Hay muchas fuentes de archivos de stop words en diferentes idiomas y en el caso de que un nombre personal (ejemplo: Banxico, Gobierno) tenga muchas repeticiones se puede agregar para generar una imágen más limpia con información relevante.

La función necesita el texto y el nombre de la imágen para guardarla.

```python
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
```

El color y la forma de la imágen se pueden modificar con un 'mask', una de las variable de WordCloud.

```python
    wc = WordCloud(
        stopwords=stopwords,
        max_words=2000,
        background_color="white",
        width=640,
        height=480,
        contour_color="black",
        colormap="twilight",
    ).generate(string)
```

Para el texto que tenemos generamos la siguiente imágen.

```python
word_cloud(anuncio, '20220324')
```
![alt text](https://github.com/Surikta/AnunciosBanxico/blob/main/WordCloud/20220324.png)

