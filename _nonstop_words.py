#preliminary
#import nltk
#nltk.download()
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('words')


from nltk import tokenize
from nltk import corpus


def _nonstop_words(text):
    words=set(corpus.stopwords.words('english'))
    word_tokens=tokenize.word_tokenize(text)
    filtered_sentence=[w for w in word_tokens if not w in words]

    total=len(filtered_sentence)

    return total
