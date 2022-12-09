#20221209 - streamlit with network visualization
#Ref: https://medium.com/towards-data-science/how-to-deploy-interactive-pyvis-network-graphs-on-streamlit-6c401d4c99db

#import required library
import streamlit as st
import streamlit.components.v1 as components
import os, sys
import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

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

st.title('Node Data')
st.write(df_node)
st.title('Edge Data')
st.write(df_edge)

#Define list of selection options
acct_list = df_node['name']

#Implement multiselect dropdown menu for option selection (returns a list)
selected_acct = st.multiselect('Select acct(s) to visualize', acct_list)

#Set info message on initial site load
if len(selected_acct)==0:
  st.text('Choose at least 1 account to get started')
else:
  df_edge_select = df_edge.loc[df_edge['Orig'].isin(selected_acct) | df_edge['Dest'].isin(selected_acct)]
  #df_edge_select = df_edge_select.reset_index(drop=True)
  st.write(df_edge_select)
  #attempt1
  #Create networkx graph object from pandas dataframe
  #G = nx.from_pandas_edgelist(df=df_edge_select, source='Orig', target='Dest', edge_attr=['Value'], create_using=nx.DiGraph())
  #net = Network(height='465px', bgcolor='#222222', font_color='white', directed=True)
  # Take Networkx graph and translate it to a PyVis graph format
  #net.from_nx(G)
  
  G = nx.from_pandas_edgelist(df=df_edge_select, source='Orig', target='Dest', edge_attr=['Value'], create_using=nx.DiGraph())
  durations = [i['Value'] for i in dict(G.edges).values()]
  labels = [i for i in dict(G.nodes).keys()]
  labels = {i:i for i in dict(G.nodes).keys()}

  fig, ax = plt.subplots(figsize=(12,5))
  pos = nx.spring_layout(G)
  #nx.draw_networkx_nodes(G, pos, ax = ax, labels=True)
  nx.draw_networkx_edges(G, pos, width=durations, ax=ax)
  
  # Generate network with specific layout settings
  #net.repulsion(node_distance=420,
  #              central_gravity=0.33,
  #              spring_length=110,
  #              spring_strength=0.10,
  #              damping=0.95)
  # Save and read graph as HTML file (on Streamlit Sharing)
  #try:
  #  path = '/tmp'
  #  net.save_graph(f'pyvis_graph.html')
  #  HtmlFile = open(f'pyvis_graph.html', 'r', encoding='utf-8')

  # Save and read graph as HTML file (locally)
  #except:
  #  path = '/html_files'
  #  net.save_graph(f'pyvis_graph.html')
  #  HtmlFile = open(f'pyvis_graph.html', 'r', encoding='utf-8')

  # Load HTML file in HTML component for display on Streamlit page
  #components.html(HtmlFile.read(), height=435)
