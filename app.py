import streamlit as st
import numpy as np
import statsmodels.api as sm
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import savgol_filter

st.set_page_config(page_title="UI Mockup - Recall Scope", layout='wide')

df = pd.read_csv('dashboard_under_1k.csv')
df2 = pd.read_csv('imdrf_codes_count.csv')

ks = df.k_numbers.unique()
selected = st.sidebar.selectbox('Review Number:', ks)

st.sidebar.title('UI Mockup - Recall Scope')
s_exp = st.sidebar.expander("Business Requirements")
s_exp.write(f"During Recall Review, the OHT Lead Reviewer is responsible for reviewing and evaluating the adequacy of the firm's scope determination"
f"If there was a way to filter MDR's during an MDR analysis at a model/lot number, it would allow reviewers to better assess if the same problem exhibited in the recall under review is evident in other model/lots of a device/brand not indicated in recall under review.")

s_exp2 = st.sidebar.expander("User Story 1")
s_exp2.write("As a reviewer, I want a link which provides me access to device Company (owner/operator) information.")

s_exp3 = st.sidebar.expander("User Story 2")
s_exp3.write(" As a reviewer, I want to see the device brand name, the K Number, the Lot/Model Number (Toggle device) to know what device is being analyzed.")

s_exp4 = st.sidebar.expander("User Story 3")
s_exp4.write("As a reviewer,  I want to know the number of similar MDRs for the present lot/model number which has the same IMDRF code/s.")

s_exp5 = st.sidebar.expander("User Story 4")
s_exp5.write("As a reviewer, I want to know if the current Lot/Model Number of the recalled device is Within Recall Scope.")

s_exp6 = st.sidebar.expander("User Story 5")
s_exp6.write("As a reviewer, I would like to know the total number of MDRs for the Product Number. ")

s_exp4 = st.sidebar.expander("User Story 6")
s_exp4.write("As a reviewer, I want to know the Risk Level Comparison (Percentage Ratio) of Similar MDRs related to Total MDRs.")



subset = df[df.k_numbers == selected].copy()


model_list = subset.model_number.unique()
lot_list = subset.lot_number.unique()

mdrf_count = df2[df2.k_numbers == selected][['imdrf_codes', 'count']]
mdrf_count.reset_index(inplace=True, drop=True)

mdrf_count_dict = {}

for i,j in zip(mdrf_count['imdrf_codes'], mdrf_count['count']):
    mdrf_count_dict[i] = j

def trasforming_lists(row_val):
    cleaned_item = row_val.strip('[]').replace(' ', '').replace("'",'')
    if ',' in cleaned_item:
       return cleaned_item.split(',')
    else:
       return [cleaned_item]

subset_model = subset[subset['model_number'].isin(model_list)]
subset_model.drop_duplicates(subset='model_number', inplace=True)
subset_model.reset_index(inplace=True, drop=True)

subset_model['imdrf_codes'] = subset_model['imdrf_codes'].apply(trasforming_lists)

#FIX THIS WE ARE TAKING ONLY THE FIRST ONE

counts_model_list = []
for idx, codes in enumerate(subset_model.imdrf_codes):
    if codes[0] in mdrf_count_dict:
        counts_model_list.append(mdrf_count_dict[codes[0]])
    else:
        counts_model_list.append(0)

subset_model['counts_model_list'] = counts_model_list

# ----------------

subset_lot = subset[subset['lot_number'].isin(lot_list)]
subset_lot.drop_duplicates(subset='lot_number', inplace=True)
subset_lot.reset_index(inplace=True, drop=True)

subset_lot['imdrf_codes'] = subset_lot['imdrf_codes'].apply(trasforming_lists)

counts_lot_list = []
for idx, codes in enumerate(subset_lot.imdrf_codes):
    if codes[0] in mdrf_count_dict:
        counts_lot_list.append(mdrf_count_dict[codes[0]])
    else:
        counts_lot_list.append(0)

subset_lot['counts_lot_list'] = counts_lot_list
subset_lot['IMDRF_Ratio'] = ((subset_lot.counts_lot_list / subset_lot.total_mdrs_both) * 100).round(2)
subset_lot.style.format({'IMDRF_Ratio': '{:.2f}'})
subset_lot = subset_lot.sort_values(by='IMDRF_Ratio', ascending=False)
subset_lot.reset_index(inplace=True, drop=True)

col1, col2, col3 = st.columns((5,5,5))

manufacturer_name = subset_lot.manufacturer_name[0]
brand = subset_lot.brand[0]
k_numbers = subset_lot.k_numbers[0]

dash = subset_lot[['lot_number','is_scope_lot', 'imdrf_codes', 'counts_lot_list', 'total_mdrs_both', 'IMDRF_Ratio']]


with col1:
    #st.markdown(f'<p style=""><b>Brand: </b>{brand}</p>', unsafe_allow_html=True,)
   ## st.markdown(f'<p style=""><b>Generic Name: </b>{generic_name}</p>', unsafe_allow_html=True,)
  #  st.markdown(f'<p style=""><b>Product Code: </b>{product_code}</p>', unsafe_allow_html=True,)
  st.markdown(f'<p style=""><b>Manufacturer Name: </b>{manufacturer_name}</p>', unsafe_allow_html=True,)
  
with col2:
    #st.markdown(f'<p style=""><b>Brand: </b>{brand}</p>', unsafe_allow_html=True,)
   ## st.markdown(f'<p style=""><b>Generic Name: </b>{generic_name}</p>', unsafe_allow_html=True,)
  #  st.markdown(f'<p style=""><b>Product Code: </b>{product_code}</p>', unsafe_allow_html=True,)
  st.markdown(f'<p style=""><b>Brand: </b>{brand}</p>', unsafe_allow_html=True,)

with col3:
   # st.markdown(f'<p style=""><b>Common Problems: </b></p>', unsafe_allow_html=True,)
   # for i in range(len(res)):
   #     st.write(res2[i])
    st.markdown(f'<p style=""><b>K_number: </b>{k_numbers}</p>', unsafe_allow_html=True,)

dash = dash.rename(columns={'lot_number': 'Lot Number','is_scope_lot': 'Is Scope', 'imdrf_codes': 'Code', 'counts_lot_list': '# Similar MDRs', 'total_mdrs_both': 'Total MDRs', 'IMDRF_Ratio':'Risk Ratio'})
col4, col5, col6 =  st.columns((2.5,5,2.5))

st.markdown("</hr>", unsafe_allow_html=True)
st.markdown("</hr>", unsafe_allow_html=True)
st.markdown("</hr>", unsafe_allow_html=True)
st.markdown("</hr>", unsafe_allow_html=True)

with col5:
    st.dataframe(dash)

# col4, col5, col6, col7, col8, col9 = st.columns((5,5,5,5,5,5))

# with col4:
#      st.markdown(f'<p style=""><b>Lot Number</b></p>', unsafe_allow_html=True,)
#      for i in subset_lot.lot_number:
#          st.write(i)
# with col5:
#      st.markdown(f'<p style=""><b>Is Scope</b></p>', unsafe_allow_html=True,)
#      for i in subset_lot.is_scope:
#          st.write(i)
# with col6:
#      st.markdown(f'<p style=""><b>Code</b></p>', unsafe_allow_html=True,)
#      for i in subset_lot.imdrf_codes:
#          st.write(i)
# with col7:
#      st.markdown(f'<p style=""><b># Similar MDRs</b></p>', unsafe_allow_html=True,)
#      for i in subset_lot.counts_lot_list:
#          st.write(i)
# with col8:
#      st.markdown(f'<p style=""><b>Total MDRs</b></p>', unsafe_allow_html=True,)
#      for i in subset_lot.total_mdrs_both:
#          st.write(i)
# with col9:
#      st.markdown(f'<p style=""><b>Risk Ratio</b></p>', unsafe_allow_html=True,)
#      for i in subset_lot.IMDRF_Ration:
#          st.write(i)
# st.write('--------------------------')


