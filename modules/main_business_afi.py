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


# In[2]:


import p_acquisition as ac
import p_wrangling as wr
import p_analysis as an
import p_reporting as rp


# In[3]:


load_dotenv(find_dotenv("../credentials/.env"))
email_key = os.environ.get("EMAIL_KEY")


# In[4]:


if __name__ == "__main__":

    def main_dataset(email_key):
        #p_acquisition
        load_dotenv(find_dotenv("../credentials/.env"))
        email_key = os.environ.get("EMAIL_KEY")
        urls_ergonomia = ac.urls_ergonomia
        urls_oficina = ac.urls_oficina
        urls_rodilla = ac.urls_rodilla
        urls_gaming = ac.urls_gaming
        urls_products_list = ac.full_urls(urls_ergonomia, urls_oficina, urls_rodilla, urls_gaming)
        parsed_products_content_list = ac.parsed_content(urls_products_list)
        parsed_products_price_class = ac.parsed_price_class(parsed_products_content_list)  
        final_price_products_list = ac.product_price(parsed_products_content_list,urls_products_list)
        final_price_products_status = ac.product_status(parsed_products_content_list,urls_products_list)
        final_name_products = ac.product_name(parsed_products_content_list)
        final_id_products = ac.product_id(parsed_products_content_list)
        final_brand_products = ac.product_brand(parsed_products_content_list)
        final_date_hyphen_products = [datetime.today().strftime('%Y-%m-%d') for i in range(len(urls_products_list))]
        final_date_slash_products = [datetime.today().strftime('%Y/%m/%d') for i in range(len(urls_products_list))]
        final_date_number_products = [int(datetime.today().strftime('%Y%m%d')) for i in range(len(urls_products_list))]
        
        #p_wrangling
        gc = wr.conection_spreadsheet(["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"], '../credentials/credentials.json')  
        df_single = wr.main_df("../files/df_single.csv",gc)
        df_append_new_files = wr.df_append_new_files(final_date_hyphen_products,final_date_slash_products,final_date_number_products,final_name_products,final_id_products,final_brand_products,final_price_products_list,final_price_products_status,urls_products_list)
        df_single = wr.concat_df(df_single,df_append_new_files)
        df_single = wr.correction_df_single(df_single)
        product_mean = wr.product_mean_dic(df_single)### b) Clean and Prepare the dataFrame
        df_single = wr.product_mean_dic_to_df(df_single,product_mean)
        df_single = wr.product_mean_status_func_apply(df_single)
        df_single = wr.product_category(df_single)
        export = wr.export_files(df_single, df_append_new_files)
        
        #p_analysis
        an.business_afi_email_sender("businessafiliacion@gmail.com","../files/out_of_stock_last_day.csv", "out_of_stock_last_day.csv", "CSV con productos descatalogados o fuera de stock",email_key)
        an.email_none_values(df_single, df_append_new_files,email_key)
        an.business_afi_email_sender("businessafiliacion@gmail.com", "../files/df_single.csv", "df_single.csv", "CSV PRINCIPAL como backup con el dataframe diario con todos los datos en formato csv",email_key)
        an.business_afi_email_sender("businessafiliacion@gmail.com", "../files/df_append_new_files_last_day.csv", "df_append_new_files_last_day.csv", "CSV CON DATOS DEL DIA como backup con el dataframe diario en formato csv",email_key)

        #p_reporting
        rp.update_spreadsheet(gc, "business_afi_scraping_df_single", "df_single", df_single)
        rp.update_spreadsheet(gc, "business_afi_scraping_last_day_files", "df_append_new_files", df_append_new_files)
        rp.out_of_stock_spreadsheet(df_append_new_files,gc)
        rp.non_values_spreadsheet(df_single)
        
#EXECUTION OF THE MAIN FUNCTION
    main_dataset(email_key)

