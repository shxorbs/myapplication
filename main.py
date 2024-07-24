import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 로드
file_path = '20240724114945.xlsx'
data = pd.read_excel(file_path)

# 데이터 정리
data.columns = ['성씨', '지역', '인구수']
data['성씨'] = data['성씨'].fillna(method='ffill')

# Streamlit 앱 제목
st.title('지역 및 성씨별 인구 데이터 조회')

# 지역 선택
regions = data['지역'].unique()
selected_region = st.selectbox('지역을 선택하세요:', regions)

# 선택한 지역에 대한 데이터 필터링
region_data = data[data['지역'] == selected_region]

# 성씨 입력
surname = st.text_input('성씨를 입력하세요:')

# 선택한 성씨에 대한 데이터 필터링
if surname:
    surname_data = region_data[region_data['성씨'].str.contains(surname, na=False)]
    if not surname_data.empty:
        st.write(f"지역: {selected_region}, 성씨: {surname} 인구 데이터")
        st.dataframe(surname_data.reset_index(drop=True))
    else:
        st.write(f"지역 '{selected_region}'에서 성씨 '{surname}'의 데이터를 찾을 수 없습니다.")
else:
    st.write("성씨를 입력하세요.")

# 특정 성씨를 입력하지 않았을 때 모든 데이터를 표시
if not surname:
    st.write(f"지역 '{selected_region}'의 모든 성씨 데이터")
    st.dataframe(region_data.reset_index(drop=True))
