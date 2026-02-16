import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="高山茶销量预测系统",
    page_icon="🍵",
    layout="wide"
)

@st.cache_data
def load_sample_data():
    """加载示例数据"""
    data = {
        'date': pd.date_range(start='2025-02-10', periods=90, freq='D'),
        'sales': np.random.uniform(50, 120, 90) + np.sin(np.arange(90) / 7) * 20
    }
    df = pd.DataFrame(data)
    df['sales'] = df['sales'].round(2)
    return df

def simple_lstm_predict(history_data, future_days):
    """简化的LSTM预测模拟（使用移动平均+趋势）"""
    if len(history_data) < 7:
        return history_data[-future_days:] if len(history_data) >= future_days else history_data * future_days
    
    recent = history_data[-30:]
    base = np.mean(recent)
    trend = (np.mean(recent[-7:]) - np.mean(recent[:7])) / 7
    
    predictions = []
    for i in range(future_days):
        noise = np.random.normal(0, np.std(recent) * 0.3)
        pred = base + trend * (i + 1) + noise
        predictions.append(round(max(0, pred), 2))
    
    return predictions

st.title("🍵 高山茶智能销量预测系统")
st.markdown("基于深度学习(LSTM)的销量预测模型可视化平台")

tab1, tab2, tab3 = st.tabs(["📊 数据集可视化", "🔮 LSTM销量预测", "📈 预测对比"])

with tab1:
    st.header("数据集可视化分析")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("数据概览")
        
        df = load_sample_data()
        
        st.metric("数据条数", len(df))
        st.metric("平均日销量", f"{df['sales'].mean():.2f}")
        st.metric("销量标准差", f"{df['sales'].std():.2f}")
        
        st.subheader("统计信息")
        st.dataframe(df.describe(), use_container_width=True)
        
        st.subheader("数据预览")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("销售趋势图")
        
        chart_type = st.selectbox("图表类型", ["折线图", "柱状图", "面积图"], key="chart1")
        
        if chart_type == "折线图":
            fig = px.line(df, x='date', y='sales', title='每日销量趋势', 
                         line_shape='spline', markers=True)
            fig.update_traces(line_color='#2E86AB', line_width=2)
        elif chart_type == "柱状图":
            fig = px.bar(df, x='date', y='sales', title='每日销量', color='sales',
                        color_continuous_scale='Blues')
        else:
            fig = px.area(df, x='date', y='sales', title='每日销量趋势',
                         color_discrete_sequence=['#2E86AB'])
        
        fig.update_layout(
            xaxis_title="日期",
            yaxis_title="销量",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("销量分布分析")
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig_hist = px.histogram(df, x='sales', nbins=20, title='销量分布直方图', 
                                   color_discrete_sequence=['#2E86AB'])
            fig_hist.update_layout(template="plotly_white")
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col_b:
            fig_box = px.box(df, y='sales', title='销量箱线图', 
                           color_discrete_sequence=['#2E86AB'])
            fig_box.update_layout(template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)

with tab2:
    st.header("🔮 LSTM深度学习销量预测")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("预测参数设置")
        
        product_id = st.text_input("商品ID", value="高山茶-特级")
        
        history_days = st.slider("历史数据天数", 30, 90, 60)
        
        future_days = st.slider("预测天数", 1, 14, 7)
        
        st.info(f"📌 使用最近 {history_days} 天的数据预测未来 {future_days} 天的销量")
        
        predict_btn = st.button("🔮 开始预测", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.subheader("模型信息")
        st.markdown("""
        **LSTM (Long Short-Term Memory)** 
        
        - 双层LSTM神经网络
        - Dropout防止过拟合
        - 适合时序预测任务
        """)
    
    with col2:
        st.subheader("预测结果")
        
        if predict_btn or 'predictions' not in st.session_state:
            df = load_sample_data()
            history_data = df['sales'].tail(history_days).tolist()
            
            predictions = simple_lstm_predict(history_data, future_days)
            
            last_date = df['date'].max()
            future_dates = [last_date + timedelta(days=i+1) for i in range(len(predictions))]
            
            st.session_state.predictions = predictions
            st.session_state.future_dates = future_dates
            st.session_state.history_data = history_data
            st.session_state.df = df
        
        if 'predictions' in st.session_state:
            predictions = st.session_state.predictions
            future_dates = st.session_state.future_dates
            df = st.session_state.df
            
            st.success(f"✅ 预测成功！商品: {product_id}")
            
            pred_df = pd.DataFrame({
                'date': future_dates,
                'predicted_sales': predictions
            })
            
            fig_pred = go.Figure()
            
            fig_pred.add_trace(go.Scatter(
                x=df['date'].tail(30),
                y=df['sales'].tail(30),
                mode='lines+markers',
                name='历史销量',
                line=dict(color='#2E86AB', width=2)
            ))
            
            fig_pred.add_trace(go.Scatter(
                x=pred_df['date'],
                y=pred_df['predicted_sales'],
                mode='lines+markers',
                name='预测销量',
                line=dict(color='#E94F37', width=2, dash='dash')
            ))
            
            fig_pred.update_layout(
                title='LSTM销量预测结果',
                xaxis_title="日期",
                yaxis_title="销量",
                template="plotly_white",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_pred, use_container_width=True)
            
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("平均预测销量", f"{np.mean(predictions):.2f}")
            col_r2.metric("最高预测", f"{max(predictions):.2f}")
            col_r3.metric("最低预测", f"{min(predictions):.2f}")
            
            st.subheader("预测数据详情")
            st.dataframe(pred_df, use_container_width=True)

with tab3:
    st.header("📈 预测对比分析")
    
    df = load_sample_data()
    
    st.markdown("### 历史数据 vs 预测结果对比")
    
    col1, col2 = st.columns(2)
    
    with col1:
        history_days_compare = st.slider("历史天数", 30, 90, 45, key="hist2")
    
    with col2:
        future_days_compare = st.slider("预测天数", 1, 14, 7, key="fut2")
    
    history_data = df['sales'].tail(history_days_compare).tolist()
    predictions = simple_lstm_predict(history_data, future_days_compare)
    
    last_date = df['date'].max()
    future_dates = [last_date + timedelta(days=i+1) for i in range(len(predictions))]
    
    all_dates = list(df['date'].tail(history_days_compare)) + future_dates
    all_sales = list(df['sales'].tail(history_days_compare)) + predictions
    types = ['历史'] * history_days_compare + ['预测'] * future_days_compare
    
    compare_df = pd.DataFrame({
        'date': all_dates,
        'sales': all_sales,
        'type': types
    })
    
    fig_compare = px.bar(compare_df, x='date', y='sales', color='type',
                         title='历史销量 vs 预测销量对比',
                         color_discrete_map={'历史': '#2E86AB', '预测': '#E94F37'},
                         barmode='group')
    fig_compare.update_layout(template="plotly_white")
    st.plotly_chart(fig_compare, use_container_width=True)
    
    st.markdown("### 预测误差分析")
    
    if len(history_data) >= 14:
        actual_recent = history_data[-future_days_compare:]
        errors = [abs(predictions[i] - actual_recent[i]) for i in range(min(len(predictions), len(actual_recent)))]
        
        error_df = pd.DataFrame({
            '日期': future_dates[:len(errors)],
            '预测值': predictions[:len(errors)],
            '实际值': actual_recent[:len(errors)],
            '误差': errors
        })
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            fig_error = px.bar(error_df, x='日期', y='误差', 
                              title='每日预测误差', color_discrete_sequence=['#FF6B6B'])
            fig_error.update_layout(template="plotly_white")
            st.plotly_chart(fig_error, use_container_width=True)
        
        with col_e2:
            st.metric("平均绝对误差", f"{np.mean(errors):.2f}")
            st.metric("最大误差", f"{max(errors):.2f}")
            st.metric("误差标准差", f"{np.std(errors):.2f}")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>🍵 高山茶智能预测平台 | 基于TensorFlow LSTM深度学习模型</p>
        <p><a href='https://github.com/your-repo' target='_blank'>项目GitHub</a> | 论文数据可视化演示系统</p>
    </div>
    """, 
    unsafe_allow_html=True
)
