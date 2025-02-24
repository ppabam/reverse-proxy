from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    a = [1, 2, 3, 4]
    b = [5, 6, 7, 8]

    result = []
    for i in range(len(a)): # zip(a, b)
        result.append(a[i] + b[i])
        
    return {"Hello": result}


@app.get("/two-dimensional-array")
def two_dimensional_array():
    a = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    b = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]
    
    result = a + b
    return {"result": result}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

