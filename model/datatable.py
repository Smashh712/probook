import pandas as pd

f = open('../data/booklist.txt','r', encoding='UTF-8')
while True:
    line = f.readline()
    if not line : break
    print(line)
f.close()

user_id, book_id, score = input("사용자 id, 책 id, 평점을 입력해주세요.\n").split(',')

print(user_id)
print(book_id)
print(score)

print(line)