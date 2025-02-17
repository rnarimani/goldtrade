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
        # Main metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                "USD/IRR",
                f"{prices['usd']:,} Tomans",
                delta=None,
                help="Current USD to Iranian Rial exchange rate"
            )
        
        with metric_col2:
            st.metric(
                "18k Gold",
                f"{prices['gold_per_gram']:,} Tomans/g",
                delta=f"{prices['gold_price_difference']:+.1f}%",
                help="Price per gram of 18k gold and its difference from global price"
            )
        
        with metric_col3:
            st.metric(
                "Global Gold",
                f"${prices['global_gold']:,.2f}/oz",
                delta=None,
                help="Global gold price per ounce"
            )
        
        st.markdown("---")  # خط جداکننده
        
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
            st.subheader("Investment Recommendations")
            if analysis.get('recommendations'):
                # تبدیل توصیه‌ها به دیتافریم
                rec_data = []
                for rec in analysis['recommendations']:
                    # تعیین نوع توصیه و آیکون
                    if "Good options" in rec:
                        rec_type = "✅ Strong Buy"
                        background = "background-color: #c6efce"
                    elif "high trading volume" in rec:
                        rec_type = "📈 High Liquidity"
                        background = "background-color: #bdd7ee"
                    elif "Caution" in rec:
                        rec_type = "⚠️ Warning"
                        background = "background-color: #ffc7ce"
                    elif "Note" in rec:
                        rec_type = "ℹ️ Info"
                        background = "background-color: #fff2cc"
                    else:
                        rec_type = "💡 Other"
                        background = "background-color: #f2f2f2"
                    
                    # جدا کردن نماد و پیام
                    symbols, message = rec.split(" have ", 1)
                    
                    rec_data.append({
                        'Signal': rec_type,
                        'Symbols': symbols,
                        'Details': f"have {message}",
                        'style': background
                    })
                
                # تبدیل به دیتافریم
                df = pd.DataFrame(rec_data)
                
                # ایجاد استایلر
                def make_pretty(styler):
                    styler.set_properties(**{
                        'padding': '10px',
                        'border-radius': '5px',
                        'margin-bottom': '10px'
                    })
                    for idx, row in df.iterrows():
                        styler.set_properties(**{
                            'background-color': row['style'].split(': ')[1]
                        }, subset=pd.IndexSlice[idx, :])
                    return styler
                
                # نمایش دیتافریم با استایل
                styled_df = df.drop('style', axis=1).style.pipe(make_pretty)
                st.dataframe(styled_df, use_container_width=True, height=200)
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

        # Non-ETF Instruments Comparison
        st.subheader("Coins and Digital Gold Comparison")
        
        # تعریف رنگ‌ها
        colors = {
            'Coin': '#d62728',    # قرمز
            'Digital': '#2ca02c'   # سبز
        }
        
        # جمع‌آوری داده‌های سکه و ارزهای دیجیتال
        other_instruments = []
        
        if prices:
            # سکه بهار آزادی
            if 'full_coin' in prices:
                local_bubble, global_bubble = cpc.calculate_bubble(
                    coin_price=prices['full_coin'],
                    coin_weight=8.133,
                    gold_gram_price=prices['gold_per_gram'],
                    global_gold_price=prices['global_gold'],
                    usd_price=prices['usd']
                )
                other_instruments.append({
                    'name': 'Full Coin',
                    'price': prices['full_coin'],
                    'local_bubble': local_bubble,
                    'global_bubble': global_bubble,
                    'type': 'Coin'
                })
            
            # نیم سکه
            if 'half_coin' in prices:
                local_bubble, global_bubble = cpc.calculate_bubble(
                    coin_price=prices['half_coin'],
                    coin_weight=4.068,
                    gold_gram_price=prices['gold_per_gram'],
                    global_gold_price=prices['global_gold'],
                    usd_price=prices['usd']
                )
                other_instruments.append({
                    'name': 'Half Coin',
                    'price': prices['half_coin'],
                    'local_bubble': local_bubble,
                    'global_bubble': global_bubble,
                    'type': 'Coin'
                })
            
            # ربع سکه
            if 'quarter_coin' in prices:
                local_bubble, global_bubble = cpc.calculate_bubble(
                    coin_price=prices['quarter_coin'],
                    coin_weight=2.034,
                    gold_gram_price=prices['gold_per_gram'],
                    global_gold_price=prices['global_gold'],
                    usd_price=prices['usd']
                )
                other_instruments.append({
                    'name': 'Quarter Coin',
                    'price': prices['quarter_coin'],
                    'local_bubble': local_bubble,
                    'global_bubble': global_bubble,
                    'type': 'Coin'
                })
            
            # پکس گلد و تتر گلد نسبت به قیمت جهانی
            if 'paxg' in prices and prices['paxg'] > 0:
                bubble = ((prices['paxg'] - prices['global_gold']) / prices['global_gold']) * 100
                other_instruments.append({
                    'name': 'PAXG',
                    'price': prices['paxg'] * prices['usd'],
                    'local_bubble': round(bubble, 1),
                    'global_bubble': round(bubble, 1),
                    'type': 'Digital'
                })
            
            if 'xaut' in prices and prices['xaut'] > 0:
                bubble = ((prices['xaut'] - prices['global_gold']) / prices['global_gold']) * 100
                other_instruments.append({
                    'name': 'XAUT',
                    'price': prices['xaut'] * prices['usd'],
                    'local_bubble': round(bubble, 1),
                    'global_bubble': round(bubble, 1),
                    'type': 'Digital'
                })
        
        # رسم دو نمودار میله‌ای جداگانه
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[item['name'] for item in other_instruments],
                y=[item['local_bubble'] for item in other_instruments],
                text=[f"{item['local_bubble']:+.1f}%" for item in other_instruments],
                textposition='auto',
                marker_color=[colors[item['type']] for item in other_instruments],
                name='Local Bubble'
            ))
            
            fig.update_layout(
                title="Bubble vs Local Gold Price",
                xaxis_title="Instrument",
                yaxis_title="Bubble (%)",
                height=400,
                showlegend=False,
                bargap=0.3,
                yaxis=dict(
                    tickformat='+.1f',
                    ticksuffix='%'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[item['name'] for item in other_instruments],
                y=[item['global_bubble'] for item in other_instruments],
                text=[f"{item['global_bubble']:+.1f}%" for item in other_instruments],
                textposition='auto',
                marker_color=[colors[item['type']] for item in other_instruments],
                name='Global Bubble'
            ))
            
            fig.update_layout(
                title="Bubble vs Global Gold Price",
                xaxis_title="Instrument",
                yaxis_title="Bubble (%)",
                height=400,
                showlegend=False,
                bargap=0.3,
                yaxis=dict(
                    tickformat='+.1f',
                    ticksuffix='%'
                )
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