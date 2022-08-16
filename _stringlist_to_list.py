from _clean_text import _clean_text


#from stringlist to proper list of keywords
def _stringlist_to_list(keywords):
    sep=", "
    
    keywords=keywords.split(sep)
    keywords=[_clean_text(x) for x in keywords]

    return keywords
