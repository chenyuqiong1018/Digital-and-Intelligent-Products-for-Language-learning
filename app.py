import streamlit as st
import pandas as pd
import os
from PIL import Image

# --- 1. 页面基本设置 ---
st.set_page_config(
    page_title="国际中文教育数智产品检索",
    page_icon="⚓",
    layout="wide"
)

# --- 2. 自定义 CSS 样式 ---
st.markdown("""
    <style>
    /* 标题区域 */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 5px;
    }
    .header-text {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-left: 15px;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 25px;
    }
    /* 导航按钮样式 */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        font-weight: bold;
    }
    /* 结果报数 */
    .result-count {
        color: #666;
        font-size: 0.9rem;
        margin: 10px 0;
        font-style: italic;
    }
    /* 卡片标签 */
    .tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 15px;
        font-size: 0.7rem;
        margin-right: 5px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 数据加载逻辑 ---
file_path = '数智资源汇总整理.xlsx'


@st.cache_data
def load_data(path, sheet_name):
    if not os.path.exists(path): return None
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
        df.columns = df.columns.str.strip()
        return df.fillna('无')
    except:
        return None


# --- 4. 标题与页面切换状态 ---
if 'page_type' not in st.session_state:
    st.session_state.page_type = '网站'

# 顶部标题栏 (Logo + 文字)
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        logo = Image.open('logo.png')  # 请确保文件名正确
        st.image(logo, width=80)
    except:
        st.write("⚓")  # 如果没图，显示锚点图标

with col_title:
    st.markdown('<div class="header-text">国际中文教育数智产品检索平台</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">同济大学国际文化交流学院</div>', unsafe_allow_html=True)

# 导航按钮
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])
with nav_col1:
    if st.button("🌐 网站检索", type="primary" if st.session_state.page_type == '网站' else "secondary"):
        st.session_state.page_type = '网站'
with nav_col2:
    if st.button("📱 APP 检索", type="primary" if st.session_state.page_type == 'app' else "secondary"):
        st.session_state.page_type = 'app'

# --- 5. 业务逻辑分离 ---

if st.session_state.page_type == '网站':
    # --- 网站检索页面 ---
    df = load_data(file_path, '网站工作本')  # 对应第一个Sheet名

    if df is not None:
        # 侧边栏筛选器
        st.sidebar.header("🔍 网站筛选")
        sc = st.sidebar.multiselect("🌍 国家/地区", sorted(df['国家/地区'].unique()))
        st_cat = st.sidebar.multiselect("📚 类别", sorted(df['类别'].unique()))
        sf = st.sidebar.multiselect("💰 是否免费", sorted(df['是否免费'].unique()))
        query = st.sidebar.text_input("📝 搜索名称")

        # 过滤
        f_df = df.copy()
        if sc: f_df = f_df[f_df['国家/地区'].isin(sc)]
        if st_cat: f_df = f_df[f_df['类别'].isin(st_cat)]
        if sf: f_df = f_df[f_df['是否免费'].isin(sf)]
        if query: f_df = f_df[f_df['网站名称'].str.contains(query, case=False)]

        # 展示
        st.markdown(f'<p class="result-count">✨ 网站库：共检索到 <b>{len(f_df)}</b> 条记录</p>', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"#### {row['网站名称']}")
                    st.markdown(
                        f'<span class="tag">📍 {row["国家/地区"]}</span><span class="tag">📁 {row["类别"]}</span><span class="tag">💰 {row["是否免费"]}</span>',
                        unsafe_allow_html=True)
                with c2:
                    st.link_button("访问网站", row['网址'], use_container_width=True)
                with st.expander("查看详情"):
                    st.write(f"**简介：** {row['网站简介']}")
                    st.write(f"**开发者：** {row['开发者']}")
                st.divider()

else:
    # --- APP 检索页面 ---
    df = load_data(file_path, 'app')  # 对应第二个Sheet名

    if df is not None:
        # 侧边栏筛选器 (根据APP表结构定制)
        st.sidebar.header("🔍 APP 筛选")
        # 提取筛选条件
        s_open = st.sidebar.multiselect("✅ 是否可打开", sorted(df['是否可以打开'].unique()))
        s_up = st.sidebar.multiselect("🔄 是否更新", sorted(df['是否仍在更新'].unique()))
        query = st.sidebar.text_input("📝 搜索名称 (中/英)")

        # 过滤逻辑
        f_df = df.copy()
        if s_open: f_df = f_df[f_df['是否可以打开'].isin(s_open)]
        if s_up: f_df = f_df[f_df['是否仍在更新'].isin(s_up)]
        if query:
            f_df = f_df[
                f_df['中文名称'].str.contains(query, case=False) | f_df['英文名称'].str.contains(query, case=False)]

        # 展示
        st.markdown(f'<p class="result-count">✨ APP库：共检索到 <b>{len(f_df)}</b> 条记录</p>', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    # 显示中文名，如果没有则显示英文名
                    display_name = row['中文名称'] if row['中文名称'] != '*' else row['英文名称']
                    st.markdown(f"#### {display_name}")

                    # 状态标签
                    tag_open = "🟢 可打开" if row['是否可以打开'] == "是" else "🔴 无法打开"
                    tag_up = "🔄 持续更新" if "持续更新" in str(row['是否仍在更新']) else "⏹️ 停止更新"
                    st.markdown(f'<span class="tag">{tag_open}</span><span class="tag">{tag_up}</span>',
                                unsafe_allow_html=True)

                with c2:
                    # 如果有网站链接则显示
                    if row['网站'] != '*' and row['网站'] != '无':
                        st.link_button("获取/官网", str(row['网站']), use_container_width=True)
                    else:
                        st.button("暂无链接", disabled=True, use_container_width=True)

                with st.expander("查看详细信息"):
                    st.write(f"**中文全称：** {row['中文名称']}")
                    st.write(f"**英文全称：** {row['英文名称']}")
                    st.write(f"**研发单位：** {row['研发单位']}")
                st.divider()

# --- 6. 页脚 ---
st.markdown(
    "<center style='color: #bbb; font-size: 0.8rem; margin-top: 50px;'>© 2024 同济大学国际文化交流学院 · 国际中文教育数智化项目组</center>",
    unsafe_allow_html=True)