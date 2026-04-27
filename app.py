import streamlit as st
import pandas as pd
import os

# --- 1. 页面基本设置 ---
st.set_page_config(
    page_title="国际中文教育数智产品检索",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 自定义 CSS 样式 ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stHeader {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .resource-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        background-color: #e2e8f0;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 数据加载 ---
file_path = '数智资源汇总整理.xlsx'


@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        return None
    df = pd.read_excel(path)
    # 清洗数据：去除空格，填充空值
    df.columns = df.columns.str.strip()
    df = df.fillna('无')
    return df


df_raw = load_data(file_path)

if df_raw is None:
    st.error(f"❌ 找不到文件：`{file_path}`。请确保 Excel 文件已上传至 GitHub 仓库根目录。")
    st.stop()

# --- 4. 标题栏设计 ---
st.markdown("""
    <div class="stHeader">
        <h1>🌐 国际中文教育数智产品检索平台</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">探索全球优质教学资源 · 数智赋能国际中文教育</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. 侧边栏：检索过滤 ---
st.sidebar.header("🔍 筛选条件")
search_query = st.sidebar.text_input("📝 搜索名称或关键字")

countries = sorted(df_raw['国家/地区'].unique().tolist())
categories = sorted(df_raw['类别'].unique().tolist())
free_options = sorted(df_raw['是否免费'].unique().tolist())

selected_countries = st.sidebar.multiselect("🌍 国家/地区", countries)
selected_categories = st.sidebar.multiselect("📚 资源类别", categories)
selected_free = st.sidebar.multiselect("💰 是否免费", free_options)

# 过滤逻辑
filtered_df = df_raw.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['网站名称'].str.contains(search_query, case=False) |
                              filtered_df['网站简介'].str.contains(search_query, case=False)]
if selected_countries:
    filtered_df = filtered_df[filtered_df['国家/地区'].isin(selected_countries)]
if selected_categories:
    filtered_df = filtered_df[filtered_df['类别'].isin(selected_categories)]
if selected_free:
    filtered_df = filtered_df[filtered_df['是否免费'].isin(selected_free)]

# --- 6. 主内容展示 ---
st.subheader(f"📊 检索结果 (共 {len(filtered_df)} 项)")

if filtered_df.empty:
    st.warning("没有找到符合条件的资源，请尝试调整筛选条件。")
else:
    # 遍历数据，以卡片形式展示
    for index, row in filtered_df.iterrows():
        # 处理状态图标
        # 是否有效
        status_valid = "🟢 有效" if row['是否有效'] == "是" else "🔴 链接失效"
        # 是否更新
        if "持续更新" in str(row['是否更新']):
            status_update = "🔄 持续更新中"
            update_color = "green"
        else:
            status_update = "⏹️ 停止更新"
            update_color = "grey"

        # 开始渲染卡片
        with st.container():
            # 使用 HTML 构建卡片的外壳（部分使用 markdown 嵌套）
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {row['网站名称']}")
                # 标签行
                st.markdown(f"""
                    <span class="tag">🌍 {row['国家/地区']}</span>
                    <span class="tag">📂 {row['类别']}</span>
                    <span class="tag">💰 {row['是否免费']}</span>
                    """, unsafe_allow_html=True)

            with col2:
                # 状态和跳转按钮
                st.write(f"**状态:** {status_valid}")
                st.write(f"**更新:** {status_update}")
                st.link_button("🔗 立即访问", row['网址'], use_container_width=True)

            # 折叠详情区
            with st.expander("📝 查看详情"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**网站简介：**")
                    st.write(row['网站简介'])
                with c2:
                    st.write("**开发者/所属机构：**")
                    st.write(row['开发者'])

            st.divider()  # 分割线

# --- 7. 页脚 ---
st.markdown("---")
st.markdown(
    "<center style='color: #666;'>© 2024 国际中文教育数智产品检索项目 · Data Updated: 2024.11</center>",
    unsafe_allow_html=True
)