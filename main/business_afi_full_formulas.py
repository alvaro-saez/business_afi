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


# # A. p_acquisition

# ### SET THE CREDENTIALS

# In[2]:


load_dotenv(find_dotenv("../credentials/.env"))
email_key = os.environ.get("EMAIL_KEY") #EMAIL PASSWORD


# ### SET THE URLS IN VARIABLES

# In[3]:


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


# In[4]:


#If want to add a new URL to the "ergonomia" category
def new_url_ergo(new_url):
    urls_ergonomia.append(new_url)
    return "new url 'ergonomia' added"


# In[5]:


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


# In[6]:


#If want to add a new URL to the "oficina" category
def new_url_oficina(new_url):
    urls_oficina.append(new_url)
    return "new url 'oficina' added"


# In[7]:


urls_rodilla = [
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/duehome/",
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/himimi-silla-de-rodillas/",
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/varier/",
"https://sillasybienestar.com/ergonomia/sillas-de-rodillas/review-individual/cinius/"
]


# In[8]:


#If want to add a new URL to the "rodilla" category
def new_url_rodilla(new_url):
    urls_rodilla.append(new_url)
    return "new url 'rodilla' added"


# In[9]:


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


# In[10]:


#If want to add a new URL to the "gaming" category
def new_url_gaming(new_url):
    urls_gaming.append(new_url)
    return "new url 'gaming' added"


# In[11]:


#JOIN all the urls
def full_urls(urls_ergonomia, urls_oficina, urls_rodilla, urls_gaming):
    urls_products_list_list = urls_ergonomia + urls_oficina + urls_rodilla + urls_gaming
    return urls_products_list_list
    
urls_products_list = full_urls(urls_ergonomia, urls_oficina, urls_rodilla, urls_gaming)


# ### web scrapping

# Obtain the HTML of all our URLs

# In[12]:


def parsed_content(urls_products_list):
    parsed_products_content_list = [bs4.BeautifulSoup(requests.get(i).content, "html.parser") for i in urls_products_list]
    return parsed_products_content_list

parsed_products_content_list = parsed_content(urls_products_list)


# Obtain the price info of its class

# In[13]:


def parsed_price_class(parsed_products_content_list):
    parsed_products_price_class = [i.find_all("span",{"class":"aawp-product__price aawp-product__price--current"})[0].text for i in parsed_products_content_list]
    return parsed_products_price_class

parsed_products_price_class = parsed_price_class(parsed_products_content_list)


# Obtain the final price

# In[14]:


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

final_price_products_list = product_price(parsed_products_content_list,urls_products_list)


# Obtain if the product is out of stock or discontinued

# In[15]:


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

final_price_products_status = product_status(parsed_products_content_list,urls_products_list)


# Create a function to handle possible erros in the product information

# In[16]:


def handling_error_vars_product(i,text):
    try:
        str(i).split(text)[1]
    except:
        return "none"
    else:
        return str(i).split(text)[1].split("';")[0].strip()


# Obtain the NAME of the different products

# In[17]:


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

final_name_products = product_name(parsed_products_content_list)


# Obtain the ID of the different products

# In[18]:


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

final_id_products = product_id(parsed_products_content_list)


# Obtain the BRAND of the different products

# In[19]:


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

final_brand_products = product_brand(parsed_products_content_list)


# Obtain the DATE of the current day in different formats

# 1. With HYPHEN. Ex: 2022-04-14

# In[20]:


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

final_date_hyphen_products = product_date_hyphen(urls_products_list)


# 2. With SLASH. Ex: 2022/04/14

# In[21]:


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

final_date_slash_products = product_date_slash(urls_products_list)


# 3. Without symbols. Ex: 20220414

# In[22]:


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

final_date_number_products = product_date_number(urls_products_list)


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

gc = conection_spreadsheet(["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"], '../credentials/credentials.json')


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

df_single = main_df("../files/df_single.csv",gc)


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

df_append_new_files = df_append_new_files(final_date_hyphen_products,final_date_slash_products,final_date_number_products,final_name_products,final_id_products,final_brand_products,final_price_products_list,final_price_products_status,urls_products_list)


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
    
df_single = concat_df(df_single,df_append_new_files)


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

df_single = correction_df_single(df_single)


# ### c) Create the price main of each product (for the total period; for the last 7 days; for the last 30 days)

# In[29]:


#product mean (TOTAL DAYS)
def product_mean_dic(df_single):
    product_id_list_mean = df_single["product_id"].unique().tolist()
    mean_dic = {}
    for i in product_id_list_mean:
        if str(df_single[df_single["product_id"] == i].loc[df_single["price"] > 0]["price"].mean()) == "nan":
            mean_dic[i] = 0
        else:
            mean_dic[i] = int(round(df_single[df_single["product_id"] == i].loc[df_single["price"] > 0]["price"].mean(),0))
    return mean_dic

product_mean = product_mean_dic(df_single### b) Clean and Prepare the dataFrame
)

#product mean (LAST 7 DAYS)
def product_mean_dic7(df_single):
    product_id_list_mean7 = df_single["product_id"].unique().tolist()
    mean_dic7 = {}
    for i in product_id_list_mean7:
        if str(df_single[df_single["product_id"] == i].iloc[-7:].loc[df_single["price"] > 0]["price"].mean()) == "nan":
            mean_dic7[i] = 0
        else:
            mean_dic7[i] = int(round(df_single[df_single["product_id"] == i].iloc[-7:].loc[df_single["price"] > 0]["price"].mean(),0))
    return mean_dic7

product_mean7 = product_mean_dic7(df_single### b) Clean and Prepare the dataFrame
)

#product mean (LAST 30 DAYS)
def product_mean_dic30(df_single):
    product_id_list_mean30 = df_single["product_id"].unique().tolist()
    mean_dic30 = {}
    for i in product_id_list_mean30:
        if str(df_single[df_single["product_id"] == i].iloc[-30:].loc[df_single["price"] > 0]["price"].mean()) == "nan":
            mean_dic30[i] = 0
        else:
            mean_dic30[i] = int(round(df_single[df_single["product_id"] == i].iloc[-30:].loc[df_single["price"] > 0]["price"].mean(),0))
    return mean_dic30

product_mean30 = product_mean_dic30(df_single### b) Clean and Prepare the dataFrame
)


# In[30]:


def product_mean_dic_to_df(df_single,product_mean):
    df_single["product_mean"] = df_single["product_id"].apply(lambda x: product_mean[x])
    return df_single

df_single = product_mean_dic_to_df(df_single,product_mean)

def product_mean_dic_to_df7(df_single,product_mean7):
    df_single["product_mean7"] = df_single["product_id"].apply(lambda x: product_mean7[x])
    return df_single

df_single = product_mean_dic_to_df7(df_single,product_mean7)

def product_mean_dic_to_df30(df_single,product_mean30):
    df_single["product_mean30"] = df_single["product_id"].apply(lambda x: product_mean30[x])
    return df_single

df_single = product_mean_dic_to_df30(df_single,product_mean30)


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

df_single = product_mean_status_func_apply(df_single)


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

df_single = product_category(df_single)


# ### e) Create a "count" column

# In[35]:


def product_count(df_single):
    df_single["product_count"] = 1
    return df_single

df_single = product_count(df_single)


# ### f) Limit the the amount of data only to a year

# In[36]:


def acotar_df_un_ano(df_single):
    if len(np.sort(df_single["date_number"].unique())) > 366:
        df_single = df_single[df_single["date_number"] > np.sort(df_single["date_number"].unique())[-366]]
        return df_single
    else:
        df_single = df_single
        return df_single
    
df_single = acotar_df_un_ano(df_single)


# ## EXPORT the dataFrames to CSVs

# In[37]:


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

export = export_files(df_single, df_append_new_files)
export


# # C. p_analysis

# We are going to study the values looking for errors to create alerts via email

# ### - EMAIL ALERTS

# In[38]:


def business_afi_email_sender(receiver_email, filename_location, csv_name, body_email, email_key):

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

# In[39]:


business_afi_email_sender("businessafiliacion@gmail.com","../files/out_of_stock_last_day.csv", "out_of_stock_last_day.csv", "CSV con productos descatalogados o fuera de stock",email_key)


# #### 2) none values

# In[40]:


def email_none_values(df_single, df_append_new_files,email_key):
    none_values = df_single[df_single["product_name"]=="none"].any().unique().tolist()
    if none_values == [True]:       
        business_afi_email_sender("businessafiliacion@gmail.com", "../files/non_values_last_day.csv", "non_values_last_day.csv", "CSV con valores none",email_key)       
        return "ALERT ALVARO, exists none values"
    else:
        return "does not exist none values"


# In[41]:


email_none_values(df_single, df_append_new_files,email_key)


# #### 3) send the csv to have a backup

# In[42]:


business_afi_email_sender("businessafiliacion@gmail.com", "../files/df_single.csv", "df_single.csv", "CSV PRINCIPAL como backup con el dataframe diario con todos los datos en formato csv",email_key)


# In[43]:


business_afi_email_sender("businessafiliacion@gmail.com", "../files/df_append_new_files_last_day.csv", "df_append_new_files_last_day.csv", "CSV CON DATOS DEL DIA como backup con el dataframe diario en formato csv",email_key)


# # D. p_reporting

# We are going to send the different DataFrames to spreadsheet
# 
# #### INDEX LIBRARY
# https://docs.gspread.org/en/latest/
# 
# #### USER GUIDE
# https://docs.gspread.org/en/latest/user-guide.html

# The conection has been done in the "p_wrangling" module. The output is located in the variable "gc"

# In[44]:


def update_spreadsheet(gc, spreadsheet_name, worksheet_name, dataframe):
    #Open the spreadhseet
    sheet = gc.open(spreadsheet_name).worksheet(worksheet_name)
    
    #Clear and Update the Worksheet
    sheet.clear()
    sheet.update('A1:O1',[dataframe.columns.tolist()])
    sheet.update('A2:O' + str(len(dataframe)+1), dataframe.values.tolist())
    
    return "worksheet updated"


# In[45]:


#sheet1 - df_single
update_spreadsheet(gc, "business_afi_scraping_df_single", "df_single", df_single)


# In[46]:


#sheet2 - df_append_new_files
update_spreadsheet(gc, "business_afi_scraping_last_day_files", "df_append_new_files", df_append_new_files)


# In[47]:


#sheet3 - out_of_stock_df
def out_of_stock_spreadsheet(df_append_new_files,gc):
    out_of_stock_df = df_append_new_files[df_append_new_files["status"] != "correcto"]
    update_spreadsheet(gc, "business_afi_scraping_last_day_files", "out_of_stock_df", out_of_stock_df)
    
    return "worksheet updated"
out_of_stock_spreadsheet(df_append_new_files,gc)


# In[48]:


#sheet4 - none_values_df
def non_values_spreadsheet(df_single):
    none_values = df_single[df_single["product_name"]=="none"].any().unique().tolist()
    if none_values == [True]:
        none_values_df = df_single[df_single["product_name"]=="none"]
        update_spreadsheet(gc, "business_afi_scraping_last_day_files", "none_values_df", none_values_df)
        
        return "worksheet updated"
    else:
        return "worksheet updated, but there is no any none value"
    
non_values_spreadsheet(df_single)


# In[49]:


#df_single.head()


# In[50]:


#df_single.tail(5)


# In[51]:


#len(df_single)


# In[ ]:




