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
