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


# # B. p_wrangling

# ## Create the DATAFRAME

# ### a) Full DataFrame with a daily injection of the new scraped data

# In[23]:


def conection_spreadsheet(scopes, credentials_location):
    scopes = scopes
    credentials = Credentials.from_service_account_file(
        credentials_location,
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    #If we want to host our credentials in a server we have to do the next code:
    # gc = gspread.service_account(filename='https://www.path/to/the/downloaded/file.json')
    print("spreadsheet conection done")
    return gc


# #### Step 1: Create or define the dataFrame
# 
#  - From a CSV if it exists
#  - If not, from spreadsheets
#  - If not, from this notebook
#  - If not, we have to create a empty dataFrame

# In[24]:


def main_df(location,gc):
#1. From a CSV if it exists
    try:
        df_single = pd.read_csv(location)
        print("df_single created through csv")
        return df_single
    
#2. If not, from spreadsheets    
    except: #if the except is executed, the try has given an error, so it does not exist in csv (we use the spreadsheets backup)   
        try:
            sheet = gc.open("business_afi_scraping_df_single").sheet1  #Abrir spreadhseet
            data_from_spreadsheets = sheet.get_all_records()  #Obtener todos los registros
            df_single = pd.DataFrame(data_from_spreadsheets)
            print("df_single created through spreadsheet")
            return df_single
        
#3. If not, from this notebook
        except: #if the except is executed, the try has given an error, so let's see if it was already created in the notebook       
            try:
                df_single.head()
                print("df_single created through this notebook")
                return df_single
            
#4. If not, we have to create a empty dataFrame
            except: #if it gives an error, it does not exist in the notebook and we will create it from scratch
                columns = ["date_hyphen","date_slash","date_number","product_name","product_id","product_brand","price","status","url"]
                df_single = pd.DataFrame(columns=columns)
                print("df_single created through zero")
                return df_single
            else: #if there is no error, it exists in the notebook and we will do nothing
                pass
            
        else: #if it doesn't give an error, it exists in spreadsheets and we won't do anything
            pass
            
    else: #f it doesn't give an error, it exists in csv and we won't do anything
        pass


# #### Step 2: Append new records in the df_single dataFrame - pd.concat()

# In[25]:


def df_append_new_files(final_date_hyphen_products,final_date_slash_products,final_date_number_products,final_name_products,final_id_products,final_brand_products,final_price_products_list,final_price_products_status,urls_products_list):
    df_append_new_files = pd.DataFrame({
        "date_hyphen":final_date_hyphen_products,
        "date_slash":final_date_slash_products,
        "date_number":final_date_number_products,
        "product_name":final_name_products,
        "product_id":final_id_products,
        "product_brand":final_brand_products,
        "price":final_price_products_list,
        "status":final_price_products_status,
        "url": urls_products_list
    })
    df_append_new_files["price"] = df_append_new_files["price"].astype("int64")
    
    return df_append_new_files


# In[26]:


def concat_df(df_single,df_append_new_files):
    if df_single.empty == True:
        df_single = pd.concat([df_single, df_append_new_files], ignore_index=True)
        return df_single
    elif df_append_new_files["date_hyphen"][0] == df_single["date_hyphen"][len(df_single)-1]:
        return df_single
    elif df_append_new_files["date_hyphen"][0] != df_single["date_hyphen"][len(df_single)-1]:
        df_single = pd.concat([df_single, df_append_new_files], ignore_index=True)
        return df_single


# ### b) Clean and Prepare the dataFrame

# In[27]:


def corregir_gam_name(url,product_name):
    if url == "https://sillasybienestar.com/gaming/sillas-gaming/review-individual/intimate-wm-heart-gaming/" and product_name == "none":
        return "intimate wm heat  Racing Silla Gamer"
    else:
        return product_name
        
def corregir_gam_id(url,product_id):
    if url == "https://sillasybienestar.com/gaming/sillas-gaming/review-individual/intimate-wm-heart-gaming/" and product_id == "none":
        return "B075CK3GVJ"
    else:
        return product_id
        
def corregir_gam_brand(url,product_brand):
    if url == "https://sillasybienestar.com/gaming/sillas-gaming/review-individual/intimate-wm-heart-gaming/" and product_brand == "none":
        return "intimate wm heat"
    else:
        return product_brand

    
def corregir_gam_name_hbada_rep(url,product_name):
    if url == "https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/hbada-reposabrazos/" and product_name == "none":
        return "Hbada B07V51M94R"
    else:
        return product_name
        
def corregir_gam_id_hbada_rep(url,product_id):
    if url == "https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/hbada-reposabrazos/" and product_id == "none":
        return "B07V51M94R"
    else:
        return product_id
        
def corregir_gam_brand_hbada_rep(url,product_brand):
    if url == "https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/hbada-reposabrazos/" and product_brand == "none":
        return "Hbada"
    else:
        return product_brand


# In[28]:


def correction_df_single(df_single):
    #intimate wm heat  Racing Silla Gamer
    df_single["product_name"] = df_single.apply(lambda df_single: corregir_gam_name(df_single["url"], df_single["product_name"]), axis=1)
    df_single["product_id"] = df_single.apply(lambda df_single: corregir_gam_id(df_single["url"], df_single["product_id"]), axis=1)
    df_single["product_brand"] = df_single.apply(lambda df_single: corregir_gam_brand(df_single["url"], df_single["product_brand"]), axis=1)

    #Hbada B07V51M94R
    df_single["product_name"] = df_single.apply(lambda df_single: corregir_gam_name_hbada_rep(df_single["url"], df_single["product_name"]), axis=1)
    df_single["product_id"] = df_single.apply(lambda df_single: corregir_gam_id_hbada_rep(df_single["url"], df_single["product_id"]), axis=1)
    df_single["product_brand"] = df_single.apply(lambda df_single: corregir_gam_brand_hbada_rep(df_single["url"], df_single["product_brand"]), axis=1)

    return df_single


# ### c) Create the price main of each product

# In[29]:


def product_mean_dic(df_single):
    product_id_list_mean = df_single["product_id"].unique().tolist()
    mean_dic = {}
    for i in product_id_list_mean:
        mean_dic[i] = int(round(df_single[df_single["product_id"] == i]["price"].mean(),0))
    return mean_dic


# In[30]:


def product_mean_dic_to_df(df_single,product_mean):
    df_single["product_mean"] = df_single["product_id"].apply(lambda x: product_mean[x])
    return df_single


# In[31]:


def product_mean_status_func_values(product_price,product_mean):
    if product_price < product_mean and product_price > 0:
        return "precio por debajo de la media"
    elif product_price > product_mean and product_price > 0:
        return "precio por encima de la media"
    elif product_price == product_mean and product_price > 0:
        return "precio igual que la media"
    elif product_price == 0:
        return "producto descatalogado o sin stock"
    else:
        return "revisar, aviso"


# In[32]:


def product_mean_status_func_apply(df_single):
    df_single["product_mean_status"] = df_single.apply(lambda x: product_mean_status_func_values(x["price"], x["product_mean"]), axis=1)
    return df_single


# ### d) Create the category of each product

# In[33]:


def categories_url(product_url):
    if "/ergonomia/sillas-ergonomicas/review-individual/" in product_url:
        return "ergonomia"
    elif "/oficina-y-escritorio/sillas-de-oficina/review-individual/" in product_url:
        return "oficina"
    elif "/ergonomia/sillas-de-rodillas/review-individual/" in product_url:
        return "rodilla"
    elif "/gaming/sillas-gaming/review-individual/" in product_url:
        return "gaming"
    else:
        return "alerta sin categoria"


# In[34]:


def product_category(df_single):
    df_single["product_category"] = df_single["url"].apply(categories_url)
    return df_single


# ## EXPORT the dataFrames to CSVs

# In[35]:


def export_files(df_single, df_append_new_files):
    df_single_to_csv = df_single.to_csv("../files/df_single.csv", sep=",", index=False)
    df_append_new_files_to_csv = df_append_new_files.to_csv("../files/df_append_new_files_last_day.csv", sep=",", index=False)#+str(datetime.today().strftime('%Y-%m-%d'))+".csv", sep=",", index=False)
    out_of_stock_df = df_append_new_files[df_append_new_files["status"] != "correcto"]
    out_of_stock_df_to_csv = out_of_stock_df.to_csv("../files/out_of_stock_last_day.csv", sep=",", index=False)
    
    none_values = df_single[df_single["product_name"]=="none"].any().unique().tolist()
    if none_values == [True]:
        none_values_df = df_single[df_single["product_name"]=="none"]
        none_values_df_to_csv = none_values_df.to_csv("../files/non_values_last_day.csv", sep=",", index=False)
    
    return "files exported successfully"


# In[ ]:




