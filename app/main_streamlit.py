from typing import Any
import streamlit as st
from logging import getLogger
from api_requests.carbon_intensity_requests import GenerationMixAPI
from services.analytics import GenerationMixService
import plotly.express as px
from datetime import datetime, tzinfo, timedelta
from services.gen_mix_dashboard import GBEnergyAnalytics

logger = getLogger(__name__)


def main():
    app = GBEnergyAnalytics()
    app.init_app()


if __name__ == "__main__":
    main()
