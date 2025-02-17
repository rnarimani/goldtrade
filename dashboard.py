import streamlit as st
import coin_price_calculator as cpc
import etf_analyzer as etf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# تنظیمات صفحه
st.set_page_config(
    page_title="تحلیل بازار طلا و سکه",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ایجاد تب‌ها
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "قیمت سکه و طلا", 
    "تحلیل صندوق‌های طلا",
    "مقایسه صندوق‌ها",
    "نمودار حباب",
    "راهنما"
])

# تب اول: قیمت سکه و طلا
with tab1:
    st.header("قیمت‌های بازار طلا و سکه")
    prices = cpc.get_prices()
    if prices:
        # نمایش قیمت‌ها در جدول
        df = pd.DataFrame(prices.items(), columns=['نوع', 'قیمت (تومان)'])
        st.dataframe(df, use_container_width=True)
    else:
        st.error("خطا در دریافت قیمت‌ها")

# تب دوم: تحلیل صندوق‌های طلا
with tab2:
    st.header("تحلیل صندوق‌های طلا")
    analyzer = etf.GoldETFAnalyzer()
    analysis = analyzer.get_analysis()
    
    if analysis and analysis['all_funds']:
        # جدول اطلاعات صندوق‌ها
        funds_data = []
        for symbol, data in analysis['all_funds'].items():
            funds_data.append({
                'نماد': symbol,
                'نام صندوق': data['name'],
                'قیمت (تومان)': f"{data['price']/10:,.0f}",
                'NAV (تومان)': f"{data['gold_value']/10:,.0f}",
                'حباب (%)': f"{data['bubble']:.1f}",
                'حجم معاملات': f"{data['volume']:,}"
            })
        
        df = pd.DataFrame(funds_data)
        st.dataframe(df, use_container_width=True)
        
        # نمایش توصیه‌ها
        if analysis['recommendations']:
            st.subheader("توصیه‌های سرمایه‌گذاری")
            for rec in analysis['recommendations']:
                st.info(rec)
        
        # نمایش بهترین گزینه‌ها
        st.subheader("بهترین گزینه‌ها")
        lowest_bubble = analysis['lowest_bubble']
        highest_volume = analysis['highest_volume']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "کمترین حباب",
                f"{lowest_bubble[0]}",
                f"{lowest_bubble[1]['bubble']:.1f}%"
            )
        with col2:
            st.metric(
                "بیشترین حجم معامله",
                f"{highest_volume[0]}",
                f"{highest_volume[1]['volume']:,} واحد"
            )
    else:
        st.error("خطا در دریافت اطلاعات صندوق‌ها")

# تب سوم: مقایسه صندوق‌ها
with tab3:
    st.header("مقایسه صندوق‌های طلا")
    if analysis and analysis['all_funds']:
        # ایجاد نمودار مقایسه‌ای
        fig = go.Figure()
        
        for symbol, data in analysis['all_funds'].items():
            fig.add_trace(go.Bar(
                name=symbol,
                x=['حباب', 'حجم معاملات'],
                y=[data['bubble'], data['volume']],
                text=[f"{data['bubble']:.1f}%", f"{data['volume']:,}"],
                textposition='auto',
            ))
        
        fig.update_layout(
            title="مقایسه حباب و حجم معاملات صندوق‌ها",
            barmode='group',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("خطا در دریافت اطلاعات صندوق‌ها")

# تب چهارم: نمودار حباب
with tab4:
    st.header("نمودار حباب صندوق‌های طلا")
    if analysis and analysis['all_funds']:
        # ایجاد نمودار حباب
        fig = go.Figure()
        
        volumes = [data['volume'] for data in analysis['all_funds'].values()]
        max_volume = max(volumes)
        
        for symbol, data in analysis['all_funds'].items():
            size = (data['volume'] / max_volume) * 100  # نرمال‌سازی اندازه حباب‌ها
            
            fig.add_trace(go.Scatter(
                x=[data['price']/10],  # تبدیل به تومان
                y=[data['bubble']],
                mode='markers+text',
                name=symbol,
                text=[symbol],
                textposition="top center",
                marker=dict(
                    size=size,
                    sizemode='area',
                    sizeref=2.*max(size)/(40.**2),
                    sizemin=4
                )
            ))
        
        fig.update_layout(
            title="نمودار حباب صندوق‌های طلا",
            xaxis_title="قیمت (تومان)",
            yaxis_title="درصد حباب",
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("خطا در دریافت اطلاعات صندوق‌ها")

# تب پنجم: راهنما
with tab5:
    st.header("راهنمای استفاده")
    st.markdown("""
    ### نحوه استفاده از داشبورد
    
    1. **تب قیمت سکه و طلا**
       - مشاهده آخرین قیمت‌های بازار طلا و سکه
       
    2. **تب تحلیل صندوق‌های طلا**
       - مشاهده اطلاعات کامل همه صندوق‌ها
       - مشاهده توصیه‌های سرمایه‌گذاری
       - مشاهده بهترین گزینه‌ها
       
    3. **تب مقایسه صندوق‌ها**
       - مقایسه حباب و حجم معاملات صندوق‌ها
       - نمودار میله‌ای مقایسه‌ای
       
    4. **تب نمودار حباب**
       - نمایش رابطه قیمت، حباب و حجم معاملات
       - اندازه هر حباب نشان‌دهنده حجم معاملات است
    
    ### نکات مهم
    - داده‌ها هر 5 دقیقه به‌روزرسانی می‌شوند
    - حباب منفی نشان‌دهنده ارزندگی صندوق است
    - حجم معاملات بالاتر نشان‌دهنده نقدشوندگی بهتر است
    """)

# نمایش زمان به‌روزرسانی
st.sidebar.write(f"آخرین به‌روزرسانی: {datetime.now().strftime('%H:%M:%S')}") 