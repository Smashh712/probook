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

book_df = pd.DataFrame(index=booklist_id)
book_df.index.name = 'book_id'
book_df.columns.name = 'user_id'

usboscore_df = book_df.join(score_table)
usboscore_df=usboscore_df.fillna(0)

score_table_T = score_table.transpose()

user_sim = cosine_similarity(score_table_T, score_table_T)

# cosine_similarity()로 반환된 Numpy 행렬을 도서명으로 매핑해 DataFrame으로 변환
user_sim_df = pd.DataFrame(data=user_sim, index=score_table.columns,
                           columns=score_table.columns)

know_user = 2021002 # 추천 받고자 하는 user의 id

rec_list = pd.DataFrame(index=score_table.index)

for j in score_table.index:
    sum = 0.0
    count = 0
    for i in user_sim_df.index:
        u = user_sim_df.loc[i, know_user]
        b = score_table.loc[j, i]
        if b != 0:
            result = u * b
            sum+=result
            count+=1
    rec_list.loc[j,know_user] = sum / count

unread_filter = score_table[know_user] == 0