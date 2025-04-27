import streamlit as st
import json
import os

# -----------------  配置 -----------------
DATA_FOLDER = './data'
V0_SUFFIX = 'V0_batch_result_data.json'
V2_SUFFIX = 'V2_batch_result_data.json'

# -----------------  工具函数 -----------------
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_v0_v2_files(folder_path):
    v0_file = None
    v2_file = None
    for file in os.listdir(folder_path):
        if file.endswith(V0_SUFFIX):
            v0_file = os.path.join(folder_path, file)
        elif file.endswith(V2_SUFFIX):
            v2_file = os.path.join(folder_path, file)
    return v0_file, v2_file

# -----------------  Streamlit UI -----------------
st.set_page_config(page_title="V0 vs V2 Result Comparison", layout="wide")
st.title('V0 vs V2 Result Comparison')

# 选择子文件夹
subfolders = [f.name for f in os.scandir(DATA_FOLDER) if f.is_dir()]
selected_folder = st.sidebar.selectbox('Select a folder:', subfolders)

# 🔥 在这里加一个小块初始化 session_state
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'last_folder' not in st.session_state or st.session_state.last_folder != selected_folder:
    st.session_state.index = 0
    st.session_state.last_folder = selected_folder

if selected_folder:
    folder_path = os.path.join(DATA_FOLDER, selected_folder)
    v0_file, v2_file = find_v0_v2_files(folder_path)


if selected_folder:
    folder_path = os.path.join(DATA_FOLDER, selected_folder)
    v0_file, v2_file = find_v0_v2_files(folder_path)

    if v0_file and v2_file:
        v0_data = load_json(v0_file)
        v2_data = load_json(v2_file)

        total_examples = min(len(v0_data), len(v2_data))

        col1, col2, col3 = st.columns([1,2,1])

        with col1:
            if st.button('⬅️ Previous'):
                st.session_state.index = max(st.session_state.index - 1, 0)

        with col3:
            if st.button('Next ➡️'):
                st.session_state.index = min(st.session_state.index + 1, total_examples-1)

        idx = st.session_state.index

        st.write(f'**Showing example {idx+1} of {total_examples}**')

        v0_example = v0_data[idx]
        v2_example = v2_data[idx]

        # 检查 instruction/output 是否一致
        if v0_example.get('instruction') != v2_example.get('instruction'):
            st.warning('⚠️ Instruction Mismatch!')
        if v0_example.get('output') != v2_example.get('output'):
            st.warning('⚠️ Reference Output Mismatch!')

        st.subheader('Instruction')
        st.code(v0_example.get('instruction', ''), language='markdown')

        st.subheader('Reference Output')
        st.code(v0_example.get('output', ''), language='markdown')

        st.subheader('Model1 Result')
        st.code(v0_example.get('result', ''), language='markdown')

        st.subheader('Model2 Result')
        st.code(v2_example.get('result', ''), language='markdown')

    else:
        st.error('V0 or V2 file not found in the selected folder.')
else:
    st.info('Please select a folder to begin.')
