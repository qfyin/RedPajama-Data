import os
import pandas as pd
from tqdm import tqdm
import glob

BASE_URL="https://archive.org/download/stackexchange/"

def download_source_table():
    table = pd.read_html(BASE_URL)[0]
    sources = [x.replace(" (View Contents)", "") for x in table['Name'].tolist()]
    sources = [x for x in sources if x.endswith(".7z")]
    return sources

def save_sources(sources):
    # save the list of sources to file
    with open("sources.txt", "w") as f:
        f.write("\n".join(sources))

def load_sources():
    with open("sources.txt", "r") as f:
        sources = f.read().split("\n")
    return sources

def download_source(source):
    print(f"source: {source}")
    os.system(f"aria2c -d data -o {source} {BASE_URL + source}")
    #os.system("7z x ./data/"+source+" -o./data/"+source[:-3])
    #os.system(f"mv ./data/{source[:-3]}/Posts.xml ./data/{source[:-3]}.xml")
    #os.system(f"rm -rf ./data/{source[:-3]}")
    #os.system(f"rm ./data/{source}")

def extract_posts():
    #use glob to enumerate all *.7z files in current folder and print the name
    for file in glob.glob("data/*.7z"):
        print(file)
        os.system(f"7z e {file} Posts.xml -y")
        os.system(f"move Posts.xml {file[:-3]}.posts.xml")



#for source in tqdm(sources):
    # if ".meta." not in source:
#    print(f"source: {source}")
    #os.system("wget "+BASE_URL+source+" -O "+"./data/"+source)
    #os.system("7z x ./data/"+source+" -o./data/"+source[:-3])
    #os.system(f"mv ./data/{source[:-3]}/Posts.xml ./data/{source[:-3]}.xml")
    #os.system(f"rm -rf ./data/{source[:-3]}")
    #os.system(f"rm ./data/{source}")

if __name__ == "__main__":
    extract_posts()