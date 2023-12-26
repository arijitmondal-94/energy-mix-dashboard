import streamlit as st
import plotly.express as px
from logging import getLogger
from services.plots import DashboardPlots
from services.analytics import GenerationMixService
from datetime import datetime

logger = getLogger(__name__)

class GenerationMixDashboard(object):
    
    def __init__(self, name: str = 'UK Generation Mix') -> None:
        self.name = name
        st.title(self.name)
        self.date = datetime.now()
        self.time = self.date.time()
    
    def daily_generation_mix(self) -> None:
        data = GenerationMixService.get_generation_mix_selected_date(self.date)
        fig = DashboardPlots.daily_gen_mix_bar_plot(data)
        
        return fig
    
    def half_hourly_egenration_mix(self) -> None:
        data = GenerationMixService.get_generation_mix_selected_date(self.date)
        fig = DashboardPlots.daily_gen_mix_bar_plot(data)
        
    
    def init_app(self):
        tab1, tab2 = st.tabs(["Daily Generation Mix", "Half-Hourly Generation Mix"])
        with tab1:
            self.date = st.date_input('Select Date:', self.date, max_value=datetime.now())
            fig = self.daily_generation_mix()
            st.plotly_chart(fig)
            st.write('Showing Energy Mix for Date:', self.date)
        with tab2:
            self.date = st.date_input('Select Date:', self.date, max_value=self.date, key='hh_d')
            self.time = st.time_input('Select Time:', self.time, key='hh_ts')
            fig = self.daily_generation_mix()
            st.plotly_chart(fig)
            st.write('Showing Energy Mix for Date: ', self.date), st.write('Time: ',self.time)