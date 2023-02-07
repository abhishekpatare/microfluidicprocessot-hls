import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html


# Creating the visual depiction of the schedule using Gantt Chart

schedule = pd.read_csv('../test/timestamps.csv')

fig1 = ff.create_gantt(schedule, showgrid_x=True, title='Schedule')

fig1.update_layout(xaxis_type='linear', xaxis_title='TimeStamps')
fig1.update_xaxes(tick0=0, dtick=1)


# Creating animated scatter line plot to display chip area usage v/s time

t_area = pd.read_csv('../test/storage.csv')


trace1 = go.Scatter(x=t_area['Time'], y=t_area['M'], mode='lines+markers', name='M', opacity=0.75)
trace2 = go.Scatter(x=t_area['Time'], y=t_area['S'], mode='lines+markers', name='S', opacity=0.75)
trace3 = go.Scatter(x=t_area['Time'], y=t_area['Total'], mode='lines+markers', name='Total=M+S', opacity=0.5)

frames = [dict(data= [dict(type='scatter',
                           x=t_area['Time'][:k+1],
                           y=t_area['M'][:k+1]),
                      dict(type='scatter',
                           x=t_area['Time'][:k+1],
                           y=t_area['S'][:k+1]),
                      dict(type='scatter',
                           x=t_area['Time'][:k+1],
                           y=t_area['Total'][:k+1]),     
                     ],
               traces= [0, 1, 2],  
              )for k  in  range(1, len(t_area))]

layout = go.Layout(title='Time v/s Chip Area Used',
                   showlegend=False,
                   hovermode='x unified',
                   updatemenus=[
                        dict(
                            type='buttons', showactive=False,
                            y=1.15,
                            x=1.15,
                            xanchor='right',
                            yanchor='top',
                            pad=dict(t=0, r=10),
                            buttons=[dict(label='Play',
                            method='animate',
                            args=[None, 
                                  dict(frame=dict(duration=500, 
                                                  redraw=False),
                                                  transition=dict(duration=0),
                                                  fromcurrent=True,
                                                  mode='immediate')]
                            )]
                        ),
                    ]              
                  )


fig2 = go.Figure(data=[trace1, trace2, trace3], frames=frames, layout=layout)
fig2.update_layout(xaxis_title='Time', yaxis_title='Area(in sq.units)', showlegend=True)


app = dash.Dash()
app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(figure=fig1)
    ]),
    html.Div([
        dcc.Graph(figure=fig2)
    ])
])

app.run_server(debug=True, use_reloader=False) 