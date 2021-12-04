import pandas as pd

f = open('../data/booklist.txt','r')
while True:
    line = f.readline()
    if not line : break
f.close()