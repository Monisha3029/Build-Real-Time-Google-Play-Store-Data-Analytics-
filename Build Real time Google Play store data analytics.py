


import pandas as pd

# Load datasets
apps_df = pd.read_csv(r"c:\Users\HP\Downloads\googleplaystore.csv (1)\googleplaystore.csv")
reviews_df = pd.read_csv(r"c:\Users\HP\Downloads\googleplaystore_user_reviews.csv~\googleplaystore_user_reviews.csv")
reviews_df = reviews_df.dropna(subset=["App", "Sentiment", "Sentiment_Polarity", "Sentiment_Subjectivity"])
sentiment_summary = reviews_df.groupby("App").agg({
    "Sentiment_Polarity": "mean",
    "Sentiment_Subjectivity": "mean",
    "Sentiment": lambda x: x.mode()[0]
}).reset_index()
# Merge
merged_df = pd.merge(apps_df, sentiment_summary, on="App", how="left")
# Save merged data 
merged_df.to_csv(r"c:\Users\HP\Downloads\googleplaystore_with_sentiment.csv", index=False)

import plotly
print(plotly.__version__)

import plotly.io as pio
pio.renderers.default = "notebook"  

import pandas as pd
import plotly.express as px
import itertools
# Clean and filter
df = merged_df.copy()
df = df[df["Reviews"].str.isnumeric()]
df["Reviews"] = df["Reviews"].astype(int)
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df = df[df["Reviews"] > 1000]
df = df.dropna(subset=["Rating", "Sentiment"])

# Create rating group
def get_rating_group(rating):
    if rating <= 2:
        return "1-2"
    elif rating <= 4:
        return "3-4"
    else:
        return "4-5"

df["Rating_Group"] = df["Rating"].apply(get_rating_group)

# Top 5 categories
top_categories = df["Category"].value_counts().nlargest(5).index
df = df[df["Category"].isin(top_categories)]

all_combos = pd.MultiIndex.from_product(
    [top_categories, ["1-2", "3-4", "4-5"], ["Positive", "Neutral", "Negative"]],
    names=["Category", "Rating_Group", "Sentiment"]
)

# Group data
grouped = df.groupby(["Category", "Rating_Group", "Sentiment"]).size().reindex(all_combos, fill_value=0).reset_index(name="Count")

# Plotting
fig1 = px.bar(
    grouped,
    x="Category",
    y="Count",
    color="Sentiment",
    barmode="stack",
    facet_col="Rating_Group",
    category_orders={
        "Rating_Group": ["1-2", "3-4", "4-5"],
        "Sentiment": ["Positive", "Neutral", "Negative"]
    },
    color_discrete_map={
        "Positive": "#3D7317",
        "Neutral": "#C7C7C7",
        "Negative": "#FF0000"
    },
    title="Sentiment Distribution by Rating Group (Top 5 Categories)",
    labels={"Count": "Review Count"}
)

fig1.update_layout(
    height=600,
    showlegend=True,
    title_x=0.15,
    bargap=0.15,
    margin=dict(l=30, r=30, t=60, b=60)
)

fig1.show()


import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time
import pytz

# Load dataset
df = pd.read_csv(r"c:\Users\HP\Downloads\googleplaystore_with_sentiment.csv")

# Clean and convert 'Installs'
df = df[df['Installs'].str.contains(r'^\d+[+,]?$', regex=True, na=False)]
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(int)

# Convert Reviews and Rating
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(int)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df = df.dropna(subset=['Rating'])

# Convert Size to MB
def convert_size(size):
    if isinstance(size, str):
        size = size.strip()
        if size.endswith('M'):
            return float(size[:-1])
        elif size.endswith(('k', 'K')):
            return float(size[:-1]) / 1024
        elif size.endswith('G'):
            return float(size[:-1]) * 1024
    return None

df['Size_MB'] = df['Size'].apply(convert_size)
df = df.dropna(subset=['Size_MB'])

# Filter by "Last Updated" in January
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
df = df.dropna(subset=['Last Updated'])
df = df[df['Last Updated'].dt.month == 1]

# Apply Rating and Size filters
df_filtered = df[(df['Rating'] <= 4.0) & (df['Size_MB'] <= 10)]

# Get top 10 categories by Installs
top_10_categories = df_filtered.groupby('Category')['Installs'].sum().nlargest(10).index
df_top10 = df_filtered[df_filtered['Category'].isin(top_10_categories)]

# Aggregate data
agg = df_top10.groupby('Category').agg(
    avg_rating=('Rating', 'mean'),
    total_reviews=('Reviews', 'sum'),
    avg_size_mb=('Size_MB', 'mean')  
).reset_index()

# show only from 3 PM to 5 PM IST
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist).time()
current_time_str = now_ist.strftime("%H:%M:%S")

fig2 = None
if time(15, 0) <= now_ist <= time(17, 0):
    fig2 = go.Figure(data=[
        go.Bar(name='Average Rating', x=agg['Category'], y=agg['avg_rating'], marker_color='#9AD8D8'),
        go.Bar(name='Total Reviews', x=agg['Category'], y=agg['total_reviews'], marker_color='#37A3A3'),
        go.Bar(name='Average Size (MB)', x=agg['Category'], y=agg['avg_size_mb'], marker_color='#147878'),
        
    ])

    fig2.update_layout(
        barmode='group',
        title='Categories by Installs (Rating ≤ 4.0, Size ≤ 10MB, Last Updated - Jan)',
        xaxis_title='Category',
        yaxis_title='Value',
        xaxis_tickangle=-45,
        template='plotly_white',
        height=600
    )

    fig2.show()
else:
    print(f"Graph will only display between 3 PM to 5 PM IST. Current time: {current_time_str}")

import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, time
import pytz

allowed_categories = ['Game', 'Beauty', 'Business', 'Comics', 'Communication',
                      'Dating', 'Entertainment', 'Event', 'Social']

category_translations = {
    'Beauty': 'सुंदरता',        
    'Business': 'வணிகம்',       
    'Dating': 'Verabredung'     
}

def size_to_mb(size_str):
    if isinstance(size_str, str):
        size_str = size_str.strip().upper()
        if 'M' in size_str:
            return float(size_str.replace('M', ''))
        elif 'K' in size_str:
            return float(size_str.replace('K', '')) / 1024
    return np.nan

def is_ist_time_between(start_hour, end_hour):
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist).time()
    start_time = time(start_hour, 0)
    end_time = time(end_hour, 0)
    if start_time <= end_time:
        return start_time <= now_ist <= end_time
    else:
        return now_ist >= start_time or now_ist <= end_time

def plot_bubble_chart(df):
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    current_time_str = now_ist.strftime("%H:%M:%S")

    if not is_ist_time_between(17, 19):
        print(f"Graph will only display between 5 PM to 7 PM IST. Current time: {current_time_str}")
        return None  

    df = df.copy()
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Installs'] = df['Installs'].astype(str).str.replace(r'[+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Sentiment_Subjectivity'] = pd.to_numeric(df['Sentiment_Subjectivity'], errors='coerce')
    df['Size_MB'] = df['Size'].apply(size_to_mb)
    df['Category'] = df['Category'].str.strip().str.title()

    df = df[
        (df['Rating'] > 3.5) &
        (df['Reviews'] > 500) &
        (df['Sentiment_Subjectivity'] > 0.5) &
        (df['Installs'] > 50000) &
        (~df['App'].str.contains('S', case=False, na=False)) &
        (df['Category'].isin(allowed_categories)) &
        (~df['Size_MB'].isna())
    ].copy()

    if df.empty:
        print("No data after applying all filters.")
        return None

    df['Category_Display'] = df['Category'].apply(lambda x: category_translations.get(x, x))

    color_discrete_map = {
        category_translations.get('Game', 'Game'): 'pink'
    }
    for cat in df['Category'].unique():
        if cat != 'Game':
            display_cat = category_translations.get(cat, cat)
            color_discrete_map[display_cat] = 'skyblue'

    fig3 = px.scatter(
        df,
        x='Size_MB',
        y='Rating',
        size='Installs',
        color='Category_Display',
        color_discrete_map=color_discrete_map,
        hover_name='App',
        size_max=70,
        title='App Size vs Rating (Bubble Size = Installs)',
        labels={'Size_MB': 'App Size (MB)', 'Rating': 'Average Rating'}
    )

    fig3.update_layout(showlegend=True)
    return fig3



fig3 = plot_bubble_chart(merged_df) 
if fig3 is not None:
    fig3.show()

import os
import ipywidgets as widgets
import webbrowser

# Convert figures to HTML snippets
html_fig1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

html_fig2 = ""
if fig2 is not None:
    html_fig2 = fig2.to_html(full_html=False, include_plotlyjs=False)
else:
    html_fig2 = f"<p><strong>Graph will only display between 3 PM to 5 PM IST. Current time: {current_time_str}</strong></p>"

html_fig3 = ""
if fig3 is not None:
    html_fig3 = fig3.to_html(full_html=False, include_plotlyjs=False)
else:
    html_fig3 = f"<p><strong>Graph will only display between 5 PM to 7 PM IST. Current time: {current_time_str}</strong></p>"

dashboard_html = f"""
<html>
<head>
    <title>Google Play Store Dashboard</title>
    <meta charset="utf-8">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Google Play Store Dashboard</h1>
    
    <h2>1. Sentiment Distribution by Rating Group (Top 5 Categories)</h2>
    {html_fig1}
    
    <h2>2. Categories by Installs (Rating ≤ 4.0, Size ≤ 10MB, Last Updated - Jan)</h2>
    {html_fig2}
    
    <h2>3. App Size vs Rating (Bubble Size = Installs)</h2>
    {html_fig3}
    
</body>
</html>
"""

# Write the dashboard HTML file
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

# Function to open dashboard in browser
def open_dashboard(btn):
    dashboard_path = os.path.abspath("dashboard.html")
    webbrowser.open(f"file://{dashboard_path}")

# Create and display button in notebook
button = widgets.Button(description="📊 Open Dashboard", button_style='success')
button.on_click(open_dashboard)
display(button)
