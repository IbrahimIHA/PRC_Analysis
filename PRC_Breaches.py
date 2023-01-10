import pandas as pd
import streamlit as st
import numpy as np
import requests as requests 

st.set_page_config(layout="wide")
# primaryColor = '#4A6DAB'
# backgroundColor = '#282936'
# secondaryBackgroundColor = '#946B48'
# textColor = '#F7F7F7'
# font = "serif"
st.title('PRC Breaches Analysis')
st.write('Author: Ibrahim Ali')

data = pd.read_csv('https://github.com/IbrahimIHA/PRC_Analysis/raw/main/PRC_Clean.csv',usecols=['Date Made Public', 'Company', 'City', 'State',
       'Type of breach', 'Type of organization', 'Total Records',
       'Description of incident', 'Year of Breach', 'Latitude', 'Longitude'])
file=data.to_csv()

year_choices = data['Year of Breach'].unique()
year_choices = np.sort(year_choices)
year_choices = np.append(year_choices,None)

filtered_year = st.sidebar.selectbox('Select Specific Year',year_choices)
filtered_data = data[data['Year of Breach']==filtered_year]

if filtered_year==None:
    Year_Freq=pd.crosstab(data['Year of Breach'],'Count of Breaches')
    Year_Sum=data['Total Records'].sum()
    Org_Sum=data.groupby('Type of organization').sum()
    Map = data.filter(['Latitude','Longitude'], axis=1).dropna()
    max_info = data[data['Total Records'] == data['Total Records'].max()]
else:
    Year_Freq=pd.crosstab(filtered_data['Year of Breach'],'Count of Breaches')
    Year_Sum=filtered_data['Total Records'].sum()
    Org_Sum=filtered_data.groupby('Type of organization').sum()
    Map = filtered_data.filter(['Latitude','Longitude'], axis=1).dropna()
    max_info = filtered_data[filtered_data['Total Records'] == filtered_data['Total Records'].max()]
Org_Sum = Org_Sum.drop(columns=['Year of Breach','Latitude','Longitude'])
Map.rename(columns={'Latitude':'lat','Longitude':'lon'},inplace=True)

# Streamlit Content
st.header('PrivacyRights.org')
st.write('''PRC, also known as Privacy Rights Clearinghouse, believe everyone deserves the opportunity to be informed which is why
They strive to increase access to understandable information about existing data privacy rights and choices. PRC 
conducts research into complex data privacy laws, engages in outreach, creates and maintains publicly-accessible 
resources that break down and clarify rights and choices.''')
st.subheader('Breaches Based On Location')
st.map(Map)
st.caption('Total Amt of Records Lost: '+ str(Year_Sum))
col1, col2 = st.columns(2)
col1.subheader('Largest Breach of ' + str(max_info['Year of Breach'].max()))
col1.write('Company: ' + max_info['Company'].max())
col1.write('Organization Classification: ' + max_info['Type of organization'].max())
col1.write('Date Made Public: ' + str(max_info['Date Made Public'].max()))
col1.write('Breach Type: ' + str(max_info['Type of breach'].max()))
col1.write('Records Lost: ' + str(max_info['Total Records'].max()))
if max_info['City'].isnull().values.any():
    col1.write('Location: Unknown')
elif max_info['State'].isnull().values.any():
    col1.write('Location: Unknown')
else:
    col1.write('Location: ' + str(max_info['City'].max()) + ', ' + str(max_info['State'].max()))
col2.subheader('Records Lost Based On Organization Type')
col2.bar_chart(Org_Sum)
st.download_button(label="Download Cleaned Dataset", data=file, file_name='PRC_Breaches.csv')
st.dataframe(data)