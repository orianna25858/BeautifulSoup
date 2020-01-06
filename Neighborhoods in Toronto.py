#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# define the dataframe columns
column_names = ['Postal Code', 'Borough', 'Neighborhood'] 

# instantiate the dataframe
neighborhoods = pd.DataFrame(columns=column_names)


# In[3]:


neighborhoods


# In[4]:


pip install beautifulsoup4


# In[5]:


pip install lxml


# In[6]:


pip install html5lib


# In[38]:


#imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#get html from wiki page and create soup object
source = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
soup = BeautifulSoup(source.text, 'lxml')

#using soup object, iterate the .wikitable to get the data from the HTML page and store it into a list
data = []
columns = []
table = soup.find(class_='wikitable')
for index, tr in enumerate(table.find_all('tr')):
    section = []
    for td in tr.find_all(['th','td']):
        section.append(td.text.rstrip())
    
    #First row of data is the header
    if (index == 0):
        columns = section
    else:
        data.append(section)

#convert list into Pandas DataFrame
canada = pd.DataFrame(data = data,columns = columns)
canada.head()


# In[39]:


#Remove Boroughs that are 'Not assigned'
canada = canada[canada['Borough'] != 'Not assigned']
canada.head()


# In[40]:


# More than one neighborhood can exist in one postal code area, combined these into one row with the neighborhoods separated with a comma
canada["Neighborhood"] = canada.groupby("Postcode")["Neighborhood"].transform(lambda neigh: ', '.join(neigh))

#remove duplicates
canada = canada.drop_duplicates()

#update index to be postcode if it isn't already
if(canada.index.name != 'Postcode'):
    canada = canada.set_index('Postcode')
    
canada.head()


# In[41]:


# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough
canada['Neighborhood'].replace("Not assigned", canada["Borough"],inplace=True)
canada.head()


# In[42]:



canada.shape

