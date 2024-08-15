import tkinter as tk
from tkinter import filedialog
import pandas as pd
import plotly.graph_objects as go

def select_csv_file():
    root = tk.Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Select CSV file"
    )
    return file_path

def create_graph(file_path):
    df = pd.read_csv(file_path)

    required_columns = ['BTC_price', 'ETH_price', 'BUSD_price', 'TRY_price']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df[required_columns] = df[required_columns].apply(pd.to_numeric, errors='coerce')
    df['snapped_at'] = pd.to_datetime(df['snapped_at'])

    df['BTC_to_ETH'] = df['BTC_price'] / df['ETH_price']
    df['BTC_to_BUSD'] = df['BTC_price'] / df['BUSD_price']
    df['BTC_to_TRY'] = df['BTC_price'] / df['TRY_price']
    df['ETH_to_BTC'] = df['ETH_price'] / df['BTC_price']
    df['BUSD_to_BTC'] = df['BUSD_price'] / df['BTC_price']
    df['TRY_to_BTC'] = df['TRY_price'] / df['BTC_price']
    df['ETH_to_BUSD'] = df['ETH_price'] / df['BUSD_price']
    df['ETH_to_TRY'] = df['ETH_price'] / df['TRY_price']
    df['BUSD_to_ETH'] = df['BUSD_price'] / df['ETH_price']
    df['BUSD_to_TRY'] = df['BUSD_price'] / df['TRY_price']
    df['TRY_to_ETH'] = df['TRY_price'] / df['ETH_price']
    df['TRY_to_BUSD'] = df['TRY_price'] / df['BUSD_price']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['snapped_at'],
        y=df['BTC_price'],
        mode='lines',
        name='BTC',
        hovertemplate=(
            'BTC Price: %{y:.10f} $ <br>'
            'ETH Equivalent: %{customdata[0]:.10f} ETH<br>'
            'BUSD Equivalent: %{customdata[1]:.10f} BUSD<br>'
            'TRY Equivalent: %{customdata[2]:.10f} TRY<br>'
            '<extra></extra>'
        ),
        customdata=df[['BTC_to_ETH', 'BTC_to_BUSD', 'BTC_to_TRY']].values
    ))
    fig.add_trace(go.Scatter(
        x=df['snapped_at'],
        y=df['ETH_price'],
        mode='lines',
        name='ETH',
        hovertemplate=(
            'ETH Price: %{y:.10f}$<br>'
            'BTC Equivalent: %{customdata[0]:.10f} BTC<br>'
            'BUSD Equivalent: %{customdata[1]:.10f} BUSD<br>'
            'TRY Equivalent: %{customdata[2]:.10f} TRY<br>'
            '<extra></extra>'
        ),
        customdata=df[['ETH_to_BTC', 'ETH_to_BUSD', 'ETH_to_TRY']].values
    ))
    fig.add_trace(go.Scatter(
        x=df['snapped_at'],
        y=df['BUSD_price'],
        mode='lines',
        name='BUSD',
        hovertemplate=(
            'BUSD Price: %{y:.10f}$<br>'
            'BTC Equivalent: %{customdata[0]:.10f} BTC<br>'
            'ETH Equivalent: %{customdata[1]:.10f} ETH<br>'
            'TRY Equivalent: %{customdata[2]:.10f} TRY<br>'
            '<extra></extra>'
        ),
        customdata=df[['BUSD_to_BTC', 'BUSD_to_ETH', 'BUSD_to_TRY']].values
    ))
    fig.add_trace(go.Scatter(
        x=df['snapped_at'],
        y=df['TRY_price'],
        mode='lines',
        name='TRY',
        hovertemplate=(
            'TRY Price: %{y:.10f}$<br>'
            'BTC Equivalent: %{customdata[0]:.10f} BTC<br>'
            'ETH Equivalent: %{customdata[1]:.10f} ETH<br>'
            'BUSD Equivalent: %{customdata[2]:.10f} BUSD<br>'
            '<extra></extra>'
        ),
        customdata=df[['TRY_to_BTC', 'TRY_to_ETH', 'TRY_to_BUSD']].values
    ))

    fig.update_layout(
        title='Token Prices and Ratios',
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        template="ggplot2",
        xaxis=dict(
            tickformat='%b %d',
            dtick='D1',
            tickangle=-45,
            rangeslider=dict(
                visible=True,
                bgcolor="antiquewhite"
            ),
            range=[df['snapped_at'].min(), df['snapped_at'].max()],
        ),
        hovermode='x unified'
    )

    fig.update_layout(dragmode='zoom',
                      xaxis=dict(fixedrange=False),
                      yaxis=dict(fixedrange=False))

    fig.show(config={'scrollZoom': True})

def main():
    file_path = select_csv_file()
    if file_path:
        create_graph(file_path)
    else:
        print("No file selected")

if __name__ == "__main__":
    main()
