import uvicorn
from fastapi import FastAPI
from app.routers import products

app = FastAPI()


@app.get("/")
def read_root():
    return {"title" : "similarity_search"}

app.include_router(products.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)