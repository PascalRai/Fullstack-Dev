from fastapi import FastAPI

from app.routers import register, login
from app.database.init_db import init_database

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)

# Database initialized after every modules is initialized (acutal required: models of DB Table)
# init_database() # use seed.py instead of alembic