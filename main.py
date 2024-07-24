import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Load the data
file_path = '202406_202406_연령별인구현황_월간 (1).csv'
data = pd.read_csv(file_path, encoding='cp949')

# List of ages corresponding to middle school
middle_school_ages = ['2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세']

# Process data to remove commas and convert to integers
for column in data.columns[1:]:
    data[column] = data[column].str.replace(',', '').astype(int)

# Streamlit app
st.title('Population Distribution by Age in Selected Region')

# Region selection
regions = data['행정구역'].unique()
selected_region = st.selectbox('Select a region:', regions)

# Filter data for the selected region
region_data = data[data['행정구역'] == selected_region]

# Calculate middle school population and total population
middle_school_population = region_data[middle_school_ages].sum(axis=1).values[0]
total_population = region_data['2024년06월_계_총인구수'].values[0]

# Calculate the percentage of middle school population
middle_school_percentage = (middle_school_population / total_population) * 100

# Display the percentage
st.write(f'The percentage of middle school population in {selected_region} is {middle_school_percentage:.2f}%')

# Plotting the pie chart
labels = ['Middle School Age Population', 'Other Age Population']
sizes = [middle_school_population, total_population - middle_school_population]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)
