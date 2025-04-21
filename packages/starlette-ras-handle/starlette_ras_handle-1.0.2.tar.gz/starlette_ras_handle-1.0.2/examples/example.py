from handler import print_handler
from starlette_ras_handle import handle_starlette_ras
handle_starlette_ras(print_handler)

from time import sleep
import uvicorn
from fastapi import FastAPI
from starlette.background import BackgroundTasks
from starlette.exceptions import HTTPException
from starlette.responses import Response

app = FastAPI()

@app.get("/example")
async def example(background_tasks: BackgroundTasks) -> Response:
    def error_task() -> None:
        sleep(1)
        raise HTTPException(status_code=500)

    background_tasks.add_task(error_task)

    return Response(status_code=200)

uvicorn.run(app, port=8080)