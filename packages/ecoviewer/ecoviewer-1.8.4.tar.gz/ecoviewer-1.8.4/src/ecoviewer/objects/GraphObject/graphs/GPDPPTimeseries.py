from ecoviewer.objects.GraphObject.GraphObject import GraphObject
from ecoviewer.objects.DataManager import DataManager
from ecoviewer.constants.constants import *
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from dash import dcc
import plotly.express as px

class GPDPPTimeseries(GraphObject):
    def __init__(self, dm : DataManager, title : str = "Daily Hot Water Usage Graph", summary_group : str = None):
        self.summary_group = summary_group
        super().__init__(dm, title, event_reports=typical_tracked_events,event_filters=['HW_LOSS'])

    def create_graph(self, dm : DataManager):
        df_daily = dm.get_daily_data_df(events_to_filter=self.event_filters)

        df_daily['Flow_CityWater_Total'] = df_daily[dm.flow_variable] * (60 * 24) #average GPM * 60min/hr * 24hr/day
        df_daily = df_daily[df_daily["Flow_CityWater_Total"].notna()] # filter nulls out
        df_daily['Flow_CityWater_PP'] = round(df_daily['Flow_CityWater_Total'] / dm.occupant_capacity, 2)
        percentile = 0.95
        mean_day = df_daily[dm.flow_variable].mean() * 24 * 60
        percentile_day = df_daily[dm.flow_variable].quantile(percentile) * 24 * 60
        mean_daily_usage = mean_day / dm.occupant_capacity
        high_daily_usage = percentile_day / dm.occupant_capacity

        units = 'Gallons/Person/Day' if dm.occupant_capacity > 1 else 'Gallons/Day'
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df_daily.index, y = df_daily.Flow_CityWater_PP.round(1), mode = 'markers',
                                marker = dict(size=5, color = 'rgb(56,166,165)'), showlegend=False,
                                hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Usage:</b> %{y:.1f} " + units))
        
        fig.add_trace(go.Scatter(
        x=[df_daily.index.min() - pd.Timedelta(hours = 23), df_daily.index.max() + pd.Timedelta(hours = 23)],
        y=[mean_daily_usage, mean_daily_usage],
        mode="lines",
        line=dict(color="darkred", dash="dash"),
        name="Mean Daily Usage",
        hoverinfo="text",
        hovertext=f"Mean Daily Usage: {mean_daily_usage:.2f} {units}"))
        
        fig.add_trace(go.Scatter(
        x=[df_daily.index.min() - pd.Timedelta(hours = 23), df_daily.index.max() + pd.Timedelta(hours = 23)],
        y=[high_daily_usage, high_daily_usage],
        mode="lines",
        line=dict(color="darkblue", dash="dash"),
        name="95th Percentile Usage",
        hoverinfo="text",
        hovertext=f"95th Percentile Usage: {high_daily_usage:.2f} {units}"))

       
        fig.update_layout(title={'text':'<b>Daily Hot Water Usage</b>','font':{'size':24}})
        fig.update_yaxes(title_text=f'<b>{units}</b>',title_font={'size':18})
        fig.update_xaxes(title_text='<b>Time</b>',title_font={'size':18})

        return dcc.Graph(figure=fig)