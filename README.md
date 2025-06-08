# 📊 Build Real-time Google Play Store Data Analytics - Python

A Python-powered real-time analytics dashboard for visualizing and interpreting data from the Google Play Store. This project uses Plotly, pandas, and time-based logic to create insightful and interactive graphs of app metadata, user reviews, sentiment, and other features.

---

## 🧠 Project Overview

This project analyzes app performance and user feedback using two datasets:

- `googleplaystore.csv`  
- `googleplaystore_user_reviews.csv`

It merges app metadata with user review sentiment data to provide insights through three main interactive visualizations, displayed conditionally based on **Indian Standard Time (IST)**.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **IDE:** Visual Studio Code / Jupyter Notebook  


## 📚 Libraries Used

- `pandas`  
- `plotly`  
- `numpy`  
- `datetime`, `pytz`  
- `ipywidgets` (for dashboard button interaction)

---

## 📊 Visualizations

### 1. **Sentiment Distribution by Rating Group**
- **Type:** Stacked Bar Chart (faceted by rating group)
- **Description:** Shows user sentiment (Positive, Neutral, Negative) segmented by app rating group (1–2, 3–4, 4–5 stars)
- **Filters:**
  - Apps with >1,000 reviews
  - Only top 5 categories based on frequency
- **🕒 Visibility:** Always visible

---

### 2. **Category-wise Install Analysis**
- **Type:** Grouped Bar Chart
- **Compares:**
  - Average Rating
  - Total Reviews
  - Average Size (MB)
- **Filters:**
  - Average rating ≤ 4.0
  - App size ≤ 10MB
  - Last updated in **January**
- **🕒 Visibility Time Window:** Only visible between **3 PM and 5 PM IST**

---

### 3. **Bubble Chart – App Size vs Rating**
- **Type:** Bubble Chart
- **X-axis:** App Size (MB)  
- **Y-axis:** Rating  
- **Bubble Size:** Number of Installs
- **Filters:**
  - Rating > 3.5
  - Reviews > 500
  - Subjectivity > 0.5
  - App name does **not** contain letter "S"
  - Categories: `Game`, `Beauty`, `Business`, `Comics`, `Communication`, `Dating`, `Entertainment`, `Event`, `Social`
  - Installs > 50K
- **Special Features:**
  - Translated Categories:
    - `Beauty` → **सुंदरता** (Hindi)
    - `Business` → **வணிகம்** (Tamil)
    - `Dating` → **Verabredung** (German)
  - `Game` category highlighted in pink
- **🕒 Visibility Time Window:** Only visible between **5 PM and 7 PM IST**

---

## **▶️ How to Run:**

1. Ensure Python is installed (3.7+)
Install required libraries:
1. pip install pandas plotly ipywidgets pytz numpy
2. Place all required CSV files in the same directory as the script.
3. Run the notebook in Visual Studio or Jupyter.
4. Click the "📊 Open Dashboard" button to launch the HTML dashboard in your browser.

---- 

## **🕐 Time-Based Logic:**

- Graph	Visible Time (IST)
- Sentiment Chart   --- 	Always
- Category Chart    ---   3 PM to 5 PM
- Bubble Chart	    ---   5 PM to 7 PM

- Charts outside their visibility window will display an appropriate message instead of rendering.

---

## **📌 Notes:**

- Data is cleaned and filtered rigorously (e.g., size units, install formats, NaNs).
- Dynamic rendering is done in Plotly with to_html() and custom layout configurations.
- Includes multilingual labeling for select categories.

---

## **🙋‍♂️ Contact:**

**Monisha M**
- For questions or suggestions, feel free to reach out via GitHub Issues or email:  📧 monishamani2908@gmail.com
- 🌐 GitHub: Monisha3029
