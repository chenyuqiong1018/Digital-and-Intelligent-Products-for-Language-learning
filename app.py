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

# --- 2. 恢复上一版的自定义 CSS 样式 (保持美观) ---
st.markdown("""
    <style>
    /* 标题栏渐变背景 */
    .stHeader {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    /* 标签样式 (恢复彩色版本) */
    .tag-container { margin: 0.5rem 0; }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 5px;
    }
    .tag-blue { background-color: #e3f2fd; color: #1976d2; border: 1px solid #bbdefb; }
    .tag-green { background-color: #f1f8e9; color: #388e3c; border: 1px solid #dcedc8; }
    .tag-orange { background-color: #fff3e0; color: #f57c00; border: 1px solid #ffe0b2; }

    /* 报数小字 */
    .result-count {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    /* 隐藏顶部默认装饰 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
        return df.fillna('无').replace('*', '无')  # 将星号统一转为“无”
    except:
        return None


# --- 4. 标题栏 (Logo + 渐变标题 + 学院名) ---
t_col1, t_col2, t_col3 = st.columns([1, 4, 1])
with t_col2:
    # 顶部 Logo 和 标题并排
    head_col1, head_col2 = st.columns([1, 5])
    with head_col1:
        try:
            logo = Image.open('logo.png')
            st.image(logo, width=90)
        except:
            st.write("🌐")
    with head_col2:
        st.markdown(
            '<div class="stHeader"><h1 style="color:white; margin:0; border:none;">国际中文教育数智产品检索平台</h1></div>',
            unsafe_allow_html=True)

    st.markdown('<div class="sub-header">同济大学国际文化交流学院</div>', unsafe_allow_html=True)

# --- 5. 导航切换 (网站 vs APP) ---
# 使用 st.tabs 或者 按钮来实现美观的切换
tab_web, tab_app = st.tabs(["🌐 网站检索 (Website Search)", "📱 APP 检索 (APP Search)"])

# --- 6. 逻辑分支：网站检索 ---
with tab_web:
    df_web = load_data(file_path, '网站工作本')
    if df_web is not None:
        # 侧边栏筛选
        with st.sidebar:
            st.header("🔍 网站筛选")
            sc = st.multiselect("🌍 国家/地区", sorted(df_web['国家/地区'].unique()), key="web_country")
            st_cat = st.multiselect("📚 类别", sorted(df_web['类别'].unique()), key="web_cat")
            sf = st.multiselect("💰 是否免费", sorted(df_web['是否免费'].unique()), key="web_free")
            q_web = st.text_input("📝 搜索网站名称", key="search_web")

        # 过滤
        f_web = df_web.copy()
        if sc: f_web = f_web[f_web['国家/地区'].isin(sc)]
        if st_cat: f_web = f_web[f_web['类别'].isin(st_cat)]
        if sf: f_web = f_web[f_web['是否免费'].isin(sf)]
        if q_web: f_web = f_web[f_web['网站名称'].str.contains(q_web, case=False)]

        # 报数
        st.markdown(f'<p class="result-count">✨ 网站库：共检索到 <b>{len(f_web)}</b> 条符合条件的记录</p>',
                    unsafe_allow_html=True)

        # 循环渲染卡片
        for idx, row in f_web.iterrows():
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"#### {row['网站名称']}")
                    st.markdown(f"""
                        <div class="tag-container">
                            <span class="tag tag-blue">📍 {row['国家/地区']}</span>
                            <span class="tag tag-green">📁 {row['类别']}</span>
                            <span class="tag tag-orange">💳 {row['是否免费']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(
                        f"<small style='color: #888;'>状态：{'✅ 有效' if row['是否有效'] == '是' else '❌ 失效'} | 更新：{row['是否更新']}</small>",
                        unsafe_allow_html=True)
                with c2:
                    st.write("")  # 间距
                    st.link_button("🔗 访问网站", str(row['网址']), use_container_width=True, key=f"web_link_{idx}")
                with st.expander("🔍 查看详细介绍"):
                    st.write(f"**【简介】** {row['网站简介']}")
                    st.write(f"**【开发者】** {row['开发者']}")
                st.markdown("<hr style='margin:10px 0; border:0.5px solid #eee;'>", unsafe_allow_html=True)

# --- 7. 逻辑分支：APP 检索 ---
with tab_app:
    df_app = load_data(file_path, 'app')
    if df_app is not None:
        with st.sidebar:
            st.header("🔍 APP 筛选")
            s_open = st.multiselect("✅ 是否可打开", sorted(df_app['是否可以打开'].unique()), key="app_open")
            s_up = st.multiselect("🔄 是否仍在更新", sorted(df_app['是否仍在更新'].unique()), key="app_up")
            q_app = st.text_input("📝 搜索名称 (中/英)", key="search_app")

        # 过滤
        f_app = df_app.copy()
        if s_open: f_app = f_app[f_app['是否可以打开'].isin(s_open)]
        if s_up: f_app = f_app[f_app['是否仍在更新'].isin(s_up)]
        if q_app:
            f_app = f_app[
                f_app['中文名称'].str.contains(q_app, case=False) | f_app['英文名称'].str.contains(q_app, case=False)]

        st.markdown(f'<p class="result-count">✨ APP库：共检索到 <b>{len(f_app)}</b> 条符合条件的记录</p>',
                    unsafe_allow_html=True)

        for idx, row in f_app.iterrows():
            # 确定显示名称 (有中文显示中文，没中文显示英文)
            name = row['中文名称'] if row['中文名称'] != "无" else row['英文名称']

            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"#### {name}")
                    st.markdown(f"""
                        <div class="tag-container">
                            <span class="tag tag-blue">状态：{row['是否可以打开']}</span>
                            <span class="tag tag-green">更新：{row['是否仍在更新']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.write("")  # 间距
                    if row['网站'] != "无":
                        st.link_button("🔗 立即获取", str(row['网站']), use_container_width=True, key=f"app_link_{idx}")
                    else:
                        # 修复 Duplicate ID 报错的关键点：增加 key=f"disabled_{idx}"
                        st.button("🚫 暂无链接", disabled=True, use_container_width=True, key=f"disabled_btn_{idx}")

                with st.expander("🔍 查看详细数据"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**中文全称：** {row['中文名称']}")
                        st.write(f"**英文全称：** {row['英文名称']}")
                    with col_b:
                        st.write(f"**研发单位：** {row['研发单位']}")
                st.markdown("<hr style='margin:10px 0; border:0.5px solid #eee;'>", unsafe_allow_html=True)

# --- 8. 页脚 ---
st.markdown(
    "<br><center style='color: #999; font-size: 0.8rem;'>© 2024 同济大学国际文化交流学院 · 国际中文教育数智化项目组</center>",
    unsafe_allow_html=True)