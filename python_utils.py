"""
Python utilities for cardiac arrest data analysis
Equivalent functions to the R code used in the blog posts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import folium
from datetime import datetime
import sqlalchemy as sa

def custom_summary(series):
    """
    Custom summary function equivalent to the R version
    Returns comprehensive statistics for a numeric series
    """
    return {
        'minimum': round(series.min(), 2),
        'mean': round(series.mean(), 2),
        'median': round(series.median(), 2),
        'q1': round(series.quantile(0.25), 2),
        'q3': round(series.quantile(0.75), 2),
        'p90th': round(series.quantile(0.90), 2),
        'maximum': round(series.max(), 2),
        'std_dev': round(series.std(), 2),
        'variance': round(series.var(), 2),
        'skewness': round(stats.skew(series.dropna()), 2),
        'kurtosis': round(stats.kurtosis(series.dropna()), 2)
    }

def extract_datetime_features(df, date_column):
    """
    Extract datetime features equivalent to the R lubridate functions
    """
    df = df.copy()
    dt_series = pd.to_datetime(df[date_column])
    
    df['day_of_week'] = dt_series.dt.day_name()
    df['week_number'] = dt_series.dt.isocalendar().week
    df['year_number'] = dt_series.dt.year
    df['hour_of_day'] = dt_series.dt.hour
    df['day_of_week_abbr'] = dt_series.dt.strftime('%a').str.upper()
    
    return df

def create_response_time_plots(df, time_column, title_prefix="Response Time"):
    """
    Create histogram, box plot, and QQ plot for response times
    Equivalent to the R ggplot2 visualizations
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Histogram with density
    axes[0, 0].hist(df[time_column].dropna(), bins=20, density=True, 
                    alpha=0.7, color='lightblue', edgecolor='black')
    axes[0, 0].set_title(f'{title_prefix} - Histogram')
    axes[0, 0].set_xlabel('Time (seconds)')
    axes[0, 0].set_ylabel('Density')
    
    # Box plot by day of week
    if 'day_of_week_abbr' in df.columns:
        df_clean = df.dropna(subset=[time_column, 'day_of_week_abbr'])
        day_order = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        sns.boxplot(data=df_clean, x='day_of_week_abbr', y=time_column, 
                   order=day_order, ax=axes[0, 1])
        axes[0, 1].set_title(f'{title_prefix} by Day of Week')
        axes[0, 1].tick_params(axis='x', rotation=45)
    
    # QQ plot
    stats.probplot(df[time_column].dropna(), dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title(f'{title_prefix} - QQ Plot')
    
    # Density plot
    df[time_column].dropna().plot.density(ax=axes[1, 1], color='steelblue')
    axes[1, 1].set_title(f'{title_prefix} - Density Plot')
    axes[1, 1].set_xlabel('Time (seconds)')
    
    plt.tight_layout()
    return fig

def create_call_frequency_chart(df, day_column='day_of_week_abbr'):
    """
    Create bar chart showing call frequency by day of week
    """
    day_order = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    day_counts = df[day_column].value_counts().reindex(day_order)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(day_counts.index, day_counts.values, 
                   color=plt.cm.viridis(np.linspace(0, 1, len(day_counts))))
    
    # Add count labels on bars
    for bar, count in zip(bars, day_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(int(count)), ha='center', va='bottom')
    
    plt.title('Count of Calls per Day of the Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Calls')
    plt.grid(True, alpha=0.3)
    return plt.gcf()

def create_geographic_map(df, lat_col='latitude', lon_col='longitude', 
                         center_lat=38.8048, center_lon=-77.0469):
    """
    Create an interactive map showing call locations
    Equivalent to the R leaflet functionality
    """
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='CartoDB positron'
    )
    
    # Add markers for each call
    for idx, row in df.iterrows():
        if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
            # Convert coordinates if they're in integer format (like the R example)
            lat = row[lat_col] / 1000000 if row[lat_col] > 180 else row[lat_col]
            lon = -abs(row[lon_col] / 1000000) if abs(row[lon_col]) > 180 else row[lon_col]
            
            popup_text = f"""
            <b>Call ID:</b> {row.get('call_id', 'N/A')}<br>
            <b>Date:</b> {row.get('response_date', 'N/A')}<br>
            <b>Address:</b> {row.get('address', 'N/A')}<br>
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=popup_text,
                color='#1c5789',
                fill=True,
                fillOpacity=0.7
            ).add_to(m)
    
    return m

def load_sql_data(connection_string, query):
    """
    Load data from SQL database
    Equivalent to the SQL queries shown in the R examples
    """
    engine = sa.create_engine(connection_string)
    df = pd.read_sql(query, engine)
    return df

# Example SQL queries as strings (equivalent to the R examples)
CARDIAC_ARREST_CURRENT_YEAR = """
USE Reporting_System;

DECLARE @time1 DATETIME2;
SET @time1 = '2025-01-01 00:00:00.0000000';

SELECT Master_Incident_Number AS call_id,
    Response_Date AS start_time,
    CAST(DATEPART(WEEK, Response_Date) AS NVARCHAR(2)) AS week_no,
    UPPER(FORMAT(Response_Date, 'ddd')) AS day_of_week,
    CAST(DATEPART(Hour, Response_Date) AS NVARCHAR(2)) AS hour,
    Address AS address,
    Latitude AS latitude,
    Longitude AS longitude,
    Time_PhonePickUp AS phone_start,
    Time_FirstCallTakingKeystroke AS keyboard_start,
    Time_CallEnteredQueue AS dispatchable,
    Time_First_Unit_Assigned AS dispatched,
    Time_CallTakingComplete AS phone_stop,
    DATEDIFF(SECOND, Response_Date, Time_CallEnteredQueue) AS call_entry_time,
    DATEDIFF(SECOND, Time_CallEnteredQueue, Time_First_Unit_Assigned) AS call_queue_time,
    DATEDIFF(SECOND, Response_Date, Time_CallTakingComplete) AS call_processing_time
FROM Response_Master_Incident
WHERE Response_Date > @time1
    AND Problem LIKE 'CARDIAC ARREST%'
    AND Master_Incident_Number != ''
ORDER BY Response_Date;
"""
