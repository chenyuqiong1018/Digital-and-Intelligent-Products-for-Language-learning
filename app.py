import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image

# --- 1. 页面基本设置 ---
st.set_page_config(
    page_title="国际中文教育数智产品检索",
    page_icon="⚓",
    layout="wide"
)


# --- 2. 图片转 Base64 (用于嵌入蓝色框) ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


try:
    logo_base64 = get_base64_of_bin_file('logo.png')
except:
    logo_base64 = ""

# --- 3. 增强版自定义 CSS ---
st.markdown(f"""
    <style>
    /* 1. 蓝色大标题框布局 */
    .header-box {{
        background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); /* 保持上一版的经典深蓝渐变 */
        padding: 40px 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-bottom: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .header-logo {{
        width: 100px;
        margin-bottom: 20px;
        filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.2));
    }}
    .header-title {{
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    .header-subtitle {{
        font-size: 1.1rem;
        margin-top: 15px;
        opacity: 0.9;
        font-weight: 400;
        letter-spacing: 1px;
    }}

    /* 2. 导航栏居中并平分宽度 */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 0px !important;
        width: 100% !important;
    }}
    div[data-baseweb="tab"] {{
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
        font-size: 1.1rem !important;
        height: 50px !important;
    }}

    /* 3. 恢复上一版的卡片标签样式 */
    .tag-container {{ margin: 0.8rem 0; }}
    .tag {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 5px;
    }}
    .tag-blue {{ background-color: #e3f2fd; color: #1976d2; border: 1px solid #bbdefb; }}
    .tag-green {{ background-color: #f1f8e9; color: #388e3c; border: 1px solid #dcedc8; }}
    .tag-orange {{ background-color: #fff3e0; color: #f57c00; border: 1px solid #ffe0b2; }}

    .result-count {{
        color: #666;
        font-size: 0.95rem;
        margin: 20px 0;
        font-style: italic;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 渲染蓝色标题框 ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="header-logo">' if logo_base64 else ''
st.markdown(f"""
    <div class="header-box">
        {logo_html}
        <div class="header-title">国际中文教育数智产品检索平台</div>
        <div class="header-subtitle">同济大学国际文化交流学院</div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. 数据加载逻辑 ---
file_path = '数智资源汇总整理.xlsx'


@st.cache_data
def load_data(path, sheet_name):
    if not os.path.exists(path): return None
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
        df.columns = df.columns.str.strip()
        return df.fillna('无').replace('*', '无')
    except:
        return None


# --- 6. 导航切换 (Tabs 居中平分模式) ---
tab_web, tab_app = st.tabs(["🌐 网站检索 (Website Search)", "📱 APP 检索 (APP Search)"])

# --- 7. 网站检索逻辑 ---
with tab_web:
    df_web = load_data(file_path, '网站工作本')
    if df_web is not None:
        with st.sidebar:
            st.header("🔍 网站筛选")
            sc = st.multiselect("🌍 国家/地区", sorted(df_web['国家/地区'].unique()), key="w_c")
            st_cat = st.multiselect("📚 类别", sorted(df_web['类别'].unique()), key="w_cat")
            sf = st.multiselect("💰 是否免费", sorted(df_web['是否免费'].unique()), key="w_f")
            q_web = st.text_input("📝 搜索名称", key="s_w")

        f_web = df_web.copy()
        if sc: f_web = f_web[f_web['国家/地区'].isin(sc)]
        if st_cat: f_web = f_web[f_web['类别'].isin(st_cat)]
        if sf: f_web = f_web[f_web['是否免费'].isin(sf)]
        if q_web: f_web = f_web[f_web['网站名称'].str.contains(q_web, case=False)]

        st.markdown(f'<p class="result-count">✨ 网站库：为您检索到 <b>{len(f_web)}</b> 条资源</p>',
                    unsafe_allow_html=True)

        for idx, row in f_web.iterrows():
            with st.container():
                c1, c2 = st.columns([4, 1.2])
                with c1:
                    st.markdown(f"### {row['网站名称']}")
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
                    st.write("")
                    st.link_button("🔗 访问网站", str(row['网址']), use_container_width=True, key=f"wb_{idx}")
                with st.expander("🔍 详细介绍"):
                    st.write(f"**【简介】** {row['网站简介']}")
                    st.write(f"**【开发者】** {row['开发者']}")
                st.divider()

# --- 8. APP 检索逻辑 ---
with tab_app:
    df_app = load_data(file_path, 'app')
    if df_app is not None:
        with st.sidebar:
            st.header("🔍 APP 筛选")
            s_open = st.multiselect("✅ 是否可打开", sorted(df_app['是否可以打开'].unique()), key="a_o")
            s_up = st.multiselect("🔄 更新状态", sorted(df_app['是否仍在更新'].unique()), key="a_u")
            q_app = st.text_input("📝 搜索名称 (中/英)", key="s_a")

        f_app = df_app.copy()
        if s_open: f_app = f_app[f_app['是否可以打开'].isin(s_open)]
        if s_up: f_app = f_app[f_app['是否仍在更新'].isin(s_up)]
        if q_app:
            f_app = f_app[
                f_app['中文名称'].str.contains(q_app, case=False) | f_app['英文名称'].str.contains(q_app, case=False)]

        st.markdown(f'<p class="result-count">✨ APP库：为您检索到 <b>{len(f_app)}</b> 条资源</p>',
                    unsafe_allow_html=True)

        for idx, row in f_app.iterrows():
            name = row['中文名称'] if row['中文名称'] != "无" else row['英文名称']
            with st.container():
                c1, c2 = st.columns([4, 1.2])
                with c1:
                    st.markdown(f"### {name}")
                    st.markdown(f"""
                        <div class="tag-container">
                            <span class="tag tag-blue">状态：{row['是否可以打开']}</span>
                            <span class="tag tag-green">更新：{row['是否仍在更新']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.write("")
                    if row['网站'] != "无":
                        st.link_button("🔗 获取/官网", str(row['网站']), use_container_width=True, key=f"al_{idx}")
                    else:
                        st.button("🚫 暂无链接", disabled=True, use_container_width=True, key=f"ad_{idx}")

                with st.expander("🔍 详细数据"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**中文全称：** {row['中文名称']}")
                        st.write(f"**英文全称：** {row['英文名称']}")
                    with col_b:
                        st.write(f"**研发单位：** {row['研发单位']}")
                st.divider()

# --- 9. 页脚 ---
st.markdown(
    "<br><center style='color: #999; font-size: 0.8rem;'>© 2024 同济大学国际文化交流学院 · 国际中文教育数智化项目组</center>",
    unsafe_allow_html=True)