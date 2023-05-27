from typing import Union
from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/events")
def load_events():
    df = pd.DataFrame([[2, 5 , 6], [4, 5, 6]], columns=["sdf", "fdsf", "fds"])
    df_json = df.to_dict(orient='list')
    return df_json