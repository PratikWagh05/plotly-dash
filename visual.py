import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
file_path = 'https://raw.githubusercontent.com/PratikWagh05/plotly-dash/main/Final.csv'
df = pd.read_csv(file_path)

# Ensure Period_start and Period_end are in datetime format
df['Period_start'] = pd.to_datetime(df['Period_start'], errors='coerce')
df['Period_end'] = pd.to_datetime(df['Period_end'], errors='coerce')
 
# Create a combined DataFrame for trend chart
df_start = df[['Client_Name', 'Period_start', 'Supply/Purchase Value AED']].rename(columns={'Period_start': 'Period'})
df_start['Type'] = 'Start'
df_end = df[['Client_Name', 'Period_end', 'Supply/Purchase Value AED']].rename(columns={'Period_end': 'Period'})
df_end['Type'] = 'End'
combined_df = pd.concat([df_start, df_end])

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
        'color': 'black',
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
            {'label': 'Trend Chart', 'value': 'trend'},
            {'label': 'Pie Chart', 'value': 'pie'},
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
    dcc.Graph(id='feature-graph')
], style=styles['container'])
 
@app.callback(
    Output('feature-graph', 'figure'),
    [Input('chart-dropdown', 'value')]
)
def update_graph(selected_chart):
    try:
        filtered_df = df
        filtered_combined_df = combined_df
 
        if selected_chart == 'scatter':
            fig = px.scatter(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', color='Client_Name', title='Scatter Plot of Supply/Purchase Value AED vs VAT Value AED')
        elif selected_chart == 'trend':
            fig = px.line(filtered_combined_df, x='Period', y='Supply/Purchase Value AED', color='Client_Name', line_dash='Type', title='Trend Chart of Supply/Purchase Value AED over Time')
        elif selected_chart == 'pie':
            # Aggregate data for pie charts
            supply_purchase_pie = filtered_df.groupby('Client_Name')['Supply/Purchase Value AED'].sum().reset_index()
            vat_pie = filtered_df.groupby('Client_Name')['VAT Value AED'].sum().reset_index()
 
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Supply/Purchase Value AED', 'VAT Value AED'),
                specs=[[{'type': 'pie'}, {'type': 'pie'}]]
            )
 
            # Add pie chart for Supply/Purchase Value AED
            fig.add_trace(go.Pie(
                labels=supply_purchase_pie['Client_Name'],
                values=supply_purchase_pie['Supply/Purchase Value AED'],
                name='Supply/Purchase Value AED'
            ), row=1, col=1)
 
            # Add pie chart for VAT Value AED
            fig.add_trace(go.Pie(
                labels=vat_pie['Client_Name'],
                values=vat_pie['VAT Value AED'],
                name='VAT Value AED'
            ), row=1, col=2)
 
            fig.update_layout(
                title_text='Pie Charts of Supply/Purchase Value AED and VAT Value AED'
            )
 
        elif selected_chart == 'histogram':
            fig = px.histogram(filtered_df, x='Final Tax Code', y='Supply/Purchase Value AED', color='Client_Name', title='Histogram of Supply/Purchase Value AED')
        elif selected_chart == 'violin':
            fig = px.violin(filtered_df, x='TRN', y='Supply/Purchase Value AED', box=True, color='Client_Name', title='Violin Plot of Supply/Purchase Value AED')
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
            fig = px.area(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', color='Client_Name', title='Area Chart of Supply/Purchase Value AED vs VAT Value AED')
        elif selected_chart == 'bubble':
            fig = px.scatter(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', size='VAT Value AED', color='Client_Name', title='Bubble Chart of Supply/Purchase Value AED vs VAT Value AED')
        elif selected_chart == 'density_heatmap':
            fig = px.density_heatmap(filtered_df, x='Supply/Purchase Value AED', y='VAT Value AED', title='Density Heatmap of Supply/Purchase Value AED vs VAT Value AED')
 
        return fig
    except Exception as e:
        print(f"Error: {e}")  # Print any errors that occur
        return go.Figure()  # Return an empty figure in case of an error
 
if __name__ == '__main__':
    app.run_server(debug=True)
