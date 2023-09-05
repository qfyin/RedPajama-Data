import re
import os
import sys
import json
import glob
# import fasttext
from bs4 import BeautifulSoup
#from multiprocessing import Pool

sys.path.append("./")

site_name = ""
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw_html):
    raw_html = raw_html.replace("<li>", "\n*")
    raw_html = raw_html.replace("</li>", "")
    raw_html = raw_html.replace("<ol>", "\n*")
    raw_html = raw_html.replace("</ol>", "")
    soup = BeautifulSoup(raw_html, "lxml")
    return soup.get_text()
    
# class LanguageIdentification:

#     def __init__(self):
#         pretrained_lang_model = "data/lid.176.bin"
#         self.model = fasttext.load_model(pretrained_lang_model)

#     def predict_lang(self, text):
#         text = text.replace("\n", " ")
#         predictions = self.model.predict(text, k=1) # returns top 2 matching languages
#         return predictions[0][0].replace("__label__", "")

# lang_id = LanguageIdentification()

LEMMA_DATA_DIR_SE = os.environ.get("LEMMA_DATA_DIR_SE", "./data/stack_exchange/")
os.makedirs(os.path.join(LEMMA_DATA_DIR_SE, "processed"), exist_ok=True)

def extract_labels(question):
    if "Tags" not in question:
        return []
    tags = question["Tags"].replace("><", "|").replace("<", "").replace(">", "")
    return tags.split("|")

def process_qa_pair(pair):
    # sort answers by score
    conversation = []
    conversation.append({
        "from": "human-q",
        "value": cleanhtml(pair["question"]["Title"]) + "\n" + cleanhtml(pair["question"]["Body"]),
        "score": pair["question"]["Score"],
        "parent_id": -1,
        "id": 0
        })
    total_score =  pair["question"]["Score"]
    id = 1
    for answer in pair["answers"]:
        conversation.append({
            "from": "human-a",
            "value": cleanhtml(answer["Body"]),
            "score": answer["Score"],
            "parent_id": 0,
            "id": id
            })
        total_score += answer["Score"]
        id += 1
    
    site_name = pair["question"]["Site"] if "Site" in pair["question"] else "stackexchange"
    return {
        "id": "c1d9f50f86825a1a2302ec2449c17196",
        "source": {
            "name": site_name,
            "location": f"https://{site_name}.com/questions/{pair['question']['Id']}",
        },
        "category_info": {
            "category": "LinuxCmd",
            "cmd_name": "",
            "cmd_manual": ""
        },
        "score": total_score,
        "labels": extract_labels(pair["question"]),
        "other_metadata": {
            "accepted_answer_id": pair["question"]["AcceptedAnswerId"],
            "view_count": pair["question"]["ViewCount"],
            "comment_count": pair["question"]["CommentCount"],
            "favorite_count": pair["question"]["FavoriteCount"],
            "answer_count": pair["question"]["AnswerCount"],
            "creation_date": pair["question"]["CreationDate"],
            "closed_date": pair["question"]["ClosedDate"],
            "last_edit_date": pair["question"]["LastEditDate"],
            "last_activity_date": pair["question"]["LastActivityDate"]
        },
        "conversation": conversation
    }

# load qa_pairs
for filename in glob.glob(os.path.join(LEMMA_DATA_DIR_SE, "qa_pairs", "*.jsonl")):
    if filename.endswith(".jsonl") and "top" not in filename:
        print(f"Processing {filename}")
        new_fullname = os.path.join(LEMMA_DATA_DIR_SE, "processed", os.path.basename(filename))
        # load qa_pairs
        with open(filename, "r", encoding="utf8") as fin, open(new_fullname, "w", encoding="utf8") as fout:
            for line in fin:
                pair = json.loads(line)
                result = process_qa_pair(pair)
                fout.write(json.dumps(result) + "\n")