import time
import numpy as np
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

app = FastAPI()

# Define a request model
class PredictRequest(BaseModel):
    n_rounds: int=5

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.post(
        "/calculate",
        response_description="Simple function"
)
async def calculate(request: PredictRequest) -> list:

    try:
        result = []
        for _ in range(request.n_rounds):
            result.append(np.random.choice([0, 1, 2, 3, 4, 5]).item())

        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )