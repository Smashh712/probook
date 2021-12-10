import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

score_df = pd.read_csv("../data/user-bookscore.csv", sep=',') #평점 데이터 파일

score_table = pd.pivot_table(score_df, values='score', index=['book_id'], columns=['user_id'], aggfunc=np.sum)
score_table = score_table.fillna(0)

with open('../data/booklist_id.csv','r', encoding='UTF-8') as f:
    line = f.read()
booklist_id = line.split(',')