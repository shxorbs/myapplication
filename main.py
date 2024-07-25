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
data['인구수'] = data['인구수'].astype(int)

# '계'를 제외한 데이터 필터링
data = data[data['성씨'] != '계']

# Streamlit 앱 제목
st.title('지역 및 성씨별 인구 데이터 조회')

# 지역 선택
regions = data['지역'].unique()
selected_region = st.selectbox('지역을 선택하세요:', regions)

# 선택한 지역에 대한 데이터 필터링
region_data = data[data['지역'] == selected_region]

# 상위 5개 성씨와 하위 5개 성씨 (인덱스를 1부터 시작)
top_5_surnames = region_data.nlargest(5, '인구수').reset_index(drop=True)
bottom_5_surnames = region_data.nsmallest(5, '인구수').reset_index(drop=True)
top_5_surnames.index += 1
bottom_5_surnames.index += 1

# 성씨 입력
surname = st.text_input('성씨를 입력하세요:')

# 선택한 성씨에 대한 데이터 필터링 및 전국 인구수 계산
if surname:
    # 지역 데이터에서 입력한 성씨의 데이터 필터링
    region_surname_data = region_data[region_data['성씨'].str.contains(surname, na=False)]
    
    # 전국 데이터에서 입력한 성씨의 데이터 필터링
    total_surname_data = data[data['성씨'].str.contains(surname, na=False)]
    
    if not region_surname_data.empty and not total_surname_data.empty:
        st.write(f"지역: {selected_region}, 성씨: {surname} 인구 데이터")
        st.dataframe(region_surname_data.reset_index(drop=True))
        
        # 모든 지역에 대한 입력된 성씨의 인구수 데이터 준비
        regions_surname_data = total_surname_data[total_surname_data['지역'] != '전국'].groupby('지역').sum().reset_index()
        
        # 각 한자별 인구수를 계산하고 그래프에 추가
        unique_chars = set(char for name in total_surname_data['성씨'] for char in name if char.isalnum())
        fig, ax = plt.subplots(figsize=(14, 7))
        
        for char in unique_chars:
            char_total_population = total_surname_data[total_surname_data['성씨'].str.contains(char, na=False)]['인구수'].sum()
            ax.axhline(y=char_total_population, linestyle='--', label=f'전국 {char} 성씨 인구수')
        
        # 지역별 인구수 꺾은선 그래프 추가
        ax.plot(regions_surname_data['지역'], regions_surname_data['인구수'], marker='o', linestyle='-', color='blue', label='지역별 인구수')
        
        ax.set_ylabel('인구수')
        ax.set_xlabel('지역')
        ax.set_title(f"{surname} 성씨 전국 대비 지역별 인구수")
        ax.legend()
        
        # 그래프에 레이블 추가
        for i, txt in enumerate(regions_surname_data['인구수']):
            ax.annotate(txt, (regions_surname_data['지역'][i], txt), textcoords="offset points", xytext=(0,10), ha='center')
        
        # 각 한자별 인구수 레이블 추가
        for char in unique_chars:
            char_total_population = total_surname_data[total_surname_data['성씨'].str.contains(char, na=False)]['인구수'].sum()
            ax.annotate(char_total_population, (1, char_total_population), textcoords="offset points", xytext=(-10,10), ha='center')

        st.pyplot(fig)
    else:
        st.write(f"지역 '{selected_region}' 또는 전국에서 성씨 '{surname}'의 데이터를 찾을 수 없습니다.")
else:
    st.write("성씨를 입력하세요.")

# 상위 5개 성씨와 하위 5개 성씨 출력
st.write(f"지역 '{selected_region}'의 상위 5개 성씨")
st.dataframe(top_5_surnames)

st.write(f"지역 '{selected_region}'의 하위 5개 성씨")
st.dataframe(bottom_5_surnames)

# 특정 성씨를 입력하지 않았을 때 모든 데이터를 표시
if not surname:
    st.write(f"지역 '{selected_region}'의 모든 성씨 데이터")
    st.dataframe(region_data.reset_index(drop=True))
