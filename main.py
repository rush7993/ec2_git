# main.py

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
# 필요한 자원 import
from sqlalchemy.orm import sessionmaker, Session


#DB 연결 설정
# "postgresql://계정:비밀번호@ip주소/database 명"
DB_URL = "postgresql://scott:tiger@172.16.8.101/scott_db"
# DB 접속해서 작업할 engine 객체 얻어내기
engine = create_engine(DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DB 세션 관리
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# FastAPI 객체를 만들고
app=FastAPI()


# templates 폴더 연결 (Jinja2 를 사용해서 응답하기 위함)
templates = Jinja2Templates(directory="templates")


# 클라이언트가 "/" 최상위 경로 요청을 해오면 응답할 내용
@app.get("/", response_class=HTMLResponse)
def home(request:Request, db: Session = Depends(get_db)):


    # sql 실행하고 결과 얻어내기
    query = text("""
        SELECT num, content
        FROM notice
        ORDER BY num DESC
    """)
    result = db.execute(query)
    noticeList = result.fetchall()


    # jinja2 템플릿 엔진이  index.html 문서를 읽어서 그대로 출력하는 것이 아니고 해석한 결과를
    # 클라이언트 웹브라우저에 응답한다
    result2 = templates.TemplateResponse(
        {"request":request},
        name="index.html",
        context={
            "fortuneToday":"동쪽으로 가면 귀인을 만나요!",
            "noticeList":noticeList
        }
    )
    return result2


