import langdetect
import nltk
import pymorphy2

class Analysis(object):
    def __init__(self):
        self.language = None
        self.article_text = None

    def determineLanguage(self):
        # We need to do something special for Russian language
        if self.article_text == None:
            return
        self.language = langdetect.detect(self.article_text)

    def processText(self):
        if self.article_text == None or self.language == None:
            return []

        cities = []

        tokens = nltk.word_tokenize(self.article_text)
        print("Tokens = ", tokens)
        # Special case of Russian
        if self.language == "ru":
            morph = pymorphy2.MorphAnalyzer()

            for token in tokens:
                item = morph.parse(token)[0]
                if "Geox" in item.tag:
                    cities.append(item.normal_form)
        else:
            chunks = nltk.ne_chunk(nltk.pos_tag(tokens))
            print("Chunks=", chunks)
            for chunk in chunks:
                print()
                if len(chunk) == 1:
                    if (chunk.label() == "GPE" or chunk.label() == "GEO") and (chunk[0][1] == "NNP"):
                        cities.append(chunk[0][0])
        
        self.cities = cities

    def findCities(self, article_text):
        self.article_text = article_text
        self.determineLanguage()
        self.processText()
        print("Cities from Analysis = ", self.cities)
        return self.cities
