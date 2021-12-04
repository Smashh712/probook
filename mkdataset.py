import requests
import xmltodict
import json

booklist_id = []
booklist_name = []

search_list = ['파이썬', '리엑트', '웹', '프론트엔드', '백엔드', '자바', '자바스크립트',
'C언어', 'C++', 'node.js', '앱 프로그래밍', '자료 구조', '컴퓨터 구조', '알고리즘',
'HTML', 'CSS', '안드로이드 프로그래밍', 'TCP/IP', 'R 프로그래밍', 'PHP', '코틀린', '프로그래밍',
'c#', 'GO 언어']

for a in search_list:
    for i in range(1,6):
        r = requests.get(f"https://aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={a}&QueryType=Keyword&MaxResults=10&start={i}&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy")
        
        print(a)

        cc = xmltodict.parse(r.text) # return collections.OrderedDict
        dd = json.loads(json.dumps(cc)) # return dict
        if "item" in dd["object"]:
            for i in range(len(dd["object"]["item"])):
                booklist_id.append(dd["object"]["item"][i]["@itemId"])
                booklist_name.append(dd["object"]["item"][i]["title"])

booklist_id = list(dict.fromkeys(booklist_id))
booklist_name = list(dict.fromkeys(booklist_name))
booklist_dict = dict(zip(booklist_id, booklist_name))
print(booklist_id)
print(booklist_name)
print(booklist_dict)