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


# # C. p_analysis

# We are going to study the values looking for errors to create alerts via email

# ### - EMAIL ALERTS

# In[2]:


def business_afi_email_sender(receiver_email, filename_location, csv_name, body_email,email_key):

    subject = "sillas y bienestar | "+ csv_name + " | " + str(datetime.today().strftime('%Y-%m-%d'))
    body = body_email 
    sender_email = "businessafiliacion@gmail.com"
    receiver_email = receiver_email
    password = email_key
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    filename = filename_location
    
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )     
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        
    return "email " + csv_name + " sended"


# #### 1) out of stock or discontinued

# In[87]:


#business_afi_email_sender("businessafiliacion@gmail.com","../files/out_of_stock_last_day.csv", "out_of_stock_last_day.csv", "CSV con productos descatalogados o fuera de stock")


# #### 2) none values

# In[70]:


def email_none_values(df_single, df_append_new_files,email_key):
    none_values = df_single[df_single["product_name"]=="none"].any().unique().tolist()
    if none_values == [True]:       
        business_afi_email_sender("businessafiliacion@gmail.com", "../files/non_values_last_day.csv", "non_values_last_day.csv", "CSV con valores none",email_key)       
        return "ALERT ALVARO, exists none values"
    else:
        return "does not exist none values"


# In[71]:


#email_none_values(df_single, df_append_new_files)


# #### 3) send the csv to have a backup

# In[72]:


#business_afi_email_sender("businessafiliacion@gmail.com", "../files/df_single.csv", "df_single.csv", "CSV PRINCIPAL como backup con el dataframe diario con todos los datos en formato csv")


# In[73]:


#business_afi_email_sender("businessafiliacion@gmail.com", "../files/df_append_new_files_last_day.csv", "df_append_new_files_last_day.csv", "CSV CON DATOS DEL DIA como backup con el dataframe diario en formato csv")


# In[ ]:




