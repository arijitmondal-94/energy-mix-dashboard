import plotly.graph_objects as go
from app.api_requests.dto import GenerationMixDTO
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


def generate_donut(data: GenerationMixDTO, path: Path, file_name: str) -> Path:
    
    start = data.from_
    end = data.to
    
    labels = [fuel.fuel.capitalize() for fuel in data.generationmix]
    values = [fuel.perc for fuel in data.generationmix]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    if path.exists():
        fp = Path(path, file_name).with_suffix('.png')
        fig.write_image(fp)
        return fp
    return None