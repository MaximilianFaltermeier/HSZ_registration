from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from sys import exit
from privat_data import PERSONAL_DATA
from timeit import default_timer as timer

# constants for readability of program. Don't touch them!
GECKODRIVER_EXE = r'D:\Code\Python_Programs\Sportanmeldung\geckodriver.exe'
XPATH_BOOKING_BUTTON = "//input[@type='submit'][@value='buchen']"

# defines time in [s] how long program is willing to wait before TimeOutException is thrown
TIMEOUT_LOADING_PAGE = 5
TIMEOUT_WAIT_FOR_BUTTON_TO_BE_CLICKABLE = 1800
# these variables need to be adjusted for different registrations
HSZ_WEBPAGE = "https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Lernraumbuchung.html"

# the privat_data file needs to be adjusted for different users
""" the structure of PERSONAL_DATA is the following

    PERSONAL_DATA = {
        'forname': 'Max',
        'surname': 'Mustermann',
        'street': 'Somestreet 1',
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
        if end-start > TIMEOUT_WAIT_FOR_BUTTON_TO_BE_CLICKABLE:
            exit('Timeout: button is not clickable after ' + str(TIMEOUT_WAIT_FOR_BUTTON_TO_BE_CLICKABLE) + ' s')

        try:
            element = WebDriverWait(driver, TIMEOUT_LOADING_PAGE).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            element.click()
            return True

        except TimeoutException:
            driver.refresh()


if __name__ == '__main__':
    # start webdriver and opens start page
    driver = webdriver.Firefox(executable_path=GECKODRIVER_EXE)
    driver.get(HSZ_WEBPAGE)
    # waits until booking is possible
    refresh_until_button_is_clicked(XPATH_BOOKING_BUTTON)
    refresh_until_button_is_clicked(XPATH_BOOKING_BUTTON)

    # registration starts as soon as elements on page are available
    sex = WebDriverWait(driver, TIMEOUT_LOADING_PAGE).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='radio'][@value='M']"))
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

    status = Select(driver.find_element_by_xpath("//select[@name='statusorig']")).select_by_value(PERSONAL_DATA['status'])

    mail = driver.find_element_by_xpath("//input[@type='text'][@name='email']")
    mail.send_keys(PERSONAL_DATA['email'])

    mat_nr = driver.find_element_by_xpath("//input[@type='text'][@name='matnr']")
    mat_nr.send_keys(PERSONAL_DATA['matriculation_number'])

    phone = driver.find_element_by_xpath("//input[@type='text'][@name='telefon']")
    phone.send_keys(PERSONAL_DATA['phone_number'])

    data_protection = driver.find_element_by_xpath("//input[@type='checkbox'][@name='tnbed']")

    data_protection.click()

    # goto next page
    # continue_with_booking = driver.find_element_by_xpath("//input[@type='submit'][@title='continue booking']")

