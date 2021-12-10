import requests
import xmltodict
import json
import pandas as pd
import numpy as np
import csv

booklist_id = []
booklist_name = []

search_list = ['파이썬', '리엑트', '웹', '프론트엔드', '백엔드', '자바', '자바스크립트',
'C언어', 'C++', 'node.js', '앱 프로그래밍', '자료 구조', '컴퓨터 구조', '알고리즘',
'HTML', 'CSS', '안드로이드 프로그래밍', 'TCP/IP', 'R 프로그래밍', 'PHP', '코틀린', '프로그래밍',
'c#', 'GO 언어']

for a in search_list:
    for i in range(1,6):
        r = requests.get(f"https://aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={a}&QueryType=Keyword&MaxResults=10&start={i}&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy")

        cc = xmltodict.parse(r.text) # return collections.OrderedDict
        dd = json.loads(json.dumps(cc)) # return dict
        if "item" in dd["object"]:
            for i in range(len(dd["object"]["item"])):
                booklist_id.append(dd["object"]["item"][i]["@itemId"])
                booklist_name.append(dd["object"]["item"][i]["title"])

save_dict = dict(zip(booklist_id, booklist_name))

seen = []
booklist_dict = dict()
for key, val in save_dict.items():
    if key not in seen:
        seen.append(key)
        booklist_dict[key] = val


booklist_id = list(booklist_dict)
booklist_name = list(booklist_dict.values())

with open("../data/booklist.txt",'w',encoding='UTF-8') as f:
    for id, name in booklist_dict.items():
        f.write(f'{id} : {name}\n')

with open("../data/bookli.txt",'w',encoding='UTF-8') as f:
    for id, name in booklist_dict.items():
        f.write(f'{id}&*&{name}\n')

with open("../data/booklist_id.csv", 'w') as file:
    writer = csv.writer(file)
    writer.writerow(booklist_id)

##
# book_df = pd.DataFrame(index=booklist_id)
# book_df.index.name = 'book_id'
# book_df.columns.name = 'user_id'

# user_id, book_id, score = input("사용자 id, 책 id, 평점을 입력해주세요.\n").split(',')

# book_df.insert(0,user_id,0)

# for j in range(len(book_df)):
#     if book_id == book_df.index[j]:
#         book_df.iloc[j,0] = score

# print(book_df)