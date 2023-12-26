import plotly.graph_objects as go
import plotly.express as px
from api_requests.dto import GenerationMixDTO
from logging import getLogger
from pathlib import Path
from api_requests.dto import GenerationMixDTO

logger = getLogger(__name__)



def plot_generation_mix_donut(data: GenerationMixDTO) -> go.Figure:

    labels = [fuel.fuel.capitalize() for fuel in data.generationmix]
    values = [fuel.perc for fuel in data.generationmix]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')

    return fig


def genration_mix_donut_png(data: GenerationMixDTO, path: Path, file_name: str) -> Path:

    start = data.from_
    end = data.to

    fig = plot_generation_mix_donut(data)

    if path.exists():
        fp = Path(path, file_name).with_suffix('.png')
        fig.write_image(fp)
        return fp
    return None


class DashboardPlots(object):
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def daily_gen_mix_bar_plot(cls, data: GenerationMixDTO) -> go.Figure:
        labels = [fuel.fuel.capitalize() for fuel in data.generationmix]
        values = [fuel.perc for fuel in data.generationmix]
        fig = px.bar(data, x=labels, y=values)
        fig.update_layout(xaxis_title='Energy Source', yaxis_title='Percentage (%)')
        
        return fig