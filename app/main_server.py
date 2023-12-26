import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from logging import getLogger
from app.api_requests.dto import GenerationMixDTO
from app.services.analytics import GenerationMixService
from app.services.poster import GeneratePoster
from app.api_requests.carbon_intensity_requests import GenerationMixAPI
from typing import List
from app.services.plots import genration_mix_donut_png
from pathlib import Path
from datetime import datetime

logger = getLogger(__name__)

app = FastAPI()
generation_mix_service = GenerationMixService()


@app.get("/")
async def root():
    return {"message": "FastAPI Online"}

@app.get("/generation_mix/")
async def select_date_generation_mix(index_date: str) -> GenerationMixDTO:
    cir = GenerationMixAPI()
    index_date = datetime.strptime(index_date, "%Y-%m-%d")
    return cir.get_generation_for_date(index_date)
    

@app.get("/generation_mix/last_month")
async def last_month_energy_mix() -> GenerationMixDTO:
    """endpoint returns generation mix 

    Returns:
        List[GenerationMixDTO]: aggragted generation mix of the last complete month
    """
    return generation_mix_service.get_last_months_energy_mix()


@app.get("/generation_mix/last_month/poster")
async def last_month_energy_mix_poster() -> FileResponse:
    p = GeneratePoster()
    p.generate_poster()
    e_mix = generation_mix_service.get_last_months_energy_mix()
    file_path = genration_mix_donut_png(e_mix, Path('./images'), 'donut')
    return FileResponse(file_path, media_type='image/png')


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
