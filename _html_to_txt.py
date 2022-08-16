import pandas as pd
from pathlib import Path


#preliminaries
encoding="utf-8"


#functions
from _markup_to_txt import _markup_to_txt


#CONVERT HTML TO TXT
def _html_to_txt(folders, items):
    resources=folders[0]
    results=folders[1]

    result=items[0]

    p=Path(resources).glob('**/*')
    files=[x for x in p if x.is_file()]
    files=[x for x in files if not x.suffix==".csv"]

    n_obs=len(files)
    tot=n_obs-1

    file_stems=[None]*n_obs
    converteds=[None]*n_obs

    for i, file in enumerate(files):
        file_stem=file.stem

        try:
            file_path=f"{resources}/{file_stem}.txt"
            with open(
                file_path, 
                "r",
                ) as f:
                text=f.read()

            text=_markup_to_txt(text)

            file_path=f"{results}/{file_stem}.txt"
            with open(
                file_path, 
                "w", 
                encoding=encoding,
                ) as f:
                f.write(text)

            converted=True

            print(f"{i}/{tot} - {file_stem} - done")

        except Exception as e:
            converted=False

            print(f"{i}/{tot} - {file_stem} - error")
            print(e)
    
        file_stems[i]=file_stem
        converteds[i]=converted

    d={
        "file_stem": file_stems,
        "converted": converteds,
        }
    df=pd.DataFrame(data=d)  

    file_path=f"{results}/{result}.csv"
    df.to_csv(file_path, index=False)

