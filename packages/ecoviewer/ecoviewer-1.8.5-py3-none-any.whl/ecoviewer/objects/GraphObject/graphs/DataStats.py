from ecoviewer.objects.GraphObject.GraphObject import GraphObject
from ecoviewer.objects.DataManager import DataManager
import pandas as pd
from dash import dcc
from ecoviewer.constants.constants import *
import plotly.colors as pc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DataStats(GraphObject):
    def __init__(self, dm : DataManager, title : str = "Raw Data Quality Statistics"):
        self.start_day = dm.start_date
        self.end_day = dm.end_date
        super().__init__(dm, title,event_reports=typical_tracked_events, event_filters=['DATA_LOSS_COP'])

    def create_graph(self, dm : DataManager):
        query = dm.generate_daily_stats_query()

        daily_tats_df = pd.DataFrame()
        try:
            daily_tats_df = dm.get_df_from_query(query)
        except:
            raise Exception("Data statistics are not configured for this site.")
        if daily_tats_df.empty:
            raise Exception("No data statistics available for parameters specified.")

        # Select columns based on suffix
        total_missing = daily_tats_df.filter(regex='_missing_mins$').rename(columns=lambda x: x.replace('_missing_mins', ''))
        max_gap_missing = daily_tats_df.filter(regex='_max_gap$').rename(columns=lambda x: x.replace('_max_gap', ''))
        avg_gap_missing = daily_tats_df.filter(regex='_avg_gap$').rename(columns=lambda x: x.replace('_avg_gap', ''))


        color_sequence = pc.qualitative.Safe
        variables = total_missing.columns.tolist()
        color_map = {var: color_sequence[i % len(color_sequence)] for i, var in enumerate(variables)}

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                "<b>Total Missing Minutes per Day",
                "<b>Max Consecutive Data Gap",
                "<b>Average Data Gap"
            )
        )

        # Top plot: Total Missing Minutes
        for var in variables:
            fig.add_trace(
                go.Scatter(
                    x=total_missing.index,
                    y=total_missing[var],
                    mode='markers',
                    name=f"{var}",
                    marker=dict(color=color_map[var]),
                    legendgroup=var,
                    showlegend=True
                ),
                row=1, col=1
            )

        # Middle plot: Max Consecutive Missing Minutes
        for var in variables:
            fig.add_trace(
                go.Scatter(
                    x=max_gap_missing.index,
                    y=max_gap_missing[var],
                    mode='markers',
                    name=f"{var}",
                    marker=dict(color=color_map[var]),
                    legendgroup=var,
                    showlegend=False  # Avoid duplicate legend entry
                ),
                row=2, col=1
            )

        # Bottom plot: Average Data Gap per Day
        for var in variables:
            fig.add_trace(
                go.Scatter(
                    x=avg_gap_missing.index,
                    y=avg_gap_missing[var],
                    mode='markers',
                    name=f"{var}",
                    marker=dict(color=color_map[var]),
                    legendgroup=var,
                    showlegend=False  # Avoid duplicate legend entry
                ),
                row=3, col=1
            )

        fig.update_layout(
            height=900,
            width=1500,
            title_text="<b>Raw Data Quality",
            title={'font': {'size': 24}},
            margin=dict(t=60, b=40),
            legend=dict(title="Variables", traceorder="normal")
        )

        return dcc.Graph(figure=fig)