
#functions
from _download import _download
from _html_to_txt import _html_to_txt
from _moral_score import _moral_score



'''
pip install -r requirements.txt
'''


#DOWNLOAD FILINGS
folders=["_download0", "_download1"]
items=["sec_idx", "_download"]
filing="10-K"
#_download(folders, items, filing)


#CONVERT HTML TO TXT
folders=["_download1", "_html_to_txt"]
items=["_html_to_txt"]
#_html_to_txt(folders, items)


#COMPUTE MORAL FOUNDATIONS FREQUENCY
folders=["_html_to_txt", "_moral_score"]
items=["_moral_score"]
_moral_score(folders, items)


print("done")