import tweepy as tw
from SQL import BaseSQL
from datetime import date
from dotenv import load_dotenv

load_dotenv()

#Claves de acceso
consumer_key= '4IojSO54b9OUtKOURMcH3qQj4'
consumer_secret = 'OUI9SHCnVC1nQqEFravqLHPgK92NOb4UghWUOaGzgcw9cym9Rh'
access_token = '268502516-1FDzuYYsuOgGAOKSwqY0UHRfSZVz3dpEJOUTMsx3'
access_secret_token = 'e4z4tUPjOPFEcevQdPxn7zSWFra2ySTSnkC9WWaqWSUAR'

class registro():
    def __init__(self):
        self.db = BaseSQL()
        self.fecha = ''
        self.usuario = ''
        self.ubicacion = ''
        self.tweet = ''
    
    def bajadaInicial(self):
        users_locs = []
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret_token)
        api = tw.API(auth, wait_on_rate_limit=True)

        search_words = ['banco nacion']
        date_since = date.today()

        tweets = tw.Cursor(api.search,
                    q=search_words,
                    lang="es",
                    since=date_since,
                    tweet_mode='extended').items(100)

        for tweet in tweets:
            if (not tweet.retweeted) and ('RT' not in tweet.full_text):
                dato = (tweet.created_at, tweet.user.screen_name, tweet.user.location, tweet.full_text)
                users_locs.append(dato)

        return users_locs
    
    def comparacionBD(self, tweets):
        listaFiltrada = []
        query = 'SELECT MAX(fechaRegistro) FROM twitter_analysis AS t'
        maximoRegistro = self.db.SeleccionarInfo(query)
        for r in tweets:
            if r[0] > maximoRegistro:
                listaFiltrada.append(r)
            else:
                pass
        return listaFiltrada

    def cargaBD(self, listado):
        query = 'INSERT INTO twitter_analysis(fechaRegistro, usuario, ubicacion, tweet) VALUES(?, ?, ?, ?)'
        self.db.InsertarRegistros(query, listado)

if __name__ == '__main__':
    twitter = registro()
    listado = twitter.bajadaInicial()
    listadoFiltrado = twitter.comparacionBD(listado)
    if len(listadoFiltrado) != 0:
        twitter.cargaBD(listadoFiltrado)