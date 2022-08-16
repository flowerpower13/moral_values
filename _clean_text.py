import re


#preliminaries
error="???"
marker="###"


#clean text
def _clean_text(text):
    #lowercase
    text=text.lower()

    #remove parentheses
    text=text.replace("(", " ").replace(")", " ")

    #remove text btw markers
    text=re.sub(f'{marker}.*?{marker}', '', text)

    #remove punctuation
    #text=re.sub(r'[^\w\s]', '', text)

    #remove newline
    text=text.replace("\n", " ")

    #remove whitespaces
    text=text.strip()
    text=re.sub(r"\s+", ' ', text)

    return text