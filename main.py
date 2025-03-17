from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List, Union
from uuid import UUID
from db.database import database
from db import crud
from schemas import Cheese, CheeseListResponse

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/cheese/", response_model=Cheese)
async def create_cheese(cheese: Cheese):
    await crud.create_cheese(cheese)
    return cheese


@app.get("/cheese/", response_model=Union[Cheese, CheeseListResponse])
async def get_cheese(
    cheese_id: Optional[UUID] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    if cheese_id:
        cheese = await crud.get_cheese_by_id(str(cheese_id))
        if cheese is None:
            raise HTTPException(status_code=404, detail="Cheese not found")
        return cheese

    return await crud.get_cheeses(limit, offset)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)