import requests
import xmltodict
import json

r = requests.get(f"https://aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query=python&QueryType=Keyword&MaxResults=10&start=1&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy")
        
print(r)