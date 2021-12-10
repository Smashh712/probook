import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

score_df = pd.read_csv("../data/user-bookscore.csv", sep=',') #평점 데이터 파일

score_tb = pd.pivot_table(score_df, values='score', index=['book_id'], columns=['user_id'], aggfunc=np.sum)
score_tb = score_tb.fillna(0)

with open('../data/booklist_id.csv','r', encoding='UTF-8') as f:
    line = f.read()
booklist_id = line.split(',')

book_df = pd.DataFrame(index=booklist_id)
book_df.index.name = 'book_id'
book_df.columns.name = 'user_id'

ub_score_df = book_df.join(score_tb) # 모든 도서 데이터와 합치는 것
ub_score_df = ub_score_df.fillna(0)

score_tb_T = score_tb.transpose()

user_sim = cosine_similarity(score_tb_T, score_tb_T)

# cosine_similarity()로 반환된 Numpy 행렬을 도서명으로 매핑해 DataFrame으로 변환
user_sim_df = pd.DataFrame(data=user_sim, index=score_tb.columns,
                           columns=score_tb.columns)

rec_user = 2021002 # 추천 받고자 하는 user의 id

rec_list = pd.DataFrame(index=score_tb.index)

for j in score_tb.index:
    sum = 0.0
    count = 0
    for i in user_sim_df.index:
        u = user_sim_df.loc[i, rec_user]
        b = score_tb.loc[j, i]
        if b != 0:
            result = u * b
            sum+=result
            count+=1
    rec_list.loc[j,rec_user] = sum / count

unread_filter = score_tb[rec_user] == 0
rec_list = rec_list.loc[unread_filter]

print(rec_list[rec_user].sort_values(ascending=False)) # 최종 결과(추천 리스트)