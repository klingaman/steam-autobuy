from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
import sys

# Set Values:  #
################
link = "https://steamcommunity.com/market/listings/730/SSG%2008%20%7C%20Acid%20Fade%20%28Factory%20New%29" # Item Link 
minfloat = 0.009 # Minimum Float
minprice = 1.45  # Minimum Price
s = 60           # Sleep Interval Seconds when No Matches
################

def run():
    chrome_options = Options()
    chrome_options.add_extension('a.crx') # https://chrome.google.com/webstore/detail/csgofloat-market-checker/jjicbefpemnphinccgikpdaagjebbnhg
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    input("Press [Enter] when logged into Steam: ")
    
    while True:
        try:
            driver.get(link)
            time.sleep(1)
            pagesize = driver.find_element_by_id("pageSize")
            pagesize.click()
            for i in range(4):
                pagesize.send_keys(Keys.DOWN)
            pagesize.send_keys(Keys.ENTER)
            time.sleep(3)
            
            x = driver.find_elements_by_class_name("csgofloat-itemfloat")
            y = driver.find_elements_by_class_name("market_listing_price_with_fee")
            z = driver.find_elements_by_class_name("item_market_action_button")
            a = []
            b = []
            for i in x:
                new = float((re.findall(r"[-+]?\d*\.\d+|\d+",(i.text)))[0])
                a.append(new)
            for i in y:
                try:
                    new = float((re.findall(r"[-+]?\d*\.\d+|\d+",(i.text)))[0])
                except:
                    new = 9999
                b.append(new)

            for i in range(len(b)):
                if b[i] <= minprice:
                    if a[i] <= minfloat:
                        z[i].click()
                        agreement = driver.find_element_by_id("market_buynow_dialog_accept_ssa")
                        agreement.click()
                        purchase = driver.find_element_by_id("market_buynow_dialog_purchase")
                        purchase.click()
                        time.sleep(1)
                        print("[Item Bought]     Price: $"+str(b[i])+"     Float: "+str(a[i]))
                else:
                    print("[No Matching Items]")
                    break
            time.sleep(s)
        except:
            print("[ERROR]", sys.exc_info()[0])
            
def main():
    print("###################\n#  STEAM AUTOBUY  #\n###################\n\n")
    run()
    driver.quit()
main()
