import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 로드
file_path = '성씨ㆍ본관별_인구__시군구_20240724114945 (1).xlsx'
data = pd.read_excel(file_path)

# 데이터 정리
data.columns = ['성씨', '지역', '인구수']
data['성씨'] = data['성씨'].fillna(method='ffill')

# 인구수를 숫자로 변환
data['인구수'] = data['인구수'].astype(int)

# Streamlit 앱 제목
st.title('지역 및 성씨별 인구 데이터 조회')

# 지역 선택
regions = data['지역'].unique()
selected_region = st.selectbox('지역을 선택하세요:', regions)

# 선택한 지역에 대한 데이터 필터링
region_data = data[data['지역'] == selected_region]

# 상위 5개 성씨와 하위 5개 성씨
top_5_surnames = region_data.nlargest(5, '인구수')
bottom_5_surnames = region_data.nsmallest(5, '인구수')

# 성씨 입력
surname = st.text_input('성씨를 입력하세요:')

# 선택한 성씨에 대한 데이터 필터링 및 전국 대비 비율 계산
if surname:
    region_surname_data = region_data[region_data['성씨'].str.contains(surname, na=False)]
    total_surname_data = data[data['성씨'].str.contains(surname, na=False)].groupby('성씨').sum().reset_index()

    if not region_surname_data.empty:
        st.write(f"지역: {selected_region}, 성씨: {surname} 인구 데이터")
        st.dataframe(region_surname_data.reset_index(drop=True))

        # 전국 대비 해당 지역 성씨 비율 그래프 (꺾은선 그래프)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(['전국', selected_region], [total_surname_data['인구수'].values[0], region_surname_data['인구수'].values[0]], marker='o', linestyle='-', color='blue', label='인구수')
        ax.set_ylabel('인구수')
        ax.set_title(f"{surname} 성씨 전국 대비 {selected_region} 인구수")
        ax.legend()

        # 그래프에 레이블 추가
        for i, txt in enumerate([total_surname_data['인구수'].values[0], region_surname_data['인구수'].values[0]]):
            ax.annotate(txt, (['전국', selected_region][i], txt), textcoords="offset points", xytext=(0,10), ha='center')

        st.pyplot(fig)
    else:
        st.write(f"지역 '{selected_region}'에서 성씨 '{surname}'의 데이터를 찾을 수 없습니다.")
else:
    st.write("성씨를 입력하세요.")

# 상위 5개 성씨와 하위 5개 성씨 출력
st.write(f"지역 '{selected_region}'의 상위 5개 성씨")
st.dataframe(top_5_surnames.reset_index(drop=True))

st.write(f"지역 '{selected_region}'의 하위 5개 성씨")
st.dataframe(bottom_5_surnames.reset_index(drop=True))

# 특정 성씨를 입력하지 않았을 때 모든 데이터를 표시
if not surname:
    st.write(f"지역 '{selected_region}'의 모든 성씨 데이터")
    st.dataframe(region_data.reset_index(drop=True))
