import os
import json
import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm
import glob

LEMMA_DATA_DIR_SE = os.environ.get("LEMMA_DATA_DIR_SE", "./data/stack_exchange/")

def extract_top_qas(filename: str, top_n: int):
    qa_pairs = []
    # open the jsonl file in LEMMA_DATA_DIR_SE with name filename, and read it line by line, parse each line as json, and append it to qa_pairs
    with open(filename, "r", encoding="utf8") as f:
        for i, line in enumerate(tqdm(f)):
            qa_pairs.append(json.loads(line))
    qa_pairs = sorted(qa_pairs, key=lambda x: int(x["question"]["Score"]), reverse=True)
    
    # write the top_n questions to a file
    #filename is a full path, so we need to extract the filename from it and add top_n to the name
    folder = os.path.dirname(filename)
    filename = os.path.basename(filename).split(".")[0]
    new_fullname = os.path.join(folder, f"{filename}.top{top_n}.jsonl")
    with open(new_fullname, "w", encoding="utf8") as f:
        for qa in qa_pairs[:top_n]:
            f.write(json.dumps(qa)+"\n")

if __name__ == "__main__":
    # read top_n from command line
    top_n = int(sys.argv[1])

    # enumerate LEMMA_DATA_DIR_SE and call extract_top_qas for each file
    for filename in glob.glob(os.path.join(LEMMA_DATA_DIR_SE, "qa_pairs", "*.jsonl")):
        if filename.endswith(".jsonl") and "top" not in filename:
            extract_top_qas(filename, top_n)

