import streamlit as st
import plotly.express as px
from logging import getLogger
from services.plots import DashboardPlots
from services.analytics import GenerationMixService, CO2IntensityServices
from datetime import datetime
import json
import geopandas as gpd

logger = getLogger(__name__)

st.set_page_config(layout='wide')

class GBEnergyAnalytics(object):

    def __init__(self, name: str = 'UK Generation Mix') -> None:
        self.name = name
        st.title(self.name)
        self.date = datetime.now()
        self.time = self.date.time()
        self.generation_mix_container = st.container()
        self.carbon_intensity_container = st.container()

    def daily_generation_mix(self) -> None:
        data = GenerationMixService.get_generation_mix_selected_date(self.date)
        fig = DashboardPlots.daily_gen_mix_bar_plot(data)

        return fig

    def half_hourly_egenration_mix(self) -> None:
        data = GenerationMixService.get_generation_mix_selected_date(self.date)
        fig = DashboardPlots.daily_gen_mix_bar_plot(data)

    def run_generation_mix_container(self) -> None:
        self.date = self.generation_mix_container.date_input(
            'Select Date:', self.date, max_value=datetime.now())
        fig = self.daily_generation_mix()
        self.generation_mix_container.plotly_chart(fig)
        # self.generation_mix_container.write('Showing Energy Mix for Date:', self.date)

    def run_co2_intensity_regional_container(self) -> None:
        regions = CO2IntensityServices.get_regions()
        from_date = self.carbon_intensity_container.date_input(
            'Select Date:', 'today', max_value=datetime.now(), key="co2")
        region = self.carbon_intensity_container.selectbox(
            'Select a region', regions)
        data = CO2IntensityServices.get_regional_co2_intensity(
            from_date, region)
        fig = self.daily_generation_mix()
        self.generation_mix_container.plotly_chart(fig)
        self.generation_mix_container.write(data)

    def run_co2_intensity_map(self) -> None:
        path = '/Users/arijitmondal/workspace/energy-mix-dashboard/app/data/dno_license_areas_20200506.json'
        uk_dno_areas_df = gpd.read_file(path)
        uk_dno_areas_df_4326 = uk_dno_areas_df.to_crs(epsg='4326')
        data = CO2IntensityServices.get_current_regional_co2_intensity()
        fig = DashboardPlots.daily_co2_intensity_map(data, uk_dno_areas_df_4326)

        self.carbon_intensity_container.plotly_chart(fig, True)

    def init_app(self):
        # self.run_co2_intensity_regional_container()
        self.run_co2_intensity_map()
        self.run_generation_mix_container()
