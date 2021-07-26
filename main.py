from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from sys import exit
from privat_data import PERSONAL_DATA

# constants for readability of program. Don't touch them!
GECKODRIVER_EXE = r'D:\Code\Python_Programs\Sportanmeldung\geckodriver.exe'
XPATH_BOOKING_BUTTON = "//input[@type='submit'][@value='buchen']"

# defines time in [s] how long program is willing to wait before TimeOutException is thrown
TIMEOUT = 1800

# these variables need to be adjusted for different registrations
HSZ_WEBPAGE = "https://buchung.hsz.rwth-aachen.de/cgi/anmeldung.fcgi"

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
if __name__ == '__main__':
    # start webdriver and opens start page
    driver = webdriver.Firefox(executable_path=GECKODRIVER_EXE)
    driver.get(HSZ_WEBPAGE)
    # waits until booking is possible
    try:
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, XPATH_BOOKING_BUTTON))
        )
        element.click()
    except TimeoutException:
        driver.quit()
        exit('timeout')

    # registration
    sex = driver.find_element_by_xpath("//input[@type='radio'][@value='M']")
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
    continue_with_booking = driver.find_element_by_xpath("//input[@type='submit'][@title='continue booking']")

