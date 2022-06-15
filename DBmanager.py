from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


query = ""
list_ = ()

def DF2DB(dataFrame):                           # DB에 데이터 저장하는 함수
    df = dataFrame
    db = create_engine("mysql+mysqldb://root:y5867360@localhost:3306/food_ingredient",encoding='utf-8')
    conn = db.connect()

    df.to_sql(name='meterials', con=db, if_exists='append')

def dataInput(flag):                            # 데이터베이스에서 데이터 불러오기
                                                # list = 사진에서 추출한 원재료명, list2 = 데이터베이스에서 추출한 데이터
                                                # flag = 0 락토, flag = 4 비채식, flag = 3 페스코
                                                # flag = 2 페스코 (락토오보에 수산물추가), flag = 1 락토오보 (페스코에 가금류 추가) 
    global query
    r_query = "select RPRSNT_RAWMTRL_NM as '원재료' from meterials where "
    LO_where = "RPRSNT_RAWMTRL_NM like '%계란%' or RPRSNT_RAWMTRL_NM like '%오리알%' or RPRSNT_RAWMTRL_NM like '%메추리알%' or RPRSNT_RAWMTRL_NM like '%전란%' or RPRSNT_RAWMTRL_NM like '%난황%' or RPRSNT_RAWMTRL_NM like '%난백%'" #락토오보
    polo_where = "RPRSNT_RAWMTRL_NM like '%닭%' or RPRSNT_RAWMTRL_NM like '오리%' or RPRSNT_RAWMTRL_NM like '%거위%' or RPRSNT_RAWMTRL_NM like '%칠면조%' or RPRSNT_RAWMTRL_NM like '%메추리%' or RPRSNT_RAWMTRL_NM like '훈제오리';"

    db = pymysql.connect(host='localhost', user='root', password='y5867360', db='food_ingredient',
                     charset='utf8')            # mysql connect
    curs = db.cursor()

    if flag == 0:
        query = r_query+"RPRSNT_RAWMTRL_NM like '%우유%' or RPRSNT_RAWMTRL_NM like '%탈지%';"
    elif flag == 1:
        query = r_query+LO_where+";"
    elif flag == 2:
        query = r_query+" MLSFC_NM='수산물';"
    elif flag == 3:
        query = r_query+polo_where
    elif flag == 4:
        query = r_query+"MLSFC_NM='%고기%';"
        

    curs.execute(query)
    select = list(curs.fetchall())              # 2차원 튜플
    db.commit()
    
    return select                                # 튜플로 반환
