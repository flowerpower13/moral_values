import time
import requests
import pandas as pd
from pathlib import Path


#functions
from _chromedriver import _chromedriver


#preliminary
encoding="utf-8"


#source
#https://wrds-www.wharton.upenn.edu/pages/get-data/wrds-sec-analytics-suite/wrds-sec-filings-index-data/sec-filings-index/



def _request(i, url):
    timeout=10
    HEADERS={
        "User-Agent": f"name{i} email{i}@outlook.com",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov"
        }

    r=requests.get(url, timeout=timeout, headers=HEADERS)
    text=r.text

    r.close()

    return text


def _dwn(i, url, file_path, tot):
    try:    
        #chromedriver
        #text=_chromedriver(url)

        #requests
        text=_request(i, url)

        with open(file_path, "w", encoding=encoding) as f:
            f.write(text)

        converted=True

        print(f"{i}/{tot} - {url} - done")

            
    except Exception as e:
        converted=False

        print(f"{i}/{tot} - {url} - error")
        print(e)
    
    return converted

    
#DOWNLOAD FILINGS
#https://www.sec.gov/developer
#https://www.sec.gov/edgar/sec-api-documentation
#https://www.sec.gov/os/accessing-edgar-data
#https://developer.edgar-online.com/docs
def _download(folders, items, filing):
    resources=folders[0]
    results=folders[1]

    resource=items[0]
    result=items[1]

    file_path=f"{resources}/{resource}.csv"
    df=pd.read_csv(
        file_path, 
        dtype="string", 
        #nrows=pow(10, 9)
        )

    #multiple types of same filing
    #df=df.loc[df["Form"].str.contains(filing)]

    #only 'pure' filings
    df=df.loc[df["Form"].isin([filing])]
    
    file_stems=df["FName"].tolist()
    #file_stems=file_stems[0:10]

    n_obs=len(file_stems)
    tot=n_obs-1

    converteds=[None]*n_obs

    base_url="https://www.sec.gov/Archives"
    time_sleep=1/10

    for i, file_stem in enumerate(file_stems):
        url=f"{base_url}/{file_stem}"
        file_name=file_stem.replace("edgar/data/","").replace("/","_")
        file_path=f"{results}/{file_name}" 
        path=Path(file_path)
        
        if not path.is_file():
            converted=_dwn(i, url, file_path, tot)
            
            time.sleep(time_sleep)

        elif path.is_file():
            size=path.stat().st_size

            if size==0:
                converted=_dwn(i, url, file_path, tot)

                time.sleep(time_sleep)

            elif size>0:
                converted=True

                print(f"{i}/{tot} - {url} - already done")

        converteds[i]=converted

    df=df.set_index("FName")
    df=df.reindex(file_stems)
    df["converted"]=converteds

    file_path=f"{results}/{result}.csv"
    df.to_csv(file_path, index=False)

