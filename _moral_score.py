import pandas as pd
from pathlib import Path


#moral foundations dictionary
from _classes import care, fairness, ingroup, authority


#functions
from _simple_count import _simple_count
from _nonstop_words import _nonstop_words


#source
#https://doi.org/10.1086/708857 - Section III C - "Supply-Side Text Analyses: Methodology and Data"


def _foundation_freq(text, foundation):

    bad_keywords="no_bad_keywords"

    keywords_count_vice, n_vice=_simple_count(text, foundation.vice, bad_keywords)
    keywords_count_virtue, n_virtue=_simple_count(text, foundation.virtue, bad_keywords)

    f=((keywords_count_vice)/n_vice + (keywords_count_virtue)/n_virtue)/2
    print(f)

    return f


def _rel_freq(text, foundations_pos, foundations_neg):

    foundation_freqs_pos=[_foundation_freq(text, foundation) for foundation in foundations_pos]
    foundation_freqs_neg=[_foundation_freq(text, foundation) for foundation in foundations_neg]

    nonstop_words=_nonstop_words(text)

    rel_freq=(sum(foundation_freqs_pos) - sum(foundation_freqs_neg))/nonstop_words

    return rel_freq


#COMPUTE MORAL FOUNDATIONS FREQUENCY
def _moral_score(folders, items):
    resources=folders[0]
    results=folders[1]

    result=items[0]

    p=Path(resources).glob('**/*')
    files=[x for x in p if x.is_file()]
    files=[x for x in files if not x.suffix==".csv"]

    n_obs=len(files)
    tot=n_obs-1

    file_stems=[None]*n_obs
    rel_freqs=[None]*n_obs

    for i, file in enumerate(files):
        file_stem=file.stem

        with open(file, "r") as f:
            text=f.read()

            foundations_pos=[care, fairness] 
            foundations_neg=[ingroup, authority]

            rel_freq=_rel_freq(text, foundations_pos, foundations_neg)
    
        file_stems[i]=file_stem
        rel_freqs[i]=rel_freq

        print(f"{i}/{tot} - {file_stem} - done")

    d={
        "file_stem": file_stems,
        "rel_freq": rel_freqs,
        }
    df=pd.DataFrame(data=d)  

    file_path=f"{results}/{result}.csv"
    df.to_csv(file_path, index=False)
