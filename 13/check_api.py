"""Інтеграційна перевірка працюючого API. Видаляє створені тестові записи."""
import json
from urllib.request import urlopen,Request
from urllib.error import HTTPError

def call(method,path,data=None,expected=200):
    req=Request("http://127.0.0.1:8000"+path,method=method,
                data=json.dumps(data).encode() if data is not None else None,
                headers={"Content-Type":"application/json"})
    try:
        resp=urlopen(req)
    except HTTPError as e:
        resp=e
    with resp:
        body=resp.read()
        assert resp.status==expected,(resp.status,body)
    return json.loads(body) if body else None

if __name__=="__main__":
    book=call("GET","/books/")[0]
    reader=call("POST","/readers/",{"name":"Тест"},201)["id"]
    path=f"/readers/{reader}"
    loan_id=None
    try:
        assert call("PATCH",path,{"name":"Іван"})["name"]=="Іван"
        loan_id=call("POST","/loans/",{"reader":reader,"book":book["id"]},201)["id"]
        item=f"/loans/{loan_id}"
        call("GET",item)
        assert call("PATCH",item,{"returned":True})["returned"]
        call("PATCH",item,{"returned":None},422)
        call("DELETE",path,expected=409)
    finally:
        if loan_id is not None:
            call("DELETE",f"/loans/{loan_id}",expected=204)
        call("DELETE",path,expected=204)
    call("GET",path,expected=404)
    print("CRUD, зв’язки, валідація та коди HTTP перевірені.")
