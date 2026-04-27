import streamlit as st
import pandas as pd
import os

# 1. 页面基本设置
st.set_page_config(page_title="国际中文教育数智产品检索", layout="wide")
st.title("🌐 国际中文教育数智产品检索平台")
st.markdown("欢迎使用！请在左侧选择过滤条件，快速找到适合的教学资源。")

# 2. 配置文件路径
# ⚠️ 注意：请务必把下面的 "你的表格名字.xlsx" 替换成你真实的 Excel 文件名！
file_path = '数智资源汇总整理.xlsx'

# 检查文件到底存不存在
if not os.path.exists(file_path):
    st.error(f"❌ 找不到文件！请检查路径：`{file_path}`")
    st.info("💡 提示：请回代码第 13 行，确保你把 '你的表格名字.xlsx' 改成了真实的 Excel 名字。")
    st.stop()  # 如果找不到，就在这里停止，不往下运行了


# 3. 加载Excel数据
@st.cache_data
def load_data(path):
    # 读取Excel文件
    df = pd.read_excel(path)
    # 把表格里所有的空缺值替换成 "无"
    df = df.fillna('无')
    return df


try:
    df = load_data(file_path)
except Exception as e:
    st.error(f"❌ 读取表格时出错了：{e}")
    st.info("💡 提示：请确保你已经安装了 openpyxl（可以在黑框框里输入 pip install openpyxl 回车）")
    st.stop()

# 4. 侧边栏：检索过滤区
st.sidebar.header("🔍 筛选条件")

# 获取所有不重复的选项 (确保列名和你的Excel完全一致)
try:
    countries = df['国家/地区'].unique().tolist()
    categories = df['类别'].unique().tolist()
    free_options = df['是否免费'].unique().tolist()
except KeyError as e:
    st.error(f"❌ 找不到这一列：{e}")
    st.info("💡 提示：请检查你的Excel表头，是不是刚好叫 '国家/地区'、'类别'、'是否免费'，如果有空格要去掉。")
    st.stop()

# 在侧边栏创建下拉多选框
selected_countries = st.sidebar.multiselect("🌍 选择国家/地区", countries)
selected_categories = st.sidebar.multiselect("📚 选择类别", categories)
selected_free = st.sidebar.multiselect("💰 是否免费", free_options)

# 5. 核心逻辑：根据用户的选择过滤数据
filtered_df = df.copy()

if selected_countries:
    filtered_df = filtered_df[filtered_df['国家/地区'].isin(selected_countries)]

if selected_categories:
    filtered_df = filtered_df[filtered_df['类别'].isin(selected_categories)]

if selected_free:
    filtered_df = filtered_df[filtered_df['是否免费'].isin(selected_free)]

# 6. 主页面：展示结果
st.subheader(f"共找到 {len(filtered_df)} 个符合条件的资源：")

# 直接展示漂亮的表格
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)