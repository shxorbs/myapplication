import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 제목
st.title("통계 그래프 생성기")

# 변수 저장용 리스트와 딕셔너리 초기화
variables = st.session_state.get('variables', {})
st.session_state['variables'] = variables

# 변수를 추가하는 섹션
with st.form("variable_form", clear_on_submit=True):
    variable_name = st.text_input("변수 이름을 입력하세요", key='variable_name_input')
    variable_values = st.text_area("변량을 쉼표로 구분하여 입력하세요 (예: 1, 2, 3, 4)", key='variable_values_input')
    
    # '변수 추가' 버튼 클릭 시 변수 추가
    if st.form_submit_button("변수 추가"):
        if variable_name and variable_values:
            try:
                values_list = list(map(float, variable_values.split(',')))
                st.session_state['variables'][variable_name] = values_list
                st.success(f"변수 '{variable_name}'이(가) 성공적으로 추가되었습니다.")
            except ValueError:
                st.error("변량을 숫자로만 입력하세요.")
        else:
            st.error("변수 이름과 변량을 모두 입력하세요.")

# 추가된 변수 보여주기
if st.session_state['variables']:
    st.subheader("추가된 변수들:")
    for var_name, values in st.session_state['variables'].items():
        st.write(f"{var_name}: {values}")

# 그래프 색상 선택
st.sidebar.subheader("그래프 옵션")
graph_color = st.sidebar.color_picker("그래프 색상을 선택하세요", "#00f900")

# 변수를 선택하는 섹션
if st.session_state['variables']:
    selected_variable = st.selectbox("그래프를 그릴 변수를 선택하세요", list(st.session_state['variables'].keys()))

    if selected_variable:
        data = st.session_state['variables'][selected_variable]
        st.write(f"선택된 변수: {selected_variable}")
        st.write(f"변량: {data}")

        # 히스토그램
        if st.checkbox("히스토그램 보기"):
            plt.figure(figsize=(10, 5))
            plt.hist(data, bins=10, color=graph_color)
            plt.title(f"{selected_variable}의 히스토그램")
            st.pyplot(plt)

        # 줄기와 잎 그림
        if st.checkbox("줄기와 잎 그림 보기"):
            stem_leaf_data = pd.Series(data).value_counts().sort_index()
            st.table(stem_leaf_data)

        # 도수분포 다각형
        if st.checkbox("도수분포 다각형 보기"):
            plt.figure(figsize=(10, 5))
            hist, bin_edges = np.histogram(data, bins=10)
            bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
            plt.plot(bin_centers, hist, marker='o', linestyle='-', color=graph_color)
            plt.title(f"{selected_variable}의 도수분포 다각형")
            st.pyplot(plt)

        # 도수와 상대도수
        if st.checkbox("도수와 상대도수"):
            df = pd.DataFrame(data, columns=["값"])
            freq = df["값"].value_counts().sort_index()
            relative_freq = freq / len(df)
            freq_df = pd.DataFrame({"도수": freq, "상대도수": relative_freq})
            st.table(freq_df)

# 주의 사항
st.write("도수분포 다각형과 히스토그램은 모두 연속적인 데이터에 적합합니다.")
