#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import bs4
import re
from datetime import datetime
pd.set_option('display.max_rows', 1000)
pd.options.display.max_colwidth = 1000

#to send emails
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#to make the conection with spreadsheets
import gspread
from google.oauth2.service_account import Credentials

#for passwords
import os
from dotenv import load_dotenv, find_dotenv


# # D. p_reporting

# We are going to send the different DataFrames to spreadsheet
# 
# #### INDEX LIBRARY
# https://docs.gspread.org/en/latest/
# 
# #### USER GUIDE
# https://docs.gspread.org/en/latest/user-guide.html

# The conection has been done in the "p_wrangling" module. The output is located in the variable "gc"

# In[74]:


def update_spreadsheet(gc, spreadsheet_name, worksheet_name, dataframe):
    #Open the spreadhseet
    sheet = gc.open(spreadsheet_name).worksheet(worksheet_name)
    
    #Clear and Update the Worksheet
    sheet.clear()
    sheet.update('A1:L1',[dataframe.columns.tolist()])
    sheet.update('A2:L' + str(len(dataframe)+1), dataframe.values.tolist())
    
    return "worksheet updated"


# In[75]:


#sheet1 - df_single
#update_spreadsheet(gc, "business_afi_scraping_df_single", "df_single", df_single)


# In[76]:


#sheet2 - df_append_new_files
#update_spreadsheet(gc, "business_afi_scraping_last_day_files", "df_append_new_files", df_append_new_files)


# In[77]:


#sheet3 - out_of_stock_df
def out_of_stock_spreadsheet(df_append_new_files,gc):
    out_of_stock_df = df_append_new_files[df_append_new_files["status"] != "correcto"]
    update_spreadsheet(gc, "business_afi_scraping_last_day_files", "out_of_stock_df", out_of_stock_df)
    
    return "worksheet updated"


# In[78]:


#sheet4 - none_values_df
def non_values_spreadsheet(df_single):
    none_values = df_single[df_single["product_name"]=="none"].any().unique().tolist()
    if none_values == [True]:
        none_values_df = df_single[df_single["product_name"]=="none"]
        update_spreadsheet(gc, "business_afi_scraping_last_day_files", "none_values_df", none_values_df)
        
        return "worksheet updated"
    else:
        return "worksheet updated, but there is no any none value"


# In[ ]:




