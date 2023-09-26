import uvicorn
from fastapi import FastAPI
from logging import getLogger
from app.api_requests.dto import GenerationMixDTO
from app.services import GenerationMixService
from typing import List

logger = getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI Online"}

@app.get("/generation_mix/last_month")
async def last_month_energy_mix() -> List[GenerationMixDTO]:
    """endpoint returns generation mix 

    Returns:
        List[GenerationMixDTO]: aggragted generation mix of the last complete month
    """
    gen_mix_service = GenerationMixService()
    return gen_mix_service.get_last_months_energy_mix()


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()