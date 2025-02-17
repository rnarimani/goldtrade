import streamlit as st
import coin_price_calculator as cpc
import etf_analyzer as etf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Gold Market Analysis",
    page_icon="🏆",
    layout="wide"
)

# Initialize analyzer
@st.cache_resource
def get_analyzer():
    return etf.GoldETFAnalyzer()

@st.cache_data(ttl=300)
def get_analysis():
    analyzer = get_analyzer()
    return analyzer.get_analysis()

@st.cache_data(ttl=300)
def get_prices():
    return cpc.get_prices()

# Get data
prices = get_prices()
analysis = get_analysis()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Market Prices",
    "ETF Analysis",
    "Charts",
    "About"
])

# Tab 1: Market Prices
with tab1:
    st.header("Gold Market Prices")
    if prices:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Gold Coins")
            coin_data = {k: v for k, v in prices.items() if 'coin' in k.lower()}
            coin_df = pd.DataFrame(coin_data.items(), columns=['Type', 'Price (IRR)'])
            st.dataframe(coin_df, use_container_width=True)
        
        with col2:
            st.subheader("Digital Gold")
            digital_data = {k: v for k, v in prices.items() if 'pax' in k.lower() or 'tether' in k.lower()}
            digital_df = pd.DataFrame(digital_data.items(), columns=['Type', 'Price (IRR)'])
            st.dataframe(digital_df, use_container_width=True)
        
        with col3:
            st.subheader("Raw Gold")
            gold_data = {k: v for k, v in prices.items() if 'gold' in k.lower() and 'coin' not in k.lower()}
            gold_df = pd.DataFrame(gold_data.items(), columns=['Type', 'Price (IRR)'])
            st.dataframe(gold_df, use_container_width=True)
    else:
        st.error("Error getting price data")

# Tab 2: ETF Analysis
with tab2:
    st.header("Gold ETF Analysis")
    if analysis and analysis.get('all_funds'):
        # ETF data table
        funds_data = []
        for symbol, data in analysis['all_funds'].items():
            funds_data.append({
                'Symbol': symbol,
                'Name': data['name'],
                'Price (IRR)': f"{data['price']:,.0f}",
                'NAV (IRR)': f"{data['gold_value']:,.0f}",
                'Bubble (%)': f"{data['bubble']:.1f}",
                'Volume': f"{data['volume']:,}"
            })
        
        df = pd.DataFrame(funds_data)
        st.dataframe(df, use_container_width=True)
        
        # Best options and recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Best Options")
            if analysis.get('lowest_bubble') and analysis.get('highest_volume'):
                lowest_bubble = analysis['lowest_bubble']
                highest_volume = analysis['highest_volume']
                
                st.metric(
                    "Lowest Bubble",
                    f"{lowest_bubble[0]}",
                    f"{lowest_bubble[1]['bubble']:.1f}%"
                )
                st.metric(
                    "Highest Volume",
                    f"{highest_volume[0]}",
                    f"{highest_volume[1]['volume']:,}"
                )
        
        with col2:
            st.subheader("Recommendations")
            if analysis.get('recommendations'):
                for rec in analysis['recommendations']:
                    st.info(rec)
    else:
        st.error("Error getting ETF data")

# Tab 3: Charts
with tab3:
    st.header("Market Analysis Charts")
    if analysis and analysis.get('all_funds'):
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Bar chart
            fig = go.Figure()
            for symbol, data in analysis['all_funds'].items():
                fig.add_trace(go.Bar(
                    name=symbol,
                    x=['Bubble', 'Volume'],
                    y=[data['bubble'], data['volume']],
                    text=[f"{data['bubble']:.1f}%", f"{data['volume']:,}"],
                    textposition='auto',
                ))
            
            fig.update_layout(
                title="ETF Comparison",
                barmode='group',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Bubble chart
            fig = go.Figure()
            volumes = [data['volume'] for data in analysis['all_funds'].values()]
            max_volume = max(volumes) if volumes else 1
            sizes = []  # لیست سایزها
            
            for symbol, data in analysis['all_funds'].items():
                size = (data['volume'] / max_volume) * 100
                sizes.append(size)  # اضافه کردن به لیست
                
                fig.add_trace(go.Scatter(
                    x=[data['price']],
                    y=[data['bubble']],
                    mode='markers+text',
                    name=symbol,
                    text=[symbol],
                    textposition="top center",
                    marker=dict(
                        size=size,
                        sizemode='area',
                        sizeref=2.*max(sizes)/(40.**2),  # استفاده از لیست sizes
                        sizemin=4
                    )
                ))
            
            fig.update_layout(
                title="Bubble vs Price (size = volume)",
                xaxis_title="Price (IRR)",
                yaxis_title="Bubble (%)",
                height=500,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Error getting ETF data")

# Tab 4: About
with tab4:
    st.header("About This Dashboard")
    st.markdown("""
    ### Gold Market Analysis Dashboard
    
    This dashboard provides real-time analysis of the Iranian gold market, including:
    
    1. **Market Prices**
       - Gold coins
       - Digital gold tokens
       - Raw gold
       
    2. **ETF Analysis**
       - Price and NAV comparison
       - Trading volume
       - Bubble percentage
       
    3. **Charts**
       - Comparative analysis
       - Bubble visualization
       
    Data is updated every 5 minutes.
    
    ### Data Sources
    - Gold prices: tgju.org
    - ETF data: tradersarena.ir
    """)

# Sidebar
st.sidebar.title("Gold Market Analysis")
st.sidebar.write(f"Last update: {datetime.now().strftime('%H:%M:%S')}") 