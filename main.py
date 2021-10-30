from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pause
from datetime import datetime
from timeit import default_timer as timer
from time import sleep
import pdfkit
from telegram_bot import telegram_bot_senddocument
from sys import exit
from privat_data import PERSONAL_DATA


# adjust these parameters !!!
SPORTSPIELE = 0
FITNESS_MIT_MUSIK = 1
START_TIME_OF_PROGRAMM = datetime(2021, 10, 30, 20, 44)  # year, month, day, hour, min, ...
if SPORTSPIELE:
    PATH_BOOKING_BUTTON = "/html/body/div[2]/div[5]/div/div/div[2]/div/form/div[4]/div[2]/table/tbody/tr[4]/td[9]/input"
    HSZ_WEBPAGE = "https://buchung.hsz.rwth-aachen.de/angebote/Wintersemeseter_2021_22/_Sportspiele.html"
elif FITNESS_MIT_MUSIK:
    PATH_BOOKING_BUTTON = "/html/body/div[2]/div[5]/div/div/div[2]/div/form/div[4]/div/table/tbody/tr[14]/td[9]/input"
    HSZ_WEBPAGE = "https://buchung.hsz.rwth-aachen.de/angebote/Wintersemeseter_2021_22/_Fitness_mit_Musik.html"
else:
    PATH_BOOKING_BUTTON = ''
    HSZ_WEBPAGE = ''
    exit()
XPATH_2ND_BOOKING_BUTTON = "/html/body/form/div/div[2]/div/div[2]/div[1]/label/div[2]/input"
# ------------------------------------------------------------------------------------------
# defines time in [s] how long program is willing to wait before TimeOutException is thrown
TIMEOUT_LOADING_PAGE = 5
TIMEOUT_WAIT_FOR_BUTTON_TO_BE_CLICKABLE = 600
# constants for readability of program. Don't touch them!
GECKODRIVER_EXE = r'D:\Code\Python_Programs\Sportanmeldung\geckodriver.exe'

# the privat_data file needs to be adjusted for different users
""" the structure of PERSONAL_DATA is the following

    PERSONAL_DATA = {
        'forname': 'Max',
        'surname': 'Mustermann',
        'street': 'some_street 1',
        'city': '12345 City',
        'matriculation_number': '123456',
        'phone_number': '0157123456',
        'email': 'myMailadress@myprovider.com'
        }

"""


def refresh_until_button_is_clicked(button_xpath):
    start = timer()
    while True:
        end = timer()
        if end - start > TIMEOUT_WAIT_FOR_BUTTON_TO_BE_CLICKABLE:
            exit('Timeout: button is not clickable after ' + str(TIMEOUT_WAIT_FOR_BUTTON_TO_BE_CLICKABLE) + ' s')

        try:
            element = WebDriverWait(driver, TIMEOUT_LOADING_PAGE).until(
                ec.presence_of_element_located((By.XPATH, button_xpath))
            )
            element.click()
            return True

        except TimeoutException:
            driver.refresh()


if __name__ == '__main__':
    pause.until(START_TIME_OF_PROGRAMM)
    # start webdriver and opens start page
    driver = webdriver.Firefox(executable_path=GECKODRIVER_EXE)
    driver.get(HSZ_WEBPAGE)
    # waits until booking is possible
    refresh_until_button_is_clicked(PATH_BOOKING_BUTTON)
    driver.switch_to.window(driver.window_handles[-1])
    refresh_until_button_is_clicked(XPATH_2ND_BOOKING_BUTTON)

    # registration starts as soon as elements on page are available
    sex = WebDriverWait(driver, TIMEOUT_LOADING_PAGE).until(
        ec.presence_of_element_located((By.XPATH, "//input[@type='radio'][@value='M']"))
    )
    sex.click()

    forename = driver.find_element_by_xpath("//input[@type='text'][@name='vorname']")
    forename.send_keys(PERSONAL_DATA['forname'])

    surname = driver.find_element_by_xpath("//input[@type='text'][@name='name']")
    surname.send_keys(PERSONAL_DATA['surname'])

    street = driver.find_element_by_xpath("//input[@type='text'][@name='strasse']")
    street.send_keys(PERSONAL_DATA['street'])

    city = driver.find_element_by_xpath("//input[@type='text'][@name='ort']")
    city.send_keys(PERSONAL_DATA['city'])

    status = Select(driver.find_element_by_xpath("//select[@name='statusorig']")) \
        .select_by_value(PERSONAL_DATA['status'])

    mail = driver.find_element_by_xpath("//input[@type='text'][@name='email']")
    mail.send_keys(PERSONAL_DATA['email'])

    mat_nr = driver.find_element_by_xpath("//input[@type='text'][@name='matnr']")
    mat_nr.send_keys(PERSONAL_DATA['matriculation_number'])

    phone = driver.find_element_by_xpath("//input[@type='text'][@name='telefon']")
    phone.send_keys(PERSONAL_DATA['phone_number'])

    data_protection = driver.find_element_by_xpath("//input[@type='checkbox'][@name='tnbed']")

    data_protection.click()

    # goto next page
    sleep(5)
    driver.find_element_by_xpath("/html/body/form/div/div[3]/div[3]/div[2]/input").click()
    sleep(5)
    driver.find_element_by_xpath("/html/body/form/div/div[3]/div[1]/div[2]/input").click()

    # sends confirmation as an pdf to telegram chat bot
    page_html = driver.page_source
    # converter = pdfcrowd.HtmlToPdfClient(CONVERTER_USER_NAME, CONVERTER_API_KEY)
    # confirmation_pdf = converter.convertString(page_html)
    confirmation_pdf = pdfkit.from_string(page_html, 'confirmation.pdf')
    telegram_bot_senddocument(confirmation_pdf)
