
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import time
import os
import shutil
from selenium.webdriver import EdgeOptions
from Logger.logging import App_Logger
from selenium.webdriver.chrome.options import Options

log_obj = App_Logger()

def scrap_data(year):
    """This function accepts int input (year) and scrap nifty 50 data from year to today date and saves in csv format and returns pandas dataframe"""
    try:
        current_year = int(date.today().year)
        #Year = int(input("Enter Year greater then 2000 : "))
        Year = int(year)
        while((Year>current_year or Year<2000)):
            Year = int(input("Enter Year greater then 2000 : "))
        option = EdgeOptions()
        option.headless = True
        browser = webdriver.Edge(options=option)
        browser.get('https://in.investing.com/indices/s-p-cnx-nifty-historical-data')
        browser.maximize_window()
        time.sleep(5)
        calender = browser.find_element(By.XPATH,"//button[@class='js-dropdown-display select']")
        calender.click()
        time.sleep(1)
        start_date = browser.find_element(By.XPATH,"//div[@class='design-select u-margin-start-auto']//input[@class='select js-date-from']")
        start_date.clear()
        time.sleep(2)
        string = '01/01/'+str(Year)
        start_date.send_keys(string)
        time.sleep(1)
        apply = browser.find_element(By.XPATH, "//button[@class='js-apply-button common-button']")
        apply.click()
        time.sleep(4)
        df = pd.read_html(browser.find_element(By.XPATH, "//table").get_attribute('outerHTML'))[0]
        df = df.sort_index(ascending=False)
        df = df.reset_index(drop=True)

        file_name = f"Data/Scraped Data/Nifty-50_Data_from_{Year}-01-01_to_{date.today()}.csv"
        if(file_name not in os.listdir("Data")):
            df.to_csv(file_name,index=False)
        return df
        #input()

    except Exception as e:
        exit()
        return(e)


# https://www.investing.com/equities/state-bank-of-india-historical-data
# https://www.investing.com/equities/tata-motors-ltd-historical-data
def generate_name(name):
    """Function accepts a string(name) and scrap stock data specific to name from investing.com and returns pandas dataframe"""
    # name = "SBIN"
    data = pd.read_csv(r"Data/Static Data/EQUITY.csv")
    full_name = (data[data['SYMBOL']==name].values[0][1])
    lst = list()
    for i in full_name.split(" "):
        if (i.lower()=="limited"):
            lst.append("ltd")
        else:
            lst.append(i.lower())
    name = "-".join(lst)
    return name


def check_browser():
    """Returns the name of default browser"""
    from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
    register_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
    with OpenKey(HKEY_CURRENT_USER, register_path) as key:
        name = (QueryValueEx(key, 'ProgId')[0].lower())
    return name

# https://in.investing.com/equities/state-bank-of-india-historical-data
def scrap_data_by_name(name):

    if name!="":
        try:
            name = str(name).upper()
            url = f"https://in.investing.com/equities/{generate_name(name)}-historical-data"
            year = (date.today().year)-2
            # options = webdriver.EdgeOptions( )
            # options.add_argument("start-maximized")
            # options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # options.add_experimental_option('useAutomationExtension', False)
            # browser = webdriver.Edge(options=options, executable_path=r"Income Prediction/My Project/msedgedriver.exe")

            if "edge" in check_browser():
                browser = webdriver.Edge()
            elif "chrome" in check_browser():
                browswer = webdriver.Chrome()
            elif "firefox" in check_browser():
                browser = webdriver.Firefox()
            elif "safari" in check_browser():
                browser = webdriver.Safari()
            header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
            browser.get(url)
            time.sleep(1)
            browser.maximize_window()
            time.sleep(1)
            set_date = browser.find_element(By.XPATH,r"//button[@class='js-dropdown-display select']")
            time.sleep(1)
            set_date.click()
            time.sleep(1)
            start_date = browser.find_element(By.XPATH,
                                              "//div[@class='design-select u-margin-start-auto']//input[@class='select js-date-from']")
            start_date.clear()
            time.sleep(1)
            string = '01/01/' + str(year)
            start_date.send_keys(string)
            time.sleep(1)
            apply = browser.find_element(By.XPATH, "//button[@class='js-apply-button common-button']")
            time.sleep(1)
            apply.click()
            time.sleep(4)
            df = pd.read_html(browser.find_element(By.XPATH, "//table").get_attribute('outerHTML'))[0]
            df = df.sort_index(ascending=False)
            df = df.reset_index(drop=True)
            if (len(os.listdir("Data/Scraped Data")) != 0):
                source = 'Data/Scraped Data'
                destination = 'Archieve_Files'
                # gather all files
                allfiles = os.listdir(source)
                # iterate on all files to move them to destination folder
                for f in allfiles:
                    if f"{name}.csv" in os.listdir('Archieve_Files'):
                        # os.remove(f"Archieve_Files/{name}.csv")
                        file_to_move = os.listdir("Data/Scraped Data")[0]
                        shutil.move(f"Data/Scraped Data/{file_to_move}", f"Archieve_Files/{file_to_move}")
                    else:
                        file_to_move = os.listdir("Data/Scraped Data")[0]
                        shutil.move(f"Data/Scraped Data/{file_to_move}", f"Archieve_Files/{file_to_move}")
            # file_name = f"Data/Scraped Data/{name}.csv"
            file_name = f"{name}.csv"
            if (file_name in os.listdir("Data/Scraped Data")):
                os.remove(f"Data/Scraped Data/{file_name}")
                df.to_csv(f"Data/Scraped Data/{file_name}", index=False)
            else:
                df.to_csv(f"Data/Scraped Data/{file_name}", index=False)
            return df

        except Exception as e:
            return e


def scrap_data_from_yahoo_finance(symbol):
    """This function scrps data from yahoo finance webise for given stock ticker symbol , returns pandas dataframe and saves in csv format"""
    try:
        log_obj.log("Entered function scrap_data_from_yahoo_finance")
        # converting passed symbol to uppercase and checking if symbol is valid or not
        symbol = symbol.upper()
        name  = symbol
        # tickers = pd.read_csv(r"Data/Static Data/EQUITY.csv")
        # while not (tickers['SYMBOL'].eq(symbol)).any():
        #     symbol = input("Enter valid Stock Ticker : ").upper()

        # creating webdriver object
        log_obj.log("converted ticker name and opened browswer fro scrapping using webdriver")

        browser = webdriver.Edge()
        browser.maximize_window()
        if (symbol == 'NIFTY' or symbol == 'BANKNIFTY'):
            if (symbol == 'NIFTY'):
                browser.get(f"https://finance.yahoo.com/quote/%5ENSEI/history?p=%5ENSEI")
            elif(symbol=='BANKNIFTY'):
                browser.get(f"https://finance.yahoo.com/quote/%5ENSEBANK/history?p=%5ENSEBANK")
        else:
            browser.get(f"https://finance.yahoo.com/quote/{symbol}.NS/history?p={symbol}.NS")
        # time.sleep(10)

        # clicking on maybe later banner
        e = "error"
        while (e == "error"):
            try:
                close_button = browser.find_element(By.XPATH,
                                                    "//button[@class='Mx(a) Fz(16px) Fw(600) Mt(20px) D(n)--mobp']")
                close_button.click()
                e = "Not"
                log_obj.log("Clicked on Maybe Later button of banner on webpage")
            except Exception as e:
                time.sleep(1)
                print(1)
                e = "error"

        # clicking on calender option.
        calendar = browser.find_element(By.XPATH,"//span[@class='C($linkColor) Fz(14px)']")
        calendar.click()
        time.sleep(1)
        log_obj.log("clicked on calender element ")
        # clicking on 5year button and apply button.
        year_5 = browser.find_element(By.XPATH,"//span[normalize-space()='5Y']")
        year_5.click()
        log_obj.log("clicked on 5 Year element ")
        apply = browser.find_element(By.XPATH,"//button[contains(@class,'Py(9px) Fl(end)')]")
        apply.click()
        log_obj.log("clicked Apply button element ")
        time.sleep(5)

        # scrolling webpage to the end.
        count = 0
        while count!=16 :
            px = 100000000000
            time.sleep(1)
            count+=1
            browser.execute_script(f"window.scrollBy(0,{px})")
        log_obj.log("Scrolling Done till end of page")


        # getting the data frame
        df = pd.read_html(browser.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table').get_attribute('outerHTML'))[0]
        df = df.sort_index(ascending=False)
        df = df.reset_index(drop=True)
        df = df[1:]
        df.rename(columns={"Close*": "Price"}, inplace=True)
        df = (df[df["Price"].str.contains("Dividend")==False])
        df = (df[df["Price"].str.contains("Split") == False])
        df = (df[df["Volume"].str.contains("-") == False])
        df = df[["Date","Price","Volume"]]

        log_obj.log("Scrapped table from webpage")

        # saving csv file
        if (len(os.listdir("Data/Scraped Data")) != 0):
            log_obj.log("Entered Mechanism to save and move CSV files from folders")
            source = 'Data/Scraped Data'
            destination = 'Archieve_Files'
            # gather all files
            allfiles = os.listdir(source)
            # iterate on all files to move them to destination folder
            for f in allfiles:
                if f"{name}.csv" in os.listdir('Archieve_Files'):
                    # os.remove(f"Archieve_Files/{name}.csv")
                    file_to_move = os.listdir("Data/Scraped Data")[0]
                    shutil.move(f"Data/Scraped Data/{file_to_move}", f"Archieve_Files/{file_to_move}")
                else:
                    file_to_move = os.listdir("Data/Scraped Data")[0]
                    shutil.move(f"Data/Scraped Data/{file_to_move}", f"Archieve_Files/{file_to_move}")
        # file_name = f"Data/Scraped Data/{name}.csv"
        file_name = f"{name}.csv"
        if (file_name in os.listdir("Data/Scraped Data")):
            os.remove(f"Data/Scraped Data/{file_name}")
            df.to_csv(f"Data/Scraped Data/{file_name}", index=False)
        else:
            df.to_csv(f"Data/Scraped Data/{file_name}", index=False)
            log_obj.log("Saved File and data frame returned by the function ends")
        return df

    except Exception as e:
        log_obj.log(f"Entered Exception block of yahoo scraping function {e}")
        return e



if __name__== "__main__":
    print(scrap_data_from_yahoo_finance('advenzymes'))
