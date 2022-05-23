from fastapi import FastAPI
import uvicorn

app = FastAPI()

fake_item_db = [
    {"item_name" : "Foo"},
    {"item_name" : "Bar"},
    {"item_name" : "Bax"}
]

@app.get("/items/")
def get_user(skip: int = 0, limit: int = 10):
    return fake_item_db[skip: skip+limit]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 30003)