import plotly.graph_objects as go
import plotly.express as px
from api_requests.dto import GenerationMixDTO, CO2Regions
from logging import getLogger
from pathlib import Path
import pandas as pd
from typing import List

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
        fig.update_layout(xaxis_title='Energy Source',
                          yaxis_title='Percentage (%)')

        return fig

    @classmethod
    def plot_generation_mix_donut(cls, data: GenerationMixDTO) -> go.Figure:

        labels = [fuel.fuel.capitalize() for fuel in data.generationmix]
        values = [fuel.perc for fuel in data.generationmix]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')

        return fig

    @classmethod
    def daily_co2_intensity_map(cls, data: List[CO2Regions], geojson_obj: dict = None) -> go.Figure:
        intensity_list = []

        for d in data:
            intensity_list.append(
                (d.regionid, d.intensity.forecast, d.dnoregion, d.intensity.index)
            )
        df = pd.DataFrame(intensity_list, columns=[
                          'ID', 'CO2 Intensity', 'DNO Region', 'index'])
        fig = px.choropleth_mapbox(df, geojson=geojson_obj,
                                   color_continuous_scale="gray",
                                   locations='ID',
                                   color='CO2 Intensity',
                                   range_color=(
                                       df["CO2 Intensity"].min(), df["CO2 Intensity"].max()),
                                   mapbox_style="carto-positron",
                                   zoom=4.2,
                                   center={"lat": 54.2289621927365,
                                           "lon": -4.536465063590197},
                                   opacity=0.5,
                                   labels={
                                       "DNO Area": "DNO Region",
                                       "CO2 Intensity": "CO2 Intensity"
                                   }
                                   )
        # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    @classmethod
    def daily_bm_prices(cls, data: pd.DataFrame) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=data.index, y=data["systemSellPrice"], mode="lines"))
        fig.add_trace(go.Bar(x=data.index, y=data["netImbalanceVolume"]))
        
        return fig
    
        
