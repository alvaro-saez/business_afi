# Sillas y Bienestar - Temporary evolution of prices to improve the web site user experience

www.sillasybienestar.com is a website which advises users about how to buy the best ergonomic chair on the market.

<p align="center"><img src="https://github.com/alvaro-saez/business_afi/blob/main/imgs/logo-name-current.png"></p>

###  :flags: Objectives - Problems to solve:

There are two stakeholders who will benefit from this solution:

 - _**USERS**_: 
  1. Amazon uses to change the price or their products with a high frequence, so this proyect aims to create a temporary price chart to embed on the web to improve the user experience and help them make the purchase decision.
  2. Create product alerts with a price lower than the average to warn users of "bargains".
 
 - _**WEB SITE ADMINS**_: 
  3. Create email product alerts about "out of stock" or "discontinued" product status which help the admins to make a decision about keeping the product in production or not.
  4. Create a online database to analyce the product price evolution, make different dashboards and detect errors in the "dataLayer".


###  :computer: Technology stack:

- _**Python**_: as a language to develop a script that does **web scraping**, **cleans** and **prepares** the data and **communicates** via API with the different tools.
- _**Online Server**_: to **allocate** the scripts and CSVs and to automate its **daily execution**.
- _**Spreadsheets**_: to upload the different dataframes resulting from the python script and also to be the **main data source** of the BI tool.
- _**Gmail**:_ to send **alerts** and to have a **daily backup** of the resulting csv.
- _**Datastudio**_: as a **dashboarding tool** to create a temporary price graph which will be embeded into the web site.
- _**Wordpress**_: as a **content management system**.


### :books: **Dependencies:**

- _ADVISE:_ Create a virtual environment with the version of Python you're going to use and the different libraries.
- This repository is tested on **Python 3.7+**.

- Install [pandas](https://pandas.pydata.org/docs/user_guide/index.html) library. Copy and paste next command in your master branch:
    ```
    conda install pandas
    ```
