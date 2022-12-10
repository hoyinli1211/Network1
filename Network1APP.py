#20221209 - streamlit with network visualization
#Ref: https://medium.com/towards-data-science/how-to-deploy-interactive-pyvis-network-graphs-on-streamlit-6c401d4c99db

#import required library
import streamlit as st
import streamlit.components.v1 as components
import os, sys
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import math

#initialization of session state
if 'indEnd' not in st.session_state:
  st.session_state['ind0'] = False
  
# Add a title and intro text
st.title('Fund Flow Network Visualization using streamlit')
st.text('This is the first attempt to use PyVis package to perform interactive network visualization in streamlit platform')

#Import template file
file_temp = 'Network1.xlsx'
df_node_temp = pd.read_excel(file_temp, 'node')
df_edge_temp = pd.read_excel(file_temp, 'edge')

df_node = df_node_temp
df_edge = df_edge_temp

df_edge['weight'] = df_edge.apply (lambda row: len(str(row.Amount)), axis=1)
df_edge['title'] = df_edge.apply (lambda row: row.Orig + ' transferred HK$' + str(row.Amount) + ' to ' + row.Dest, axis=1)

df_onus = pd.concat([df_edge.loc[df_edge['Orig.Bank']=='on-us']['Orig'],
                    df_edge.loc[df_edge['Dest.Bank']=='on-us']['Dest']],
                    axis=0).drop_duplicates().rename('name').to_frame().reset_index()

df_offus = pd.concat([df_edge.loc[df_edge['Orig.Bank']!='on-us']['Orig'],
                    df_edge.loc[df_edge['Dest.Bank']!='on-us']['Dest']],
                    axis=0).drop_duplicates().rename('name').to_frame().reset_index()

st.title('Edge Data')
st.write(df_edge)

#Define show first layer only, or second layer as well
nlayer = st.radio("Number of layer",
                 ('first layer only', 'with second layer'))

#Define list of selection options
acct_list = df_node['name']
onus_list = df_onus['name']
offus_list = df_offus['name']

#Implement multiselect dropdown menu for option selection (returns a list)
#selected_acct = st.multiselect('Select acct(s) to visualize', acct_list)
selected_onus_acct = st.multiselect('Select on-us acct(s) to visualize', onus_list)
selected_offus_acct = st.multiselect('Select off-us acct(s) to visualize', offus_list)

if (len(selected_onus_acct)==0 and len(selected_offus_acct)==0):
  st.text('Choose at least 1 onus/offus account to get started.')
elif (len(selected_onus_acct)>0 or len(selected_offus_acct)>0):
  firstlayer_onus_acct = selected_onus_acct
  st.write(type(firstlayer_onus_acct))
  firstlayer_offus_acct = selected_offus_acct
  firstlayer_acct = [firstlayer_onus_acct, firstlayer_offus_acct]
  df_edge_firstlayer = df_edge.loc[df_edge['Orig'].isin(firstlayer_acct) | df_edge['Dest'].isin(firstlayer_acct)]
  
  secondlayer_acct = pd.concat([df_edge_firstlayer['Orig'], df_edge_firstlayer['Dest']], axis=0).drop_duplicates()
    
  #df_edge_1stlayer = df_edge.loc[df_edge['Orig'].isin(selected_acct) | df_edge['Dest'].isin(selected_acct)]
  if nlayer == 'first layer only':
    #st.write(firstlayer_acct)
    #st.write(df_edge_firstlayer)
    #st.write(secondlayer_acct)
    ''
  elif nlayer == 'with second layer':
    ''
  elif nlayer == 'with third layer':
    ''
  else:
    ''
else:
  pass
   
"""
#Set info message on initial site load
if len(selected_acct)==0:
  st.text('Choose at least 1 account to get started')
else:
  if nlayer == 'first layer only':
    df_edge_select = df_edge.loc[df_edge['Orig'].isin(selected_acct) | df_edge['Dest'].isin(selected_acct)]
  elif nlayer == 'with second layer':
    df_edge_select0 = df_edge.loc[df_edge['Orig'].isin(selected_acct) | df_edge['Dest'].isin(selected_acct)]
    selected_acct_second = pd.concat([df_edge_select0['Orig'], df_edge_select0['Dest']], axis=0).drop_duplicates()
    df_edge_select = df_edge.loc[df_edge['Orig'].isin(selected_acct_second) | df_edge['Dest'].isin(selected_acct_second)]
  else:
    pass
  #df_edge_select = df_edge_select.reset_index(drop=True)
  st.write(df_edge_select)
  
  #Create networkx graph object from pandas dataframe
  G = nx.from_pandas_edgelist(df=df_edge_select, source='Orig', target='Dest', edge_attr=['weight', 'title'], create_using=nx.DiGraph())
  st.write(G.nodes)
  net = Network(height='465px', bgcolor='#222222', font_color='white', directed=True)
  # Take Networkx graph and translate it to a PyVis graph format
  net.from_nx(G)
  
  # Generate network with specific layout settings
  net.repulsion(node_distance=420,
                central_gravity=0.33,
                spring_length=110,
                spring_strength=0.10,
                damping=0.95)
  # Save and read graph as HTML file (on Streamlit Sharing)
  try:
    path = '/tmp'
    net.save_graph(f'pyvis_graph.html')
    HtmlFile = open(f'pyvis_graph.html', 'r', encoding='utf-8')

  # Save and read graph as HTML file (locally)
  except:
    path = '/html_files'
    net.save_graph(f'pyvis_graph.html')
    HtmlFile = open(f'pyvis_graph.html', 'r', encoding='utf-8')

  # Load HTML file in HTML component for display on Streamlit page
  components.html(HtmlFile.read(), height=435)
"""
