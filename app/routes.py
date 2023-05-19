from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import os

from app import app

# Define your DataFrame
app_folder = os.path.dirname(os.path.realpath(__file__))
static_folder = os.path.join(app_folder, 'static')
csv_path = os.path.join(static_folder, 'word_counts_by_year_rolling_5.csv')
df_rolling = pd.read_csv(csv_path, index_col=0)

csv_path = os.path.join(static_folder, 'tf_idf.csv')
df_tf_idf = pd.read_csv(csv_path, index_col=0)

#df = pd.DataFrame()
    
def generate_plotly(word, df):
    x_data = df.index
    y_data = df[word]
    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color='black'), fillcolor='white'))
    fig.update_layout(plot_bgcolor='white')
    # Disable the mode bar
    config = {'displayModeBar': False}

    # Convert the graph to HTML
    graph_html = fig.to_html(full_html=False, config=config)
    return graph_html

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/word', methods=['GET'])
def word():
    word = request.args.get('word', '').lower()
    if word in df_rolling.columns:
        rolling_graph = generate_plotly(word, df_rolling)
        tf_idf_graph = generate_plotly(word, df_tf_idf)
        return render_template('graph.html', rolling_graph=rolling_graph, tf_idf_graph=tf_idf_graph, word=word)
    else:
        return render_template('error.html')
