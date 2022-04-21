#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# # A. p_acquisition

# ### SET THE CREDENTIALS

# In[4]:


load_dotenv(find_dotenv("../credentials/.env"))
email_key = os.environ.get("EMAIL_KEY") #EMAIL PASSWORD


# ### SET THE URLS IN VARIABLES

# In[5]:


urls_ergonomia = [
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/tlv-myx-801-1/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/songmics-obn55bk/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/cashoffice-silla-ergonomica/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/cedric/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/noblewell/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/sihoo-lb14/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/ronda-silla-espanola/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/diablo-v-master/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/diablo-v-basic/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/songmics-obn61bkv1/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/hbada-reposapies/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/songmics-obn86bk/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/femor/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/hbada-reposabrazos/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/mfavour/",
"https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/umi/"   
]


# In[6]:


#If want to add a new URL to the "ergonomia" category
def new_url_ergo(new_url):
    urls_ergonomia.append(new_url)
    return "new url 'ergonomia' added"


# In[7]:


urls_oficina = [
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/songmics-obn52bk/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/songmics-obn22bk/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/allguest-cedric/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/hbada-hdny108bm-eu/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/intimate-wm-heart-sillon-b07x8tqh96/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/vinsetto-sillon-de-oficina-azul-claro/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/exofcer-mc6310/",
"https://sillasybienestar.com/oficina-y-escritorio/sillas-de-oficina/review-individual/songmics-obg24b/"
]


# In[8]:


#If want to add a new URL to the "oficina" category
def new_url_oficina(new_url):
    urls_oficina.append(new_url)
    return "new url 'oficina' added"


# In[9]:


urls_rodilla = [
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/duehome/",
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/himimi-silla-de-rodillas/",
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/varier/",
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/cinius/"
]


# In[10]:


#If want to add a new URL to the "rodilla" category
def new_url_rodilla(new_url):
    urls_rodilla.append(new_url)
    return "new url 'rodilla' added"


# In[11]:


urls_gaming = [
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/gtplayer-rosa/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/diablo-x-gamer-2-0/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/intimate-wm-heart-silla-gamer-barata/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/nokaxus-yk-6008-rosa/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/newskill-nayuki/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/silla-gamer-bgeu-a136-sencillez-y-buen-precio-ofertas-2021/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/autofull-pink-bunny/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/adec-drw/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/femor-gaming/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/hbada-gaming-hdjy001bmj-cb/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/intimate-wm-heart-gaming/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/corsair-t3-rush/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/dxracer-king-ks06/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/diablo-x-horn/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/diablo-x-ray/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/dxracer-formula-f08/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/newskill-kitsune/",
"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/newskill-takamikura/"
#"https://sillasybienestar.com/gaming/sillas-gaming/review-individual/songmics-racing/" - no usamos
]


# In[12]:


#If want to add a new URL to the "gaming" category
def new_url_gaming(new_url):
    urls_gaming.append(new_url)
    return "new url 'gaming' added"


# In[13]:


#JOIN all the urls
def full_urls(urls_ergonomia, urls_oficina, urls_rodilla, urls_gaming):
    urls_products_list_list = urls_ergonomia + urls_oficina + urls_rodilla + urls_gaming
    return urls_products_list_list


# ### web scrapping

# Obtain the HTML of all our URLs

# In[14]:


def parsed_content(urls_products_list):
    parsed_products_content_list = [bs4.BeautifulSoup(requests.get(i).content, "html.parser") for i in urls_products_list]
    return parsed_products_content_list


# Obtain the price info of its class

# In[15]:


def parsed_price_class(parsed_products_content_list):
    parsed_products_price_class = [i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text for i in parsed_products_content_list]
    return parsed_products_price_class


# Obtain the final price

# In[16]:


def product_price(parsed_products_content_list,urls_products_list):
    final_price_products_list =[]
    for i,e in zip(parsed_products_content_list, range(len(urls_products_list))):
        try:
            i.find_all("div",{"class":"wp-block-media-text__content"})[0]
            #if it fails the except is executed
        except:
            if  urls_products_list[e] == "https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/mfavour/":
                price_supuesto_0 = i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text
                price_supuesto_0_cleaned = re.sub("[^\d|\,]","",str(price_supuesto_0)).replace(",",".")
                final_price_products_list.append(float(price_supuesto_0_cleaned))
            else:
                final_price_products_list.append(-1)
                print("revisar funcion price, valor con -1")
        else:
            if i.find_all("div",{"class":"wp-block-media-text__content"})[0].text.strip() == "No products found.":
                final_price_products_list.append(0)
            elif i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text == "":
                final_price_products_list.append(0)
            elif i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text != "":
                price_supuesto_1 = i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text
                price_supuesto_1_cleaned = re.sub("[^\d|\,]","",str(price_supuesto_1)).replace(",",".")
                final_price_products_list.append(float(price_supuesto_1_cleaned))
            else:
                print("revisar funcion price")
    return final_price_products_list


# Obtain if the product is out of stock or discontinued

# In[17]:


def product_status(parsed_products_content_list,urls_products_list):
    final_price_products_status =[]
    for i,e in zip(parsed_products_content_list, range(len(urls_products_list))):
        try:
            i.find_all("div",{"class":"wp-block-media-text__content"})[0]
            #if it fails the except is executed
        except:
            if  urls_products_list[e] == "https://sillasybienestar.com/ergonomia/sillas-ergonomicas/review-individual/mfavour/":
                final_price_products_status.append("correcto")
            else:
                print("revisar funcion price, valor con -1")
                final_price_products_status.append("revisar")
        else:
            if i.find_all("div",{"class":"wp-block-media-text__content"})[0].text.strip() == "No products found.":
                final_price_products_status.append("descatalogado")
            elif i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text == "":
                final_price_products_status.append("sin_stock")
            elif i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text != "":
                final_price_products_status.append("correcto")
            else:
                print("revisar funcion price")
    return final_price_products_status


# Create a function to handle possible erros in the product information

# In[18]:


def handling_error_vars_product(i,text):
    try:
        str(i).split(text)[1]
    except:
        return "none"
    else:
        return str(i).split(text)[1].split("';")[0].strip()


# Obtain the NAME of the different products

# In[19]:


def product_name(parsed_products_content_list):
    
    def handling_error_vars_product(i,text):
        try:
            str(i).split(text)[1]
        except:
            return "none"
        else:
            return str(i).split(text)[1].split("';")[0].strip()
    
    final_name_products = [handling_error_vars_product(i,"ficha_product_name='") for i in parsed_products_content_list]
    return final_name_products


# Obtain the ID of the different products

# In[20]:


def product_id(parsed_products_content_list):

    def handling_error_vars_product(i,text):
        try:
            str(i).split(text)[1]
        except:
            return "none"
        else:
            return str(i).split(text)[1].split("';")[0].strip()
        
    final_id_products = [handling_error_vars_product(i,"ficha_product_id='") for i in parsed_products_content_list]
    return final_id_products


# Obtain the BRAND of the different products

# In[21]:


def product_brand(parsed_products_content_list):

    def handling_error_vars_product(i,text):
        try:
            str(i).split(text)[1]
        except:
            return "none"
        else:
            return str(i).split(text)[1].split("';")[0].strip()
    
    final_brand_products = [handling_error_vars_product(i,"ficha_product_brand='") for i in parsed_products_content_list]
    return final_brand_products


# Obtain the DATE of the current day in different formats

# 1. With HYPHEN. Ex: 2022-04-14

# In[22]:


def product_date_hyphen(urls_products_list):

    def handling_error_vars_product(i,text):
        try:
            str(i).split(text)[1]
        except:
            return "none"
        else:
            return str(i).split(text)[1].split("';")[0].strip()
        
    final_date_hyphen_products = [datetime.today().strftime('%Y-%m-%d') for i in range(len(urls_products_list))]
    return final_date_hyphen_products


# 2. With SLASH. Ex: 2022/04/14

# In[23]:


def product_date_slash(urls_products_list):

    def handling_error_vars_product(i,text):
        try:
            str(i).split(text)[1]
        except:
            return "none"
        else:
            return str(i).split(text)[1].split("';")[0].strip()
        
    final_date_slash_products = [datetime.today().strftime('%Y/%m/%d') for i in range(len(urls_products_list))]
    return final_date_slash_products


# 3. Without symbols. Ex: 20220414

# In[24]:


def product_date_number(urls_products_list):

    def handling_error_vars_product(i,text):
        try:
            str(i).split(text)[1]
        except:
            return "none"
        else:
            return str(i).split(text)[1].split("';")[0].strip()
        
    final_date_number_products = [int(datetime.today().strftime('%Y%m%d')) for i in range(len(urls_products_list))]
    return final_date_number_products


# In[ ]:





# In[ ]:




