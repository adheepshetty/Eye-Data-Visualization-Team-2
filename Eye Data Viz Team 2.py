#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import os


# In[24]:


def create_dfs(archive_path):
    directories_table = {}
    files_table = {}
    for directory in os.listdir(archive_path):
        if directory != "__MACOSX":
            directories_table[directory] = files_table
            for file in os.listdir(archive_path + "\\" + directory):
                if "EVD" in file:
                    filepath = archive_path + "\\" + directory + "\\" + file
                    files_table[file] = pd.read_csv(filepath, 
                                                    sep='\t', 
                                                    error_bad_lines=False, 
                                                    names = ['Time', 'Event', 'EventKey', 'Data1', 'Data2', 'Description'] )
                if "FXD" in file:
                    filepath = archive_path+ "\\" + directory + "\\" + file
                    files_table[file] = pd.read_csv(filepath, 
                                                    sep='\t', 
                                                    error_bad_lines=False, 
                                                    names = ['ID', 'Time', 'Duration', 'X' , 'Y'] )
                
                if "GZD" in file:
                    filepath = archive_path+ "\\" + directory + "\\" + file
                    files_table[file] = pd.read_csv(filepath, 
                                                    sep='\t', 
                                                    error_bad_lines=False, 
                                                    names = ['Time', 'ID', 'ScreenL X', 'ScreenL Y', 'CamL X', 'CamL Y', 'DistL', 'PupilL', 'CodeL',
                                                            'ScreenR X', 'ScreenR Y', 'CamR X', 'CamR Y', 'DistR', 'PupilR', 'CodeR'] )
                    
    return directories_table  


# In[26]:


cd C:\\Users\\adhee\\Downloads


# In[28]:


# directories_table = create_dfs("C:\\Users\\018094724sa\\Downloads\\Archive\\")
directories_table = create_dfs("C:\\Users\\adhee\\Downloads\\Archive\\")


# In[ ]:


directories_table['p1']['p1.graphEVD.txt'].head()


# In[ ]:


def domain_segregation(archive_path):
    domain = {}
    file_path = archive_path + 'Additional Participant Data.csv'
    domain_df = pd.read_csv(file_path)
#   Ontologie -> 1 -> 'general'
#   Ontologie -> 2 -> 'expert'
#   Visualization -> 1 -> 'tree'
#   Visualization -> 2 -> 'graph'
#     for viz, ont in zip(domain_df['Visualization'], domain_df['Ontologies']):
#         if ont == 1 and viz == 1:
    participants = domain_df.loc[((domain_df['Visualization'] == 1) & (domain_df['Ontologies'] == 1))]['ID']
    for participant in participants:
        for key in directories_table[participant].keys():
            if "tree" in key:
                domain['GeneralTree'] = directories_table[participant]
                
    participants = domain_df.loc[((domain_df['Visualization'] == 1) & (domain_df['Ontologies'] == 2))]['ID']
    for participant in participants:
        for key in directories_table[participant].keys():
            if "tree" in key:
                domain['ExpertTree'] = directories_table[participant]
                
    participants = domain_df.loc[((domain_df['Visualization'] == 2) & (domain_df['Ontologies'] == 1))]['ID']
    for participant in participants:
        for key in directories_table[participant].keys():
            if "graph" in key:
                domain['GeneralGraph'] = directories_table[participant]
                
    participants = domain_df.loc[((domain_df['Visualization'] == 2) & (domain_df['Ontologies'] == 2))]['ID']
    for participant in participants:
        for key in directories_table[participant].keys():
            if "graph" in key:
                domain['ExpertGraph'] = directories_table[participant]
    return domain


# In[ ]:


# domain = domain_segregation("C:/Users/018094724sa/Downloads/Archive")
domain = domain_segregation("C:/Users/adhee/Downloads/Archive/")


# In[ ]:


domain['ExpertTree']

