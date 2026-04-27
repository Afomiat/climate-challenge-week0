import streamlit as st
from utils import load_data, filter_data, plot_line_chart, plot_boxplot, get_summary_stats

# 1. Page Configuration
st.set_page_config(
    page_title="African Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

# 2. Title & Intro
st.title("🌍 African Climate Challenge Dashboard")
st.markdown("""
This interactive dashboard analyzes climate trends across five African nations (2015–2026).
Use the sidebar to filter data and explore specific climate variables.
""")

# 3. Sidebar Widgets
st.sidebar.header("🕹️ Controls")

# Country Multi-select
countries_list = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=countries_list,
    default=countries_list
)

# Variable Selectbox
variables = {
    "T2M": "Avg Temperature (°C)",
    "T2M_MAX": "Max Temperature (°C)",
    "PRECTOTCORR": "Precipitation (mm/day)",
    "RH2M": "Relative Humidity (%)",
    "WS2M": "Wind Speed (m/s)"
}
selected_var = st.sidebar.selectbox(
    "Select Climate Variable",
    options=list(variables.keys()),
    format_func=lambda x: variables[x]
)

# Year Range Slider
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=2015,
    max_value=2026,
    value=(2015, 2026)
)

# 4. Data Processing
if selected_countries:
    df_all = load_data(selected_countries)
    
    if not df_all.empty:
        df_filtered = filter_data(df_all, year_range)
        
        # 5. Dashboard Layout (Columns)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"📈 {variables[selected_var]} Trend")
            line_fig = plot_line_chart(df_filtered, selected_var, selected_countries)
            st.pyplot(line_fig)
            
        with col2:
            st.subheader(f"📊 {variables[selected_var]} Distribution")
            box_fig = plot_boxplot(df_filtered, selected_var)
            st.pyplot(box_fig)
            
        # 6. Summary Stats Section
        st.divider()
        st.subheader("📋 Statistical Summary")
        stats_table = get_summary_stats(df_filtered, selected_var)
        st.dataframe(stats_table, use_container_width=True)
        
        # 7. Insights (Dynamic)
        st.info(f"**Insights:** Currently viewing {variables[selected_var]} for "
                f"{', '.join(selected_countries)} between {year_range[0]} and {year_range[1]}.")
    else:
        st.warning("No data found for the selected countries. Please check the data/ folder.")
else:
    st.info("Please select at least one country in the sidebar to begin.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Data Source: NASA POWER | Developed for COP32 Reporting")
