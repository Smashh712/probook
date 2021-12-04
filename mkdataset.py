import requests
import xmltodict
import json

from scipy import spatial

dataSet1 = [5, 5, -4, 0, 0]
dataSet2 = [5, 5, 5, 5, 0]
dataSet3 = [5, 5, 0, 0, 0]
result = 1 - spatial.distance.cosine(dataSet1, dataSet2)
result2 = 1 - spatial.distance.cosine(dataSet3, dataSet2)

print(result, result2)