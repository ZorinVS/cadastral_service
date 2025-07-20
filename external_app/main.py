import asyncio
import random
from typing import Annotated

from fastapi import Body, FastAPI

from schemas import QueryRequestDTO

app = FastAPI(title="External App")


@app.post("/result", summary="Эмуляция обработки запроса внешним сервером")
async def get_result(_info_to_check: Annotated[QueryRequestDTO, Body(...)]) -> dict[str, bool]:
    await asyncio.sleep(random.randint(1, 3))
    # await asyncio.sleep(random.randint(1, 60))
    return {"result": bool(random.randrange(0, 5))}  # False с вероятностью 20%
