__author__ = 'roloprogramating'
import chatbot.qaengine.datasets.available as av
import os


class SearchLemmatizer:
    word_lemma_dic = {}

    def __init__(self, ignore_diacritics=True):
        self.ignore_diacritics = ignore_diacritics

    def __read_file(self, path, from_base=True):
        if from_base:
            script_dir = os.path.dirname(__file__)
            abs_file_path = os.path.join(script_dir, path)
        else:
            abs_file_path = path
        lemmas = {}
        with open(abs_file_path) as file:
            for line in file:
                key = remove_diacritics(line.rstrip().rsplit()[1]) if self.ignore_diacritics else \
                    line.rstrip().rsplit()[1]
                word = remove_diacritics(line.rstrip().rsplit()[0]) if self.ignore_diacritics else \
                    line.rstrip().rsplit()[0]
                lemmas[key] = word
        return lemmas

    def load_lemmas_from_file(self, path):
        self.word_lemma_dic.update(self.__read_file(path))

    def load_from_preset(self, language):
        self.load_lemmas_from_file(av.languages[language])

    def lemmatize(self, word):
        word = remove_diacritics(word) if self.ignore_diacritics else word
        return self.word_lemma_dic.get(word, word)


def remove_diacritics(word):
    return (word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('u', 'u'))


s = SearchLemmatizer()
s.load_from_preset("spanish")
print(s.lemmatize('eres'))