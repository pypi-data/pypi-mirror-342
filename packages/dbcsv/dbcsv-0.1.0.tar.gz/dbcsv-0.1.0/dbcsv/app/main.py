from fastapi import FastAPI

from .api.routes import auth, query

app = FastAPI()


@app.get("/")
def root():
    return "This is for database engine!"


app.include_router(router=query.router)
app.include_router(router=auth.router)
