#Tech Clock In / Clock Out
import time
from selenium import webdriver

# need chrome driver to work with chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # for By. functions
from selenium.webdriver.common.keys import Keys
from utilities.BaseClass import BaseClass


#load bit (To change system please change SystemNumber,UserName , PassWord , App & Page links)
EmployeeID = "AC"
ClockInMes ="Tech is Clocking In"
ClockOutMes ="Tech is Clocking Out"
#Page = "https://staging.na4.bitdms.net/onlineapp/mainmenu/partsmodulex.php?theXml=run_parts_reports.xml"
Page = 0

class TestClockINOUT(BaseClass):#calling parent class in to child class
    def test_ClockINOUT(self):#,setup
        data = self.getData(Page)  # Call the method to get the data
        log = self.logging()#Call log function
        time.sleep(3)
        try:
            # click on Time Clock Link
            self.driver.find_element(By.CSS_SELECTOR, "#timeclock").click()
            # add Tech ID and press enter to load the tech
            text_field = self.driver.find_element(By.CSS_SELECTOR, "#timeclock_idcode")
            # Enter text in the text field
            text_field.send_keys(EmployeeID)
            # pressing "Enter"
            text_field.send_keys(Keys.ENTER)
            try:
                clockin = self.driver.find_element(By.CSS_SELECTOR, "#timeclock_in")
                time.sleep(2)
                if clockin.is_enabled():
                    clockin.click()
                    alert = self.driver.switch_to.alert
                    # alert.send_keys(ClockInMes)
                    alert.accept()  # clicks on OK
                    # get success message
                    textmess = self.driver.find_element(By.XPATH, "(//div[normalize-space()='Success'])[1]")
                    time.sleep(1)
                    if textmess.text == "Success":
                        self.driver.find_element(By.XPATH,"(//button[@type='button'][normalize-space()='OK'])[1]").click()  # clicks on OK
                        print("Success: " + EmployeeID + " Tech Clocked In")
                        log.info("Success: " + EmployeeID + " Tech Clocked In")
                    else:
                        print("Error: Tech could not Clock In")
                        log.error("Error: Tech could not Clock In")
                else:
                    clockout = self.driver.find_element(By.CSS_SELECTOR, "#timeclock_out")
                    time.sleep(2)
                    if clockout.is_enabled():
                        clockout.click()
                        alert = self.driver.switch_to.alert
                        # alert.send_keys(ClockOutMes)
                        alert.accept()  # clicks on OK
                        # get success message
                        textmess = self.driver.find_element(By.XPATH, "(//div[normalize-space()='Success'])[1]")
                        time.sleep(1)
                        if textmess.text == "Success":
                            self.driver.find_element(By.XPATH,"(//button[@type='button'][normalize-space()='OK'])[1]").click()  # clicks on OK
                            print("Success: " + EmployeeID + " Tech was Clocked In and now Clocked Out")
                            log.info("Success: " + EmployeeID + " Tech was Clocked In and now Clocked Out")
                        else:
                            print("Error: Tech could not Clock Out")
                            log.error("Error: Tech could not Clock Out")
            except:
                print("Error: Time Clock In / Clock Out Failed")
                log.error("Error: Time Clock In / Clock Out Failed")
                self.driver.quit()
        except:
            print("Error:[WinError 10061] No connection could be made , run test again")
            log.error("Error:[WinError 10061] No connection could be made , run test again")
            self.driver.quit()

        try:
            if not clockin.is_enabled() and not clockout.is_enabled():
                # get Not Found message
                textmess = self.driver.find_element(By.XPATH, "(//div[normalize-space()='Not Found'])[1]")
                if textmess.text == "Not Found":
                    self.driver.find_element(By.XPATH,"(//button[@type='button'][normalize-space()='OK'])[1]").click()  # clicks on OK
                    self.driver.find_element(By.XPATH,"(//button[@type='button'][normalize-space()='Cancel'])[1]").click()  # clicks on Cancel
                    print("Error: " + EmployeeID + " Tech Not Found")
                    log.error("Error: " + EmployeeID + " Tech Not Found")
                else:
                    print("Error: Time Clock did not load , please run test again!!")
                    log.error("Error: Time Clock did not load , please run test again!!")
                    self.driver.quit()
        except:
            result = None  # Handle the exception by setting the result to None

        time.sleep(2)

