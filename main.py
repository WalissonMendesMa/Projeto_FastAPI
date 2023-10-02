from fastapi import FastAPI, Request, status, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated 
from database import engine, get_db
import models


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", response_class=HTMLResponse)
async def home(request:Request, db: db_dependency):
    """
    request -> requisicao web;
    db -> responsavel por realizar as acoes no banco de dados.

    Funcao que retorna um template '.html' passando como objeto tabela do banco de dados.
    """
    products = db.query(models.ToExpired).all()
    return templates.TemplateResponse("get.html", {"request": request, "products": products})

@app.post("/post")
async def post_new_product(db: db_dependency,product_code: str = Form(...), name: str = Form(...), expired_in: str = Form(...)):
    """
    Espera receber 3 parametros vindos de 'post.html', atribuindos a product do tipo 'ToExpired'
    e o sava no banco de dados.

    -> redireciona para a pagina pricipal apos execucao descrita acima.
    """
    product = models.ToExpired(product_code=product_code, name=name, expired_in=expired_in)
    db.add(product)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/add-new")
async def add_new(request: Request):
    return templates.TemplateResponse("post.html", {"request":request})

@app.post("/edit/{product_code}")
async def update(db: db_dependency, product_code = str ,name: str = Form(...), expired_in: str = Form(...)):
    """
    busca um objeto no banco de dados filtrando-o pelo codigo e reatribuindo seus valores quando encontrado.
    -> redireciona para pagina principal quando encontrado.
    """
    product_edited = db.query(models.ToExpired).filter(models.ToExpired.product_code == product_code).first()
    product_edited.name = name
    product_edited.expired_in = expired_in
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/edit-product/{product_code}")
async def edit_product(request: Request, product_code: str, db: db_dependency):
    product = db.query(models.ToExpired).filter(models.ToExpired.product_code == product_code).first()
    return templates.TemplateResponse("update.html", {"request":request, "product":product})

@app.get("/delete-product/{product_code}")
async def delete_product(request: Request, product_code: str, db: db_dependency):
    """
    busca um objeto no banco de dados filtrando-o pelo codigo e o deletando quando encontrado.
    -> redireciona para pagina principal quando encontrado.
    """
    product = db.query(models.ToExpired).filter(models.ToExpired.product_code == product_code).first()
    db.delete(product)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)