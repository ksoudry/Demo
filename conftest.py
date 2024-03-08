#conftest is a file that will run fixture in all test files in the package

import pytest
import time
driver = None

from selenium import webdriver
# need chrome driver to work with chrome
from selenium.webdriver.chrome.service import Service

#how your browser should look like , find chrome options python in google
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")#start browser as maximazed
#chrome_options.add_argument("--headless")#run chrome headless
chrome_options.add_argument("--ignore-certificate-errors")#will ignore and take care of error pages


def pytest_addoption(parser): #declared a cmd var that runs the browser
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )

@pytest.fixture(scope="class")#scope="class" will run the fixture only once before the class is run and once after all test cases are run @pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        #integreating the chrome browser
        service_obj = Service("/Users/Karen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")  # enter chrome driver path her so we can work with chrome,chrome driver download from browser
        driver = webdriver.Chrome(service=service_obj,options=chrome_options)  #obj will exciqute the chrome browser
        driver.implicitly_wait(10)  # global wait!!
    #elif browser_name == "firefox":
        #driver = webdriver.Firefox(executable_path="c:\\geckodriver.exe")
    request.cls.driver = driver #driver will be sent to class object
    yield #run once at the end of the test
    driver.close()
    driver.quit()

@pytest.mark.hookwrapper #will take a screen shot and put in html report when TEST IS FAILD!
def pytest_runtest_makereport(item):
        """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
        pytest_html = item.config.pluginmanager.getplugin('html')
        outcome = yield
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])

        if report.when == 'call' or report.when == "setup":
            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                file_name = report.nodeid.replace("::", "_") + ".png"
                _capture_screenshot(file_name)
                if file_name:
                    html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))
            report.extra = extra

def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)