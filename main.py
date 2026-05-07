#

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# FastAPI객체 만들고
app = FastAPI()
#templates 폴더 연결(jinja2 사용해서 응답)
templates = Jinja2Templates(directory="templates")
# 클라이언트가 "/" 최상위 경로 요청 해오면 응답할 내용
@app.get("/", response_class=HTMLResponse)
def home(request:Request):
    # jinja2 템플릿 엔진이 index.html 문서를 (읽기x) 해석해서 클라이언트 웬문서에 출력
    result = templates.TemplateResponse("index.html", {
        "request": request,
        "fortuneToday":"동쪽으로 가면  귀인을 만나요"
        "noticeList": [
                {"content": "서버 점검 예정"},
                {"content": "신규 기능 업데이트"},
                {"content": "이벤트 참여 안내"}
            ]
    })
   

    return result