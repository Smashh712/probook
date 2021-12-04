import requests
import xmltodict
import json

r = requests.get(f"https://aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query=python&QueryType=Keyword&MaxResults=10&start=1&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy")

cc = xmltodict.parse(r.text) # return collections.OrderedDict
dd = json.loads(json.dumps(cc)) # return dict

print(r)
print(cc)
print(dd)

print(dd["object"]["item"])
print(dd["object"]["item"][0]["@itemId"])
print(dd["object"]["item"][0]["title"])