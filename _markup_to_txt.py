import re
import html
from bs4 import BeautifulSoup


def _getDistinctDocumentsIndexes(textLines):
    documentsIndexes = [] 
    for lineIndex, line in enumerate(textLines):
        if line.startswith("<DOCUMENT>"):
            startLine = lineIndex
        elif line.startswith("</DOCUMENT>"):
            documentsIndexes.append((startLine,lineIndex))
    return documentsIndexes

def _isAnHtmlDocument(text):
    return "<html>" in text or '<?xml version="1.0" encoding="utf-8"?><html' in text


def _removeHeadingTags(text):
    headingEnd = text.find("</head><body")
    if headingEnd >= 0:
        text = text[headingEnd:]
    xmlHeading = text.find("</ix:header>")
    if xmlHeading >= 0:
        text = text[xmlHeading:]
    return text


def markupToText(rawText):
    textLines = rawText.splitlines()
    documentsIndexes = _getDistinctDocumentsIndexes(textLines)

    documentsIndexes = [doc for doc in documentsIndexes if _isAnHtmlDocument("".join(textLines[doc[0]:doc[1]]))]
    
    cleanedText = ""
    for doc in documentsIndexes:
        documentText = "\n".join(textLines[doc[0]:doc[1]])
        documentText = html.unescape(documentText)
        documentText = _removeHeadingTags(documentText)
        
        soup = BeautifulSoup(documentText, 'html.parser')
        cleanedText += soup.text
     
    text=re.sub(r'\n+', '\n', cleanedText)

    pattern=r"[^ ^\n]+:[^ ^\n]+"
    text=re.sub(pattern, text)

    return text



def _markup_to_txt(text):
    #take only text
    text=markupToText(text)

    #lowercase
    text=text.lower()
    
    '''
    #remove non-english words
    words=set(corpus.words.words())
    word_tokens=tokenize.word_tokenize(text)
    filtered_sentence=[w for w in word_tokens if w in words]
    text=" ".join(filtered_sentence)

    #remove singleton letters
    word_tokens=tokenize.word_tokenize(text)
    filtered_sentence=[w for w in word_tokens if len(w)>1] 
    #text=" ".join(filtered_sentence)

    #remove punctuation
    #text=re.sub(r"[^\w\s]", "", text)

    #remove whitespaces
    #text=text.strip()
    #text=re.sub(r"\s+", " ", text)
    #'''

    return text