import streamlit as st
import pandas as pd
import os

# --- 1. 页面基本设置 ---
st.set_page_config(
    page_title="国际中文教育数智产品检索",
    page_icon="🌐",
    layout="wide"
)

# --- 2. 自定义 CSS 样式 ---
st.markdown("""
    <style>
    /* 标题栏渐变背景 */
    .stHeader {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    /* 卡片容器样式 */
    .resource-card {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #e1e4e8;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    /* 标签样式 */
    .tag-container {
        margin: 0.5rem 0;
    }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 5px;
    }
    .tag-country { background-color: #e3f2fd; color: #1976d2; border: 1px solid #bbdefb; }
    .tag-category { background-color: #f1f8e9; color: #388e3c; border: 1px solid #dcedc8; }
    .tag-price { background-color: #fff3e0; color: #f57c00; border: 1px solid #ffe0b2; }

    /* 报数小字样式 */
    .result-count {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 数据加载逻辑 ---
file_path = '数智资源汇总整理.xlsx'


@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_excel(path)
        # 清洗列名空格
        df.columns = df.columns.str.strip()
        # 填充空值为“无”
        df = df.fillna('无')
        return df
    except Exception as e:
        st.error(f"读取文件失败: {e}")
        return None


df_raw = load_data(file_path)

if df_raw is None:
    st.error(f"❌ 找不到文件：`{file_path}`，请确保文件已上传。")
    st.stop()

# --- 4. 侧边栏：检索过滤区 ---
st.sidebar.header("🔍 筛选条件")

# 提取各列去重后的列表
countries = sorted(df_raw['国家/地区'].unique().tolist())
categories = sorted(df_raw['类别'].unique().tolist())
free_options = sorted(df_raw['是否免费'].unique().tolist())

# 创建多选框
selected_countries = st.sidebar.multiselect("🌍 选择国家/地区", countries)
selected_categories = st.sidebar.multiselect("📚 选择类别", categories)
selected_free = st.sidebar.multiselect("💰 收费模式", free_options)

# 搜索框
search_name = st.sidebar.text_input("📝 搜索产品名称")

# --- 5. 核心过滤逻辑 ---
filtered_df = df_raw.copy()

if selected_countries:
    filtered_df = filtered_df[filtered_df['国家/地区'].isin(selected_countries)]
if selected_categories:
    filtered_df = filtered_df[filtered_df['类别'].isin(selected_categories)]
if selected_free:
    filtered_df = filtered_df[filtered_df['是否免费'].isin(selected_free)]
if search_name:
    filtered_df = filtered_df[filtered_df['网站名称'].str.contains(search_name, case=False)]

# --- 6. 主页面渲染 ---

# 标题
st.markdown("""
    <div class="stHeader">
        <h1 style='color: white; border-bottom: none;'>🌐 国际中文教育数智产品检索平台</h1>
        <p style='opacity: 0.9;'>智能化检索 · 数字化赋能 · 模块化资源展示</p>
    </div>
    """, unsafe_allow_html=True)

# 报数功能 (小字显示)
st.markdown(f'<p class="result-count">✨ 检索结果：系统共为您找到 <b>{len(filtered_df)}</b> 条符合条件的记录</p>',
            unsafe_allow_html=True)

if filtered_df.empty:
    st.info("💡 未找到匹配项，请尝试减少筛选条件或搜索其他关键词。")
else:
    # 循环展示卡片
    for _, row in filtered_df.iterrows():
        # 图标映射逻辑
        status_valid = "✅ 有效" if row['是否有效'] == "是" else "❌ 失效"
        update_icon = "🔄 持续更新" if "持续更新" in str(row['是否更新']) else "⏹️ 停止更新"

        # 使用 Streamlit Container 模拟卡片
        with st.container():
            col_info, col_btn = st.columns([4, 1])

            with col_info:
                # 标题
                st.markdown(f"#### {row['网站名称']}")

                # 动态标签组 (国家、类别、收费)
                st.markdown(f"""
                    <div class="tag-container">
                        <span class="tag tag-country">📍 {row['国家/地区']}</span>
                        <span class="tag tag-category">📁 {row['类别']}</span>
                        <span class="tag tag-price">💳 {row['是否免费']}</span>
                    </div>
                """, unsafe_allow_html=True)

                # 状态小字
                st.markdown(f"<small style='color: #888;'>状态：{status_valid} | 更新：{update_icon}</small>",
                            unsafe_allow_html=True)

            with col_btn:
                # 居中显示的跳转按钮
                st.write("")  # 占位
                st.link_button("🔗 访问网站", row['网址'], use_container_width=True)

            # 可折叠详情
            with st.expander("🔍 查看详细介绍及开发信息"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**【产品简介】**")
                    st.write(row['网站简介'])
                with c2:
                    st.write("**【开发者/所属机构】**")
                    st.write(row['开发者'])

            st.markdown("<hr style='margin: 0.5rem 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)

# --- 7. 页脚 ---
st.markdown("""
    <br><br>
    <center style='color: #999; font-size: 0.8rem;'>
        © 2024 国际中文教育数智产品检索项目组 · 资源持续完善中
    </center>
""", unsafe_allow_html=True)