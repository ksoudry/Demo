import inspect
import os
import logging
import time

import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#load bit (To change system please change SystemNumber,UserName , PassWord , App & Page links)
SystemNumber = "500000"
UserName = "ksoudry"
PassWord = "c_6qDyYEgopk"
App = "https://staging.na4.bitdms.net/onlineapp/"
PageSitePaths = ("https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=run_parts_reports.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=create_close_otc_invoice.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=cashRec.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=create_close_otc_invoice.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/financemodulex.php?theXml=create_deal.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=view_stock_order.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/financemodulex.php?theXml=add_modify_prospect.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/servicemodulex.php?theXml=create_close_wo.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/settingsmodulex.php?theXml=modify_dealer_parameters.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=view_inventory_screen.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=priceUpdate.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/servicemodulex.php?theXml=create_modify_packages.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=interchange.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/servicemodulex.php?theXml=BOAT.xml&type=BOAT",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=add_modify_cust.xml",
                 "https://staging.na4.bitdms.net/onlineapp/mainmenu/financemodulex.php?theXml=fi_salestax.xml",)

@pytest.mark.usefixtures("setup")
class BaseClass:
   # pass

   #@pytest.fixture(params=[(SystemNumber,UserName,PassWord,App)])
   def getData(self,Pagenum):
       data = {"SystemNumber": SystemNumber,"UserName": UserName,"PassWord": PassWord,"App": App}#dictionary

       # Log in to the system
       # Navigate to the login page
       self.driver.get(data["App"])

       # enter system number
       self.driver.find_element(By.CSS_SELECTOR, "#business").send_keys(data["SystemNumber"])
       self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()

       # Wait for the second window to be available
       wait = WebDriverWait(self.driver, 10)  # Maximum wait time of 10 seconds
       windows_open = wait.until(EC.number_of_windows_to_be(2))

       # click popup allowed in child window
       windowsOpen = self.driver.window_handles  # list of open windows from the first window that was opend in list [0]
       #
       if len(windowsOpen) > 1:
           self.driver.switch_to.window(windowsOpen[1])  # switch to another window
       else:
           print("Not enough windows open to switch.")

       # click on check box
       self.driver.find_element(By.CSS_SELECTOR, "#popupAllowed").click()

       # close child window
       # driver.close()

       # go back to parent first window
       self.driver.switch_to.window(windowsOpen[0])
       # cookies??
       try:
           # enter user name
           self.driver.find_element(By.CSS_SELECTOR, "#user").send_keys(data["UserName"])
           # enter pass word
           self.driver.find_element(By.CSS_SELECTOR, "#pass").send_keys(data["PassWord"])
           # click on submit
           self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()
       except:
           print("Error: loading page , run test again")
           self.driver.quit()

       time.sleep(5)
       try:
           # if you get the goLogout page
           goLogout = self.driver.find_element(By.CSS_SELECTOR, "#goLogout").text
           # get substring Login Failed
           textfailed = goLogout[0:12]
           if textfailed == "Login Failed":
               self.driver.find_element(By.XPATH, "//button[text()='Yes']").click()
               self.driver.refresh()
               # Navigate to the login page
               self.driver.get(data["App"])
               time.sleep(3)  # to give the pop up time to load...
               # enter system number
               self.driver.find_element(By.CSS_SELECTOR, "#business").send_keys(data["SystemNumber"])
               self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()

               # enter user name
               self.driver.find_element(By.CSS_SELECTOR, "#user").send_keys(data["UserName"])
               # enter pass word
               self.driver.find_element(By.CSS_SELECTOR, "#pass").send_keys(data["PassWord"])
               # click on submit
               self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()

               time.sleep(12)#to let storage table load
               # click on submit
               self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()
               time.sleep(10)
               # Wait for the dialog to appear
               wait = WebDriverWait(self.driver, 50)

               # Wait until an element is located
               element = wait.until(EC.presence_of_element_located((By.ID, "_priceUpdates")))
               # Wait until an element is visible
               #element_visible = wait.until(EC.visibility_of_element_located((By.ID, "_priceUpdates")))
               delay = 20  # second
               try:
                   element_visible = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.ID, '_priceUpdates')))
                   print("Page is ready!")
               except TimeoutException:
                   print("Loading took too much time!")
                   self.driver.quit()

               dialog = wait.until(EC.presence_of_element_located((By.ID, "myConfirmDlg0")))

               if dialog:
                   # Wait for the "Dismiss" button to be clickable
                   dismiss_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Dismiss']")))
               else:
                   print("No myConfirmDlg0 dialog")

               if element_visible and dialog:
                   # Click the "Dismiss" button
                   dismiss_button.click()
               else:
                   print("No myConfirmDlg0 dialog and _priceUpdates")

               if element:
                   time.sleep(5)
                   # go to next page
                   self.driver.get(PageSitePaths[Pagenum])
               else:
                   print("next page not loaded")
           else:# textfailed != "Login Failed"
               time.sleep(12)
               self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()
               time.sleep(10)

               wait = WebDriverWait(self.driver, 50)

               # Wait until an element is located
               element = wait.until(EC.presence_of_element_located((By.ID, "_priceUpdates")))
               # Wait until an element is visible
               # element_visible = wait.until(EC.visibility_of_element_located((By.ID, "_priceUpdates")))
               delay = 20  # second
               try:
                   element_visible = WebDriverWait(self.driver, delay).until(
                       EC.visibility_of_element_located((By.ID, '_priceUpdates')))
                   print("Page is ready!!")
               except TimeoutException:
                   print("Loading took too much time!!")
                   self.driver.quit()

               dialog = wait.until(EC.presence_of_element_located((By.ID, "myConfirmDlg0")))

               if dialog:
                   # Wait for the "Dismiss" button to be clickable
                   dismiss_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Dismiss']")))
               else:
                   print("No myConfirmDlg0 dialog!")

               if element_visible and dialog:
                   # Click the "Dismiss" button
                   dismiss_button.click()
               else:
                   print("No myConfirmDlg0 dialog and _priceUpdates!")

               if element:
                   time.sleep(5)
                   # go to next page
                   self.driver.get(PageSitePaths[Pagenum])
               else:
                   print("next page not loaded!")
       except:
           # Navigate to the login page
          # self.driver.get(data["App"])
           time.sleep(2)
           wait = WebDriverWait(self.driver, 50)

           # Wait until an element is located
           element = wait.until(EC.presence_of_element_located((By.ID, "_priceUpdates")))
           # Wait until an element is visible
           delay = 20  # seconds
           try:
               element_visible = WebDriverWait(self.driver, delay).until(
                   EC.visibility_of_element_located((By.ID, '_priceUpdates')))
               print("Page is ready!")
           except TimeoutException:
               print("Loading took too much time!")

           if element:
               #time.sleep(5)
               # go to next page
               self.driver.get(PageSitePaths[Pagenum])

       return data

   # Mark the getLogger function as non-testable will add it to the html log report as skip , if you take off the test_functionname it will not write to the log ,Functions that start with "test_" are considered test functions and are executed.
   #@pytest.mark.skip(reason="Not a test case")
   def logging(self):  # when you declare a method in a class you have to pass the "self" param
       # loggerName = inspect.stack()[1][3]  # to put the right method test case name in the log file
       # Get the filename of the calling frame
       filename = inspect.stack()[1].filename
       # Extract just the filename without the path and extension
       module_name = filename.split('\\')[-1].split('.')[0]
       logger = logging.getLogger(module_name)  # __name__  name of the test file ,loggerName

       fileHandler = logging.FileHandler('logfile.log')  # use parent logging and not logger
       formater = logging.Formatter(
           "%(asctime)s :%(levelname)s :%(name)s :%(message)s")  # format time will be printed and log type - s is for string
       fileHandler.setFormatter(formater)
       logger.addHandler(fileHandler)  # filehandler object , in which file do the loggs print and what format to use

       logger.setLevel(logging.INFO)

       return logger



