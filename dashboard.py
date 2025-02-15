import streamlit as st
import coin_price_calculator as cpc
import plotly.graph_objects as go
import time
import pandas as pd

st.set_page_config(page_title="Gold Market Dashboard", layout="wide")

def create_gauge(value, title, min_val, max_val, color):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, (max_val-min_val)/3], 'color': "lightgray"},
                {'range': [(max_val-min_val)/3, (max_val-min_val)*2/3], 'color': "gray"}
            ]
        }
    ))
    return fig

def main():
    st.title("🏆 Gold Market Dashboard")
    
    # Add refresh button
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
    
    # Get data with caching
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_market_data():
        return cpc.get_prices()
    
    prices = get_market_data()
    
    if prices:
        # Create three columns for main metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Global Gold Price",
                f"${prices['global_gold']:,.2f}",
                "per ounce"
            )
            
        with col2:
            st.metric(
                "USD/IRR",
                f"{prices['usd']:,}",
                "Tomans"
            )
            
        with col3:
            st.metric(
                "18k Gold",
                f"{prices['gold_per_gram']:,}",
                "Tomans/gram"
            )
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Market Overview", "Coin Analysis", "Investment Recommendations"])
        
        with tab1:
            # Create gauges for price differences
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_gauge(
                    prices['gold_price_difference'],
                    "Gold Price Premium/Discount (%)",
                    -20, 20,
                    "gold"
                ), use_container_width=True)
                
            with col2:
                # Create comparison chart for digital gold
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['PAXG', 'XAUT'],
                    y=[prices['paxg'], prices['xaut']],
                    name='Price'
                ))
                fig.update_layout(title="Digital Gold Comparison")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Create bubble chart for coins
            bubbles_df = pd.DataFrame({
                'Coin': ['Full Coin', 'Half Coin', 'Quarter Coin'],
                'Price': [prices['full_coin'], prices['half_coin'], prices['quarter_coin']],
                'Bubble': [prices['bubbles']['full_coin'], 
                          prices['bubbles']['half_coin'],
                          prices['bubbles']['quarter_coin']]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=bubbles_df['Coin'],
                y=bubbles_df['Bubble'],
                name='Bubble %'
            ))
            fig.update_layout(title="Coin Bubbles Comparison")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show coin prices in a table
            st.dataframe(bubbles_df)
        
        with tab3:
            # Show investment recommendations
            st.subheader("Market Analysis")
            st.info(f"Timing: {prices['advice']}")
            st.success(f"Best Choice: {prices['best_investment']}")
            
            # Create a table of all investment options
            options_df = pd.DataFrame(prices['investment_options'])
            st.dataframe(options_df.sort_values('premium', key=abs))

if __name__ == "__main__":
    main() 