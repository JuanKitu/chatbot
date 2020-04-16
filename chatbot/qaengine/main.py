__author__ = 'roloprogramating'
from chatbot.qaengine.entities import Question
import chatbot.qaengine.distances as distances
from chatbot.qaengine.lemmatizers import SearchLemmatizer
import string

class Kernel:
    pre_defined_questions = []

    def __init__(self, language='spanish', ignore_diacritics=False):
        self.lemmatizer = SearchLemmatizer(ignore_diacritics)
        self.lemmatizer.load_from_preset(language)

    def load_questions(self, path):
        with open(path) as file:
            for line in file:
                self.pre_defined_questions.append(Question(line.rstrip().rsplit()[0], line.rstrip().rsplit()[1]))


    def match_question(self, query, distance=distances.bag_of_word_count_diff, remove_punctuation=True):
        query ="".join(c for c in query if c not in string.punctuation) if remove_punctuation else query
        matched = self.pre_defined_questions[0]
        query_matched_dist = distance(self.lemmatize_phrase(query), self.lemmatize_phrase(matched.text))
        for question in self.pre_defined_questions[1:]:
            query_question_dist = distance(self.lemmatize_phrase(query), self.lemmatize_phrase(question.text))
            if query_question_dist < query_matched_dist:
                matched = question
                query_matched_dist = query_question_dist
        return (query_matched_dist, matched)

    def lemmatize_phrase(self, phrase):
        return ' '.join([self.lemmatizer.lemmatize(word) for word in phrase.rsplit()])


k = Kernel()
k.pre_defined_questions = [Question(0, 'como ser alumno regular'), Question(1, 'como me inscribo a un final')]
s, q = k.match_question('cuales son los requisitos para alumno regular')
print(k.lemmatize_phrase('corriendo comia rapidez saludos nosotras normalice amistades valores manejaria'))
print(str(s) + ' ' + q.text)