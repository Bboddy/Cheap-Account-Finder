import os
import winsound
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def getRustPrices():
    url = "https://lolz.guru/market/steam/?game[]=252490&order_by=price_to_up"

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    driver.get("https://lolz.guru/market/steam/?game[]=252490&order_by=price_to_up")

    try: #Wait 10 seconds until the id we are looking for is found if not we close the driver
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mainContent"))
        )

        marketItems = main.find_elements_by_class_name('marketIndexItem  ')
        priceList = []
        for item in marketItems:
            price = item.find_element_by_class_name("Value")
            priceList.append(int(price.text))

        link = driver.find_element_by_class_name('marketIndexItem--Title').get_attribute('href')

        cls()
        print("Total Accounts {}.".format(len(priceList)))
        print("Account Average Price {}.".format((sum(priceList) / len(priceList))))
        print("Cheapest Accout: {}.".format(link))
        print("Account Prices:")
        print(priceList)

        return(priceList)
    finally:
        driver.quit()

first = True
accOldAverage = 99999

def findAccount(val, accAmmount):
    global first, accOldAverage
    priceList = getRustPrices()
    if accAmmount == 1:
        if priceList[0] >= val:
            print("No Cheap Accounts.")
            print("Trying Again......")
            sleep(30)
            findAccount(val, 1)
    if accAmmount > 1:
        accTotal = 0
        for i in range(accAmmount):
            accTotal = accTotal + priceList[i]
        accAverage = accTotal / accAmmount
        print("Account Average: {}.".format(accAverage))
        if first == True:
            first = False
            accOldAverage = accAverage
            print("Account Average Set")
        if accOldAverage >= accAverage:
            print("Old Account Average: {}.".format(accOldAverage))
            print("No new accounts in range ({}).".format(accAmmount))
            print("Trying Again......")
            sleep(30)
            findAccount(val, accAmmount)
    winsound.Beep(600 , 200)
    sleep(0.1)
    winsound.Beep(600 , 200)
    sleep(0.1)
    winsound.Beep(600 , 200)
    print("Cheap Account Found!")

accType = str(input("Do you want the cheapest account? Y/N:"))
if accType == "Y":
    val = int(input("Enter your min price: "))
    findAccount(val, 1)
else:
    accAmmount = int(input("Number of accounts:"))
    findAccount(0, accAmmount)