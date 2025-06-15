from fastapi import FastAPI, HTTPException, status, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import User
from typing import Dict, List, Optional
import uuid

app = FastAPI(title="User Management System")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

users_db: Dict[str, User] = {}
#hello, its git commit -a

@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    search: Optional[str] = Query(None)
):
    users = list(users_db.values())
    if search:
        users = [u for u in users if search.lower() in u.name.lower()]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": users,
            "search_query": search or ""
        }
    )

@app.post("/users/", response_class=RedirectResponse)
async def create_user(
    name: str = Form(..., min_length=2, max_length=50),
    age: int = Form(..., gt=0, lt=150)
):
    user_id = str(uuid.uuid4())
    users_db[user_id] = User(id=user_id, name=name, age=age)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "user": users_db[user_id]
        }
    )

@app.post("/users/{user_id}/edit", response_class=RedirectResponse)
async def update_user(
    user_id: str,
    name: str = Form(..., min_length=2, max_length=50),
    age: int = Form(..., gt=0, lt=150)
):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = User(id=user_id, name=name, age=age)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/users/{user_id}/delete", response_class=RedirectResponse)
async def delete_user(user_id: str):
    if user_id in users_db:
        del users_db[user_id]
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

#для мобильных клиентов
@app.get("/api/users", response_model=List[User])
async def api_get_users():
    return list(users_db.values())
