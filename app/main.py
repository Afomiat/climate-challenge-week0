import streamlit as st
from utils import load_data, filter_data, plot_interactive_line, plot_interactive_box, calculate_vulnerability

# 1. Page Configuration
st.set_page_config(
    page_title="COP32 Climate Intelligence",
    page_icon="🌍",
    layout="wide"
)

# 2. Premium UI Styling (CSS Injection)
st.markdown("""
    <style>
    .main {
        background-color: #0F172A;
    }
    .stMetric {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        color: #E63946;
        font-weight: 700;
    }
    .stSidebar {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Branding & Navigation
st.sidebar.markdown("# 🛡️ COP32 Portal")
st.sidebar.caption("v1.0.2 | Intelligence & Strategy")
st.sidebar.divider()

# --- SIDEBAR ZONE 1: FILTERING ---
st.sidebar.subheader("🔍 Data Filtering")
countries_list = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]
selected_countries = st.sidebar.multiselect(
    "Target Nations",
    options=countries_list,
    default=countries_list
)

variables = {
    "T2M": "Avg Temp (°C)",
    "T2M_MAX": "Max Temp (°C)",
    "PRECTOTCORR": "Rainfall (mm/day)",
    "RH2M": "Humidity (%)",
    "WS2M": "Wind (m/s)"
}
selected_var = st.sidebar.selectbox(
    "Analysis Metric",
    options=list(variables.keys()),
    format_func=lambda x: variables[x]
)

year_range = st.sidebar.slider(
    "Observation Window",
    min_value=2015,
    max_value=2026,
    value=(2015, 2026)
)

st.sidebar.divider()

# 4. Header Section (Main Panel)
st.title("🛰️ African Climate Intelligence Portal")
st.caption("Strategic Synthesis of NASA POWER Satellite Data for COP32 Policy Briefing")

# 5. Data Processing
if selected_countries:
    df_all = load_data(selected_countries)
    
    if not df_all.empty:
        df_f = filter_data(df_all, year_range)
        
        # --- SIDEBAR ZONE 2: EXPORT CENTER ---
        st.sidebar.subheader("📥 Export Center")
        
        # CSV Export
        csv_data = df_f.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📄 Download Cleaned CSV",
            data=csv_data,
            file_name="climate_intelligence_data.csv",
            mime="text/csv",
            help="Export the currently filtered dataset to CSV."
        )
        
        # Stats Export
        stats_df = df_f.groupby('Country')[selected_var].agg(['mean', 'median', 'std']).round(2)
        stats_csv = stats_df.to_csv().encode('utf-8')
        st.sidebar.download_button(
            label="📊 Download Summary Table",
            data=stats_csv,
            file_name="climate_summary_stats.csv",
            mime="text/csv",
            help="Download the summary statistics table for your current selection."
        )

        # --- Main Panel: Analytics ---
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Nations Analyzed", len(selected_countries))
        with m2:
            st.metric("Daily Records", f"{len(df_f):,}")
        with m3:
            at_risk = calculate_vulnerability(df_f)
            st.metric("Highest Vulnerability", at_risk)
            
        st.markdown("---")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"### 📈 {variables[selected_var]} Historical Trend")
            line_fig = plot_interactive_line(df_f, selected_var, selected_countries)
            if line_fig:
                st.plotly_chart(line_fig, use_container_width=True)
            
        with c2:
            st.markdown(f"### 📊 Distribution & Variance")
            box_fig = plot_interactive_box(df_f, selected_var)
            if box_fig:
                st.plotly_chart(box_fig, use_container_width=True)
                
        st.markdown("---")
        with st.expander("🔍 View Raw Regional Statistics"):
            st.dataframe(stats_df, use_container_width=True)
            
    else:
        st.error("⚠️ Data files not found. Ensure CSVs are in the 'data/' folder.")
else:
    st.sidebar.warning("Select at least one nation to activate Export Center.")
    st.warning("👈 Please select one or more nations in the sidebar to begin analysis.")

# Sidebar Footer
st.sidebar.divider()
st.sidebar.info("Framework developed for 10 Academy | Ethiopia COP32 Delegation")
