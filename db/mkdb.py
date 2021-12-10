import sqlite3
 
def viewDBdata(db, table) :
    #SQLite DB 연결
    conn = sqlite3.connect(db)
 
    # Connection 으로부터 Cursor 생성
    cur = conn.cursor()
 
    # SQL 쿼리 실행
    query = "select * from {0}".format(table)
    cur.execute(query)
 
    # 데이타 Fetch
    rows = cur.fetchall() # 모든 데이터를 한번에 클라이언트로 가져옴
    for row in rows :
        print(row)
 
    # Connection 닫기
    cur.close()
 
def saveDBtable(db, data) :
    conn = sqlite3.connect(db)
    cur = conn.cursor()
 
    sql = "insert into bookdb(book_id, book_name, book_img, book_pubD, book_auth, book_publi) values (?,?,?,?,?,?)"
    cur.executemany(sql, data)
 
    conn.commit() # 트랜젝션의 내용을 DB에 반영함
    conn.close()
 
if __name__ == '__main__':
    f = open('../data/bookli.txt', 'r', encoding='UTF-8')
 
    #matrix = [[0 for col in range(10)] for row in range(10)]
    matrix =[[0]*6 for row in range(891)]

    tempFile = f.read().splitlines()

    for i, tf in enumerate(tempFile):
        for j, saveFile in enumerate(tf.split('&*&')):
            matrix[i][j] = saveFile
 
    f.close()
 
    # DB에 테이블 입력
    saveDBtable('bookDB_.db', matrix)
 
    # DB에 저장되어 있는 테이블값 출력
    viewDBdata('bookDB_.db', 'bookdb')
