# third-party
from plotly import graph_objects as go
from plotly_resampler import FigureResampler
import pandas as pd


COLOR_PALETTE = ['#4179A0', '#A0415D', '#44546A',
                 '#44AA97', '#FFC000', '#0F3970', '#873C26']


def hex_to_rgba(h, alpha):
    '''
    converts color value in hex format to rgba format with alpha transparency
    '''
    return tuple([int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)] + [alpha])


def plot_channels(data, channels, datetime_as_index=True):
    ''' Plots the signals corresponding to the channel namels in "channels".

    Parameters
    ----------
    data : mne.io.Raw or pd.DataFrame
        Instance of mne.io.Raw or dataframe containing the columns "time" and the ones in "channels".
    channels : list
        List containing the names of the channels to plot. 
    datetime_as_index : bool, defaults to True
        Whether to use datetime as x-axis or not, in which case a timedelta (in seconds) will be used.
    Returns
    -------
    None
    '''
    if isinstance(data, pd.DataFrame):
        data_df = data.copy()
    else:
        data_df = data.copy().to_data_frame(picks=channels)

    fig = FigureResampler(go.Figure())

    # Plot data channels
    for i, ch in enumerate(channels):
        if datetime_as_index:
            axis_label = 'Time (H:M:S)'
            t = pd.to_timedelta(data_df.time, unit='s') + \
                pd.Timestamp(2024, 1, 1)
        else:
            axis_label = 'Time (s)'
            t = data_df.time

        fig.add_trace(go.Scatter(
            x=t, y=data_df[ch],
            line=dict(width=3, color=COLOR_PALETTE[i]),
            name=ch
        ))

    # Config plot layout
    fig.update_yaxes(
        gridcolor='lightgrey',
        title='Amplitude (mV)'
    )
    fig.update_xaxes(
        gridcolor='lightgrey',
        title=axis_label,
        tickformat="%H:%M:%S",
    )
    fig.update_layout(
        title='ECG data',
        showlegend=True,
        plot_bgcolor='white',
    )
    fig.show_dash(mode='inline')
