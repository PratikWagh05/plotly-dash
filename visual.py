import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
file_path = 'https://raw.githubusercontent.com/PratikWagh05/plotly-dash/main/Final.csv'
df = pd.read_csv(file_path)

# Dash App
app = dash.Dash(__name__)
server = app.server

# Define styles
styles = {
    'container': {
        'padding': '20px',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f9f9f9',
        'color': '#333',
    },
    'header': {
        'textAlign': 'center',
        'color': '#007BFF',
        'marginBottom': '20px',
    },
    'dropdown': {
        'width': '50%',
        'marginBottom': '20px',
    }
}

app.layout = html.Div([
    html.H1("Final Dataset Visualization", style=styles['header']),
    dcc.Dropdown(
        id='chart-dropdown',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Box Plot', 'value': 'box'},
            {'label': 'Histogram', 'value': 'histogram'},
            {'label': 'Violin Plot', 'value': 'violin'},
            {'label': 'Heatmap', 'value': 'heatmap'},
            {'label': '3D Scatter Plot', 'value': '3d_scatter'},
            {'label': 'Parallel Coordinates', 'value': 'parallel_coords'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Area Chart', 'value': 'area'},
            {'label': 'Bubble Chart', 'value': 'bubble'},
            {'label': 'Density Heatmap', 'value': 'density_heatmap'}
        ],
        value='scatter',
        style=styles['dropdown']
    ),
    dcc.Graph(id='feature-graph'),
    dcc.Slider(
        id='value-slider',
        min=df['Supply/Purchase Value AED'].min(),
        max=df['Supply/Purchase Value AED'].max(),
        value=df['Supply/Purchase Value AED'].max(),
        marks={str(value): str(value) for value in df['Supply/Purchase Value AED'].unique()},
        step=None
    )
], style=styles['container'])

@app.callback(
    Output('feature-graph', 'figure'),
    [Input('chart-dropdown', 'value'), Input('value-slider', 'value')]
)
def update_graph(selected_chart, max_value):
    filtered_df = df[df['Supply/Purchase Value AED'] <= max_value]
    
    if selected_chart == 'scatter':
        fig = px.scatter(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', color='Client_Name', title=f'Scatter Plot of Supply/Purchase Value AED vs VAT Value AED with Value <= {max_value}')
    elif selected_chart == 'line':
        fig = px.line(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', color='Client_Name', title=f'Line Chart of Supply/Purchase Value AED vs VAT Value AED with Value <= {max_value}')
    elif selected_chart == 'pie':
        fig = px.pie(filtered_df, names='Client_Name', values='Supply/Purchase Value AED', title=f'Pie Chart of Supply/Purchase Value AED')
    elif selected_chart == 'box':
        fig = px.box(filtered_df, x='Client_Name', y='Supply/Purchase Value AED', title=f'Box Plot of Supply/Purchase Value AED')
    elif selected_chart == 'histogram':
        fig = px.histogram(filtered_df, x='Supply/Purchase Value AED', color='Client_Name', barmode='overlay', title=f'Histogram of Supply/Purchase Value AED')
    elif selected_chart == 'violin':
        fig = px.violin(filtered_df, x='Client_Name', y='Supply/Purchase Value AED', box=True, points='all', title=f'Violin Plot of Supply/Purchase Value AED')
    elif selected_chart == 'heatmap':
        numeric_df = filtered_df[['Supply/Purchase Value AED', 'VAT Value AED']]
        fig = px.imshow(numeric_df.corr(), text_auto=True, title='Heatmap of Feature Correlations')
    elif selected_chart == '3d_scatter':
        fig = px.scatter_3d(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', z='VAT Value AED', color='Client_Name', title='3D Scatter Plot')
    elif selected_chart == 'parallel_coords':
        filtered_df['Client_Name_id'] = filtered_df['Client_Name'].factorize()[0]
        fig = px.parallel_coordinates(filtered_df, dimensions=['Supply/Purchase Value AED', 'VAT Value AED'], color='Client_Name_id', labels={'Client_Name_id': 'Client Name ID'}, title='Parallel Coordinates')
    elif selected_chart == 'bar':
        fig = px.bar(filtered_df, x='Client_Name', y='Supply/Purchase Value AED', color='Client_Name', title='Bar Chart of Supply/Purchase Value AED')
    elif selected_chart == 'area':
        fig = px.area(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', color='Client_Name', title=f'Area Chart of Supply/Purchase Value AED vs VAT Value AED with Value <= {max_value}')
    elif selected_chart == 'bubble':
        fig = px.scatter(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', size='VAT Value AED', color='Client_Name', title=f'Bubble Chart of Supply/Purchase Value AED vs VAT Value AED with Value <= {max_value}')
    elif selected_chart == 'density_heatmap':
        fig = px.density_heatmap(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', title=f'Density Heatmap of Supply/Purchase Value AED vs VAT Value AED with Value <= {max_value}')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
