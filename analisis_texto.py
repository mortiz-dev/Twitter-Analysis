import nltk
from nltk import tokenize
from nltk.corpus import stopwords
import re
import string

text = 'Adrián Cosentino, presidente de la CNV, junto al titular del Banco Nación, Eduardo Hecker, lanzaron el primer FCI Cerrado inmobiliario Pellegrini I, de impacto social, destinado a financiar construcción de viviendas para sectores de ingresos bajos y medios'

def limpieza_texto(text):
    text = text.lower()
    text = re.sub('\[.*¿?\}\%', ' ', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('\w*\d\w*', ' ', text)
    return text

def limpieza_texto2(text):
    listalimpia = []
    stop_words = stopwords.words('spanish')
    for r in text:
        if r not in stop_words:
            listalimpia.append(r)
    return listalimpia

text = limpieza_texto(text)
tokens = [t for t in text.split()]
text = limpieza_texto2(tokens)

freq = nltk.FreqDist(text)

#for key,val in freq.items():
#    print (str(key) + ':' + str(val))
freq.plot(20,cumulative=False)