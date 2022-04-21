#!/usr/bin/env python
# coding: utf-8

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
update_spreadsheet(gc, "business_afi_scraping_df_single", "df_single", df_single)


# In[76]:


#sheet2 - df_append_new_files
update_spreadsheet(gc, "business_afi_scraping_last_day_files", "df_append_new_files", df_append_new_files)


# In[77]:


#sheet3 - out_of_stock_df
def out_of_stock_spreadsheet(df_append_new_files):
    out_of_stock_df = df_append_new_files[df_append_new_files["status"] != "correcto"]
    update_spreadsheet(gc, "business_afi_scraping_last_day_files", "out_of_stock_df", out_of_stock_df)
    
    return "worksheet updated"
out_of_stock_spreadsheet(df_append_new_files)


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
    
non_values_spreadsheet(df_single)


# In[ ]:




