import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords

class Bigram:
    def __init__(self, language='spanish'):
        """
        Inicializa la clase Bigram.
        :param language: Idioma para los stopwords (por defecto 'spanish').
        """
        self.language = language
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.stopset = set(stopwords.words(self.language))

    def scape_stopwords(self, bcf):
        """
        Elimina las stopwords y palabras con menos de 3 caracteres del BigramCollocationFinder.
        :param bcf: BigramCollocationFinder que será filtrado.
        :return: BigramCollocationFinder filtrado.
        """
        filter_stops = lambda w: len(w) < 3 or w in self.stopset
        bcf.apply_word_filter(filter_stops)
        return bcf

    def tokenize_text(self, texto):
        """
        Tokeniza el texto y lo convierte a minúsculas.
        :param texto: Texto de entrada.
        :return: Lista de palabras tokenizadas.
        """
        tokens = nltk.word_tokenize(texto, self.language)
        return [w.lower() for w in tokens]

    def create_bigram_finder(self, texto):
        """
        Crea un objeto BigramCollocationFinder a partir de un texto.
        :param texto: Texto de entrada.
        :return: BigramCollocationFinder filtrado.
        """
        words = self.tokenize_text(texto)
        bcf = BigramCollocationFinder.from_words(words)
        return self.scape_stopwords(bcf)

    def get_bigrams_by_raw_freq(self, texto, top_n=10):
        """
        Obtiene los bigramas ordenados por frecuencia bruta.
        :param texto: Texto de entrada.
        :param top_n: Número de bigramas a devolver.
        :return: Lista de bigramas ordenados por frecuencia bruta.
        """
        bcf = self.create_bigram_finder(texto)
        scored = bcf.score_ngrams(BigramAssocMeasures.raw_freq)
        return scored[:top_n]

    def get_bigrams_by_likelihood_ratio(self, texto, top_n=10):
        """
        Obtiene los bigramas ordenados por likelihood ratio.
        :param texto: Texto de entrada.
        :param top_n: Número de bigramas a devolver.
        :return: Lista de bigramas ordenados por likelihood ratio.
        """
        bcf = self.create_bigram_finder(texto)
        return bcf.nbest(BigramAssocMeasures.likelihood_ratio, top_n)

    def get_bigrams_by_chi_squared(self, texto, top_n=10):
        """
        Obtiene los bigramas ordenados por chi-squared.
        :param texto: Texto de entrada.
        :param top_n: Número de bigramas a devolver.
        :return: Lista de bigramas ordenados por chi-squared.
        """
        bcf = self.create_bigram_finder(texto)
        return bcf.nbest(BigramAssocMeasures.chi_sq, top_n)

    def get_bigrams_by_pmi(self, texto, top_n=10):
        """
        Obtiene los bigramas ordenados por Point-wise Mutual Information (PMI).
        :param texto: Texto de entrada.
        :param top_n: Número de bigramas a devolver.
        :return: Lista de bigramas ordenados por PMI.
        """
        bcf = self.create_bigram_finder(texto)
        return bcf.nbest(BigramAssocMeasures.pmi, top_n)
