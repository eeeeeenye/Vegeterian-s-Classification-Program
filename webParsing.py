from asyncio.windows_events import NULL
import threading
import requests
import pprint
import bs4
import pandas as pd
import DBmanager as DB


datas = []
name_list = []                                                   # 열이름값

class APIparser(threading.Thread):                               # OpenAPI 파싱 스레드
    def run(self): 
        Serv_Key = '0c92e79c0ebd4fb79256'
        Url = 'http://openapi.foodsafetykorea.go.kr/api/'
        startNum = 10582                                         # 원재료명의 분류 추출(수산물, 축산물 등 포함, 식물성 재료 제외)
        EndNum = 18850
        global datas,name_list,ingr_df

        for i in range(9):
            name_list = []                                       # 빈 리스트로 초기화
            mid_Num = startNum + 1000                            # 한번 호출 당 최대 1000개씩만 호출 가능

            if i == 8:
                mid_Num = EndNum

            url_m = Url+Serv_Key+'/'+'I1020/'+'xml/'+str(startNum)+'/'+str(mid_Num)
            response = requests.get(url_m)
            print(response)
            content = response.text
            pp = pprint.PrettyPrinter(indent=4)
            xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
            ingr = xml_obj.findAll('row')                        # <row> 태그에 원재료에 대한 정보가 담겨있음 
            #print(ingr)
            """
            sample
            0 <RAWMTRL_STATS_CD_NM/>
            1 <LCLAS_NM>식품원료(A코드)</LCLAS_NM>
            2 <RPRSNT_RAWMTRL_NM>Abiu열매</RPRSNT_RAWMTRL_NM>
            3 <REGN_CD_NM>열매</REGN_CD_NM>
            4 <RAWMTRL_NCKNM/>
            5 <SCNM>Pouteria caimito Radlk / Lucuma caimito Roem. & Schult / Achras caimito Ruiz & Pavon</SCNM>
            6 <ENG_NM>Yellow star apple, Caimito, Caimo, Luma</ENG_NM>
            7 <MLSFC_NM>식물</MLSFC_NM>
            8 <USE_CND_NM>제한적사용</USE_CND_NM>

            """

                                                                 # xml 안의 데이터 수집
            for i in range(0, len(ingr)):                        # 0부터 ingr의 길이까지
                columns = ingr[i].find_all()                     # i번째에 있는 태그값들을 모두 가져옴 
                if i > 0  and i < 9 :
                    if str(columns[i].name) == 'LCLAS_NM' or str(columns[i].name) == 'RPRSNT_RAWMTRL_NM' or str(columns[i].name) == 'MLSFC_NM' :   
                        name_list.append(columns[i].name) 

                                                                 # ingr의 각 데이터 값 저장
                LCLAS = ingr[i].LCLAS_NM.string.strip()
                RPRSNT = ingr[i].RPRSNT_RAWMTRL_NM.string.strip()
                MLSFC = ingr[i].MLSFC_NM.string.strip()
                data = [LCLAS,RPRSNT,MLSFC]
                datas.append(data)

            startNum = mid_Num+1
            url_m = Url
        
        ingr_df = pd.DataFrame(datas, columns=name_list)
        DB.DF2DB(ingr_df)                                       # 데이터베이스에 DataFrame 형태의 데이터를 저장
        print(ingr_df)



