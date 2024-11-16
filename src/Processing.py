import re
import nltk
from nltk.stem import SnowballStemmer

class Processing:
    def __init__(self, language="spanish"):
        self.language = language

    def tokenizacion(self, text):
        """Divide un texto en tokens"""
        tokens = nltk.word_tokenize(text, self.language)
        return tokens

    def stemming(self, tokens):
        """Obtiene las palabras raíz en una sentencia"""
        stemmer = SnowballStemmer(self.language)
        singles = [stemmer.stem(word) for word in tokens]
        return singles

    def remove_stopwords(self, text):
        if self.language == "spanish":
            stopwordsList = ["i"]
        elif self.language == "english":
            stopwordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
        else:
            print("No se ha programado la funcionalidad para el idioma elegido.")
            return text
        
        regexSeq = " |\\b".join(stopwordsList)
        regexSeq = "\\b"+regexSeq
        text = re.sub(regexSeq,"", text)
        return text

    def segmentacion_sentencias(self, texto):
        """Divide un texto en sentencias"""
        sentences = nltk.sent_tokenize(texto, self.language)
        return sentences

    def pos_tagging(self, texto):
        """Etiqueta gramaticalmente el texto"""
        tokens = nltk.word_tokenize(texto, self.language)
        tags = nltk.pos_tag(tokens, lang=self.language)
        return tags

    def ner(self, texto):
        """Reconocimiento de entidades nombradas"""
        sentences = nltk.sent_tokenize(texto, self.language)
        tokenized_sentences = [nltk.word_tokenize(sentence, self.language) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence, lang=self.language) for sentence in tokenized_sentences]
        
        for sent in tagged_sentences:
            print(nltk.ne_chunk(sent, "spanish"))

    def parser(self):
        """Realiza el análisis sintáctico (para inglés)"""
        from nltk.corpus import treebank
        from nltk import PCFG, ViterbiParser

        productions = []
        S = nltk.Nonterminal('S')
        for f in treebank.fileids():
            for tree in treebank.parsed_sents(f):
                productions += tree.productions()
        
        grammar = nltk.induce_pcfg(S, productions)
        for p in grammar.productions()[1:15]:
            print(p)
        
        parser = ViterbiParser(grammar)
        parse, = parser.parse(['it', 'is', 'a', 'small', 'group', 'of', 'workers', 'and', 'researchers'])
        print(parse, "\n")
        