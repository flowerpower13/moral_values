import re


#functions
from _stringlist_to_list import _stringlist_to_list


#simply count n of words
#text="string"
#keywords="""
# key, words
# """
def _simple_count(text, keywords, bad_keywords):

    keywords=_stringlist_to_list(keywords)
    bad_keywords=_stringlist_to_list(bad_keywords)

    keywords=[x for x in keywords if x not in bad_keywords]

    marker="*"

    x=0
    for i, keyword in enumerate(keywords):

        if marker in keyword:
            pattern=keyword.replace(marker, "")
            matches=re.findall(pattern, text)

        elif not marker in keyword:
            pattern=rf"\b{keyword}\b"
            matches=re.findall(pattern, text)

        if matches:
            y=len(matches)

        else:   
            y=0
        
        x=x+y

    n_keywords=len(keywords)

    return x, n_keywords
    