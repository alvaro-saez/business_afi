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
    
- Install [numpy](https://numpy.org/doc/stable/reference/index.html) library. Copy and paste next command in your master branch:
    ```
    conda install numpy
    ```
    
- Install [requests](https://docs.python-requests.org/en/latest/) library. Copy and paste next command in your master branch:
    ```
    conda install -c anaconda requests
    ```
    
- Install [bs4](https://pypi.org/project/beautifulsoup4/) library. Copy and paste next command in your master branch:
    ```
    conda install -c anaconda beautifulsoup4
    ```
    
- Install [re](https://docs.python.org/3/library/re.html) library. Copy and paste next command in your master branch:
    ```
    conda install -c conda-forge regex
    ```
- Install [datetime](https://docs.python.org/3/library/datetime.html) library. Copy and paste next command in your master branch:
    ```
    conda install -c trentonoliphant datetime
    ```

- Install [gspread](https://docs.gspread.org/en/latest/) library. Copy and paste next command in your master branch:
    ```
    conda install -c conda-forge gspread
    ```
   
- Install [dotenv](https://pypi.org/project/python-dotenv/) library. Copy and paste next command in your master branch:
    ```
    conda install -c conda-forge python-dotenv
    ```
 
_**LIBRARIES WITHOUT A MANUAL INSTALLATION:**_

The nest libraries are a built-in package for both python2.7 and python3.x, so there is no need for installation. You can import them without installing any other package.

- Import [email, smtplib, ssl](https://docs.python.org/es/3/library/email.examples.html) library.

- Import [os](https://docs.python.org/3/library/os.html) library.


### :runner: **STEPS:**

1. **PYTHON:**
   a) **_p_acquisition:_**
      - set the URLS for the web scrapping
      - set the credentials with the passwords to can make the API connections
      - make the web scrapping
      - create the different datetime formats

   b) **_p_wrangling:_**
      - make the connection with Google Spreadsheet
      - Create or define the MAIN dataFrame (a single dataframe which will contain all the daily records):
        - From a CSV if it exists
        - If not, from spreadsheets
        - If not, from this notebook
        - If not, we have to create a empty dataFrame
      - Create a second dataFrame with only the daily scrapped data (each day will replace the previous day's data)
      - Append the daily scrapped data into the Main dataFrame
      - Clean and Prepare the Main dataFrame
      - Create new columns
      - Limit the the amount of data only to a year to avoid the limits of Spreadsheets and to avoid to have huge CSVs
      - Export the dataFrames to CSVs 

    c) **_p_analysis:_**
      - study the values looking for errors to create alerts via email:
        - out of stock or discontinued products alert
        - none values alert
        - send the CSVs via email to have a backup
 
    d) **_p_reporting:_**
      - send the different dataFrames to spreadsheet:
        - sheet1: MAIN dataFrame
        - sheet2 | worksheet 1: daily scrapped data dataFrame
        - sheet2 | worksheet 2: out of stock or discontinued dataFrame
        - sheet2 | worksheet 3: none values dataFrame
        
2. **create spreadsheets and datastudio connection:**
<p align="center"><img src="https://github.com/alvaro-saez/business_afi/blob/main/imgs/SPREADSHEET.png"></p>

4. **embed the different charts in wordpress:**
- a chart with the evolution of the prices in a 7 days window:
<p align="center"><img src="https://github.com/alvaro-saez/business_afi/blob/main/imgs/graf_7.png"></p>

- a chart with the evolution of the prices in a 30 days window:
<p align="center"><img src="https://github.com/alvaro-saez/business_afi/blob/main/imgs/graf_31.png"></p>

- _NEXT STEP_ --> a chart with the evolution of the prices in a whole year window
<p align="center"><img src="https://github.com/alvaro-saez/business_afi/blob/main/imgs/work_in_progress_clip_art.jpg"></p>
 
