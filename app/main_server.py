import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from logging import getLogger
from app.api_requests.dto import GenerationMixDTO
from app.services.service import GenerationMixService
from typing import List
from app.services.plots import generate_donut
from pathlib import Path

logger = getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI Online"}

@app.get("/generation_mix/last_month")
async def last_month_energy_mix() -> GenerationMixDTO:
    """endpoint returns generation mix 

    Returns:
        List[GenerationMixDTO]: aggragted generation mix of the last complete month
    """
    return GenerationMixService.get_last_months_energy_mix()

@app.get("/generation_mix/last_month/poster")
async def last_month_energy_mix_poster() -> FileResponse:
    e_mix = GenerationMixService.get_last_months_energy_mix()
    file_path = generate_donut(e_mix, Path('./images'), 'donut')
    return FileResponse(file_path, media_type='image/png')


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()