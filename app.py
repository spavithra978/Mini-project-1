import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Earthquake Data Analysis Dashboard",
    layout="wide"
)

# ---------------------------
# Dark Theme CSS
# ---------------------------
st.markdown("""
<style>
html, body {
    background-color: #0E1117;
    color: white;
}
.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Load ENV & DB Connection
# ---------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "earthquake_db")

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ---------------------------
# Title
# ---------------------------
st.title("🌍 Earthquake Data Analysis Dashboard")
st.caption("Select a problem statement (1–30) and run the query")

# ---------------------------
# QUERY DICTIONARY
# ---------------------------
queries = {
    "1. Top 10 strongest earthquakes (mag)": """
        SELECT time, place, mag, depth_km
        FROM earthquakes
        ORDER BY mag DESC
        LIMIT 10;
    """,

    "2. Top 10 deepest earthquakes": """
        SELECT time, place, depth_km, mag
        FROM earthquakes
        ORDER BY depth_km DESC
        LIMIT 10;
    """,

    "3. Shallow earthquakes (<50km) & mag > 7.5": """
        SELECT time, place, mag, depth_km
        FROM earthquakes
        WHERE depth_km < 50 AND mag > 7.5;
    """,

    "4. Average depth per year": """
        SELECT year, ROUND(AVG(depth_km),2) AS avg_depth
        FROM earthquakes
        GROUP BY year
        ORDER BY year;
    """,

    "5. Average magnitude by magType": """
        SELECT magType, ROUND(AVG(mag),2) AS avg_mag
        FROM earthquakes
        GROUP BY magType
        ORDER BY avg_mag DESC;
    """,

    "6. Year with most earthquakes": """
        SELECT year, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY year
        ORDER BY total_events DESC;
    """,

    "7. Month with highest earthquakes": """
        SELECT month, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY month
        ORDER BY total_events DESC;
    """,

    "8. Day of week with most earthquakes": """
        SELECT day_of_week, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY day_of_week
        ORDER BY total_events DESC;
    """,

    "9. Earthquakes per hour": """
        SELECT hour, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY hour
        ORDER BY hour;
    """,

    "10. Most active reporting networks": """
        SELECT net, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY net
        ORDER BY total_events DESC
        LIMIT 10;
    """,

    "11. Tsunami vs Non-Tsunami events": """
        SELECT tsunami, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY tsunami;
    """,

    "12. Reviewed vs Automatic events": """
        SELECT status, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY status;
    """,

    "13. Avg RMS by year": """
        SELECT year, ROUND(AVG(rms),3) AS avg_rms
        FROM earthquakes
        GROUP BY year;
    """,

    "14. Avg GAP by year": """
        SELECT year, ROUND(AVG(gap),2) AS avg_gap
        FROM earthquakes
        GROUP BY year;
    """,

    "15. Events with high station coverage (NST > 50)": """
        SELECT time, place, mag, nst
        FROM earthquakes
        WHERE nst > 50
        ORDER BY nst DESC;
    """,
    
    "16. Count by earthquake type": """
        SELECT type, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY type
        ORDER BY total_events DESC;
    """,

    "17. Count by data types (origin, shakemap, dyfi etc)": """
        SELECT types, COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY types
        ORDER BY total_events DESC;
    """,

    "18. Average RMS and GAP by year": """
        SELECT year,
               ROUND(AVG(rms),3) AS avg_rms,
               ROUND(AVG(gap),2) AS avg_gap
        FROM earthquakes
        GROUP BY year
        ORDER BY year;
    """,

    "19. Tsunami events per year": """
        SELECT year, COUNT(*) AS tsunami_events
        FROM earthquakes
        WHERE tsunami = 1
        GROUP BY year
        ORDER BY year;
    """,

    "20. Earthquakes by alert level": """
        SELECT alert, COUNT(*) AS total_events
        FROM earthquakes
        WHERE alert IS NOT NULL
        GROUP BY alert
        ORDER BY total_events DESC;
    """,

    "21. Top 5 years with highest average magnitude": """
        SELECT year, ROUND(AVG(mag),2) AS avg_magnitude
        FROM earthquakes
        GROUP BY year
        ORDER BY avg_magnitude DESC
        LIMIT 5;
    """,

    "22. Years with both shallow and deep earthquakes": """
        SELECT year
        FROM earthquakes
        GROUP BY year
        HAVING 
            SUM(depth_km < 70) > 0
            AND SUM(depth_km > 300) > 0;
    """,

    "23. Year-over-year earthquake growth": """
        SELECT year,
               COUNT(*) AS total_events
        FROM earthquakes
        GROUP BY year
        ORDER BY year;
    """,

    "24. Most seismically active years (freq + avg mag)": """
        SELECT year,
               COUNT(*) AS total_events,
               ROUND(AVG(mag),2) AS avg_magnitude
        FROM earthquakes
        GROUP BY year
        ORDER BY total_events DESC, avg_magnitude DESC
        LIMIT 5;
    """,

    "25. Avg depth of earthquakes near equator (±5°)": """
        SELECT ROUND(AVG(depth_km),2) AS avg_depth_equatorial
        FROM earthquakes
        WHERE latitude BETWEEN -5 AND 5;
    """,

    "26. Shallow vs deep earthquake ratio by year": """
        SELECT year,
               SUM(depth_km < 70) AS shallow_count,
               SUM(depth_km > 300) AS deep_count
        FROM earthquakes
        GROUP BY year;
    """,

    "27. Avg magnitude: tsunami vs non-tsunami": """
        SELECT tsunami,
               ROUND(AVG(mag),2) AS avg_magnitude
        FROM earthquakes
        GROUP BY tsunami;
    """,

    "28. Events with lowest data reliability (high RMS & GAP)": """
        SELECT time, place, mag, rms, gap
        FROM earthquakes
        ORDER BY rms DESC, gap DESC
        LIMIT 10;
    """,

    "29. Consecutive earthquakes (same year & hour)": """
        SELECT year, hour, COUNT(*) AS events
        FROM earthquakes
        GROUP BY year, hour
        HAVING events > 1
        ORDER BY events DESC;
    """,

    "30. Deep-focus earthquakes (>300 km) by year": """
        SELECT year, COUNT(*) AS deep_events
        FROM earthquakes
        WHERE depth_km > 300
        GROUP BY year
        ORDER BY deep_events DESC;
    """

}

# ---------------------------
# DROPDOWN
# ---------------------------
selected_query = st.selectbox(
    "📌 Choose Task Number",
    list(queries.keys())
)

# ---------------------------
# RUN BUTTON
# ---------------------------
if st.button("▶ Run Query"):
    with st.spinner("Running query..."):
        df = pd.read_sql(queries[selected_query], engine)

    st.success("Query executed successfully!")
    st.subheader(f"Results for: {selected_query}")
    st.dataframe(df, use_container_width=True)

