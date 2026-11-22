import os
import databases
import sqlalchemy
import ormar
from fastapi import FastAPI,HTTPException
from ormar.exceptions import NoMatch

url=os.environ["DATABASE_URL"]
db=databases.Database(url)
metadata=sqlalchemy.MetaData()
engine=sqlalchemy.create_engine(url)
class BaseMeta(ormar.ModelMeta):
    database=db
    metadata=metadata

class Book(ormar.Model):
    class Meta(BaseMeta):
        tablename="books"
    id:int=ormar.Integer(primary_key=True)
    title:str=ormar.String(max_length=100)
    description:str=ormar.Text()
    published_year:int=ormar.Integer()

app=FastAPI(title="Бібліотека")
@app.on_event("startup")
async def startup():
    metadata.create_all(engine)
    await db.connect()
    if not await Book.objects.count():
        async with db.transaction():
            for title,year,description in [
                ("1984",1949,"Антиутопія Джорджа Орвелла."),
                ("To Kill a Mockingbird",1960,"Роман Гарпер Лі."),
                ("The Great Gatsby",1925,"Роман Френсіса Скотта Фіцджеральда.")]:
                await Book.objects.create(title=title,published_year=year,description=description)
@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    engine.dispose()

async def by_id(model,ident):
    try:
        return await model.objects.get(id=ident)
    except NoMatch:
        raise HTTPException(404,"Запис не знайдено")

@app.get("/books/",response_model=list[Book])
async def books():
    return await Book.objects.order_by("id").all()

@app.get("/books/{ident}",response_model=Book)
async def book(ident:int):
    return await by_id(Book,ident)

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import Response
from pydantic import BaseModel,Field,validator

# Одна книга може мати багато позик. Кожна позика посилається на книгу і читача.
class Reader(ormar.Model):
    class Meta(BaseMeta):
        tablename="readers"
    id:int=ormar.Integer(primary_key=True)
    name:str=ormar.String(max_length=80)

class Loan(ormar.Model):
    class Meta(BaseMeta):
        tablename="loans"
    id:int=ormar.Integer(primary_key=True)
    reader:Reader=ormar.ForeignKey(Reader,ondelete="RESTRICT")
    book:Book=ormar.ForeignKey(Book,ondelete="RESTRICT")
    returned:bool=ormar.Boolean(default=False)

class ReaderInput(BaseModel):
    name:str=Field(min_length=1,max_length=80)
    class Config:
        anystr_strip_whitespace=True
        extra="forbid"

class LoanInput(BaseModel):
    reader:int=Field(gt=0)
    book:int=Field(gt=0)
    returned:bool=False
    class Config:
        extra="forbid"

class LoanPatch(BaseModel):
    reader:int | None=Field(None,gt=0)
    book:int | None=Field(None,gt=0)
    returned:bool | None=None
    @validator("*",pre=True)
    def require_value(cls,value):
        if value is None:
            raise ValueError("Явний null заборонено")
        return value
    class Config:
        extra="forbid"

@app.get("/readers/",response_model=list[Reader])
async def readers():
    return await Reader.objects.all()

@app.get("/readers/{ident}",response_model=Reader)
async def reader(ident:int):
    return await by_id(Reader,ident)

@app.post("/readers/",response_model=Reader,status_code=201)
async def add_reader(data:ReaderInput):
    return await Reader.objects.create(**data.dict())

@app.patch("/readers/{ident}",response_model=Reader)
async def edit_reader(ident:int,data:ReaderInput):
    row=await by_id(Reader,ident)
    return await row.update(**data.dict())

@app.delete("/readers/{ident}",status_code=204)
async def delete_reader(ident:int):
    row=await by_id(Reader,ident)
    try:
        await row.delete()
    except ForeignKeyViolationError:
        raise HTTPException(409,"У читача є позики")
    return Response(status_code=204)

@app.get("/loans/",response_model=list[Loan])
async def loans():
    return await Loan.objects.select_related(["reader","book"]).all()

@app.get("/loans/{ident}",response_model=Loan)
async def loan(ident:int):
    return await by_id(Loan,ident)

async def links(data):
    for name,model in (("reader",Reader),("book",Book)):
        if name in data:
            data[name]=await by_id(model,data[name])
    return data

@app.post("/loans/",response_model=Loan,status_code=201)
async def add_loan(data:LoanInput):
    try:
        return await Loan.objects.create(**await links(data.dict()))
    except ForeignKeyViolationError:
        raise HTTPException(409,"Пов’язаний запис змінився")

@app.patch("/loans/{ident}",response_model=Loan)
async def edit_loan(ident:int,data:LoanPatch):
    row=await by_id(Loan,ident)
    try:
        return await row.update(**await links(data.dict(exclude_unset=True)))
    except ForeignKeyViolationError:
        raise HTTPException(409,"Пов’язаний запис змінився")

@app.delete("/loans/{ident}",status_code=204)
async def delete_loan(ident:int):
    row=await by_id(Loan,ident)
    await row.delete()
    return Response(status_code=204)
